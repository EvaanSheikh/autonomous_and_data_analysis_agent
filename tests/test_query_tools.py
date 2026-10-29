import pandas as pd
import pytest

from app.tools.query_tools import (
    filter_data,
    sort_data,
    group_and_aggregate,
    aggregate_multiple,
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "region": [
            "North",
            "North",
            "South",
            "South",
            "East",
        ],
        "product": [
            "Laptop",
            "Phone",
            "Laptop",
            "Phone",
            "Laptop",
        ],
        "quantity": [2, 4, 3, 5, 1],
        "revenue": [
            120000,
            60000,
            180000,
            75000,
            60000,
        ],
    })


def test_filter_data(sample_dataframe):
    result = filter_data(
        sample_dataframe,
        "region",
        "==",
        "North",
    )

    assert len(result) == 2
    assert all(result["region"] == "North")


def test_filter_numeric_data(sample_dataframe):
    result = filter_data(
        sample_dataframe,
        "revenue",
        ">",
        100000,
    )

    assert len(result) == 2
    assert all(result["revenue"] > 100000)


def test_invalid_filter_operator(sample_dataframe):
    with pytest.raises(ValueError):
        filter_data(
            sample_dataframe,
            "region",
            "LIKE",
            "North",
        )


def test_sort_data(sample_dataframe):
    result = sort_data(
        sample_dataframe,
        "revenue",
        ascending=False,
    )

    assert result.iloc[0]["revenue"] == 180000


def test_group_and_aggregate(sample_dataframe):
    result = group_and_aggregate(
        sample_dataframe,
        "region",
        "revenue",
        "sum",
    )

    north = result.loc[
        result["region"] == "North",
        "revenue",
    ].iloc[0]

    assert north == 180000


def test_group_mean(sample_dataframe):
    result = group_and_aggregate(
        sample_dataframe,
        "region",
        "quantity",
        "mean",
    )

    north = result.loc[
        result["region"] == "North",
        "quantity",
    ].iloc[0]

    assert north == 3


def test_multiple_aggregation(sample_dataframe):
    result = aggregate_multiple(
        sample_dataframe,
        "region",
        ["quantity", "revenue"],
        "sum",
    )

    assert "quantity" in result.columns
    assert "revenue" in result.columns
    assert len(result) == 3


def test_invalid_group_column(sample_dataframe):
    with pytest.raises(ValueError):
        group_and_aggregate(
            sample_dataframe,
            "invalid",
            "revenue",
        )