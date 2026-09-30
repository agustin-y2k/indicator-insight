from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.health import router
from app.db.session import create_database_engine


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    engine = create_database_engine()
    application.state.database_engine = engine
    try:
        yield
    finally:
        engine.dispose()


def create_app() -> FastAPI:
    application = FastAPI(title="Indicator Insight", version="0.1.0", lifespan=lifespan)
    application.include_router(router)
    return application


app = create_app()
