from app.agents.planner import create_analysis_plan


def test_planner_creates_revenue_by_region_plan():
    state = {
        "user_query": "What is the total revenue by region?",
        "analysis_plan": [],
        "current_step": 0,
        "status": "initialized",
    }

    result = create_analysis_plan(state)

    assert result["status"] == "planned"
    assert len(result["analysis_plan"]) == 3
    assert result["analysis_plan"][1]["action"] == "group_and_aggregate"


def test_planner_creates_average_plan():
    state = {
        "user_query": "What is the average revenue?",
        "analysis_plan": [],
        "current_step": 0,
        "status": "initialized",
    }

    result = create_analysis_plan(state)

    assert result["status"] == "planned"
    assert result["analysis_plan"][1]["action"] == (
        "calculate_descriptive_statistics"
    )


def test_planner_creates_correlation_plan():
    state = {
        "user_query": "What is the correlation between revenue and quantity?",
        "analysis_plan": [],
        "current_step": 0,
        "status": "initialized",
    }

    result = create_analysis_plan(state)

    assert result["status"] == "planned"
    assert result["analysis_plan"][1]["action"] == (
        "calculate_correlation"
    )


def test_planner_falls_back_to_dataset_profile():
    state = {
        "user_query": "Tell me something interesting about this dataset.",
        "analysis_plan": [],
        "current_step": 0,
        "status": "initialized",
    }

    result = create_analysis_plan(state)

    assert result["status"] == "planned"
    assert result["analysis_plan"][0]["action"] == "profile_dataset"