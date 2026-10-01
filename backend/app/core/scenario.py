"""Domain-neutral Scenario v1 contracts; no persistence or resolution execution."""

import hashlib
import json
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Annotated, Literal, Self

from pydantic import (
    AfterValidator,
    AwareDatetime,
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    model_validator,
)

Text = Annotated[str, Field(strict=True, min_length=1), AfterValidator(lambda s: _text(s))]
PositiveInt = Annotated[int, Field(strict=True, ge=1)]


def _timestamp(value: object) -> object:
    if not isinstance(value, (str, datetime)):
        raise ValueError("timestamp must be a timezone-aware datetime or ISO 8601 string")
    return value


Instant = Annotated[
    AwareDatetime, BeforeValidator(_timestamp), AfterValidator(lambda t: t.astimezone(UTC))
]


def _text(value: str) -> str:
    if not value.strip() or value != value.strip():
        raise ValueError("text must be nonblank without surrounding whitespace")
    return value


class Contract(BaseModel):
    """Nested values use immutable models and tuples, never mutable mappings."""

    model_config = ConfigDict(frozen=True, extra="forbid", revalidate_instances="always")

    def model_copy(self, *, update: Mapping[str, object] | None = None, deep: bool = False) -> Self:
        # BaseModel.model_copy(update=...) bypasses validation; forbid this escape hatch.
        if update:
            raise ValueError("construct and validate a new version instead")
        return super().model_copy(deep=deep)


class AvailableText(Contract):
    """An adapter's declared availability and source dependencies for visible text."""

    text: Text
    available_at: Instant
    source_available_at: tuple[Instant, ...] = ()

    @model_validator(mode="after")
    def sources_available(self) -> Self:
        if any(t > self.available_at for t in self.source_available_at):
            raise ValueError("source was unavailable when content became available")
        return self


class Evidence(AvailableText):
    evidence_id: Text


class Alternative(AvailableText):
    alternative_id: Text


class Difficulty(Contract):
    """Opaque level in an explicitly named scheme; no numerical scale assumed."""

    scheme: Text
    level: Text


class ProbabilitySpace(Contract):
    """Finite outcome identifiers; scoring and probability submission are separate."""

    question: AvailableText
    outcomes: Annotated[tuple[Alternative, ...], Field(min_length=2)]

    @model_validator(mode="after")
    def unique_outcomes(self) -> Self:
        _unique(tuple(x.alternative_id for x in self.outcomes))
        return self


def _unique(values: tuple[str, ...]) -> None:
    if len(set(values)) != len(values):
        raise ValueError("identifiers must be unique")


class ScenarioVersionRef(Contract):
    scenario_id: Text
    version: PositiveInt
    content_sha256: Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class LearnerScenarioRef(Contract):
    """Public identity only; never derived from private publication content."""

    scenario_id: Text
    version: PositiveInt


class LearnerScenario(Contract):
    """The only contract intended for pre-decision delivery."""

    schema_version: Literal[1] = 1
    reference: LearnerScenarioRef
    domain: Text
    competencies: Annotated[tuple[Text, ...], Field(min_length=1)]
    difficulty: Difficulty | None = None
    cutoff_time: Instant
    context: AvailableText
    evidence: tuple[Evidence, ...]
    alternatives: tuple[Alternative, ...] = ()
    probability_space: ProbabilitySpace | None = None

    @model_validator(mode="after")
    def visible_constraints(self) -> Self:
        _unique(self.competencies)
        _unique(tuple(x.evidence_id for x in self.evidence))
        _unique(tuple(x.alternative_id for x in self.alternatives))
        visible = [self.context, *self.evidence, *self.alternatives]
        if self.probability_space is not None:
            visible += [self.probability_space.question, *self.probability_space.outcomes]
        if any(x.available_at > self.cutoff_time for x in visible):
            raise ValueError("learner-visible content exceeds cutoff_time")
        return self


class ResolutionRule(Contract):
    """Private versioned rule reference, interpreted by a future domain adapter."""

    rule_id: Text
    rule_version: Text
    description: Text


class ResolutionSpec(Contract):
    rule: ResolutionRule
    data: tuple[Evidence, ...] = ()

    @model_validator(mode="after")
    def unique_data(self) -> Self:
        _unique(tuple(x.evidence_id for x in self.data))
        return self


class ScenarioVersion(Contract):
    """Immutable publication. Content changes have a different reference digest."""

    schema_version: Literal[1] = 1
    scenario_id: Text
    version: PositiveInt
    domain: Text
    competencies: Annotated[tuple[Text, ...], Field(min_length=1)]
    difficulty: Difficulty | None = None
    cutoff_time: Instant
    context: AvailableText
    evidence: tuple[Evidence, ...]
    alternatives: tuple[Alternative, ...] = ()
    probability_space: ProbabilitySpace | None = None
    resolution: ResolutionSpec

    def canonical_bytes(self) -> bytes:
        """V1 internal hash input. Changes require an explicit contract version decision.

        UTF-8 JSON of validated content, UTC instants, all defaults/nulls included,
        sorted object keys, ordered arrays, unescaped Unicode and compact separators.
        """
        return json.dumps(
            self.model_dump(mode="json"), sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")

    @property
    def reference(self) -> ScenarioVersionRef:
        return ScenarioVersionRef(
            scenario_id=self.scenario_id,
            version=self.version,
            content_sha256=hashlib.sha256(self.canonical_bytes()).hexdigest(),
        )

    def learner_view(self) -> LearnerScenario:
        values = self.model_dump(exclude={"scenario_id", "version", "resolution"})
        return LearnerScenario(
            reference=LearnerScenarioRef(scenario_id=self.scenario_id, version=self.version),
            **values,
        )

    @model_validator(mode="after")
    def validate_visible(self) -> Self:
        self.learner_view()
        return self

    def next_version(self, **changes: object) -> Self:
        if {"scenario_id", "version", "schema_version"} & changes.keys():
            raise ValueError("scenario identity and next version number are managed automatically")
        values = self.model_dump()
        values.update(changes)
        values["version"] = self.version + 1
        return type(self).model_validate(values)


class GroundTruth(Contract):
    """Private resolution result; access control/decision locking are not implemented here."""

    reference: ScenarioVersionRef
    outcome_id: Text
    resolved_at: Instant


def scenario_contract_schema() -> dict[str, object]:
    """Generate internal ScenarioVersion schema plus related contract definitions."""
    schema = ScenarioVersion.model_json_schema()
    definitions = schema.setdefault("$defs", {})
    for model in (ScenarioVersionRef, LearnerScenarioRef, LearnerScenario, GroundTruth):
        related = model.model_json_schema()
        definitions.update(related.pop("$defs", {}))
        definitions[model.__name__] = related
    schema["$schema"] = "https://json-schema.org/draft/2020-12/schema"
    return schema
