# Deploy on Railway

1. Create project and link repo.
2. Add service for backend (`backend/`) with start command:
   `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Set environment variables.
4. Add frontend service (`frontend/`) with `npm run build && npm run start`.
