from pathlib import Path

from app.security import validate_analysis_limits

from app.security import validate_dataset_resource

from app.agents.tool_validation import validate_tool_call

import pandas as pd

from app.agents.provenance import record_tool_evidence
from app.tools.visualization_tools import (
    create_bar_chart,
    create_line_chart,
    create_histogram,
    create_scatter_plot,
)


def _load_dataset(dataset_id: str) -> pd.DataFrame:
    path = Path(dataset_id)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {dataset_id}"
        )

    df = pd.read_csv(path)

    # ---------------------------------------------------------
    # Deterministic derived metrics
    # ---------------------------------------------------------
    if "revenue" not in df.columns:
        required = {
            "Quantity",
            "UnitSellingPrice",
            "DiscountPercentage",
        }

        if required.issubset(df.columns):
            gross_sales = (
                df["Quantity"] * df["UnitSellingPrice"]
            )

            discount_amount = (
                gross_sales
                * df["DiscountPercentage"]
                / 100
            )

            df["revenue"] = (
                gross_sales - discount_amount
            )

    if "profit" not in df.columns:
        required = {
            "Quantity",
            "UnitSellingPrice",
            "UnitCostPrice",
            "DiscountPercentage",
            "ShippingCost",
        }

        if required.issubset(df.columns):
            gross_sales = (
                df["Quantity"] * df["UnitSellingPrice"]
            )

            discount_amount = (
                gross_sales
                * df["DiscountPercentage"]
                / 100
            )

            revenue = (
                gross_sales - discount_amount
            )

            total_cost = (
                df["Quantity"]
                * df["UnitCostPrice"]
            )

            df["profit"] = (
                revenue
                - total_cost
                - df["ShippingCost"]
            )

    # ---------------------------------------------------------
    # Normalize analytical names
    # ---------------------------------------------------------
    rename_map = {
        "Region": "region",
        "Country": "country",
        "Category": "category",
        "ProductName": "product",
        "OrderDate": "date",
    }

    for source, target in rename_map.items():
        if source in df.columns and target not in df.columns:
            df[target] = df[source]

    return df


def _execute_action(
    df: pd.DataFrame,
    action: str,
    parameters: dict,
):
    # ---------------------------------------------------------
    # Dataset profiling
    # ---------------------------------------------------------
    if action == "profile_dataset":
        derived_columns = {
            "revenue",
            "profit",
            "region",
            "country",
            "category",
            "product",
            "date",
        }

        source_columns = [
            column
            for column in df.columns
            if column not in derived_columns
        ]

        return {
            "rows": int(df.shape[0]),
            "columns": len(source_columns),
            "column_names": source_columns,
            "missing_values": {
                column: int(df[column].isna().sum())
                for column in source_columns
            },
            "duplicate_rows": int(df[source_columns].duplicated().sum()),
        }

    # ---------------------------------------------------------
    # Group and aggregate
    # ---------------------------------------------------------
    if action == "group_and_aggregate":
        group_by = parameters["group_by"]
        metric = parameters["metric"]
        aggregation = parameters.get(
            "aggregation",
            "sum",
        )

        if group_by not in df.columns:
            raise ValueError(
                f"Column not found: {group_by}"
            )

        if metric not in df.columns:
            raise ValueError(
                f"Metric not found: {metric}"
            )

        result = (
            df.groupby(
                group_by,
                dropna=False,
            )[metric]
            .agg(aggregation)
            .reset_index()
        )

        return result.to_dict(
            orient="records"
        )

    # ---------------------------------------------------------
    # Bar chart
    # ---------------------------------------------------------
    if action == "create_bar_chart":
        x_column = parameters["x_column"]
        y_column = parameters["y_column"]

        if x_column not in df.columns:
            raise ValueError(
                f"Column not found: {x_column}"
            )

        if y_column not in df.columns:
            raise ValueError(
                f"Column not found: {y_column}"
            )

        chart_df = df

        # Never send hundreds of thousands of categorical
        # observations directly to Matplotlib.
        if (
            len(df) > 5000
            and not pd.api.types.is_numeric_dtype(
                df[x_column]
            )
        ):
            chart_df = (
                df.groupby(
                    x_column,
                    dropna=False,
                )[y_column]
                .sum()
                .reset_index()
            )

        return str(
            create_bar_chart(
                chart_df,
                x_column,
                y_column,
            )
        )

    # ---------------------------------------------------------
    # Line chart
    # ---------------------------------------------------------
    if action == "create_line_chart":
        x_column = parameters["x_column"]
        y_column = parameters["y_column"]

        if x_column not in df.columns:
            raise ValueError(
                f"Column not found: {x_column}"
            )

        if y_column not in df.columns:
            raise ValueError(
                f"Column not found: {y_column}"
            )

        chart_df = df

        if len(df) > 5000:
            if pd.api.types.is_datetime64_any_dtype(
                df[x_column]
            ):
                chart_df = (
                    df.set_index(x_column)[y_column]
                    .resample("ME")
                    .sum()
                    .reset_index()
                )

            elif not pd.api.types.is_numeric_dtype(
                df[x_column]
            ):
                chart_df = (
                    df.groupby(
                        x_column,
                        dropna=False,
                    )[y_column]
                    .sum()
                    .reset_index()
                )

        return str(
            create_line_chart(
                chart_df,
                x_column,
                y_column,
            )
        )

    # ---------------------------------------------------------
    # Histogram
    # ---------------------------------------------------------
    if action == "create_histogram":
        column = parameters["column"]

        if column not in df.columns:
            raise ValueError(
                f"Column not found: {column}"
            )

        return str(
            create_histogram(
                df,
                column,
            )
        )

    # ---------------------------------------------------------
    # Scatter plot
    # ---------------------------------------------------------
    if action == "create_scatter_plot":
        x_column = parameters["x_column"]
        y_column = parameters["y_column"]

        if x_column not in df.columns:
            raise ValueError(
                f"Column not found: {x_column}"
            )

        if y_column not in df.columns:
            raise ValueError(
                f"Column not found: {y_column}"
            )

        return str(
            create_scatter_plot(
                df,
                x_column,
                y_column,
            )
        )

    raise ValueError(
        f"Unsupported analysis action: {action}"
    )


