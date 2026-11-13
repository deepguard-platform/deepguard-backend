from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.api.jobs import router as jobs_router
from app.core.config import settings
from app.db.init_db import init_db
from app.db.session import engine


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)
app.include_router(jobs_router)


@app.get("/health", tags=["health"])
def health() -> dict:
    """The app is alive."""
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
def ready() -> dict:
    """The app can reach PostgreSQL and Redis."""
    checks = {}
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"
    try:
        redis.Redis.from_url(settings.redis_url, socket_connect_timeout=2).ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "error"
    if "error" in checks.values():
        raise HTTPException(status_code=503, detail=checks)
    return {"status": "ready", **checks}
