""""Task to download the financial data and store it."""

import pytask
from tradingstrattester.config import ASSETS, BLD
from tradingstrattester.data_management.data_functions import data_download

for asset in ASSETS:
    """Download financial data and store it in the bld folder."""

    @pytask.task(id=asset)
    def task_download_1d_data(
        symbol=asset,
        produces=BLD / "python" / "data" / f"1d_{asset}.pkl",
    ):
        data_1d = data_download(
            symbol,
            end_date="2024-01-01",
            start_date="2004-01-01",
            frequency="1d",
        )
        data_1d.to_pickle(produces)

    @pytask.task(id=asset)
    def task_download_5m_data(
        symbol=asset,
        produces=BLD / "python" / "data" / f"5m_{asset}.pkl",
    ):
        data_5m = data_download(
            symbol,
            end_date="2024-01-01",
            frequency="5m",
        )
        data_5m.to_pickle(produces)

    @pytask.task(id=asset)
    def task_download_60m_data(
        symbol=asset,
        produces=BLD / "python" / "data" / f"60m_{asset}.pkl",
    ):
        data_60m = data_download(
            symbol,
            end_date="2024-01-01",
            frequency="60m",
        )
        data_60m.to_pickle(produces)
