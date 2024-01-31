""""Test for the data management functions."""

import pandas as pd
import pytest
from tradingstrattester.config import ASSETS
from tradingstrattester.data_management.data_functions import (
    _handle_errors_in_define_dates,
    data_download,
)


# Test data_download
@pytest.mark.parametrize("assets", ASSETS)
def test_is_empty_data_download(assets):
    """Test if downloaded data is non-empty."""
    assert not data_download(assets).empty


@pytest.mark.parametrize("assets", ASSETS)
def test_is_pd_DataFrame_data_download(assets):
    """Test if downloaded data has the correct data type."""
    assert isinstance(data_download(assets), pd.core.frame.DataFrame)


# Test _handle_errors_in_define_dates
value_start = ["2024-01-01", "typo", "2024-01-01", "01-01-2024", "typo", "2024-01-01"]
value_end = ["typo", "2024-01-01", "01-01-2024", "2024-01-01", "typo", "2023-01-01"]


@pytest.mark.parametrize(("start_date", "end_date"), zip(value_start, value_end))
def test__handle_errors_in_define_dates_value_error_dates(start_date, end_date):
    """Test the value error handling of dates in _handle_error_in_define_dates."""
    with pytest.raises(ValueError):
        _handle_errors_in_define_dates(
            start_date=start_date,
            end_date=end_date,
            frequency="60m",
        )


invalid_frequencies = ["60", "3m", "typo"]


@pytest.mark.parametrize("frequency", invalid_frequencies)
def test__handle_errors_in_define_dates_value_error_frequency(frequency):
    """Test the value error handling of frequency in _handle_error_in_define_dates."""
    with pytest.raises(ValueError):
        _handle_errors_in_define_dates(
            start_date="2024-01-01",
            end_date="2024-01-05",
            frequency=frequency,
        )


def test__handle_errors_in_define_dates_type_error_dates():
    """Test the type error handling of dates in _handle_error_in_define_dates."""
    with pytest.raises(TypeError):
        _handle_errors_in_define_dates(
            start_date=1,
            end_date="2024-01-05",
            frequency="60m",
        )


def test__handle_errors_in_define_dates_type_error_frequency():
    """Test the type error handling of frequency in _handle_error_in_define_dates."""
    with pytest.raises(TypeError):
        _handle_errors_in_define_dates(
            start_date="2024-01-01",
            end_date="2024-01-05",
            frequency=1,
        )
