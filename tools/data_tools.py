from __future__ import annotations

from typing import Any

import pandas as pd


def _validate_dataframe(df: pd.DataFrame) -> None:
    """Validate that the input is a Pandas DataFrame."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame.")

    if df.empty:
        raise ValueError("The dataset is empty.")


def _validate_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> None:
    """Validate that requested columns exist."""
    missing = [column for column in columns if column not in df.columns]

    if missing:
        raise ValueError(
            f"Column(s) not found: {missing}. "
            f"Available columns: {df.columns.tolist()}"
        )


def filter_data(
    df: pd.DataFrame,
    column: str,
    operator: str,
    value: Any,
) -> dict:
    """
    Filter dataset rows using a comparison condition.

    Supported operators:
        ==, !=, >, >=, <, <=

    Returns:
        Structured information about the filtering operation.
    """
    _validate_dataframe(df)
    _validate_columns(df, [column])

    valid_operators = {"==", "!=", ">", ">=", "<", "<="}

    if operator not in valid_operators:
        raise ValueError(
            f"Unsupported operator '{operator}'. "
            f"Supported operators: {sorted(valid_operators)}"
        )

    series = df[column]

    if operator == "==":
        mask = series == value
    elif operator == "!=":
        mask = series != value
    elif operator == ">":
        mask = series > value
    elif operator == ">=":
        mask = series >= value
    elif operator == "<":
        mask = series < value
    else:
        mask = series <= value

    filtered_df = df.loc[mask].copy()

    return {
        "operation": "filter_data",
        "parameters": {
            "column": column,
            "operator": operator,
            "value": value,
        },
        "input_rows": int(len(df)),
        "output_rows": int(len(filtered_df)),
        "rows_removed": int(len(df) - len(filtered_df)),
        "data": filtered_df,
    }


def group_data(
    df: pd.DataFrame,
    group_by: str | list[str],
) -> dict:
    """
    Group the dataset by one or more columns.

    This tool creates a grouped Pandas object that can subsequently
    be used by aggregation operations.
    """
    _validate_dataframe(df)

    if isinstance(group_by, str):
        group_columns = [group_by]
    else:
        group_columns = group_by

    if not group_columns:
        raise ValueError("At least one grouping column is required.")

    _validate_columns(df, group_columns)

    grouped = df.groupby(group_columns, dropna=False)

    group_count = int(grouped.ngroups)

    return {
        "operation": "group_data",
        "parameters": {
            "group_by": group_columns,
        },
        "input_rows": int(len(df)),
        "group_count": group_count,
        "grouped_data": grouped,
    }


def aggregate_data(
    df: pd.DataFrame,
    group_by: str | list[str],
    aggregations: dict[str, str],
) -> dict:
    """
    Group data and calculate deterministic aggregations.

    Example:
        aggregate_data(
            df,
            group_by="Country",
            aggregations={"Quantity": "sum"}
        )

    Supported Pandas aggregation functions can be used, such as:
        sum, mean, median, min, max, count, std
    """
    _validate_dataframe(df)

    if isinstance(group_by, str):
        group_columns = [group_by]
    else:
        group_columns = group_by

    if not group_columns:
        raise ValueError("At least one grouping column is required.")

    if not aggregations:
        raise ValueError("At least one aggregation is required.")

    _validate_columns(df, group_columns)
    _validate_columns(df, list(aggregations.keys()))

    valid_aggregations = {
        "sum",
        "mean",
        "median",
        "min",
        "max",
        "count",
        "std",
        "var",
    }

    for column, aggregation in aggregations.items():
        if aggregation not in valid_aggregations:
            raise ValueError(
                f"Unsupported aggregation '{aggregation}' for '{column}'. "
                f"Supported aggregations: {sorted(valid_aggregations)}"
            )

    result_df = (
        df.groupby(group_columns, dropna=False)
        .agg(aggregations)
        .reset_index()
    )

    return {
        "operation": "aggregate_data",
        "parameters": {
            "group_by": group_columns,
            "aggregations": aggregations,
        },
        "input_rows": int(len(df)),
        "output_rows": int(len(result_df)),
        "data": result_df,
    }