# Architecture

## Estilo
**Monolito modular** con frontend separado. Evita complejidad distribuida sin sacrificar límites de dominio.

```text
Browser
 │
React + TypeScript
 │ HTTPS/REST
 ▼
FastAPI Modular Monolith
 ├─ identity
 ├─ catalog
 ├─ scenarios
 ├─ replay
 ├─ assessment
 ├─ learner_model
 ├─ judgment
 ├─ adaptation
 ├─ experiments
 ├─ analytics
 ├─ audit
 └─ adapters/
 └─ finance
 │
PostgreSQL
```

Procesos pesados de importación/precomputación pueden ejecutarse como `worker` del mismo codebase. No introducir broker hasta que exista una necesidad real.

## Límites
### Core
No conoce tickers, RSI, MACD ni APIs de mercado.

### Domain Adapter
Transforma datos del dominio al contrato neutral `Scenario` y resuelve outcomes.

### Scenario/Replay
Entrega un snapshot visible hasta `cutoff_time` y aplica Temporal Leakage Guard.

### Assessment
Valida respuestas conceptuales y registra pronósticos.

### Learner Model
BKT exclusivamente.

### Judgment
Brier, accuracy y calibración/reportes.

### Adaptation
P0/P1/P2 y logs de explicación.

### Experiments
Asignación, freezes, benchmark, cohortes.

## Stack baseline
- Frontend: React + TypeScript.
- Backend: Python + FastAPI.
- ORM: SQLAlchemy 2.x.
- DB: PostgreSQL.
- Migrations: Alembic.
- Tests backend: pytest.
- Tests browser: Playwright.
- Containerización: Docker Compose.
- Exposición: Cloudflare Tunnel.

## Regla de dependencia
Los módulos de dominio pueden depender de interfaces del core. El core nunca importa código específico de finance.
