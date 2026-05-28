# AI Software Compiler (Deterministic Multi-Stage System)

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Tests](https://img.shields.io/badge/tests-pytest-blue)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![TypeScript](https://img.shields.io/badge/typescript-Next.js-3178C6)

Internship-grade compiler-style system that transforms natural language product requirements into executable application configuration through deterministic, modular stages.

## Project Overview
This project is designed to feel like an engineered compiler pipeline rather than a one-shot prompt generator. It emphasizes:
- deterministic generation
- strict schema contracts
- targeted repair instead of full regeneration
- runtime execution awareness
- measurable benchmark outcomes

## Architecture
```text
Prompt
  -> Intent Extraction
  -> System Design
  -> Schema Generation (UI/API/DB/Auth)
  -> Validation Engine (lineage + semantic consistency)
  -> Repair Engine (targeted module fixes)
  -> Runtime Simulation (execution confidence)
  -> Executable JSON + Metrics
```

### Screenshot Placeholders
- `docs/screenshots/dashboard-home.png` (main control panel)
- `docs/screenshots/pipeline-stage-output.png` (stage cards + status)
- `docs/screenshots/benchmark-dashboard.png` (evaluation metrics)

## Pipeline Stages
1. **Intent Extraction**: domain templates + deterministic keyword inference.
2. **System Design**: modules, permissions, relationships, navigation topology.
3. **Schema Generation**: strict JSON contracts for UI/API/DB/Auth.
4. **Validation**: lineage graph checks and cross-layer semantic checks.
5. **Repair**: module-scoped deterministic repairs.
6. **Runtime Simulation**: execution readiness + confidence scoring.
7. **Metrics**: quality score and cost-vs-quality tradeoff snapshots.

## Validation + Repair Strategy
- Validation outputs:
  - `errors`
  - `warnings`
  - `consistency_score`
  - `repair_candidates`
- Repair applies targeted fixes only to failing modules:
  - field insertion
  - schema alignment
  - dependency reconciliation
- No brute-force full pipeline regeneration.

## Runtime Simulation
Runtime simulation verifies:
- UI renderability
- API route integrity and mapping
- DB schema/relation integrity
- auth role/rule integrity
- feature-level consistency

Outputs include:
- `executable` (boolean)
- `confidence_score` (0-100)
- `issues` (actionable list)

## Benchmark Evaluation
Runs across **20 prompts** (10 real + 10 edge), with metrics:
- success_rate
- failure_rate
- repair_rate
- avg_repairs
- avg_latency
- consistency_score
- execution_rate
- runtime_failures

Generated artifacts:
- `evaluation_report.json`
- `docs/evaluation_report.md`

## Tech Stack
- Frontend: Next.js + Tailwind CSS + TypeScript
- Backend: FastAPI + Pydantic
- Validation: Pydantic + semantic consistency engine
- Storage: SQLite scaffold
- Testing: Pytest
- CI: GitHub Actions

## How to Run
### Backend
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pytest
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Frontend
```bash
cd frontend
npm install
npm run build
npm run dev
```

## API Endpoints
- `GET /api/v1/health`
- `POST /api/v1/compile`
- `GET /api/v1/compile/contracts`
- `POST /api/v1/compile/export/json`
- `POST /api/v1/compile/export/markdown`
- `GET /api/v1/evaluation/report`
- `POST /api/v1/evaluation/run`
- `GET /api/v1/evaluation/export/json`
- `GET /api/v1/evaluation/export/markdown`

## Demo Instructions
1. Start backend and frontend.
2. Use demo preset prompts in the UI.
3. Click **Generate** or **Run Full Pipeline Demo**.
4. Inspect stage outputs, validation, repair actions, runtime confidence.
5. Click **Run Benchmark** and review analytics cards.
6. Export JSON/Markdown reports for submission artifacts.

## Tradeoffs
- Deterministic heuristics increase reliability and reproducibility, but reduce creative variance.
- Targeted repair lowers retry cost, but still requires bounded repair loops for edge prompts.

## Future Improvements
- richer entity graph constraints
- migration planning/generation
- provider-backed strict decoding adapters
- expanded frontend e2e test coverage
