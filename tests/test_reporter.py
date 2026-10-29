from app.agents.reporter import generate_report


def test_generate_report():
    state = {
        "user_query": "What is total revenue by region?",
        "dataset_id": "data/sample/sales.csv",
        "evidence": [
            {
                "operation": "group_and_aggregate",
                "columns": ["region", "revenue"],
                "parameters": {
                    "group_by": "region",
                    "metric": "revenue",
                    "aggregation": "sum",
                },
                "result": [
                    {
                        "region": "North",
                        "revenue": 1000,
                    }
                ],
            }
        ],
        "validation_results": [
            {
                "check": "tool_execution",
                "passed": True,
                "message": "All tools succeeded.",
            }
        ],
        "visualizations": [],
        "tool_calls": [
            {"action": "group_and_aggregate"}
        ],
        "replan_count": 0,
    }

    result = generate_report(state)

    assert result["final_report"]
    assert "Autonomous Data Analyst Report" in result["final_report"]
    assert "total revenue by region" in result["final_report"]
    assert "group_and_aggregate" in result["final_report"]
    assert "PASS" in result["final_report"]