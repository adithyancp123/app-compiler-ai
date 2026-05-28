# Deploy on Vercel

## Frontend
1. Import repo on Vercel.
2. Root directory: `frontend`.
3. Build command: `npm run build`.
4. Env: `NEXT_PUBLIC_API_BASE_URL=<backend-url>`.

## Backend
Deploy backend separately (Render/Railway/Fly) and use that URL in frontend env.
