# AI Software Compiler (Deterministic Multi-Stage System)

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-pytest-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![TypeScript](https://img.shields.io/badge/typescript-Next.js-3178C6)

Internship-grade project that compiles natural language requirements into executable software configuration through modular deterministic stages.

## Problem Statement
Most prompt-to-app systems behave like opaque generators. This project introduces compiler-style engineering:
- deterministic stage contracts
- strict schema validation
- module-scoped repair
- execution-aware simulation
- measurable benchmark outcomes

## Architecture Diagram
```
Prompt
  -> Intent Extraction
  -> System Design
  -> Schema Generation (UI/API/DB/Auth)
  -> Validation Engine (lineage + semantic consistency)
  -> Repair Engine (targeted only)
  -> Runtime Simulation (execution confidence)
  -> Executable JSON + Metrics
```

## Pipeline Overview
1. **Intent Extraction**: domain template + keyword inference for features, roles, entities, pages, assumptions.
2. **System Design**: deterministic modules, permissions, relationships, and navigation map.
3. **Schema Generation**: strict typed JSON for UI/API/DB/Auth.
4. **Validation Engine**: field lineage graph checks, feature consistency, navigation integrity, role consistency.
5. **Repair Engine**: repairs only failing modules (field insertion, schema alignment, dependency reconciliation).
6. **Runtime Simulation**: validates renderability, route reachability, DB/auth/feature integrity and confidence score.
7. **Quality + Cost Metrics**: deterministic scoring and mode tradeoffs.

## Determinism Controls
- fixed stage ordering
- deterministic templates
- stable sorting
- strict Pydantic contracts
- JSON-only outputs
- bounded repair loop

## Validation and Repair Strategy
- Detects orphan fields/routes/roles and semantic contradictions.
- Produces:
  - `errors`
  - `warnings`
  - `consistency_score` (0-100)
  - `repair_candidates`
- Repair operates in module scope only; no full pipeline rerun.

## Runtime Execution Awareness
Runtime simulator returns:
- `executable`
- `confidence_score` (0-100)
- integrity flags and issue list

## Benchmarking and Evaluation
Benchmarks run across 20 prompts (10 real + 10 edge):
- success_rate
- failure_rate
- repair_rate
- avg_repairs
- avg_latency
- consistency_score
- execution_rate
- runtime_failures

Artifacts generated on benchmark run:
- `evaluation_report.json`
- `docs/evaluation_report.md`

## Cost vs Quality Modes
Metrics include tradeoff summary:
- **fast**: lower latency/cost, reduced expected quality
- **balanced**: default deterministic reliability
- **high_reliability**: more cost/latency, higher expected quality

## Tech Stack
- Frontend: Next.js + Tailwind + TypeScript
- Backend: FastAPI + Pydantic
- Validation: Pydantic contracts + semantic engine
- Storage: SQLite scaffold
- Testing: Pytest

## Run Locally
### Backend
```bash
cd backend
python -m venv .venv
.venv\Scriptsctivate
python -m pip install -r requirements.txt
python -m pytest
python -m uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## API Endpoints
- `GET /api/v1/health`
- `POST /api/v1/compile`
- `GET /api/v1/compile/contracts`
- `GET /api/v1/evaluation/report`
- `POST /api/v1/evaluation/run`

## Demo Prompts
- CRM
- E-commerce
- Hospital Management
- School Management
- Subscription SaaS
- Marketplace
- Inventory System

## Tradeoffs
- Deterministic heuristics improve predictability but may reduce creative variance.
- Targeted repair reduces regeneration cost but may require multiple bounded attempts.

## Future Improvements
- richer entity graph constraints
- migration plan generation
- provider-backed deterministic LLM adapters with schema decoding
- CI/CD pipeline + containerized deployment profiles
