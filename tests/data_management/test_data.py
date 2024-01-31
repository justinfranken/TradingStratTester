""""Test for the data management functions."""

import pandas as pd
import pytest
from tradingstrattester.config import ASSETS
from tradingstrattester.data_management.data_functions import (
    _define_dates,
    data_download,
)


# Test data_download main function
@pytest.mark.parametrize("assets", ASSETS)
def test_is_empty_data_download(assets):
    assert not data_download(assets).empty


@pytest.mark.parametrize("assets", ASSETS)
def test_is_pd_DataFrame_data_download(assets):
    assert isinstance(data_download(assets), pd.core.frame.DataFrame)


# Test _define_dates helper function
value_start = ["2024-01-01", "typo", "2024-01-01", "01-01-2024", "typo", "2024-01-01"]
value_end = ["typo", "2024-01-01", "01-01-2024", "2024-01-01", "typo", "2023-01-01"]


@pytest.mark.parametrize(("start_date", "end_date"), zip(value_start, value_end))
def test_define_dates_value_error(start_date, end_date):
    with pytest.raises(ValueError):
        _define_dates(frequency="60m", start_date=start_date, end_date=end_date)
