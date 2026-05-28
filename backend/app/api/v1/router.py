"""API router registration for v1 endpoints."""

from fastapi import APIRouter

from app.api.v1.endpoints import compile, evaluation, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(compile.router, prefix="/compile", tags=["compile"])
api_router.include_router(evaluation.router, prefix="/evaluation", tags=["evaluation"])
