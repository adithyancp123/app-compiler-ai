# AI Software Compiler

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Vercel-blue)](https://app-compiler-ai.vercel.app/)
[![Backend API](https://img.shields.io/badge/Backend%20API-Render-0ea5e9)](https://app-compiler-ai-backend.onrender.com/)
[![API Docs](https://img.shields.io/badge/API%20Docs-Swagger-22c55e)](https://app-compiler-ai-backend.onrender.com/docs)
![Build Status](https://img.shields.io/badge/CI-build%20passing-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Next.js](https://img.shields.io/badge/Next.js-16-black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)

A deterministic compiler-style system that converts natural language software requirements into structured, executable system architecture through multi-stage compilation, validation, targeted repair, runtime simulation, and benchmarking.

## Live Demo
- **Live Frontend**: `https://app-compiler-ai.vercel.app/`
- **Backend API**: `https://app-compiler-ai-backend.onrender.com/`
- **API Docs (Swagger)**: `https://app-compiler-ai-backend.onrender.com/docs`

## Features
- **Deterministic multi-stage pipeline** (compiler-like, modular stages)
- **Strict contracts & schema enforcement** (typed outputs, stable structure)
- **Semantic validation** (UI → API → DB lineage checks + policy checks)
- **Targeted repair** (fix only the failing module; bounded attempts)
- **Runtime simulation** (execution confidence + issue reporting)
- **Benchmark suite** (10 real + 10 edge prompts, aggregated metrics)
- **Explainability** (“why decisions were made” per stage)
- **Export outputs** (JSON/Markdown for compile + benchmark reports)

## Why this project matters (recruiter summary)
This is not a “one prompt → one blob” generator. It demonstrates production-minded AI systems engineering:
- **Deterministic engineering**: stable, repeatable outputs for the same input
- **Validation lineage**: verifies field mappings across UI, API, and DB layers
- **Targeted repair vs monolithic retries**: cheaper and more debuggable recovery
- **Runtime execution confidence**: checks that the generated config is executable
- **Benchmark evaluation**: measurable outcomes over real and adversarial prompts
- **Explainability**: traceable reasoning and repair actions, reviewer-friendly

## Architecture Overview
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

## Deterministic Pipeline Stages
1. **Intent Extraction**: domain templates + deterministic keyword inference.
2. **System Design**: modules, permissions, relationships, navigation topology.
3. **Schema Generation**: strict JSON contracts for UI/API/DB/Auth.
4. **Validation**: lineage graph checks and cross-layer semantic checks.
5. **Repair**: module-scoped deterministic repairs (no full regeneration).
6. **Runtime Simulation**: execution readiness + confidence scoring.
7. **Metrics**: quality score and cost-vs-quality tradeoff snapshots.

## Validation + Repair Strategy
- Validation produces:
  - `errors`
  - `warnings`
  - `consistency_score` (0–100)
  - `repair_candidates`
- Repair applies targeted fixes only to failing modules:
  - field insertion
  - schema alignment
  - dependency reconciliation
- Bounded repair attempts (no brute-force regeneration loops).

## Runtime Simulation
Runtime simulation validates:
- UI renderability
- API route integrity and mapping
- DB schema/relation integrity
- auth role/rule integrity
- feature-level consistency

Outputs include:
- `executable` (boolean)
- `confidence_score` (0–100)
- `issues` (actionable list)

## Benchmarking & Metrics
Benchmarks run across **20 prompts** (10 real + 10 edge), tracking:
- success_rate / failure_rate
- repair_rate / avg_repairs
- avg_latency
- consistency_score
- execution_rate / runtime_failures

Artifacts:
- `evaluation_report.json`
- `docs/evaluation_report.md`

## Explainability Engine
Each run includes an `explainability` section with human-readable reasoning:
- why certain features/entities were inferred
- which validations triggered
- what targeted repairs were applied
- why runtime confidence/executability was reached

## Tech Stack
- **Frontend**: Next.js 16 + Tailwind CSS + TypeScript (Vercel)
- **Backend**: FastAPI + Pydantic (Render)
- **Validation**: Pydantic contracts + semantic consistency engine
- **Storage**: SQLite scaffold
- **Testing**: Pytest
- **CI**: GitHub Actions

## Deployment
- **Frontend**: Vercel
- **Backend**: Render

## Production URLs
- Frontend: `https://app-compiler-ai.vercel.app/`
- Backend: `https://app-compiler-ai-backend.onrender.com/`
- Swagger: `https://app-compiler-ai-backend.onrender.com/docs`

## Local Development Setup

### Backend
```bash
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
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
- `POST /api/v1/compile/export/json`
- `POST /api/v1/compile/export/markdown`
- `GET /api/v1/evaluation/report`
- `POST /api/v1/evaluation/run`
- `GET /api/v1/evaluation/export/json`
- `GET /api/v1/evaluation/export/markdown`

## API Examples (Production)

### Compile
```bash
curl -X POST \"https://app-compiler-ai-backend.onrender.com/api/v1/compile\" \\
  -H \"Content-Type: application/json\" \\
  -d '{\"prompt\":\"Build a CRM with login and premium billing.\"}'
```

### Run benchmark
```bash
curl -X POST \"https://app-compiler-ai-backend.onrender.com/api/v1/evaluation/run\"
```

### Get benchmark report
```bash
curl \"https://app-compiler-ai-backend.onrender.com/api/v1/evaluation/report\"
```

### Export compile output (JSON)
```bash
curl -X POST \"https://app-compiler-ai-backend.onrender.com/api/v1/compile/export/json\" \\
  -H \"Content-Type: application/json\" \\
  -d '{\"prompt\":\"Build a CRM with login and premium billing.\"}' \\
  -o compile_output.json
```

### Export benchmark report (Markdown)
```bash
curl \"https://app-compiler-ai-backend.onrender.com/api/v1/evaluation/export/markdown\" \\
  -o benchmark_report.md
```

## Demo Flow
1. Open the live app: `https://app-compiler-ai.vercel.app/`
2. Choose a preset in **Prompt Studio**.
3. Click **Generate** to see:
   - stage outputs (intent → design → schema → validation → repair → runtime)
   - consistency score, confidence score, quality score
4. Click **Run Full Pipeline Demo** for a guided progression.
5. Click **Run Benchmark** to populate the benchmark dashboard.
6. Use export buttons to download JSON/Markdown artifacts.

## Screenshots (placeholders)
- `docs/screenshots/dashboard-home.png`
- `docs/screenshots/pipeline-stage-output.png`
- `docs/screenshots/benchmark-dashboard.png`

## Tradeoffs & Design Decisions
- Determinism increases reproducibility and auditability, but reduces creative variance.
- Targeted repair lowers retry cost and improves debuggability vs full regeneration.
- Execution-aware simulation prioritizes deployable correctness over “pretty” outputs.

## Future Improvements
- richer entity graph constraints
- migration planning/generation
- provider-backed strict decoding adapters
- expanded frontend e2e test coverage

## Contributing
See `CONTRIBUTING.md`.

## License
MIT — see `LICENSE`.
