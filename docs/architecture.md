# Architecture Design

## System Goal
Build a compiler-like, deterministic pipeline that transforms user product prompts into executable application configuration.

## Pipeline Stages (Modular)
1. Intent Extraction Layer
2. System Design Layer
3. Schema Generation Layer
4. Validation Engine
5. Repair Engine
6. Runtime Simulation Layer
7. Evaluation Framework

Each stage receives typed input and emits typed output. Cross-layer consistency is enforced by validators and targeted repair actions.

## Backend High-Level Components
- `app/pipeline/*`: Stage implementations and contracts
- `app/services/orchestrator.py`: Pipeline coordinator
- `app/models/contracts.py`: Pydantic models for stage I/O
- `app/core/llm.py`: Provider-agnostic OpenAI-compatible client abstraction
- `app/core/config.py`: Settings and deterministic generation controls
- `app/storage/*`: SQLite repository and persistence hooks
- `app/api/v1/endpoints/*`: HTTP APIs for compile/generate, health, and evaluation

## Deterministic Output Strategy
- Structured prompts per stage
- Temperature and decoding params fixed by policy
- Strict JSON contracts (Pydantic + JSON Schema)
- Fail-fast validation with module-scoped repair

## Validation + Repair Strategy
- Validation checks syntax, schema, and semantic cross-layer consistency
- Repair engine performs targeted corrections only on failing module output
- No full regeneration unless explicitly escalated by policy

## Runtime Simulation
Dry-run simulation checks generated config:
- UI component compatibility
- API endpoint mapping
- DB table/field existence
- Auth role/permission coherence

## Frontend
Single-page control panel to:
- submit prompt
- view each stage output
- inspect validation and repair logs
- inspect simulation results and quality/cost metrics
