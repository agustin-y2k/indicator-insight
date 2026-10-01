# Scenario v1 contract

`backend/app/core/scenario.py` is the executable domain-neutral contract.
`docs/examples/scenario.schema.json` is generated from
`scenario_contract_schema()` (JSON Schema draft 2020-12), rooted in
`ScenarioVersion.model_json_schema()`; its `$defs`
also include generated schemas for `ScenarioVersionRef`, `LearnerScenarioRef`,
`LearnerScenario` and `GroundTruth` from their respective models. The former
illustrative schema is replaced; no application consumer used it. JSON Schema
expresses structural constraints; cross-field temporal comparisons, uniqueness
and timezone normalization are enforced by Python validation.

## Types and fields

- `ScenarioVersion`: `schema_version=1`, stable `scenario_id`, positive integer
  `version`, `domain`, nonempty unique `competencies`, optional `difficulty`,
  mandatory `cutoff_time`, `context`, `evidence`, optional `alternatives` and
  `probability_space`, private `resolution`.
- `AvailableText`: nonblank `text`, timezone-aware `available_at`, and optional
  `source_available_at` timestamps for declared input dependencies.
- `Evidence` / `Alternative`: available text with unique `evidence_id` /
  `alternative_id` within its collection. Context, alternative labels and
  probabilistic questions/outcome labels have the same availability obligations.
- `Difficulty`: opaque `scheme` and `level`; null means unspecified. No scale,
  ordering or scientific meaning is inferred. The former illustrative numeric
  range did not define an operational scale and is not adopted.
- `ProbabilitySpace`: available question and at least two unique outcome IDs with
  available labels. This finite representation does not define scoring, submitted
  probability validation or a final experimental event design.
- `ResolutionRule`: private `rule_id`, `rule_version`, `description`.
  `ResolutionSpec` holds that rule and private evidence `data`; future timestamps
  are allowed there. Interpretation belongs to adapters.
- `ScenarioVersionRef`: internal scenario ID, version number and content SHA-256.
- `LearnerScenarioRef`: public scenario ID and version number only, without hashes.
- `LearnerScenario`: explicit allowlisted visible fields and version reference;
  no resolution rule, private data, ground truth or private-derived digest.
- `GroundTruth`: separate private result with exact version reference,
  `outcome_id` and timezone-aware `resolved_at`. It describes a result, does not
  execute resolution or authorize disclosure. Outcome membership, decision lock
  and rule timing must be enforced by the future resolution service.

Unknown fields, blank identifiers, duplicate IDs and invalid structures are
rejected. Evidence may be empty or unordered; availability is checked independently
of array ordering. No arbitrary mutable metadata dictionaries are accepted.

## Time boundary

Every timestamp must carry an explicit timezone; naive timestamps are rejected.
Accepted instants normalize to UTC before comparison, serialization and hashing.
For every visible text `available_at <= cutoff_time`; each declared source must
also satisfy `source_available_at <= available_at`. Equality at cutoff is valid.
This implies `max(t_visible) <= cutoff_time` for all declared visible material.
For empty evidence the context and other visible fields still satisfy the boundary.

Availability is an adapter assertion, not proof of the truth of arbitrary text.
Adapters must declare dependencies accurately and must not place outcomes in text.
Auditing complete upstream lineage, datasets, transformations and metadata is the
Temporal Leakage Guard/replay responsibility of II-15, not implemented here.

## Publication, identity and immutability

Construct with `ScenarioVersion.model_validate(data)` or normal validated constructors.
All contract models are frozen; nested values are frozen models, strings and tuples.
Input containers are converted, so later input mutation does not alter a publication.
Updates through `model_copy(update=...)` are rejected because they bypass validation.
As with other Python validation models, low-level reflection or `model_construct`
are trusted-code escape hatches and must never ingest external/unvalidated input.

`reference` is internal only. `canonical_bytes()` defines the hash input and
preserves the original v1 byte representation. It hashes the entire validated
internal version, including resolution
specification, with SHA-256 over UTF-8 JSON, sorted object keys, no insignificant
whitespace, explicit default/null fields and UTC instants. Array ordering remains
significant. Round-trip serialization and equivalent timezone representations
preserve the reference. This digest algorithm is part of v1; changing it requires
an explicit contract revision. It identifies content, not authorship or signatures.
A fixed golden fixture and expected SHA-256 in `test_scenario.py` detect accidental
serialization drift. Deliberate canonicalization changes require an explicit
contract versioning decision, including dependency-induced serialization changes.

`learner_view()` constructs `LearnerScenarioRef` directly from scenario ID and
version, without computing or exposing the internal digest. A controlled
reconstruction changing only resolution changes the internal reference but leaves
the entire learner-visible payload byte-for-byte identical. This test does not
permit overwriting publications: normal content changes still create a new version.

`next_version(**changes)` preserves scenario identity, increments the version
number and validates all replacement content. Never overwrite an existing
publication. Even rebuilding different content under an existing number produces
a different full reference and cannot silently match a saved reference. Future
storage must enforce uniqueness of `(scenario_id, version)` and reject replacements;
concurrent version allocation belongs to that storage service. Attempts must save
the full `ScenarioVersionRef`, never resolve a mutable "latest" alias.

Ground truth is separate from publication so later resolution does not mutate the
version. Persisting attempts, enforcing publication uniqueness in a database,
locking decisions and gating result access are future responsibilities.

## Delivery and scope

Only `version.learner_view()` / `LearnerScenario` may be serialized for pre-decision
clients. Never send `ScenarioVersion` or `GroundTruth` to those clients. No endpoint
or UI delivery is implemented by II-7, so this is a contract boundary, not a working
authorization mechanism. Private rule/data stay on the server.

No database changes, migrations, historical replay, domain adapter, attempt
persistence, score, learner model or adaptive policy is introduced.
Dataset/transform/generator provenance will be added with their actual pipeline,
without using unvalidated public metadata as an extension channel.

## Reproducible checks

From `backend`:

```sh
.venv/bin/pytest -q -m 'not integration'
.venv/bin/ruff check .
.venv/bin/ruff format --check .
```

The tests compare the checked-in JSON schema with the executable model and exercise
cutoff boundaries, timezone equivalence/naive rejection, declared future inputs,
immutability, version references, private serialization, invalid structures and
absence of domain-specific imports/fields. These tests run in the existing backend
CI job; a failed temporal assertion fails CI.

Regenerate the single schema artifact from `backend`:

```sh
.venv/bin/python -c 'import json; from pathlib import Path; from app.core.scenario import scenario_contract_schema; Path("../docs/examples/scenario.schema.json").write_text(json.dumps(scenario_contract_schema(), indent=2) + "\n")'
```
