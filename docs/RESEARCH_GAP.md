# Research Gap and Claim Discipline

## Aporte propuesto
Indicator Insight estudia una **arquitectura adaptativa dual e interpretable** para práctica de decisiones bajo incertidumbre. La contribución no está en inventar BKT, Brier, calibración, replay o simulación, sino en cómo se separan, conectan, verifican y comparan dentro de una plataforma reutilizable.

## Contribuciones potenciales
1. **Separación formal de estados:** conocimiento conceptual y juicio probabilístico se mantienen como señales distintas.
2. **Política dual explicable:** selección de escenarios basada en ambos estados sin colapsarlos en una puntuación opaca.
3. **Contrato de escenario independiente del dominio:** mismo core para finance y un segundo adaptador mínimo.
4. **Temporal Leakage Guard:** propiedad verificable que impide que datos futuros lleguen a la experiencia del aprendiz.
5. **Comparación P0/P1/P2:** la tesis evalúa políticas, no sólo usabilidad del producto.
6. **Reproducibilidad:** datasets versionados, seeds, escenarios inmutables y registros de decisiones adaptativas.

## NO reclamar
- “Primer sistema que combina BKT y confianza”.
- “Primer sistema educativo que usa Brier”.
- “Brier mide conocimiento”.
- “Brier es calibración”.
- “Ganar una operación demuestra buena decisión”.
- “El sistema enseña a ganar dinero”.
- “El core general demuestra transferencia del aprendizaje”.
- “Los usuarios sintéticos demuestran eficacia pedagógica”.
- “El dataset no tiene survivorship bias” sin evidencia documental.

## Qué puede afirmarse si se verifica
- El core puede ser domain-agnostic a nivel de software.
- La política adaptativa es auditable y puede explicar por qué eligió un escenario.
- Los escenarios financieros se reproducen con información disponible hasta un instante de corte.
- Las métricas conceptuales y probabilísticas pueden evolucionar de manera diferente en un mismo aprendiz.
- La política P2 mejora/no mejora frente a baselines según los resultados observados.

## Regla de cambio
Toda modificación de pregunta, hipótesis, variable primaria, política experimental o interpretación de métrica requiere ADR y, si el experimento ya comenzó, una versión nueva del protocolo; nunca una edición retrospectiva silenciosa.
