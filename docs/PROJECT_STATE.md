# Project State

**Baseline:** II-6 development infrastructure on `feature/II-6-repository-skeleton`.
**Status:** M1 technical foundation validated locally and ready for review; not merged.
**Date:** 2026-09-30.

## Technical foundation

React/TypeScript frontend, FastAPI backend, PostgreSQL, SQLAlchemy 2.x, initial
Alembic baseline, development Compose and CI are prepared in II-6.
See `docs/DEVELOPMENT.md` for setup and validation. No scientific/business behavior
or business tables are implemented. Review and merge remain required.

## Decisions frozen for start
- Product working name: Indicator Insight.
- Formal thesis title is domain-neutral.
- Finance is validation domain, not core identity.
- Architecture: modular monolith.
- Frontend: React + TypeScript.
- Backend/statistics: Python + FastAPI.
- DB: PostgreSQL + Alembic.
- Core learner model: BKT for conceptual evidence only.
- Probabilistic judgment: Brier + calibration-related metrics kept separate.
- Adaptation policies: P0/P1/P2.
- Kanban without fixed 16-week schedule.
- GitFlow + PR + human merge review.

## Not yet frozen
- exact finance dataset/provider;
- final competency graph;
- BKT parameter values;
- exact calibration aggregation/binning;
- participant population/sample size;
- exact statistical test/model;
- second domain adapter;
- production hostname.

These are deliberate research/implementation decisions, not missing requirements to guess.

## Next milestone
M1 Scientific Vertical Slice.

## First recommended issues
1. `II-001` Create repository skeleton + CI + Docker dev environment.
2. `II-002` Define Scenario v1 schema and immutable version model.
3. `II-003` Implement binary Brier module + reference tests.
4. `II-004` Implement conceptual assessment + BKT pure functions/tests.
5. `II-005` Build single end-to-end demo scenario without finance API dependency.
