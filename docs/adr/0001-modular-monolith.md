# ADR 0001 — Use a modular monolith

**Status:** Accepted

## Context
The thesis needs clear module boundaries but does not benefit from distributed-systems overhead.

## Decision
One FastAPI codebase with internal modules and optional same-codebase worker. Microservices require a future ADR.

## Consequences
This decision is part of Thesis Baseline. Supersede it with a new ADR rather than silently editing the rationale after implementation/experimentation begins.
