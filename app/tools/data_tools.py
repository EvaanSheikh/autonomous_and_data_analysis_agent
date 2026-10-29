from pathlib import Path

import pandas as pd


SUPPORTED_EXTENSIONS = {
    ".csv",
    ".xlsx",
    ".xls",
    ".json",
}


def load_dataset(file_path: str) -> pd.DataFrame:
    """
    Load a supported dataset into a Pandas DataFrame.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    if extension == ".csv":
        return pd.read_csv(path)

    if extension in {".xlsx", ".xls"}:
        return pd.read_excel(path)

    if extension == ".json":
        return pd.read_json(path)

    raise ValueError(
        f"Unsupported file format: {extension}"
    )


def profile_dataset(df: pd.DataFrame) -> dict:
    """
    Generate a structured profile of the dataset.
    """

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": list(df.columns),
        "data_types": {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        },
        "missing_values": {
            column: int(count)
            for column, count in df.isnull().sum().items()
            if count > 0
        },
        "duplicate_rows": int(df.duplicated().sum()),
        "numerical_columns": list(
            df.select_dtypes(include="number").columns
        ),
        "categorical_columns": list(
    df.select_dtypes(
        include=["object", "string", "category"]
    ).columns
),
    }