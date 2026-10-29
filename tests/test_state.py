from app.agents.state import AnalysisState


def test_analysis_state_can_store_core_fields():
    state: AnalysisState = {
        "session_id": "test-session",
        "user_query": "What is the total revenue by region?",
        "dataset_id": "sales.csv",
        "dataset_profile": {
            "rows": 10,
            "columns": 5,
        },
        "analysis_plan": [],
        "current_step": 0,
        "tool_calls": [],
        "tool_results": [],
        "findings": [],
        "visualizations": [],
        "validation_results": {},
        "errors": [],
        "final_report": "",
        "status": "initialized",
    }

    assert state["session_id"] == "test-session"
    assert state["user_query"] == "What is the total revenue by region?"
    assert state["current_step"] == 0
    assert state["status"] == "initialized"


def test_analysis_state_supports_tool_results():
    state: AnalysisState = {
        "tool_results": [
            {
                "tool": "group_and_aggregate",
                "success": True,
                "result": {
                    "North": 300000,
                    "South": 285000,
                },
            }
        ]
    }

    assert len(state["tool_results"]) == 1
    assert state["tool_results"][0]["success"] is True


def test_analysis_state_supports_errors():
    state: AnalysisState = {
        "errors": [
            {
                "type": "recoverable",
                "message": "Column not found",
                "tool": "group_and_aggregate",
            }
        ]
    }

    assert state["errors"][0]["type"] == "recoverable"