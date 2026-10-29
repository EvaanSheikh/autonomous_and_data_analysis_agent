import pandas as pd
import pytest


from app.tools.statistics_tools import (
    calculate_descriptive_statistics,
    calculate_percentage_change,
    calculate_correlation,
    detect_outliers,
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "sales": [100, 200, 300, 400, 500],
        "quantity": [10, 20, 30, 40, 50],
    })


def test_descriptive_statistics(sample_dataframe):
    result = calculate_descriptive_statistics(
        sample_dataframe,
        ["sales"],
    )

    assert result["sales"]["count"] == 5
    assert result["sales"]["mean"] == 300
    assert result["sales"]["median"] == 300
    assert result["sales"]["min"] == 100
    assert result["sales"]["max"] == 500


def test_percentage_change():
    result = calculate_percentage_change(100, 120)

    assert result == 20.0


def test_percentage_change_from_zero():
    with pytest.raises(ValueError):
        calculate_percentage_change(0, 100)


def test_correlation(sample_dataframe):
    result = calculate_correlation(
        sample_dataframe,
        "sales",
        "quantity",
    )

    assert result == pytest.approx(1.0)


def test_invalid_correlation_column(sample_dataframe):
    with pytest.raises(ValueError):
        calculate_correlation(
            sample_dataframe,
            "sales",
            "invalid",
        )


def test_outlier_detection():
    df = pd.DataFrame({
        "sales": [10, 11, 12, 13, 14, 100]
    })

    result = detect_outliers(df, "sales")

    assert result["outlier_count"] == 1