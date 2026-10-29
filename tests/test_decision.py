from app.agents.decision import evaluate_analysis


def test_analysis_is_complete_when_all_steps_succeed():
    state = {
        "analysis_plan": [
            {"step": 1, "action": "profile_dataset"},
            {"step": 2, "action": "group_and_aggregate"},
        ],
        "tool_results": [
            {
                "tool": "profile_dataset",
                "success": True,
            },
            {
                "tool": "group_and_aggregate",
                "success": True,
            },
        ],
        "errors": [],
        "status": "analyzed",
    }

    result = evaluate_analysis(state)

    assert result["status"] == "analysis_complete"


def test_analysis_needs_more_work_when_steps_are_incomplete():
    state = {
        "analysis_plan": [
            {"step": 1, "action": "profile_dataset"},
            {"step": 2, "action": "group_and_aggregate"},
        ],
        "tool_results": [
            {
                "tool": "profile_dataset",
                "success": True,
            },
        ],
        "errors": [],
        "status": "analyzed",
    }

    result = evaluate_analysis(state)

    assert result["status"] == "needs_analysis"


def test_analysis_fails_when_errors_exist():
    state = {
        "analysis_plan": [
            {"step": 1, "action": "profile_dataset"},
        ],
        "tool_results": [],
        "errors": [
            {
                "type": "fatal",
                "message": "Dataset not found.",
            }
        ],
        "status": "failed",
    }

    result = evaluate_analysis(state)

    assert result["status"] == "failed"


def test_empty_plan_requires_analysis():
    state = {
        "analysis_plan": [],
        "tool_results": [],
        "errors": [],
        "status": "planned",
    }

    result = evaluate_analysis(state)

    assert result["status"] == "needs_analysis"