import json
import re
from pathlib import Path

import pytest
from pydantic import ValidationError

from app.core.scenario import GroundTruth, LearnerScenario, ScenarioVersion


def payload():
    return {
        "scenario_id": "demo-neutral",
        "version": 1,
        "domain": "demo",
        "competencies": ["reasoning"],
        "difficulty": {"scheme": "demo-labels-v1", "level": "introductory"},
        "cutoff_time": "2026-01-01T12:00:00Z",
        "context": {
            "text": "Choose using the available observations.",
            "available_at": "2026-01-01T11:00:00Z",
        },
        "evidence": [
            {
                "evidence_id": "observation-1",
                "text": "An observation.",
                "available_at": "2026-01-01T12:00:00Z",
                "source_available_at": ["2026-01-01T10:00:00Z"],
            }
        ],
        "resolution": {
            "rule": {"rule_id": "demo-rule", "rule_version": "1", "description": "Private rule."},
            "data": [
                {
                    "evidence_id": "private",
                    "text": "Hidden observation.",
                    "available_at": "2026-01-02T12:00:00Z",
                }
            ],
        },
    }


@pytest.mark.parametrize(
    "instant", ["2026-01-01T11:59:59Z", "2026-01-01T12:00:00Z", "2026-01-01T09:00:00-03:00"]
)
def test_valid_cutoff_boundaries(instant):
    data = payload()
    data["evidence"][0]["available_at"] = instant
    scenario = ScenarioVersion.model_validate(data)
    assert scenario.learner_view().evidence[0].available_at <= scenario.cutoff_time
    assert scenario.cutoff_time.utcoffset().total_seconds() == 0


@pytest.mark.parametrize("field", ["context", "evidence", "alternative", "question", "outcome"])
def test_all_visible_content_rejects_future(field):
    data = payload()
    future = {"text": "Future", "available_at": "2026-01-01T12:00:01Z"}
    if field == "context":
        data[field] = future
    elif field == "evidence":
        data[field] = [dict(future, evidence_id="future")]
    elif field == "alternative":
        data["alternatives"] = [dict(future, alternative_id="a")]
    else:
        data["probability_space"] = probability_space()
        if field == "question":
            data["probability_space"]["question"] = future
        else:
            data["probability_space"]["outcomes"][0] = dict(future, alternative_id="yes")
    with pytest.raises(ValidationError, match="cutoff_time"):
        ScenarioVersion.model_validate(data)


def probability_space():
    return {
        "question": {"text": "Will the event occur?", "available_at": "2026-01-01T11:00:00Z"},
        "outcomes": [
            {"alternative_id": value, "text": value, "available_at": "2026-01-01T11:00:00Z"}
            for value in ("yes", "no")
        ],
    }


@pytest.mark.parametrize("field", ["cutoff", "visible", "source", "private", "resolved"])
def test_naive_timestamps_rejected(field):
    data = payload()
    naive = "2026-01-01T12:00:00"
    if field == "cutoff":
        data["cutoff_time"] = naive
    elif field == "visible":
        data["context"]["available_at"] = naive
    elif field == "source":
        data["evidence"][0]["source_available_at"] = [naive]
    elif field == "private":
        data["resolution"]["data"][0]["available_at"] = naive
    else:
        with pytest.raises(ValidationError):
            GroundTruth(
                reference=ScenarioVersion.model_validate(data).reference,
                outcome_id="yes",
                resolved_at=naive,
            )
        return
    with pytest.raises(ValidationError):
        ScenarioVersion.model_validate(data)


def test_future_dependency_rejected_even_with_backdated_visible_timestamp():
    data = payload()
    data["evidence"][0]["source_available_at"] = ["2026-01-02T00:00:00Z"]
    with pytest.raises(ValidationError, match="source was unavailable"):
        ScenarioVersion.model_validate(data)


