# Adaptive Policy

## Objetivo
Comparar políticas con complejidad incremental y mantener la política propuesta interpretable.

## P0 — Fixed Sequence
- Secuencia predefinida/estratificada.
- Registra conocimiento, probabilidades y métricas.
- No utiliza el estado del usuario para elegir el siguiente escenario.
- Baseline principal.

## P1 — Knowledge-only
- Usa BKT para priorizar competencias conceptuales no dominadas.
- No utiliza calibración/Brier para seleccionar el escenario.
- Permite aislar el valor adicional de la señal probabilística.

## P2 — Dual Adaptive (Indicator Insight)
Combina necesidad conceptual con necesidad de práctica probabilística y restricciones de cobertura.

Esquema inicial auditable:

`score(s,u) = wK*KNeed(s,u) + wJ*JNeed(s,u) + wD*DifficultyFit(s,u) + wS*Spacing(s,u) + wC*Coverage(s,u) - repetition_penalty`

Donde:
- `KNeed`: función de `1-P(mastery)` para competencias del escenario.
- `JNeed`: necesidad de practicar el tipo de juicio, considerando Brier/calibración y cantidad de evidencia.
- `DifficultyFit`: evita saltos extremos de dificultad.
- `Spacing`: favorece recuperación espaciada.
- `Coverage`: evita que el sistema se encierre en pocas competencias.

## Reglas
- Pesos y definiciones se versionan (`policy_version`).
- No se ajustan con resultados del mismo experimento que pretenden evaluar.
- Debe existir fallback determinista si no hay datos suficientes.
- Empates se resuelven con una regla reproducible/seed registrada.
- El motor no busca maximizar rentabilidad ni acertar mercados.

## Explicación al usuario/investigador
Ejemplo interno:
> Seleccionado SC-204 porque `probabilidad_condicional` tiene mastery 0.41, no se practica hace 6 intentos y el usuario presenta sobreconfianza en escenarios de incertidumbre media. Se descartó SC-198 por repetición reciente.

La interfaz de aprendiz puede mostrar una explicación simplificada; el log de investigación conserva la explicación completa.
