# Desarrollo y validación de la base técnica

II-6 prepara la infraestructura; no crea tablas de negocio ni implementa escenarios,
métricas, modelos del aprendiz, adaptación, adapters o autenticación.

## Estructura y dependencias

`backend/app/core` se reserva para contratos y lógica independientes de dominio e
infraestructura. `modules` alojará los módulos de aplicación; `adapters` las
implementaciones de dominio. `core/scenario.py` define el contrato neutral
[Scenario v1](SCENARIO_CONTRACT.md); `modules` y `adapters` conservan marcadores de paquete.
`api` contiene health checks y `db` la base declarativa y creación del engine.
No se agregan paquetes finance ni entidades anticipadas.

Backend: Python 3.12, FastAPI (HTTP/OpenAPI), Uvicorn (ASGI), SQLAlchemy 2.x (ORM),
psycopg 3 binary (driver PostgreSQL) y Alembic (migraciones).
pytest verifica API y migraciones; HTTPX2 permite usar TestClient; Ruff proporciona
lint y formato. pip-tools genera los locks; setuptools construye el paquete.

Frontend: Node 22.12 o superior dentro de la rama 22, React y React DOM para la UI;
Vite y su plugin React para desarrollo/build. TypeScript y los paquetes de tipos
verifican contratos; ESLint, typescript-eslint, globals y los plugins React
verifican código. Playwright prepara pruebas de navegador con Chromium.

`package-lock.json`, `requirements.txt` y `requirements-dev.txt` fijan dependencias
directas y transitivas. Los locks Python se generan con Python 3.12.
Las imágenes base usan etiquetas de versión mayor/menor; sus parches pueden cambiar
al reconstruir. No se pretende un build idéntico a nivel de digest.

## Desarrollo local sin contenedores de aplicación

El arranque completo con Compose está en README. Para trabajar fuera de las imágenes,
crear un entorno Python 3.12 y usar Node 22:

```sh
cd backend
python3.12 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install --no-deps --no-build-isolation -e .
ruff check .
ruff format --check .
pytest -q -m 'not integration'
```

Configurar `DATABASE_URL` con PostgreSQL accesible antes de ejecutar
`alembic upgrade head` y `uvicorn app.main:app --reload`. La aplicación no lee `.env`
directamente; Compose lo usa para interpolar variables. No copiar la URL interna de
Compose a un proceso local: `postgres` sólo se resuelve en la red de contenedores.

En otra terminal:

```sh
cd frontend
npm ci
npm run typecheck
npm run lint
npm run build
npm run dev
```

Vite redirige `/api` a `http://127.0.0.1:8000` localmente y a `http://backend:8000`
en Compose mediante `API_PROXY_TARGET`. El navegador usa el mismo origen;
no necesita conocer la URL interna ni habilitar CORS.

## Health checks y migraciones

`GET /api/health/live` verifica el proceso. `GET /api/health/ready` ejecuta `SELECT 1`
contra PostgreSQL y devuelve 503 genérico si no hay conexión, sin exponer credenciales.
Readiness no reemplaza la validación de la revisión Alembic.

La revisión `0001` establece una baseline vacía: Alembic crea y mantiene su tabla
`alembic_version`, pero no existen tablas de dominio. `upgrade()` y `downgrade()`
son intencionalmente vacíos. El downgrade a `base` vacía el registro de versión;
Alembic conserva su tabla de control. Las siguientes issues agregarán sus tablas.

Prueba de upgrade, comprobación de metadata, downgrade y nuevo upgrade en una base
dedicada y vacía (no usar la base de desarrollo con datos):

```sh
docker compose exec postgres sh -c 'createdb -U "$POSTGRES_USER" indicator_migration_test'
docker compose exec -T -e TEST_DATABASE_URL=postgresql+psycopg://indicator:LOCAL_PASSWORD@postgres:5432/indicator_migration_test backend pytest -q
docker compose exec postgres sh -c 'dropdb -U "$POSTGRES_USER" indicator_migration_test'
```

Reemplazar usuario y contraseña por los de `.env`; codificar caracteres reservados
en la URL. La suite rechaza una base que ya contenga tablas. Sin `TEST_DATABASE_URL`,
el test de integración se omite explícitamente. CI siempre proporciona una base vacía.

Para regenerar locks tras modificar dependencias, desde `backend` con Python 3.12:

```sh
pip-compile --allow-unsafe --strip-extras --no-emit-index-url --output-file=requirements.txt pyproject.toml
pip-compile --allow-unsafe --strip-extras --no-emit-index-url --extra=dev --output-file=requirements-dev.txt pyproject.toml
```

## Playwright y CI

```sh
cd frontend
npm ci
npx playwright install --with-deps chromium
npm run test:e2e
# Con Compose activo, incluye la prueba real frontend → backend → PostgreSQL:
E2E_BASE_URL=http://127.0.0.1:5173 npm run test:e2e
```

Sin `E2E_BASE_URL`, Playwright inicia Vite y prueba loading, conexión y error con
respuestas HTTP controladas; la prueba de integración real se omite.
Con la variable, usa la aplicación existente. No se requieren APIs financieras ni
escenarios de negocio. Los futuros flujos científicos necesitan sus propios E2E.

CI tiene jobs independientes para pytest/migraciones/Ruff, TypeScript/ESLint/build/
Playwright y arranque/health checks de Compose. Los pasos fallidos hacen fallar el job;
la protección de ramas debe exigir estos checks en GitHub para impedir merges.
Los fallos conservan trazas locales en `test-results`, ignoradas por Git.

Compose usa tres servicios, arranque ordenado mediante health checks, usuarios sin
privilegios en las aplicaciones, puertos de aplicación limitados a localhost y un
volumen explícito para PostgreSQL. No incluye configuración de producción o túnel.
