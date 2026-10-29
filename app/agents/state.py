from typing import Any, TypedDict


class AnalysisState(TypedDict, total=False):
    session_id: str

    user_query: str
    dataset_id: str

    dataset_metadata: dict[str, Any]
    dataset_profile: dict[str, Any]

    analysis_plan: list[dict[str, Any]]
    current_step: int

    tool_calls: list[dict[str, Any]]
    tool_results: list[dict[str, Any]]

    findings: list[dict[str, Any]]
    visualizations: list[str]

    validation_results: dict[str, Any]

    errors: list[dict[str, Any]]

    final_report: str

    status: str
    
