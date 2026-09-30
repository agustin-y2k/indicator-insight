# Roadmap — Kanban, no calendario artificial

No existe restricción de 16 semanas. El flujo se gestiona por valor, riesgo y dependencias.

## Estados
`Backlog → Ready → In Progress → Review → Validation → Done`

Estado adicional: `Blocked`.

## WIP recomendado
- In Progress: máximo 1–2 issues personales simultáneas.
- Review: máximo 2.

## Milestones
### M0 — Thesis Baseline Frozen
Documentación, ADRs y pitch/anteproyecto alineados.

### M1 — Scientific Vertical Slice
Scenario → respuesta → outcome → Brier/concept score → persistencia → UI.

### M2 — Scenario & Temporal Safety
Dataset snapshot, finance adapter, replay y leakage guard.

### M3 — Learner & Judgment Models
BKT validado, métricas, dashboards mínimos.

### M4 — Adaptive Policies
P0/P1/P2, explanation log, simulations.

### M5 — Finance Validation Domain
Currículum mínimo, pool de escenarios, benchmark.

### M6 — Experiment Ready
Freeze de protocolo, power/feasibility, consent, export.

### M7 — Human Study
Recolección con control de versiones.

### M8 — Analysis & Thesis
Estadística, resultados, limitaciones, memoria escrita.

### M9 — Demo/Release
Deploy estable en servidor propio con Docker + Cloudflare Tunnel.

## Orden de prioridad
1. riesgo científico;
2. vertical slice;
3. seguridad/reproducibilidad;
4. experiencia de usuario;
5. extensiones.
