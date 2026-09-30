# Formal Model

## 1. Dos estados, no uno
Para un aprendiz `u` en tiempo `t`:

- `K_u,t`: estado de conocimiento conceptual por competencia.
- `J_u,t`: resumen de calidad de juicio probabilístico.

No se define una función única obligatoria que colapse ambos estados.

## 2. BKT para dominio conceptual
Por competencia `k` se mantienen cuatro parámetros clásicos:
- `P(L0)`: probabilidad inicial de dominio.
- `P(T)`: probabilidad de transición/aprendizaje.
- `P(G)`: probabilidad de acertar sin dominar (guess).
- `P(S)`: probabilidad de fallar aun dominando (slip).

Si la observación conceptual es correcta:

`P(L | correct) = P(L)*(1-S) / [P(L)*(1-S) + (1-P(L))*G]`

Si es incorrecta:

`P(L | incorrect) = P(L)*S / [P(L)*S + (1-P(L))*(1-G)]`

Después de observar:

`P(L_next) = P(L | obs) + (1-P(L | obs))*T`

### Restricción crítica
Sólo una observación con clave conceptual verificable puede alimentar BKT. Un retorno, una ganancia, una dirección futura o cualquier outcome estocástico del dominio no constituye evidencia directa de mastery.

## 3. Pronóstico probabilístico binario
Para un evento resoluble `Y_i ∈ {0,1}`, el usuario declara `p_i ∈ [0,1]`.

Brier binario adoptado por el proyecto:

`BS = (1/N) * Σ (p_i - y_i)^2`

Convención:
- 0 = mejor posible.
- 1 = peor posible para evento binario.

Esta convención debe permanecer estable en todo el producto, tests, informes y tesis.

## 4. Exactitud
Si se deriva una decisión binaria a partir de un umbral previamente fijado (por ejemplo 0.5):

`Accuracy = correct_decisions / total_decisions`

Accuracy no reemplaza Brier porque ignora la intensidad de la probabilidad declarada.

## 5. Calibración
Para predicciones agrupadas por rangos o mediante estimadores definidos antes del análisis:
- confianza media del grupo;
- frecuencia observada del evento;
- diferencia entre ambas.

La curva de reliability grafica `forecast probability` vs `observed frequency`.

Puede informarse un error de calibración agregado, pero su método (bins, pesos, mínimos por bin) debe quedar congelado en el protocolo antes del experimento principal.

## 6. Resolución
La resolución expresa la capacidad de emitir probabilidades diferentes en situaciones con frecuencias diferentes. Brier puede descomponerse conceptualmente como:

`Brier = Reliability - Resolution + Uncertainty`

La implementación sólo presentará esta descomposición cuando haya tamaño muestral suficiente y la metodología esté validada.

## 7. Resumen de juicio `J`
`J` no es una única “nota” obligatoria. Para adaptación puede incluir features auditables como:
- Brier rolling con ventana/versionado;
- sesgo de confianza (`mean(p_confidence) - empirical_accuracy`) cuando sea aplicable;
- cobertura/número de observaciones;
- dificultad y tipo de escenarios vistos;
- recencia.

Con pocos datos, el motor debe expresar insuficiencia de evidencia en vez de inventar un diagnóstico.

## 8. Parámetros BKT
Los parámetros no se elegirán para maximizar resultados del experimento principal. Estrategia:
1. valores iniciales documentados/literatura;
2. piloto o simulación para sanity checks;
3. análisis de sensibilidad;
4. congelamiento antes del experimento principal.

## 9. Interpretabilidad
Toda `AdaptationDecision` debe poder reconstruirse a partir de:
- estado BKT usado;
- métricas `J` usadas;
- restricciones del currículum;
- candidatos considerados;
- pesos/heurística versionados;
- escenario finalmente seleccionado.
