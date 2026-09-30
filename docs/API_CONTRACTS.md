# API Contracts — Draft

Los paths exactos se congelan durante implementación; estos contratos describen responsabilidades.

```text
GET /api/v1/domains
GET /api/v1/competencies
POST /api/v1/sessions
GET /api/v1/scenarios/next
GET /api/v1/scenarios/{id}
POST /api/v1/attempts
POST /api/v1/attempts/{id}/conceptual-response
POST /api/v1/attempts/{id}/probabilistic-judgment
POST /api/v1/attempts/{id}/lock
POST /api/v1/attempts/{id}/resolve
GET /api/v1/me/knowledge-state
GET /api/v1/me/judgment-summary
GET /api/v1/me/progress
```

## Seguridad de payload
Antes de lock/resolution, ningún payload del escenario debe incluir:
- `ground_truth`;
- `resolution_value`;
- timestamps futuros no visibles;
- identificadores que rompan una condición de ceguera experimental.

## Idempotencia
Lock y resolve deben ser idempotentes o rechazar estados inconsistentes de forma explícita.
