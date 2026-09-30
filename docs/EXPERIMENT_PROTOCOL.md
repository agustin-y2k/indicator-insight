# Experiment Protocol

## Objetivo
Evaluar la política adaptativa, no sólo la usabilidad de la plataforma.

## Diseño mínimo

`Consentimiento → Pretest fijo → Asignación → Training → Posttest fijo → Encuesta breve`

Retención diferida es deseable si el calendario y la aprobación ética lo permiten.

## Grupos/políticas
Preferencia científica:
- P0: secuencia fija.
- P1: adaptación sólo por BKT.
- P2: adaptación dual.

Si el número de participantes no permite tres grupos con potencia razonable, priorizar P0 vs P2 y dejar P1 para simulación/análisis secundario. La decisión se toma **antes** de recolectar el experimento principal mediante análisis de potencia y disponibilidad real.

## Pretest/Posttest
- Condiciones fijas y comparables.
- Items equivalentes o formas paralelas versionadas.
- No adaptativos.
- Separados del pool de training cuando sea posible.
- Miden tanto conceptual como probabilístico.

## Resultados
### Co-primarios propuestos
1. cambio en desempeño conceptual en benchmark fijo;
2. cambio en Brier Score sobre pronósticos del benchmark fijo.

### Secundarios
- accuracy;
- reliability/calibration error predefinido;
- resolución si N lo permite;
- tiempo por intento;
- cobertura de competencias;
- retención, si existe medición diferida;
- usabilidad como resultado secundario, no prueba principal de aprendizaje.

## Análisis
- reportar tamaños de efecto e intervalos de confianza;
- no depender únicamente de `p < 0.05`;
- controlar baseline/pretest en el análisis cuando corresponda;
- documentar datos excluidos y motivos;
- separar análisis confirmatorio de exploratorio.

Con muestra pequeña, presentar la investigación como estudio de factibilidad/piloto cuantitativo y evitar conclusiones causales excesivas.

## Randomización
- seed/version registrada;
- asignación antes del training;
- no cambiar grupo por desempeño;
- almacenar `experiment_assignment` inmutable.

## Participantes
La población exacta depende del acceso institucional y debe aprobarse con tutor. No asumir inversores reales; estudiantes universitarios/novatos son una población viable si la pregunta y el material pedagógico se alinean.

## Ética
- consentimiento informado;
- no inducir inversión real;
- no recolectar PII innecesaria;
- posibilidad de retirarse;
- tratamiento de datos documentado;
- aprobación institucional cuando corresponda.

## Congelamiento
Antes del primer participante del estudio principal se debe etiquetar una versión del:
- protocolo;
- pool benchmark;
- policy P0/P1/P2;
- parámetros BKT;
- esquema de métricas;
- dataset snapshot.
