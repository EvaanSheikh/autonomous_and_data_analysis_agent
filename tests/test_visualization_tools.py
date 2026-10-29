from pathlib import Path

import pandas as pd
import pytest

from app.tools.visualization_tools import (
    create_line_chart,
    create_bar_chart,
    create_histogram,
    create_scatter_plot,
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "month": ["Jan", "Feb", "Mar", "Apr"],
        "revenue": [100, 150, 125, 200],
        "quantity": [10, 15, 12, 20],
    })


def test_line_chart(sample_dataframe, tmp_path):
    result = create_line_chart(
        sample_dataframe,
        "month",
        "revenue",
        output_dir=tmp_path,
    )

    assert Path(result).exists()


def test_bar_chart(sample_dataframe, tmp_path):
    result = create_bar_chart(
        sample_dataframe,
        "month",
        "revenue",
        output_dir=tmp_path,
    )

    assert Path(result).exists()


def test_histogram(sample_dataframe, tmp_path):
    result = create_histogram(
        sample_dataframe,
        "revenue",
        output_dir=tmp_path,
    )

    assert Path(result).exists()


def test_scatter_plot(sample_dataframe, tmp_path):
    result = create_scatter_plot(
        sample_dataframe,
        "quantity",
        "revenue",
        output_dir=tmp_path,
    )

    assert Path(result).exists()


def test_invalid_column(sample_dataframe, tmp_path):
    with pytest.raises(ValueError):
        create_bar_chart(
            sample_dataframe,
            "invalid",
            "revenue",
            output_dir=tmp_path,
        )


def test_histogram_requires_numeric(sample_dataframe, tmp_path):
    with pytest.raises(ValueError):
        create_histogram(
            sample_dataframe,
            "month",
            output_dir=tmp_path,
        )