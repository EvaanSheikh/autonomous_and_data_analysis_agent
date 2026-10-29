from datetime import datetime, timezone


def generate_report(state: dict) -> dict:
    evidence = state.get("evidence", [])
    validation = state.get("validation_results", [])

    lines = [
        "# Autonomous Data Analyst Report",
        "",
        f"**Question:** {state.get('user_query', '')}",
        f"**Dataset:** {state.get('dataset_id', '')}",
        "",
        "## Analysis Steps",
    ]

    for index, item in enumerate(evidence, start=1):
        lines.extend([
            f"{index}. **{item['operation']}**",
            f"   - Columns: {', '.join(item['columns']) or 'N/A'}",
            f"   - Parameters: `{item['parameters']}`",
            f"   - Result: `{item['result']}`",
            "",
        ])

    lines.append("## Validation")

    for check in validation:
        status = "PASS" if check["passed"] else "FAIL"

        lines.append(
            f"- **{check['check']}**: {status} — "
            f"{check['message']}"
        )

    lines.extend([
        "",
        "## Visualizations",
    ])

    visualizations = state.get(
        "visualizations",
        [],
    )

    if visualizations:
        for path in visualizations:
            lines.append(f"- `{path}`")
    else:
        lines.append("- None")

    lines.extend([
        "",
        "## Execution Summary",
        f"- Tool calls: {len(state.get('tool_calls', []))}",
        f"- Evidence records: {len(evidence)}",
        f"- Replans: {state.get('replan_count', 0)}",
        f"- Generated at: "
        f"{datetime.now(timezone.utc).isoformat()}",
    ])

    state["final_report"] = "\n".join(lines)

    return state