# ADR 0003 — Use finance as primary validation domain, not core identity

**Status:** Accepted

## Context
Historical financial data offers time-indexed evidence and objective future outcomes, but a finance-only architecture would weaken generalization.

## Decision
Finance implements the DomainAdapter contract. The core contains no financial indicators.

## Consequences
This decision is part of Thesis Baseline. Supersede it with a new ADR rather than silently editing the rationale after implementation/experimentation begins.
