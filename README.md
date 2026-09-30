# Indicator Insight

**Estado:** especificación previa a implementación.  
**Carrera:** Ingeniería en Informática.  
**Producto:** Indicator Insight.  
**Título de tesis propuesto:** *Diseño y evaluación de una plataforma adaptativa e interpretable para el entrenamiento de decisiones bajo incertidumbre*.

Indicator Insight estudia un **núcleo adaptativo reutilizable** para entrenar decisiones bajo incertidumbre. El diseño mantiene separados:

1. el **dominio conceptual** del aprendiz;
2. la **calidad del juicio probabilístico**;
3. la **política que selecciona el siguiente escenario**.

Finanzas es el dominio principal de validación porque permite construir escenarios históricos reproducibles y resultados objetivos, pero el núcleo no depende de conceptos financieros.

## Principios del proyecto

- BKT modela conocimiento conceptual; un resultado financiero nunca actualiza BKT directamente.
- Brier Score evalúa pronósticos probabilísticos; no equivale por sí solo a calibración ni a dominio conceptual.
- Una ganancia o pérdida financiera no se interpreta como buena o mala decisión sin considerar la información disponible al decidir.
- Ningún escenario puede exponer datos posteriores a su `cutoff_time`.
- La portabilidad del software entre dominios no implica transferencia cognitiva entre dominios.
- Los usuarios sintéticos sirven para validar algoritmos y casos extremos, no para demostrar aprendizaje humano.
- La aplicación no ejecuta operaciones reales ni brinda asesoramiento financiero.

## Documentación principal

1. `docs/THESIS_SCOPE.md` — alcance, pregunta, objetivos e hipótesis.
2. `docs/RESEARCH_GAP.md` — aporte defendible y límites de las afirmaciones.
3. `docs/FORMAL_MODEL.md` — definiciones matemáticas y separación entre estados.
4. `docs/ARCHITECTURE.md` — arquitectura técnica.
5. `docs/EXPERIMENT_PROTOCOL.md` — diseño experimental.
6. `docs/ROADMAP_KANBAN.md` — hitos y flujo de trabajo.
7. `docs/PROJECT_STATE.md` — estado vigente del proyecto.
8. `docs/MASTER_INDEX.md` — índice completo.

## Próxima meta

La primera meta de implementación no es construir todo el backend, sino lograr un **vertical slice científico reproducible**:

`escenario → respuesta conceptual/probabilística → resolución → métricas → persistencia → visualización`

El trabajo operativo se gestiona en Linear y el código, PR, revisión y CI en GitHub.