def test_immutable_identity_roundtrip_and_new_version():
    data = payload()
    scenario = ScenarioVersion.model_validate(data)
    original = scenario.reference
    assert ScenarioVersion.model_validate_json(scenario.model_dump_json()).reference == original
    data["context"]["available_at"] = "2026-01-01T08:00:00-03:00"
    assert ScenarioVersion.model_validate(data).reference == original
    data["context"]["text"] = "changed external input"
    assert scenario.context.text != data["context"]["text"]
    with pytest.raises(ValidationError):
        scenario.version = 2
    with pytest.raises(ValidationError):
        scenario.context.text = "tampered"
    with pytest.raises(ValueError):
        scenario.model_copy(update={"version": 2})
    updated = scenario.next_version(context=data["context"])
    assert updated.version == 2
    assert updated.scenario_id == original.scenario_id
    assert updated.reference.content_sha256 != original.content_sha256
    assert scenario.reference == original
    with pytest.raises(ValueError):
        scenario.next_version(scenario_id="other")
    with pytest.raises(ValidationError):
        scenario.next_version(cutoff_time="2025-01-01T00:00:00Z")
    # A reconstruction under the same number cannot silently match the original reference.
    assert ScenarioVersion.model_validate(data).reference != original


def test_outcome_separation_and_finite_space():
    data = payload()
    data["probability_space"] = probability_space()
    scenario = ScenarioVersion.model_validate(data)
    truth = GroundTruth(
        reference=scenario.reference, outcome_id="yes", resolved_at="2026-01-02T12:00:00Z"
    )
    visible = scenario.learner_view().model_dump_json()
    for private in (
        "resolution",
        "Private rule",
        "Hidden observation",
        "resolved_at",
        "outcome_id",
    ):
        assert private not in visible
    assert truth.reference == scenario.reference
    with pytest.raises(ValidationError):
        LearnerScenario.model_validate(dict(json.loads(visible), resolution=data["resolution"]))


@pytest.mark.parametrize(
    "changes",
    [
        {"competencies": []},
        {"competencies": ["x", "x"]},
        {"competencies": [" "]},
        {"competencies": [1]},
        {"difficulty": {"level": "x"}},
        {"difficulty": 0.5},
        {"version": 0},
        {"version": True},
        {"scenario_id": ""},
        {"domain": " demo "},
        {"ticker": "unsupported"},
        {"resolution": {}},
        {"schema_version": 2},
    ],
)
def test_invalid_structure(changes):
    with pytest.raises(ValidationError):
        ScenarioVersion.model_validate(dict(payload(), **changes))


def test_duplicate_evidence_and_outcomes():
    data = payload()
    data["evidence"] *= 2
    with pytest.raises(ValidationError):
        ScenarioVersion.model_validate(data)
    data = payload()
    data["probability_space"] = probability_space()
    data["probability_space"]["outcomes"][1]["alternative_id"] = "yes"
    with pytest.raises(ValidationError):
        ScenarioVersion.model_validate(data)


def test_empty_unordered_evidence_and_unknown_difficulty():
    data = payload()
    data["evidence"] = []
    data["difficulty"] = None
    assert ScenarioVersion.model_validate(data).evidence == ()
    data["evidence"] = [
        {"evidence_id": key, "text": key, "available_at": instant}
        for key, instant in [("a", "2026-01-01T12:00:00Z"), ("b", "2026-01-01T10:00:00Z")]
    ]
    assert len(ScenarioVersion.model_validate(data).evidence) == 2


def test_schema_matches_implementation_and_core_is_neutral():
    root = Path(__file__).resolve().parents[2]
    schema = json.loads((root / "docs/examples/scenario.schema.json").read_text())
    expected = ScenarioVersion.model_json_schema()
    expected["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    assert schema == expected
    for file in (root / "backend/app/core").glob("*.py"):
        source = file.read_text().lower()
        for term in ("ticker", "ohlcv", "rsi", "macd", "atr", "market_horizon"):
            assert re.search(r"\b" + re.escape(term) + r"\b", source) is None


@pytest.mark.parametrize("timestamp", [0, 1767268800, True, "2026-01-01"])
def test_timestamp_requires_explicit_timezone_representation(timestamp):
    data = payload()
    data["cutoff_time"] = timestamp
    with pytest.raises(ValidationError):
        ScenarioVersion.model_validate(data)


def test_insufficient_outcomes_and_nested_extra_fields():
    data = payload()
    data["probability_space"] = probability_space()
    data["probability_space"]["outcomes"] = data["probability_space"]["outcomes"][:1]
    with pytest.raises(ValidationError):
        ScenarioVersion.model_validate(data)
    data = payload()
    data["context"]["ground_truth"] = "hidden"
    with pytest.raises(ValidationError):
        ScenarioVersion.model_validate(data)
