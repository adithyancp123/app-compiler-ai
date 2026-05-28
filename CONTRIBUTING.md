# Contributing

## Setup
1. `cd backend && python -m pip install -r requirements.txt`
2. `cd frontend && npm install`

## Development Rules
- Keep deterministic behavior and stable ordering.
- Do not replace modular stages with monolithic generation.
- Add tests for every new rule or repair strategy.

## Quality Gate
- Backend: `python -m pytest`
- Frontend: `npm run build`
- Benchmark: `POST /api/v1/evaluation/run`
