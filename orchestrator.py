import logging

import pandas as pd

from helper import get_dataset_path


logger = logging.getLogger(__name__)


class Orchestrator:
    """Central controller for the Autonomous Data Analyst."""

    def __init__(self):
        self.dataset_path = get_dataset_path()
        self.dataset: pd.DataFrame | None = None

    def load_dataset(self) -> pd.DataFrame:
        """Load the primary dataset."""

        logger.info("Loading dataset: %s", self.dataset_path)

        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {self.dataset_path}"
            )

        self.dataset = pd.read_csv(self.dataset_path)

        logger.info(
            "Dataset loaded: %d rows, %d columns",
            self.dataset.shape[0],
            self.dataset.shape[1],
        )

        return self.dataset

    def profile_dataset(self) -> dict:
        """Generate a deterministic profile of the dataset."""

        if self.dataset is None:
            self.load_dataset()

        df = self.dataset

        missing_values = df.isna().sum()
        missing_percentages = (
            df.isna().mean() * 100
        ).round(2)

        numerical_columns = df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        categorical_columns = df.select_dtypes(
            include=["object", "category"]
        ).columns.tolist()

        datetime_columns = df.select_dtypes(
            include=["datetime"]
        ).columns.tolist()

        unique_values = {
            column: int(df[column].nunique(dropna=True))
            for column in df.columns
        }

        numerical_ranges = {}

        for column in numerical_columns:
            numerical_ranges[column] = {
                "min": float(df[column].min()),
                "max": float(df[column].max()),
            }

        profile = {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),

            "dtypes": {
                column: str(dtype)
                for column, dtype in df.dtypes.items()
            },

            "missing_values": {
                column: int(value)
                for column, value in missing_values.items()
            },

            "missing_percentages": {
                column: float(value)
                for column, value in missing_percentages.items()
            },

            "duplicate_rows": int(df.duplicated().sum()),

            "numerical_columns": numerical_columns,
            "categorical_columns": categorical_columns,
            "datetime_columns": datetime_columns,

            "unique_values": unique_values,

            "numerical_ranges": numerical_ranges,
        }

        logger.info(
            "Dataset profile created: %d rows, %d columns, %d duplicates",
            profile["rows"],
            profile["columns"],
            profile["duplicate_rows"],
        )

        return profile

    def run(self, user_query: str) -> dict:
        """Run the initial deterministic workflow."""

        logger.info("User query: %s", user_query)

        self.load_dataset()

        profile = self.profile_dataset()

        return {
            "user_query": user_query,
            "dataset_profile": profile,
        }