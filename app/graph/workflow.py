from pathlib import Path

from app.agents.reporter import generate_report

import pandas as pd
from langgraph.graph import StateGraph, START, END

from app.agents.analyst import execute_analysis_plan
from app.agents.validator import validate_analysis
from app.agents.llm_planner import generate_analysis_plan
from app.state import AgentState


MAX_REPLANS = 2


def _profile_dataset(dataset_id: str) -> dict:
    path = Path(dataset_id)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {dataset_id}"
        )

    df = pd.read_csv(path)

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "column_names": df.columns.tolist(),
        "dtypes": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "missing_values": {
            column: int(value)
            for column, value in df.isna().sum().items()
        },
        "duplicate_rows": int(df.duplicated().sum()),
    }


def _fallback_plan(query: str) -> list:
    query = query.lower()

    plan = [
        {
            "step": 1,
            "action": "profile_dataset",
        }
    ]

    if "revenue" in query and "region" in query:
        plan.extend([
            {
                "step": 2,
                "action": "group_and_aggregate",
                "parameters": {
                    "group_by": "region",
                    "metric": "revenue",
                    "aggregation": "sum",
                },
            },
            {
                "step": 3,
                "action": "create_bar_chart",
                "parameters": {
                    "x_column": "region",
                    "y_column": "revenue",
                },
            },
        ])

    elif "revenue" in query:
        plan.append({
            "step": 2,
            "action": "group_and_aggregate",
            "parameters": {
                "group_by": "region",
                "metric": "revenue",
                "aggregation": "sum",
            },
        })

    return plan


def planner(state: AgentState) -> AgentState:
    state["dataset_profile"] = _profile_dataset(
        state["dataset_id"]
    )

    try:
        state["analysis_plan"] = generate_analysis_plan(
            state["user_query"],
            state["dataset_profile"],
        )

    except Exception as exc:
        state.setdefault("errors", []).append({
            "type": "planner",
            "message": str(exc),
        })

        state["analysis_plan"] = _fallback_plan(
            state["user_query"]
        )

    state["current_step"] = (
        state.get("current_step", 0) + 1
    )

    state["status"] = "planned"

    return state


def analyst(state: AgentState) -> AgentState:
    return execute_analysis_plan(state)


def observe(state: AgentState) -> AgentState:
    """
    Inspect the latest execution and determine whether
    the workflow needs another planning attempt.
    """

    tool_results = state.get(
        "tool_results",
        [],
    )

    if not tool_results:
        state["status"] = "needs_replan"
        return state

    failed_tools = [
        result
        for result in tool_results
        if result.get("success") is not True
    ]

    if not failed_tools:
        state["status"] = "analysis_complete"
        return state

    state["status"] = "needs_replan"

    return state


def should_replan(state: AgentState) -> str:
    """
    Bounded routing decision.

    The workflow can never replan indefinitely.
    """

    if state.get("status") != "needs_replan":
        return "validate"

    replan_count = state.get(
        "replan_count",
        0,
    )

    if replan_count >= MAX_REPLANS:
        return "validate"

    state["replan_count"] = replan_count + 1

    return "replan"


def replan(state: AgentState) -> AgentState:
    """
    Generate a new plan after an unsuccessful analysis.

    The original user question and latest dataset profile
    remain the planning context.
    """

    try:
        state["analysis_plan"] = generate_analysis_plan(
            state["user_query"],
            state["dataset_profile"],
        )

        state["status"] = "replanned"

    except Exception as exc:
        state.setdefault("errors", []).append({
            "type": "replan",
            "message": str(exc),
        })

        state["analysis_plan"] = _fallback_plan(
            state["user_query"]
        )

        state["status"] = "replanned"

    return state


def validator(state: AgentState) -> AgentState:
    return validate_analysis(state)


def finalize(state: AgentState) -> AgentState:
    state = generate_report(state)

    if state.get("status") == "validated":
        state["status"] = "analyzed"

    elif state.get("status") == "validation_failed":
        state["status"] = "failed"

    return state


def create_analysis_graph():
    graph = StateGraph(AgentState)

    graph.add_node("planner", planner)
    graph.add_node("analyst", analyst)
    graph.add_node("observe", observe)
    graph.add_node("replan", replan)
    graph.add_node("validator", validator)
    graph.add_node("finalize", finalize)

    graph.add_edge(
        START,
        "planner",
    )

    graph.add_edge(
        "planner",
        "analyst",
    )

    graph.add_edge(
        "analyst",
        "observe",
    )

    graph.add_conditional_edges(
        "observe",
        should_replan,
        {
            "replan": "replan",
            "validate": "validator",
        },
    )

    graph.add_edge(
        "replan",
        "analyst",
    )

    graph.add_edge(
        "validator",
        "finalize",
    )

    graph.add_edge(
        "finalize",
        END,
    )

    return graph.compile()