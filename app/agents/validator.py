from typing import Any


def validate_analysis(state: dict) -> dict:
    validation_results = []
    errors = state.setdefault("errors", [])

    tool_results = state.get("tool_results", [])

    if not tool_results:
        validation_results.append({
            "check": "tool_execution",
            "passed": False,
            "message": "No tool results were produced.",
        })

        errors.append({
            "type": "validation",
            "message": "Analysis produced no tool results.",
        })

        state["status"] = "failed"
        state["validation_results"] = validation_results
        return state

    all_tools_successful = all(
        result.get("success") is True
        for result in tool_results
    )

    validation_results.append({
        "check": "tool_execution",
        "passed": all_tools_successful,
        "message": (
            "All analysis tools executed successfully."
            if all_tools_successful
            else "One or more analysis tools failed."
        ),
    })

    has_results = any(
        result.get("result") is not None
        for result in tool_results
        if result.get("success") is True
    )

    validation_results.append({
        "check": "result_presence",
        "passed": has_results,
        "message": (
            "Analysis produced results."
            if has_results
            else "Analysis produced no usable results."
        ),
    })

    visualizations = state.get("visualizations", [])

    visualization_paths_valid = True

    for path in visualizations:
        if not isinstance(path, str):
            visualization_paths_valid = False
            break

    validation_results.append({
        "check": "visualization_consistency",
        "passed": visualization_paths_valid,
        "message": (
            "Visualization references are valid."
            if visualization_paths_valid
            else "Invalid visualization reference detected."
        ),
    })

    validation_passed = all(
        result["passed"]
        for result in validation_results
    )

    if validation_passed:
        state["status"] = "validated"
    else:
        state["status"] = "validation_failed"

    state["validation_results"] = validation_results

    return state