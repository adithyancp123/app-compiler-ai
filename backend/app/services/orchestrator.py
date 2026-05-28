"""Pipeline orchestrator coordinating all generation and checks."""

from __future__ import annotations

from uuid import uuid4

from app.core.config import get_settings
from app.models.contracts import (
    CompileRequest,
    CompileResponse,
    MetricsSnapshot,
    SimulationResult,
    StageName,
    StageOutput,
    StageStatus,
    ValidationReport,
)
from app.pipeline.evaluation.metrics import MetricsCollector
from app.pipeline.evaluation.scoring import score_quality
from app.pipeline.intent.extractor import IntentExtractor
from app.pipeline.repair.engine import RepairEngine
from app.pipeline.runtime.simulator import RuntimeSimulator
from app.pipeline.schema.generator import SchemaGenerator
from app.pipeline.system_design.designer import SystemDesigner
from app.pipeline.validation.engine import ValidationEngine


class PipelineOrchestrator:
    """Coordinates stage execution in deterministic modular order."""

    def __init__(self) -> None:
        self.settings = get_settings()
        self.intent_extractor = IntentExtractor()
        self.system_designer = SystemDesigner()
        self.schema_generator = SchemaGenerator()
        self.validation_engine = ValidationEngine()
        self.repair_engine = RepairEngine()
        self.runtime_simulator = RuntimeSimulator()

    def run(self, payload: CompileRequest) -> CompileResponse:
        """Execute modular deterministic pipeline with targeted repairs."""
        metrics_collector = MetricsCollector()
        stage_outputs: list[StageOutput] = []

        intent = self.intent_extractor.run(payload.prompt)
        stage_outputs.append(intent)

        design = self.system_designer.run(intent)
        stage_outputs.append(design)

        schema_stage = self.schema_generator.run(design)
        stage_outputs.append(schema_stage)

        generated_schema = schema_stage.content
        validation_report = self.validation_engine.run(generated_schema)
        stage_outputs.append(
            StageOutput(
                stage=StageName.validation,
                status=StageStatus.success if validation_report.valid else StageStatus.warning,
                content=validation_report.model_dump(),
                notes=["Entity lineage, feature, role, and navigation checks completed"],
            )
        )

        repair_actions = []
        repair_attempts = 0
        while not validation_report.valid and repair_attempts < self.settings.max_repair_attempts:
            generated_schema, actions = self.repair_engine.run(generated_schema, validation_report.errors)
            repair_actions.extend(actions)
            repair_attempts += 1
            validation_report = self.validation_engine.run(generated_schema)

        stage_outputs.append(
            StageOutput(
                stage=StageName.repair,
                status=StageStatus.success if validation_report.valid else StageStatus.failed,
                content={"actions": [action.model_dump() for action in repair_actions], "attempts": repair_attempts},
                notes=["Targeted module repairs only; full regeneration avoided"],
            )
        )

        simulation = self.runtime_simulator.run(generated_schema)
        stage_outputs.append(
            StageOutput(
                stage=StageName.runtime_simulation,
                status=StageStatus.success if simulation["executable"] else StageStatus.failed,
                content=simulation,
                notes=["Execution-aware dry run checks completed"],
            )
        )

        simulation_result = SimulationResult(**simulation)
        quality_score = score_quality(
            validation_report=validation_report,
            simulation_result=simulation_result,
            retry_count=repair_attempts,
            deterministic=True,
        )

        metrics = metrics_collector.snapshot(
            retries=repair_attempts,
            error_count=len(validation_report.errors),
            warning_count=len(validation_report.warnings),
            stage_count=len(stage_outputs),
            quality_score=quality_score.final_score,
        )

        assumptions = list(intent.content.get("assumptions", []))
        clarification_questions = self._clarification_questions(payload.prompt, intent.content.get("constraints", []))
        explainability = self._build_explainability(intent.content, validation_report, repair_actions, simulation_result)

        return CompileResponse(
            request_id=str(uuid4()),
            assumptions=assumptions,
            clarification_questions=clarification_questions,
            stage_outputs=stage_outputs,
            generated_schema=generated_schema,
            validation_report=ValidationReport.model_validate(validation_report.model_dump()),
            repair_actions=repair_actions,
            simulation_result=simulation_result,
            quality_score=quality_score,
            metrics=MetricsSnapshot(**metrics),
            explainability=explainability,
        )

    def _clarification_questions(self, prompt: str, constraints: list[str]) -> list[str]:
        questions = []
        lowered = prompt.lower()
        if "build an app for my business" in lowered or len(lowered.split()) <= 5:
            questions.append("What are your top 3 core workflows (e.g., billing, orders, scheduling)?")
            questions.append("Which user roles must be supported (admin, manager, member)?")
        if "payment" in lowered and "stripe" not in lowered:
            questions.append("Which payment provider should be used (Stripe, Razorpay, or PayPal)?")
        if any("conflicting" in constraint.lower() for constraint in constraints):
            questions.append("Please choose one preferred workflow where alternatives were provided.")
        if "everyone is admin" in lowered and "admins only" in lowered:
            questions.append("Should all users be admin, or should analytics remain admin-only?")
        return questions

    def _build_explainability(
        self,
        intent_content: dict,
        validation_report: ValidationReport,
        repair_actions: list,
        simulation_result: SimulationResult,
    ) -> dict[str, list[str]]:
        features = intent_content.get("features", [])
        reasons = {
            "intent_extraction": [
                f"Detected features: {', '.join(features)}" if features else "Used default baseline feature set.",
                "Applied deterministic domain template and stable field ordering.",
            ],
            "validation": [
                f"Consistency score computed as {validation_report.consistency_score}/100.",
                "Validated UI->API->DB field lineage and role/access constraints.",
            ],
            "repair": [
                action.action for action in repair_actions
            ]
            or ["No repair required because validation passed."],
            "runtime_simulation": [
                "Checked route integrity, auth gates, DB relation integrity, and feature gating.",
                f"Runtime confidence evaluated as {simulation_result.confidence_score}/100.",
            ],
        }
        if "billing" in features:
            reasons["intent_extraction"].append("Detected payments -> inferred billing routes and subscription entities.")
        if any(error.code == "ADMIN_ANALYTICS_GATE_MISSING" for error in validation_report.errors):
            reasons["validation"].append("Analytics requires explicit admin gate by policy.")
        if simulation_result.executable:
            reasons["runtime_simulation"].append("Premium/billing and analytics checks passed with deterministic rules.")
        return reasons
