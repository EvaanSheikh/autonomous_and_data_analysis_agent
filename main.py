from helper import configure_logging, ensure_directories
from orchestrator import Orchestrator


def main():
    configure_logging()
    ensure_directories()

    orchestrator = Orchestrator()

    query = input(
        "Ask the Autonomous Data Analyst: "
    )

    result = orchestrator.run(query)

    profile = result["dataset_profile"]

    print("\nDataset Profile")
    print("================")

    print(f"Rows: {profile['rows']:,}")
    print(f"Columns: {profile['columns']}")
    print(f"Duplicate Rows: {profile['duplicate_rows']:,}")

    print("\nColumns")
    print("--------")

    for column in profile["column_names"]:
        dtype = profile["dtypes"][column]
        unique = profile["unique_values"][column]
        missing = profile["missing_values"][column]
        missing_pct = profile["missing_percentages"][column]

        print(
            f"{column:<22} "
            f"type={dtype:<10} "
            f"unique={unique:<8} "
            f"missing={missing:<8} "
            f"({missing_pct}%)"
        )

    print("\nNumerical Columns")
    print("-----------------")

    for column in profile["numerical_columns"]:
        ranges = profile["numerical_ranges"][column]

        print(
            f"{column}: "
            f"min={ranges['min']}, "
            f"max={ranges['max']}"
        )


if __name__ == "__main__":
    main()