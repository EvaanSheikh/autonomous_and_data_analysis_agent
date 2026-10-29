import pandas as pd
import pytest

from tools.data_tools import (
    aggregate_data,
    filter_data,
    group_data,
)


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "Country": ["India", "India", "USA", "USA"],
            "Quantity": [10, 20, 30, 40],
            "UnitSellingPrice": [100, 200, 150, 250],
        }
    )


def test_filter_data(sample_data):
    result = filter_data(
        sample_data,
        column="Quantity",
        operator=">",
        value=20,
    )

    assert result["input_rows"] == 4
    assert result["output_rows"] == 2
    assert result["rows_removed"] == 2


def test_group_data(sample_data):
    result = group_data(
        sample_data,
        group_by="Country",
    )

    assert result["group_count"] == 2


def test_aggregate_data(sample_data):
    result = aggregate_data(
        sample_data,
        group_by="Country",
        aggregations={"Quantity": "sum"},
    )

    output = result["data"]

    india_quantity = output.loc[
        output["Country"] == "India",
        "Quantity",
    ].iloc[0]

    usa_quantity = output.loc[
        output["Country"] == "USA",
        "Quantity",
    ].iloc[0]

    assert india_quantity == 30
    assert usa_quantity == 70


def test_invalid_column(sample_data):
    with pytest.raises(ValueError):
        filter_data(
            sample_data,
            column="DoesNotExist",
            operator="==",
            value=10,
        )


def test_invalid_operator(sample_data):
    with pytest.raises(ValueError):
        filter_data(
            sample_data,
            column="Quantity",
            operator="LIKE",
            value=10,
        )


def test_empty_dataset():
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        filter_data(
            df,
            column="Quantity",
            operator=">",
            value=10,
        )