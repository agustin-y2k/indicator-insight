# Scenario Replay and Temporal Safety

## Modelo temporal
Cada escenario histórico fija:
- `cutoff_time = t0`: último instante visible al usuario.
- `horizon`: ventana de resolución.
- `resolution_time`: instante/regla para conocer el outcome.

Invariante:
`max(source_timestamp_visible) <= cutoff_time`

## Temporal Leakage Guard
El backend debe rechazar un escenario si:
- una vela/fila visible excede `cutoff_time`;
- un indicador fue calculado usando una ventana que mira hacia adelante;
- una feature contiene información derivada del futuro;
- metadata revela fecha/activo cuando esa información debe estar cegada;
- el outcome llega en el mismo payload antes de cerrar el intento.

## Arquitectura de datos
Preferir snapshots/versiones con hashes reproducibles. El escenario guarda referencias a:
- dataset snapshot;
- transform version;
- scenario generator version;
- policy-independent scenario version.

## Tests obligatorios
- boundary exacta en `t0`;
- timezone normalizada;
- splits/dividendos documentados;
- ventanas rolling sólo retrospectivas;
- indicadores comparados contra implementación de referencia;
- no endpoint leakage;
- no leakage por caché/frontend;
- outcome inaccessible hasta `attempt.locked_at`.

## Ceguera
Ocultar activo/fecha es una opción experimental, no una garantía universal. Debe ser configurable y versionada.

## Sesgo de supervivencia
El sistema no afirmará eliminarlo a menos que el dataset incluya y documente de forma adecuada activos deslistados/universo histórico. Si no es posible, se declara como limitación.
