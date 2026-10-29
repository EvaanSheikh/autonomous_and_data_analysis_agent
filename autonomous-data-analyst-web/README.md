# Autonomous Data Analyst — Web Frontend

Premium analytical frontend for the existing FastAPI + LangGraph backend.

## Stack

- Next.js App Router
- React + TypeScript
- Tailwind CSS v4
- shadcn/ui source-owned primitives
- Geist Sans / Geist Mono
- Apache ECharts-ready visualization layer
- TanStack Query-ready data layer
- Zod-ready API validation layer
- Lucide icons

## Run

```powershell
npm install
$env:NEXT_PUBLIC_API_BASE_URL="http://127.0.0.1:8000/api"
npm run dev
```

Open `http://localhost:3000`.

The backend must already be running:

```powershell
uvicorn app.api.main:app --reload
```

## Design principle

This is an analytical workstation rather than a conventional SaaS dashboard. The interface prioritizes the answer, visualization, evidence and validation trace.
