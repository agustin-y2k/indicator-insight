# Thesis Scope — Baseline

## Título propuesto
**Diseño y evaluación de una plataforma adaptativa e interpretable para el entrenamiento de decisiones bajo incertidumbre.**

Producto de validación: **Indicator Insight**.

## Problema
Los entornos educativos suelen reducir el desempeño a respuestas correctas/incorrectas. En decisiones bajo incertidumbre esa observación es insuficiente: una persona puede dominar conceptos y estar mal calibrada, acertar por azar o equivocarse a pesar de haber usado un proceso razonable. Una adaptación pedagógica que mezcle estas señales sin distinguirlas puede inferir incorrectamente qué necesita practicar el aprendiz.

## Pregunta principal
**¿Puede una política adaptativa e interpretable que combine, sin confundir, estimaciones de dominio conceptual y desempeño probabilístico mejorar el aprendizaje y la calidad del juicio bajo incertidumbre frente a una secuencia de práctica no adaptativa?**

## Pregunta de ingeniería
**¿Puede el mismo núcleo de escenarios, evaluación y adaptación reutilizarse en más de un dominio mediante adaptadores, sin modificar la lógica central?**

La segunda pregunta evalúa portabilidad arquitectónica. No implica afirmar transferencia cognitiva entre dominios.

## Hipótesis de trabajo
H1. Una política dual (P2) producirá una mejora mayor en desempeño conceptual y/o probabilístico en un benchmark fijo que una secuencia no adaptativa (P0). 
H2. La política P2 puede explicar cada selección de escenario mediante variables observables del estado del aprendiz. 
H3. Un segundo adaptador mínimo puede reutilizar el core sin cambios en los módulos de evaluación, learner model y adaptación.

Las hipótesis son falsables. Resultados nulos o adversos no invalidan la tesis si el diseño, implementación y análisis son correctos.

## Objetivo general
Diseñar, implementar y evaluar una plataforma web adaptativa e interpretable para entrenar decisiones bajo incertidumbre, separando el modelado del dominio conceptual de la evaluación del juicio probabilístico y utilizando finanzas como dominio principal de validación.

## Objetivos específicos
1. Diseñar un motor de escenarios reproducibles, versionados y portables entre dominios, con garantías automáticas contra filtración temporal de información.
2. Implementar un modelo dual del aprendiz: BKT para competencias conceptuales y métricas probabilísticas para juicio/confianza, junto con políticas adaptativas comparables P0/P1/P2.
3. Evaluar la plataforma mediante tests automatizados, simulaciones para validar algoritmos y un protocolo con participantes reales basado en pretest fijo, entrenamiento y posttest fijo.

## Alcance
Incluye:
- aplicación web;
- motor de escenarios;
- finance adapter;
- conceptual assessment;
- pronósticos probabilísticos binarios iniciales;
- BKT interpretable;
- Brier Score, exactitud y análisis de calibración;
- adaptación interpretable;
- experiment engine;
- auditoría/reproducibilidad;
- despliegue Dockerizado.

Fuera de alcance obligatorio:
- trading real;
- asesoramiento financiero;
- predicción automática de precios;
- aprendizaje profundo;
- ranking por rentabilidad;
- microservicios;
- demostrar transferencia cognitiva entre dominios;
- prometer ausencia de sesgo de supervivencia si el dataset disponible no permite documentarla.

## Dominio financiero
Finanzas se usa porque los eventos pueden reconstruirse históricamente y resolverse objetivamente. El núcleo no contiene tickers, RSI, MACD ni reglas financieras: esos conceptos pertenecen al adaptador.

## Criterio de éxito de tesis
El proyecto se considera defendible si entrega:
- modelo formal coherente;
- software funcionando end-to-end;
- garantías de no-leakage verificadas;
- comparación explícita de políticas;
- protocolo y análisis reproducible;
- discusión honesta de limitaciones y resultados.
