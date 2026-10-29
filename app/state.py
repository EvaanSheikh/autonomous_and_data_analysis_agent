from typing import TypedDict


class AgentState(TypedDict, total=False):
    session_id: str
    user_query: str
    dataset_id: str

    dataset_metadata: dict
    dataset_profile: dict
    analysis_plan: list

    current_step: int
    tool_calls: list
    tool_results: list
    findings: list
    visualizations: list

    validation_results: list
    errors: list

    final_report: str
    status: str

    replan_count: int
    max_replans: int

    evidence: list