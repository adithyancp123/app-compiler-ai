"""Deterministic quality scoring utilities."""

from __future__ import annotations

from app.models.contracts import QualityScoreBreakdown, SimulationResult, ValidationReport


def score_quality(
    *,
    validation_report: ValidationReport,
    simulation_result: SimulationResult,
    retry_count: int,
    deterministic: bool,
) -> QualityScoreBreakdown:
    schema_quality = max(0, 100 - len(validation_report.errors) * 15)
    consistency = validation_report.consistency_score
    execution_readiness = simulation_result.confidence_score
    repair_stability = max(0, 100 - retry_count * 20)
    determinism = 100 if deterministic else 70

    final_score = int(round((schema_quality + consistency + execution_readiness + repair_stability + determinism) / 5))
    reasoning = [
        f"Schema quality penalized by {len(validation_report.errors)} validation errors.",
        f"Consistency score derived from lineage and semantic checks: {consistency}.",
        f"Execution readiness uses runtime confidence score: {execution_readiness}.",
        f"Repair stability penalized by retry count: {retry_count}.",
        f"Determinism score set to {determinism} due to fixed templates and stable ordering.",
    ]

    return QualityScoreBreakdown(
        schema_quality=schema_quality,
        consistency=consistency,
        execution_readiness=execution_readiness,
        repair_stability=repair_stability,
        determinism=determinism,
        final_score=final_score,
        reasoning=reasoning,
    )
