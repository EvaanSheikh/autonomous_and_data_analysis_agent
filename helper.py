from pathlib import Path
import logging


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"


def configure_logging() -> None:
    """Configure application-wide logging."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def get_dataset_path() -> Path:
    """Return the path to the primary dataset."""
    return DATA_DIR / "autonomous_business_sales_dataset_fixed.csv"


def ensure_directories() -> None:
    """Create required project directories."""
    DATA_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)