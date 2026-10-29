# NOHA frontend

Next.js App Router frontend for the FastAPI Autonomous Data Analyst.

## Install and run

```bash
npm install geist motion      # only if not already in package.json
npm run dev                   # http://localhost:3000
```

Backend (from the HCL_Training project root, so charts land in ./reports/charts):

```bash
uvicorn app.api.main:app --reload --port 8000
```

`.env.local`:

```
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api
```

Assumes Tailwind CSS v4 (the Next.js 16 default) and the `@/*` path alias at the project root.
