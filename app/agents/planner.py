from app.agents.state import AnalysisState


def create_analysis_plan(state: AnalysisState) -> AnalysisState:
    """Create an initial analysis plan from the user's query."""

    query = state.get("user_query", "").lower()

    plan = []

    if "revenue" in query and "region" in query:
        plan = [
            {
                "step": 1,
                "action": "profile_dataset",
                "reason": "Understand dataset structure",
            },
            {
                "step": 2,
                "action": "group_and_aggregate",
                "parameters": {
                    "group_by": "region",
                    "metric": "revenue",
                    "aggregation": "sum",
                },
                "reason": "Calculate total revenue by region",
            },
            {
                "step": 3,
                "action": "create_bar_chart",
                "parameters": {
                    "x_column": "region",
                    "y_column": "revenue",
                },
                "reason": "Visualize revenue by region",
            },
        ]

    elif "average" in query or "mean" in query:
        plan = [
            {
                "step": 1,
                "action": "profile_dataset",
                "reason": "Understand dataset structure",
            },
            {
                "step": 2,
                "action": "calculate_descriptive_statistics",
                "reason": "Calculate numerical averages",
            },
        ]

    elif "correlation" in query:
        plan = [
            {
                "step": 1,
                "action": "profile_dataset",
                "reason": "Identify numerical columns",
            },
            {
                "step": 2,
                "action": "calculate_correlation",
                "reason": "Measure relationship between variables",
            },
        ]

    else:
        plan = [
            {
                "step": 1,
                "action": "profile_dataset",
                "reason": "Inspect the dataset before determining analysis",
            }
        ]

    return {
        **state,
        "analysis_plan": plan,
        "current_step": 0,
        "status": "planned",
    }