"""Compile endpoints exposing the pipeline orchestrator."""

import json

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, Response

from app.models.contracts import CompileRequest, CompileResponse, export_contract_schemas
from app.services.exporter import to_markdown
from app.services.orchestrator import PipelineOrchestrator

router = APIRouter()


@router.post("", response_model=CompileResponse)
def compile_prompt(payload: CompileRequest) -> CompileResponse:
    """Run compile pipeline with deterministic modular behavior."""
    orchestrator = PipelineOrchestrator()
    return orchestrator.run(payload)


@router.get("/contracts")
def get_contract_schemas() -> dict:
    """Expose JSON Schemas for strict contract inspection."""
    return export_contract_schemas()


@router.post("/export/json")
def export_compile_json(payload: CompileRequest) -> Response:
    """Export compiled output as JSON file content."""
    result = PipelineOrchestrator().run(payload).model_dump()
    return Response(
        content=json.dumps(result, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=compile_output.json"},
    )


@router.post("/export/markdown")
def export_compile_markdown(payload: CompileRequest) -> PlainTextResponse:
    """Export compiled output as markdown."""
    result = PipelineOrchestrator().run(payload).model_dump()
    body = to_markdown("Compile Output", result)
    return PlainTextResponse(
        content=body,
        headers={"Content-Disposition": "attachment; filename=compile_output.md"},
    )
