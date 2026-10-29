from app.agents.validator import validate_analysis


def test_validator_passes_successful_analysis():
    state = {
        "tool_results": [
            {
                "action": "profile_dataset",
                "success": True,
                "result": {"rows": 10},
            },
            {
                "action": "group_and_aggregate",
                "success": True,
                "result": [{"region": "North", "revenue": 1000}],
            },
        ],
        "visualizations": [],
        "errors": [],
    }

    result = validate_analysis(state)

    assert result["status"] == "validated"
    assert all(
        check["passed"]
        for check in result["validation_results"]
    )


def test_validator_rejects_failed_tool():
    state = {
        "tool_results": [
            {
                "action": "group_and_aggregate",
                "success": False,
                "error": "Column not found",
            }
        ],
        "visualizations": [],
        "errors": [],
    }

    result = validate_analysis(state)

    assert result["status"] == "validation_failed"