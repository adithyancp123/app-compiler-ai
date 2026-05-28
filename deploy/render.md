# Deploy on Render

1. Create Web Service for backend from `backend/`.
2. Build command: `pip install -r requirements.txt`.
3. Start command: `python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
4. Add env vars from `backend/.env.example`.
5. Deploy frontend on Render static/web service from `frontend/`.
