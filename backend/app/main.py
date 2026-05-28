"""Application entrypoint for FastAPI backend."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)

# CORS (safe for internship deployment)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/")
def root():
    return {
        "service": settings.app_name,
        "status": "ok",
    }