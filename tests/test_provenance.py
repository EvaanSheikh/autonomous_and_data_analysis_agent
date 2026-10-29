from app.agents.provenance import (
    record_tool_evidence,
)


def test_record_tool_evidence():
    state = {
        "dataset_id": "data/sample/sales.csv",
        "evidence": [],
    }

    result = record_tool_evidence(
        state,
        "group_and_aggregate",
        {
            "group_by": "region",
            "metric": "revenue",
            "aggregation": "sum",
        },
        [
            {
                "region": "North",
                "revenue": 1000,
            }
        ],
    )

    assert len(result["evidence"]) == 1

    evidence = result["evidence"][0]

    assert (
        evidence["dataset_id"]
        == "data/sample/sales.csv"
    )

    assert (
        evidence["operation"]
        == "group_and_aggregate"
    )

    assert evidence["columns"] == [
        "region",
        "revenue",
    ]

    assert evidence["parameters"]["aggregation"] == "sum"

    assert evidence["result"] == [
        {
            "region": "North",
            "revenue": 1000,
        }
    ]


def test_evidence_extracts_multiple_columns():
    state = {
        "dataset_id": "data/sample/sales.csv",
    }

    result = record_tool_evidence(
        state,
        "create_scatter_plot",
        {
            "x_column": "revenue",
            "y_column": "profit",
        },
        "reports/charts/scatter_plot.png",
    )

    assert result["evidence"][0]["columns"] == [
        "revenue",
        "profit",
    ]