from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as analysis_router
from app.api.upload import router as upload_router
from app.logging_config import configure_application_logging
from app.storage.database import initialize_database


# ---------------------------------------------------------
# Application setup
# ---------------------------------------------------------

configure_application_logging()
initialize_database()

app = FastAPI(
    title="Autonomous Data Analyst",
    description="Agentic AI system for autonomous dataset analysis.",
    version="1.0.0",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# Static reports
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

app.mount(
    "/reports",
    StaticFiles(directory=str(REPORTS_DIR)),
    name="reports",
)


# ---------------------------------------------------------
# API routes
# ---------------------------------------------------------

app.include_router(
    analysis_router,
    prefix="/api",
)

app.include_router(
    upload_router,
    prefix="/api",
)


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "service": "Autonomous Data Analyst",
        "status": "running",
        "api": "/api",
    }