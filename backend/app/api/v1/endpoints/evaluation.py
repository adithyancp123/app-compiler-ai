"""Evaluation endpoints for benchmark and metrics reporting."""

import json

from fastapi import APIRouter
from fastapi.responses import PlainTextResponse, Response

from app.models.contracts import BenchmarkArtifact, EvaluationReport
from app.pipeline.evaluation.harness import run_benchmark
from app.services.exporter import to_markdown

router = APIRouter()


@router.get("/report", response_model=EvaluationReport)
def get_evaluation_report() -> EvaluationReport:
    """Run benchmark and return latest aggregated report."""
    return run_benchmark().report


@router.post("/run", response_model=BenchmarkArtifact)
def run_evaluation_benchmark() -> BenchmarkArtifact:
    """Execute benchmark and persist JSON/Markdown artifacts."""
    return run_benchmark()


@router.get("/export/json")
def export_evaluation_json() -> Response:
    """Export benchmark report as JSON."""
    report = run_benchmark().report.model_dump()
    return Response(
        content=json.dumps(report, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=benchmark_report.json"},
    )


@router.get("/export/markdown")
def export_evaluation_markdown() -> PlainTextResponse:
    """Export benchmark report as markdown."""
    report = run_benchmark().report.model_dump()
    return PlainTextResponse(
        content=to_markdown("Benchmark Report", report),
        headers={"Content-Disposition": "attachment; filename=benchmark_report.md"},
    )
