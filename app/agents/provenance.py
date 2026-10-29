from datetime import datetime, timezone
from typing import Any


def record_tool_evidence(
    state: dict,
    action: str,
    parameters: dict,
    result: Any,
) -> dict:
    """
    Record the evidence produced by a deterministic tool.
    """

    evidence = state.setdefault(
        "evidence",
        [],
    )

    evidence.append({
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "dataset_id": state.get(
            "dataset_id"
        ),
        "columns": _extract_columns(
            parameters
        ),
        "operation": action,
        "parameters": parameters,
        "result": result,
    })

    return state


def _extract_columns(
    parameters: dict,
) -> list[str]:
    columns = []

    for key in (
        "column",
        "column_a",
        "column_b",
        "x_column",
        "y_column",
        "group_by",
        "metric",
    ):
        value = parameters.get(key)

        if isinstance(value, str):
            columns.append(value)

    values = parameters.get("columns")

    if isinstance(values, list):
        columns.extend(
            value
            for value in values
            if isinstance(value, str)
        )

    return list(dict.fromkeys(columns))