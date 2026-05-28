# Submission Checklist

## GitHub Repo Checklist
- [ ] Repo is public (or correct share permissions)
- [ ] Root `README.md` renders correctly
- [ ] `LICENSE` present
- [ ] `CONTRIBUTING.md` present
- [ ] `.github/workflows/ci.yml` present and green on latest commit
- [ ] No large artifacts committed (`node_modules/`, `.next/`, `__pycache__/`, `.env`)
- [ ] `backend/.env.example` + `backend/.env.production.example` present
- [ ] `frontend/.env.local.example` + `frontend/.env.production.example` present
- [ ] `docs/demo-script.md` present
- [ ] `docs/final-audit.md` present

## Loom / Video Checklist
- [ ] Screen recording includes terminal + browser
- [ ] Use **Run Full Pipeline Demo** once on a preset
- [ ] Show explainability panel
- [ ] Show export/download buttons (JSON + Markdown)
- [ ] Run Benchmark and show dashboard
- [ ] Mention determinism + repair scope rules
- [ ] Mention runtime simulator confidence score

## Live Demo Checklist
- [ ] Start backend (`uvicorn`) and verify `GET /api/v1/health`
- [ ] Start frontend (`npm run dev`) and verify prompt presets load instantly
- [ ] Run the conflicting prompt preset to show constraint detection
- [ ] Run benchmark and verify report appears

## Google Form / Submission Checklist
- [ ] GitHub repo URL
- [ ] Loom video URL
- [ ] Short description:
  - deterministic multi-stage compiler pipeline
  - strict validation + targeted repair
  - execution-aware simulation + benchmark reporting
- [ ] Include how to run commands (copy from README)

