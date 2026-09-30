# Domain Adapter Contract

## Objetivo
Permitir que el core entrene decisiones bajo incertidumbre sin acoplarse a finanzas.

## Conceptos neutralizados
Un adaptador debe proveer:
- `Domain`;
- `Competency` catalog;
- `ScenarioDefinition/Version`;
- evidencia visible;
- pregunta conceptual opcional;
- evento probabilístico resoluble;
- `cutoff_time` cuando el dominio es temporal;
- `resolution_rule`;
- `ground_truth/outcome`;
- dificultad y tags.

## Interface conceptual
```python
class DomainAdapter(Protocol):
 def build_scenario(self, scenario_version_id: UUID) -> ScenarioPayload: ...
 def validate_temporal_safety(self, scenario_version_id: UUID) -> SafetyReport: ...
 def resolve_outcome(self, scenario_version_id: UUID) -> Outcome: ...
 def validate_conceptual_answer(self, item_id: UUID, answer: object) -> ConceptualResult: ...
```

## Finance Adapter
Puede conocer:
- OHLCV;
- indicadores técnicos;
- horizonte;
- activo/universo;
- reglas de evento financiero.

No entrega al core una “señal de compra”. Entrega evidencia y una resolución objetiva.

## Segundo adaptador
Para demostrar portabilidad arquitectónica basta un adaptador mínimo de otro ámbito con varios escenarios y tests contractuales. No hace falta realizar un segundo experimento humano salvo que la tesis se amplíe explícitamente.
