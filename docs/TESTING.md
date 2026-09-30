# Testing Strategy

## Pirámide pragmática
1. **Unit tests**: BKT, Brier, validaciones, policy scoring, temporal boundaries.
2. **Contract/integration**: DB + módulos + adapters.
3. **Property-based**: invariantes matemáticos/temporales.
4. **End-to-end**: Playwright para flujo completo.
5. **Simulation tests**: learners sintéticos para estabilidad, no para eficacia pedagógica.

## Tests matemáticos mínimos
### Brier
- predicción perfecta → 0;
- valores siempre en `[0,1]` para convención binaria;
- rechazar `p < 0` y `p > 1`;
- casos manuales conocidos.

### BKT
- posterior en `[0,1]`;
- correcta aumenta evidencia de mastery bajo parámetros válidos habituales;
- incorrecta reduce evidencia bajo parámetros válidos habituales;
- transición sólo se ejecuta una vez por oportunidad;
- outcome financiero no llama la función de update BKT.

### Adaptación
- P0 independiente del estado del aprendiz;
- P1 ignora métricas de juicio;
- P2 registra todos los features usados;
- fallback determinista con poca evidencia.

## Gate de merge
No mergear si falla:
- temporal leakage suite;
- math tests;
- migrations/integrity;
- E2E científico crítico;
- policy workflow.
