"""Typed contracts for compiler pipeline stages and API I/O."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator, model_validator


class StageName(str, Enum):
    intent_extraction = "intent_extraction"
    system_design = "system_design"
    schema_generation = "schema_generation"
    validation = "validation"
    repair = "repair"
    runtime_simulation = "runtime_simulation"


class StageStatus(str, Enum):
    success = "success"
    warning = "warning"
    failed = "failed"


class CompileRequest(BaseModel):
    prompt: str = Field(..., min_length=3, description="Natural language product requirement prompt")

    @field_validator("prompt")
    @classmethod
    def normalize_prompt(cls, value: str) -> str:
        return " ".join(value.strip().split())


class IntentSpec(BaseModel):
    app_name: str
    app_type: str
    features: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    entities: list[str] = Field(default_factory=list)
    pages: list[str] = Field(default_factory=list)
    integrations: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)


class FeatureFlow(BaseModel):
    feature: str
    primary_role: str
    steps: list[str] = Field(default_factory=list)


class EntityRelationship(BaseModel):
    source: str
    target: str
    relation: str


class PermissionRule(BaseModel):
    role: str
    permissions: list[str] = Field(default_factory=list)


class SystemDesignSpec(BaseModel):
    modules: list[str] = Field(default_factory=list)
    feature_flows: list[FeatureFlow] = Field(default_factory=list)
    entity_relationships: list[EntityRelationship] = Field(default_factory=list)
    permissions: list[PermissionRule] = Field(default_factory=list)
    page_navigation: dict[str, list[str]] = Field(default_factory=dict)
    api_domains: list[str] = Field(default_factory=list)


class UIComponent(BaseModel):
    component: str
    bind_entity: str | None = None


class UIFormField(BaseModel):
    name: str
    type: str
    required: bool = True


class UIForm(BaseModel):
    form_id: str
    submit_route: str
    fields: list[UIFormField] = Field(default_factory=list)


class UIAction(BaseModel):
    id: str
    type: str
    target: str


class UIPage(BaseModel):
    name: str
    path: str
    layout: str
    components: list[UIComponent] = Field(default_factory=list)
    forms: list[UIForm] = Field(default_factory=list)
    actions: list[UIAction] = Field(default_factory=list)


class UISchema(BaseModel):
    pages: list[UIPage] = Field(default_factory=list)
    navigation: dict[str, list[str]] = Field(default_factory=dict)


class APIField(BaseModel):
    name: str
    type: str
    required: bool = True


class APIRoute(BaseModel):
    name: str
    domain: str
    path: str
    method: str
    auth_required: bool = True
    request_model: list[APIField] = Field(default_factory=list)
    response_model: list[APIField] = Field(default_factory=list)


class APISchema(BaseModel):
    routes: list[APIRoute] = Field(default_factory=list)


class DBColumn(BaseModel):
    name: str
    type: str
    nullable: bool = False
    primary_key: bool = False


class DBRelation(BaseModel):
    table: str
    column: str
    references_table: str
    references_column: str


class DBTable(BaseModel):
    name: str
    columns: list[DBColumn] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class DBSchema(BaseModel):
    tables: list[DBTable] = Field(default_factory=list)
    relations: list[DBRelation] = Field(default_factory=list)


class AuthRole(BaseModel):
    name: str
    permissions: list[str] = Field(default_factory=list)


class AccessRule(BaseModel):
    route: str
    allowed_roles: list[str] = Field(default_factory=list)


class AuthSchema(BaseModel):
    roles: list[AuthRole] = Field(default_factory=list)
    access_rules: list[AccessRule] = Field(default_factory=list)


class GeneratedSchema(BaseModel):
    ui: UISchema
    api: APISchema
    db: DBSchema
    auth: AuthSchema


class StageOutput(BaseModel):
    stage: StageName
    status: StageStatus
    content: dict[str, Any]
    notes: list[str] = Field(default_factory=list)


class ValidationErrorItem(BaseModel):
    module: str
    code: str
    message: str


class ValidationWarningItem(BaseModel):
    module: str
    code: str
    message: str


class ValidationReport(BaseModel):
    valid: bool
    errors: list[ValidationErrorItem] = Field(default_factory=list)
    warnings: list[ValidationWarningItem] = Field(default_factory=list)
    consistency_score: int = Field(default=100, ge=0, le=100)
    repair_candidates: list[str] = Field(default_factory=list)


class RepairAction(BaseModel):
    module: str
    action: str
    status: str
    repair_type: str


class SimulationResult(BaseModel):
    ui_renderable: bool
    api_mapped: bool
    db_schema_exists: bool
    auth_rules_valid: bool
    route_integrity: bool
    executable: bool
    confidence_score: int = Field(default=100, ge=0, le=100)
    issues: list[str] = Field(default_factory=list)


class QualityScoreBreakdown(BaseModel):
    schema_quality: int = Field(default=0, ge=0, le=100)
    consistency: int = Field(default=0, ge=0, le=100)
    execution_readiness: int = Field(default=0, ge=0, le=100)
    repair_stability: int = Field(default=0, ge=0, le=100)
    determinism: int = Field(default=0, ge=0, le=100)
    final_score: int = Field(default=0, ge=0, le=100)
    reasoning: list[str] = Field(default_factory=list)


class ModeTradeoff(BaseModel):
    mode: str
    estimated_latency_ms: int
    estimated_token_cost: float
    expected_quality_score: int
    notes: str


class MetricsSnapshot(BaseModel):
    latency_ms: int = 0
    token_estimate: int = 0
    estimated_token_cost: float = 0
    retry_count: int = 0
    repair_cost: float = 0
    quality_score: float = 0
    tradeoff_summary: list[ModeTradeoff] = Field(default_factory=list)


class CompileResponse(BaseModel):
    request_id: str
    assumptions: list[str] = Field(default_factory=list)
    clarification_questions: list[str] = Field(default_factory=list)
    stage_outputs: list[StageOutput] = Field(default_factory=list)
    generated_schema: dict[str, Any] = Field(default_factory=dict)
    validation_report: ValidationReport
    repair_actions: list[RepairAction] = Field(default_factory=list)
    simulation_result: SimulationResult
    quality_score: QualityScoreBreakdown
    metrics: MetricsSnapshot
    explainability: dict[str, list[str]] = Field(default_factory=dict)

    @model_validator(mode="after")
    def ensure_schema_present(self) -> "CompileResponse":
        if not self.generated_schema:
            raise ValueError("generated_schema cannot be empty")
        return self


class EvaluationPromptResult(BaseModel):
    prompt: str
    success: bool
    retries: int
    latency_ms: int
    consistency_score: int = 0
    executable: bool = False
    failure_category: str | None = None


class EvaluationReport(BaseModel):
    real_prompts: list[EvaluationPromptResult] = Field(default_factory=list)
    edge_prompts: list[EvaluationPromptResult] = Field(default_factory=list)
    success_rate: float = 0
    failure_rate: float = 0
    repair_rate: float = 0
    avg_repairs: float = 0
    avg_latency: float = 0
    consistency_score: float = 0
    execution_rate: float = 0
    runtime_failures: int = 0


class BenchmarkArtifact(BaseModel):
    report: EvaluationReport
    markdown_report: str


def export_contract_schemas() -> dict[str, dict[str, Any]]:
    """Export JSON Schema for strict contract visibility."""
    contract_models = {
        "IntentSpec": IntentSpec,
        "SystemDesignSpec": SystemDesignSpec,
        "GeneratedSchema": GeneratedSchema,
        "ValidationReport": ValidationReport,
        "SimulationResult": SimulationResult,
        "CompileResponse": CompileResponse,
        "EvaluationReport": EvaluationReport,
    }
    return {name: model.model_json_schema() for name, model in contract_models.items()}
