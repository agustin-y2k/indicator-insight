# ADR 0004 — Use PostgreSQL as persistence

**Status:** Accepted

## Context
The domain is relational and requires integrity, versioning, experiment joins and reproducible analytics.

## Decision
Use PostgreSQL + Alembic. MongoDB references in legacy documentation are obsolete.

## Consequences
This decision is part of Thesis Baseline. Supersede it with a new ADR rather than silently editing the rationale after implementation/experimentation begins.
