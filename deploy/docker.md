# Docker Deployment

1. Build images:
   - `docker compose build`
2. Start services:
   - `docker compose up -d`
3. Verify:
   - Backend: `http://localhost:8000/api/v1/health`
   - Frontend: `http://localhost:3000`

For production, add reverse proxy and TLS termination.
