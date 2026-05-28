"""Evaluation harness with curated prompt suites and benchmark execution."""

from __future__ import annotations

import json
from pathlib import Path

from app.models.contracts import BenchmarkArtifact, CompileRequest, EvaluationPromptResult, EvaluationReport
from app.services.orchestrator import PipelineOrchestrator

REAL_PROMPTS = [
    "Build a CRM with login, lead tracking, and payment subscriptions",
    "Create an e-commerce app with catalog, cart, checkout, and order tracking",
    "Develop a hospital management system with appointments and billing",
    "Build a school portal with classes, attendance, and report cards",
    "Create a SaaS project management app with team roles and subscriptions",
    "Build an HR system with employee onboarding and payroll",
    "Create a logistics app with shipment tracking and alerts",
    "Develop a support desk app with tickets and SLA reporting",
    "Build a property management portal with tenants and rent collection",
    "Create an event booking platform with payment and notifications",
]

EDGE_PROMPTS = [
    "app",
    "Build fast scalable secure modern thing",
    "Create CRM or maybe e-commerce with hospital features",
    "No auth, but every route must be protected",
    "Use payments but no money-related fields",
    "Need analytics only for all users including guests and admin-only",
    "Generate system with zero pages and full UI coverage",
    "Use no database but persist all records",
    "Need role-based access but do not define roles",
    "Build app now with everything and nothing specified",
]


def run_benchmark() -> BenchmarkArtifact:
    orchestrator = PipelineOrchestrator()

    real_results = [_run_prompt(orchestrator, prompt) for prompt in REAL_PROMPTS]
    edge_results = [_run_prompt(orchestrator, prompt) for prompt in EDGE_PROMPTS]
    all_results = real_results + edge_results

    total = len(all_results)
    success_count = sum(1 for result in all_results if result.success)
    failure_count = total - success_count
    repair_count = sum(1 for result in all_results if result.retries > 0)
    avg_repairs = sum(result.retries for result in all_results) / total if total else 0
    avg_latency = sum(result.latency_ms for result in all_results) / total if total else 0
    avg_consistency = sum(result.consistency_score for result in all_results) / total if total else 0
    execution_rate = (sum(1 for result in all_results if result.executable) / total) if total else 0
    runtime_failures = sum(1 for result in all_results if not result.executable)

    report = EvaluationReport(
        real_prompts=real_results,
        edge_prompts=edge_results,
        success_rate=round((success_count / total) * 100, 2) if total else 0,
        failure_rate=round((failure_count / total) * 100, 2) if total else 0,
        repair_rate=round((repair_count / total) * 100, 2) if total else 0,
        avg_repairs=round(avg_repairs, 2),
        avg_latency=round(avg_latency, 2),
        consistency_score=round(avg_consistency, 2),
        execution_rate=round(execution_rate * 100, 2),
        runtime_failures=runtime_failures,
    )

    markdown = _build_markdown_report(report)
    _persist_reports(report, markdown)

    return BenchmarkArtifact(report=report, markdown_report=markdown)


def _run_prompt(orchestrator: PipelineOrchestrator, prompt: str) -> EvaluationPromptResult:
    result = orchestrator.run(CompileRequest(prompt=prompt))
    failure_category = None
    if not result.validation_report.valid:
        failure_category = result.validation_report.errors[0].code if result.validation_report.errors else "validation_failed"
    elif not result.simulation_result.executable:
        failure_category = "runtime_failed"

    return EvaluationPromptResult(
        prompt=prompt,
        success=result.validation_report.valid and result.simulation_result.executable,
        retries=result.metrics.retry_count,
        latency_ms=result.metrics.latency_ms,
        consistency_score=result.validation_report.consistency_score,
        executable=result.simulation_result.executable,
        failure_category=failure_category,
    )


def _persist_reports(report: EvaluationReport, markdown: str) -> None:
    workspace_root = Path(__file__).resolve().parents[4]
    json_path = workspace_root / "evaluation_report.json"
    markdown_path = workspace_root / "docs" / "evaluation_report.md"

    json_path.write_text(json.dumps(report.model_dump(), indent=2), encoding="utf-8")
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(markdown, encoding="utf-8")


def _build_markdown_report(report: EvaluationReport) -> str:
    return "\n".join(
        [
            "# Evaluation Benchmark Report",
            "",
            f"- Success rate: {report.success_rate}%",
            f"- Failure rate: {report.failure_rate}%",
            f"- Repair rate: {report.repair_rate}%",
            f"- Avg repairs: {report.avg_repairs}",
            f"- Avg latency: {report.avg_latency} ms",
            f"- Avg consistency score: {report.consistency_score}",
            f"- Execution rate: {report.execution_rate}%",
            f"- Runtime failures: {report.runtime_failures}",
            "",
            "## Real Prompt Results",
            *[
                f"- {'PASS' if item.success else 'FAIL'} | consistency={item.consistency_score} | retries={item.retries} | {item.prompt}"
                for item in report.real_prompts
            ],
            "",
            "## Edge Prompt Results",
            *[
                f"- {'PASS' if item.success else 'FAIL'} | failure={item.failure_category or 'none'} | {item.prompt}"
                for item in report.edge_prompts
            ],
        ]
    )
