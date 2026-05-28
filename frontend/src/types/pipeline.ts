export type StageStatus = "success" | "warning" | "failed";

export type StageOutput = {
  stage: string;
  status: StageStatus;
  content: Record<string, unknown>;
  notes: string[];
};

export type ValidationErrorItem = {
  module: string;
  code: string;
  message: string;
};

export type ValidationWarningItem = {
  module: string;
  code: string;
  message: string;
};

export type ValidationReport = {
  valid: boolean;
  errors: ValidationErrorItem[];
  warnings: ValidationWarningItem[];
  consistency_score: number;
  repair_candidates: string[];
};

export type RepairAction = {
  module: string;
  action: string;
  status: string;
  repair_type: string;
};

export type SimulationResult = {
  ui_renderable: boolean;
  api_mapped: boolean;
  db_schema_exists: boolean;
  auth_rules_valid: boolean;
  route_integrity: boolean;
  executable: boolean;
  confidence_score: number;
  issues: string[];
};

export type QualityScoreBreakdown = {
  schema_quality: number;
  consistency: number;
  execution_readiness: number;
  repair_stability: number;
  determinism: number;
  final_score: number;
  reasoning: string[];
};

export type ModeTradeoff = {
  mode: string;
  estimated_latency_ms: number;
  estimated_token_cost: number;
  expected_quality_score: number;
  notes: string;
};

export type MetricsSnapshot = {
  latency_ms: number;
  token_estimate: number;
  estimated_token_cost: number;
  retry_count: number;
  repair_cost: number;
  quality_score: number;
  tradeoff_summary: ModeTradeoff[];
};

export type CompileResponse = {
  request_id: string;
  assumptions: string[];
  clarification_questions: string[];
  stage_outputs: StageOutput[];
  generated_schema: Record<string, unknown>;
  validation_report: ValidationReport;
  repair_actions: RepairAction[];
  simulation_result: SimulationResult;
  quality_score: QualityScoreBreakdown;
  metrics: MetricsSnapshot;
  explainability: Record<string, string[]>;
};

export type EvaluationPromptResult = {
  prompt: string;
  success: boolean;
  retries: number;
  latency_ms: number;
  consistency_score: number;
  executable: boolean;
  failure_category: string | null;
};

export type EvaluationReport = {
  real_prompts: EvaluationPromptResult[];
  edge_prompts: EvaluationPromptResult[];
  success_rate: number;
  failure_rate: number;
  repair_rate: number;
  avg_repairs: number;
  avg_latency: number;
  consistency_score: number;
  execution_rate: number;
  runtime_failures: number;
};
