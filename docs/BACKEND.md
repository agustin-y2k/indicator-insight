# Backend

## Runtime
Python + FastAPI dentro de un monolito modular.

## Estructura orientativa
```text
backend/
 app/
 main.py
 core/
 modules/
 identity/
 catalog/
 scenarios/
 replay/
 assessment/
 learner_model/
 judgment/
 adaptation/
 experiments/
 analytics/
 audit/
 adapters/finance/
 db/
 tests/
```

## Reglas
- lógica de dominio fuera de routers;
- funciones matemáticas puras cuando sea posible;
- timestamps UTC internos;
- `Decimal`/tipos controlados donde la reproducibilidad lo requiera;
- migrations Alembic revisables;
- responses versionables para experimentos;
- no depender de APIs externas durante la resolución de un experimento ya congelado: usar snapshots locales/versionados.

## Worker
Usar un proceso separado del mismo contenedor/imagen sólo para importación, generación o precómputo costoso. No introducir Celery/Redis inicialmente.
