from uuid import uuid4

from app.storage.database import (
    get_analysis_session,
    save_analysis_session,
)

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.graph.workflow import create_analysis_graph
from app.storage.database import get_analysis_session


router = APIRouter()

analysis_graph = create_analysis_graph()


class AnalyzeRequest(BaseModel):
    user_query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Natural-language analytical question.",
    )

    dataset_id: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Path or identifier of the dataset.",
    )


class AnalyzeResponse(BaseModel):
    session_id: str
    status: str
    user_query: str
    dataset_id: str

    analysis_plan: list = Field(default_factory=list)
    tool_calls: list = Field(default_factory=list)
    findings: list = Field(default_factory=list)
    visualizations: list = Field(default_factory=list)
    evidence: list = Field(default_factory=list)
    validation_results: list = Field(default_factory=list)
    errors: list = Field(default_factory=list)

    final_report: str = ""


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "autonomous-data-analyst",
    }


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    session_id = str(uuid4())

    initial_state = {
        "session_id": session_id,
        "user_query": request.user_query,
        "dataset_id": request.dataset_id,
        "status": "created",
        "replan_count": 0,
        "max_replans": 2,
        "tool_calls": [],
        "tool_results": [],
        "findings": [],
        "visualizations": [],
        "evidence": [],
        "validation_results": [],
        "errors": [],
    }

    try:
        result = analysis_graph.invoke(initial_state)
        save_analysis_session(result)

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Analysis execution failed.",
        ) from exc

    return AnalyzeResponse(
        session_id=result.get("session_id", session_id),
        status=result.get("status", "failed"),
        user_query=result.get("user_query", request.user_query),
        dataset_id=result.get("dataset_id", request.dataset_id),
        analysis_plan=result.get("analysis_plan", []),
        tool_calls=result.get("tool_calls", []),
        findings=result.get("findings", []),
        visualizations=result.get("visualizations", []),
        evidence=result.get("evidence", []),
        validation_results=result.get("validation_results", []),
        errors=result.get("errors", []),
        final_report=result.get("final_report", ""),
    )
@router.get("/analysis/{session_id}")
def get_analysis(session_id: str):
    session = get_analysis_session(session_id)

    if session is None:
        raise HTTPException(
            status_code=404,
            detail="Analysis session not found.",
        )

    return session