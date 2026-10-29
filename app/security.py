from pathlib import Path


MAX_DATASET_SIZE_BYTES = 100 * 1024 * 1024
MAX_ANALYSIS_ROWS = 1_000_000
MAX_REPLANS = 2
MAX_TOOL_CALLS = 20


def validate_dataset_resource(path: str) -> None:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    size = file_path.stat().st_size

    if size > MAX_DATASET_SIZE_BYTES:
        raise ValueError(
            f"Dataset exceeds the {MAX_DATASET_SIZE_BYTES // (1024 * 1024)} MB limit."
        )


def validate_analysis_limits(state: dict) -> None:
    tool_calls = len(state.get("tool_calls", []))

    if tool_calls >= MAX_TOOL_CALLS:
        raise RuntimeError(
            f"Maximum tool-call limit of {MAX_TOOL_CALLS} exceeded."
        )

    replan_count = state.get("replan_count", 0)

    if replan_count > MAX_REPLANS:
        raise RuntimeError(
            f"Maximum replan limit of {MAX_REPLANS} exceeded."
        )