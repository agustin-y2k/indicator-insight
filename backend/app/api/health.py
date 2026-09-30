from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter(prefix="/api/health", tags=["health"])


@router.get("/live")
def liveness() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def readiness(request: Request) -> JSONResponse:
    try:
        with request.app.state.database_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(status_code=503, content={"status": "unavailable"})
    return JSONResponse(content={"status": "ok"})
