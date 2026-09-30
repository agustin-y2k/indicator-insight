# ADR 0002 — Separate conceptual mastery from probabilistic judgment

**Status:** Accepted

## Context
A stochastic outcome is not equivalent to conceptual understanding, and Brier/calibration answer different questions from BKT.

## Decision
BKT consumes verified conceptual observations only. Judgment metrics live in a separate module/state and adaptation consumes both explicitly.

## Consequences
This decision is part of Thesis Baseline. Supersede it with a new ADR rather than silently editing the rationale after implementation/experimentation begins.
