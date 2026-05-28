# Loom Recording Script (10 Minutes, Stress-Free)

## Pre-flight (30 sec)
Exact commands:

```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest
python -m uvicorn app.main:app --reload
```

```bash
cd frontend
npm install
npm run dev
```

Open:
- Frontend: `http://localhost:3000`
- Backend health: `http://localhost:8000/api/v1/health`

Backup if `npm install` is slow:
- Start backend first, then run only `npm run build` to prove production viability.

## 0:00-1:00 Problem Statement
Say:
- “Prompt-to-app tools are often opaque and inconsistent.”
- “This project compiles prompts through deterministic stages with strict contracts.”

Show:
- Home screen and the tabs bar.

## 1:00-3:00 Architecture Overview
Click:
- **Pipeline** tab

Say:
- “Not one giant prompt. Each stage is independent and typed.”
- “Validation finds exact failures; repair only patches the broken module.”

Show:
- `GET /api/v1/compile/contracts` in browser (optional).

## 3:00-5:00 Full Demo (Happy Path)
Click preset button:
- **“Build a CRM with premium billing…”**

Click:
- **Run Full Pipeline Demo**

Show expected:
- Progress bar moves through stages
- **Consistency** and **Confidence** cards near ~90–100
- `Executable` shows **Yes**

## 5:00-7:00 Failure Handling Mode
Click preset:
- **“Build an app for my business.”**

Click:
- **Generate**

Show expected:
- `clarification_questions` populated and/or assumptions added

Click preset:
- **“Everyone is admin but admins only can view analytics.”**

Click:
- **Generate**

Show expected:
- Constraints include a **conflict** line
- Explainability panel mentions policy expectations

## 7:00-8:00 Explainability + Exports
Click:
- **Download JSON** and **Download Markdown**
Then:
- **Benchmark JSON** / **Benchmark Markdown**

Show expected:
- Files download successfully

Say:
- “Every decision is explained; exports make review easy.”

## 8:00-10:00 Benchmark + Tradeoffs
Click:
- **Run Benchmark**

Show expected:
- Benchmark dashboard renders with rates + consistency
- Mention generated artifacts:
  - `evaluation_report.json`
  - `docs/evaluation_report.md`

Say:
- “Metrics include fast/balanced/high reliability tradeoffs and bounded repair attempts.”

## Backup flow if anything fails
- If frontend can’t start: show backend via curl:
  - `POST /api/v1/compile` with any preset prompt
  - show `explainability`, `validation_report`, `simulation_result`
