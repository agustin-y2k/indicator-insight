# State of the Art

## 1. Bayesian Knowledge Tracing
BKT, introducido por Corbett y Anderson, modela la probabilidad de dominio de una habilidad latente a partir de oportunidades observables, considerando aprendizaje, guess y slip. Su principal ventaja para esta tesis es la interpretabilidad: cada competencia conserva un estado probabilístico explícito.

## 2. Proper scoring rules y Brier Score
Brier (1950) define una regla cuadrática para evaluar pronósticos probabilísticos. Murphy (1973) muestra que el Brier puede analizarse mediante componentes como confiabilidad/calibración, resolución e incertidumbre. Por lo tanto, **Brier y calibración no son sinónimos**.

## 3. Entrenamiento de calibración
La evidencia no es uniforme. Gruetzemacher, Lee y Paradice reportan mejoras modestas mediante una app de entrenamiento de calibración, mientras que Martin y Mandel reportan que un esquema de feedback basado en practical scoring rule no mejoró la calibración en dos experimentos amplios. Este desacuerdo hace pertinente evaluar la política de feedback/adaptación en vez de asumir su efectividad.

## 4. Confianza + knowledge tracing/adaptación
Ya existen antecedentes que incorporan la confianza declarada en sistemas de práctica adaptativa junto con knowledge tracing (por ejemplo, ZPD-KT). Por eso Indicator Insight **no reclama como novedad** “usar BKT y confianza juntos”.

## 5. Simulación financiera y forecasting
Existen plataformas de paper trading, simuladores y servicios de forecasting con puntuación probabilística. Tampoco es novedoso por sí solo reproducir mercados o usar Brier Score. El dominio financiero se justifica como banco de pruebas reproducible, no como fuente única de novedad.

## 6. Gap de interés
El espacio de tesis se concentra en la integración formal y evaluable de:
- estado conceptual interpretable;
- juicio probabilístico medido por separado;
- selección adaptativa explicable;
- escenarios versionados con control temporal;
- portabilidad por adaptadores;
- comparación experimental de políticas.

Ver `RESEARCH_GAP.md` para las afirmaciones autorizadas.
