from app.agents.state import AnalysisState


def evaluate_analysis(state: AnalysisState) -> AnalysisState:
    """Determine whether the current analysis is complete."""

    errors = state.get("errors", [])
    analysis_plan = state.get("analysis_plan", [])
    tool_results = state.get("tool_results", [])

    if errors:
        return {
            **state,
            "status": "failed",
        }

    if not analysis_plan:
        return {
            **state,
            "status": "needs_analysis",
        }

    successful_results = [
        result
        for result in tool_results
        if result.get("success") is True
    ]

    if len(successful_results) >= len(analysis_plan):
        return {
            **state,
            "status": "analysis_complete",
        }

    return {
        **state,
        "status": "needs_analysis",
    }