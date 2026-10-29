from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".json"}


def validate_dataset(path: str) -> dict:
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            "Unsupported dataset format. "
            "Allowed formats: CSV, XLSX, JSON."
        )

    try:
        if file_path.suffix.lower() == ".csv":
            df = pd.read_csv(file_path)

        elif file_path.suffix.lower() == ".xlsx":
            df = pd.read_excel(file_path)

        else:
            df = pd.read_json(file_path)

    except Exception as exc:
        raise ValueError(
            f"Dataset could not be parsed: {exc}"
        ) from exc

    if df.empty:
        raise ValueError("Dataset is empty.")

    if len(df.columns) == 0:
        raise ValueError("Dataset contains no columns.")

    return {
        "valid": True,
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": df.columns.tolist(),
        "missing_values": int(df.isna().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "file_size_bytes": file_path.stat().st_size,
    }