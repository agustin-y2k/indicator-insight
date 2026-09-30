# Data Model

## Entidades principales

### Usuarios y estudio
- `User`
- `LearnerProfile`
- `Experiment`
- `ExperimentAssignment`
- `ConsentRecord`

### Currículum
- `Domain`
- `Competency`
- `CompetencyPrerequisite`

### Escenarios
- `ScenarioDefinition`
- `ScenarioVersion` (inmutable después de publicar)
- `EvidenceItem`
- `ConceptualItem`
- `ResolutionRule`
- `DatasetSnapshot`

### Interacción
- `Attempt`
- `ConceptualResponse`
- `ProbabilisticJudgment`
- `Outcome`

### Modelos
- `KnowledgeState` (BKT por usuario/competencia/version)
- `JudgmentSummary` (ventana/metodología versionada)
- `AdaptationDecision`

### Auditoría
- `MetricComputation`
- `AuditEvent`
- `SoftwareRelease`

## Reglas de integridad
- Cada `Attempt` apunta a una `ScenarioVersion` exacta.
- Probabilidades se almacenan como valor decimal validado `[0,1]` y como input raw si es útil para auditoría.
- Outcomes no se sobrescriben: cualquier corrección genera nueva versión/audit trail.
- `KnowledgeState` registra qué respuesta conceptual produjo la transición.
- `AdaptationDecision` almacena candidatos, features, policy_version y motivo.
- Experimentos congelados no pueden cambiar políticas/pools sin nueva versión.

## PostgreSQL
PostgreSQL reemplaza MongoDB de diseños antiguos porque predominan relaciones, integridad referencial, consultas analíticas y versionado explícito.
