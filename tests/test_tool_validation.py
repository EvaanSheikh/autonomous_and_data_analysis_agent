import pytest

from app.agents.tool_validation import validate_tool_call


def test_valid_group_aggregate():
    validate_tool_call(
        "group_and_aggregate",
        {
            "group_by": "region",
            "metric": "revenue",
            "aggregation": "sum",
        },
    )


def test_invalid_action():
    with pytest.raises(ValueError, match="Unsupported analysis action"):
        validate_tool_call(
            "delete_database",
            {},
        )


def test_missing_parameter():
    with pytest.raises(ValueError, match="Missing required parameters"):
        validate_tool_call(
            "create_bar_chart",
            {
                "x_column": "region",
            },
        )


def test_invalid_parameter_type():
    with pytest.raises(ValueError, match="must be a dictionary"):
        validate_tool_call(
            "create_bar_chart",
            None,
        )