def _extract_findings(
    action: str,
    result,
) -> list:
    findings = []

    if (
        action == "group_and_aggregate"
        and isinstance(result, list)
    ):
        if not result:
            return findings

        numeric_keys = [
            key
            for key, value in result[0].items()
            if isinstance(value, (int, float))
        ]

        if not numeric_keys:
            return findings

        metric = numeric_keys[0]

        highest = max(
            result,
            key=lambda row: row.get(
                metric,
                float("-inf"),
            ),
        )

        lowest = min(
            result,
            key=lambda row: row.get(
                metric,
                float("inf"),
            ),
        )

        category_keys = [
            key
            for key in result[0]
            if key != metric
        ]

        category = (
            category_keys[0]
            if category_keys
            else "category"
        )

        findings.append({
            "type": "group_aggregate",
            "metric": metric,
            "highest": highest,
            "lowest": lowest,
            "message": (
                f"Highest {metric}: "
                f"{highest.get(category)} = "
                f"{highest.get(metric)}. "
                f"Lowest {metric}: "
                f"{lowest.get(category)} = "
                f"{lowest.get(metric)}."
            ),
        })

    return findings


def execute_analysis_plan(state: dict) -> dict:
    state.setdefault("tool_calls", [])
    state.setdefault("tool_results", [])
    state.setdefault("findings", [])
    state.setdefault("visualizations", [])
    state.setdefault("evidence", [])
    state.setdefault("errors", [])

    try:
        validate_dataset_resource(state["dataset_id"])

        df = _load_dataset(
            state["dataset_id"]
        )

        for step in state.get(
            "analysis_plan",
            [],
        ):
            validate_analysis_limits(state)

            action = step["action"]
            parameters = step.get(
                "parameters",
                {},
            )
            validate_tool_call(action, parameters)

            state["tool_calls"].append({
                "action": action,
                "parameters": parameters,
            })

            try:
                result = _execute_action(
                    df,
                    action,
                    parameters,
                )

                state["tool_results"].append({
                    "action": action,
                    "success": True,
                    "result": result,
                })

                # Record provenance for every
                # successfully executed tool.
                record_tool_evidence(
                    state,
                    action,
                    parameters,
                    result,
                )

                # Extract human-readable findings.
                state["findings"].extend(
                    _extract_findings(
                        action,
                        result,
                    )
                )

                if action.startswith("create_"):
                    state["visualizations"].append(
                        result
                    )

            except Exception as exc:
                state["tool_results"].append({
                    "action": action,
                    "success": False,
                    "error": str(exc),
                })

                raise

        state["status"] = "analyzed"
        return state

    except FileNotFoundError as exc:
        state["errors"].append({
            "type": "fatal",
            "message": str(exc),
        })

        state["status"] = "failed"
        return state

    except Exception as exc:
        state["errors"].append({
            "type": "recoverable",
            "message": str(exc),
        })

        state["status"] = "failed"
        return state