"""Application entrypoint for FastAPI backend."""

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()
app = FastAPI(title=settings.app_name)
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/")
def root() -> dict[str, str]:
    """Simple service status endpoint."""
    return {"service": settings.app_name, "status": "ok"}
