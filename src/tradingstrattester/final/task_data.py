""""Task to download the financial data and store it."""

import pytask
from tradingstrattester.config import ASSETS, BLD
from tradingstrattester.data_management.data_gathering import data_download

for asset in ASSETS:

    @pytask.task(id=asset)
    def task_download_1d_data(
        symbol=asset,
        produces=BLD / "python" / "data" / f"{asset}_1d.pkl",
    ):
        """Download financial data and store it in the bld folder."""
        data_1d = data_download(
            symbol,
            end_date="2024-01-01",
            start_date="2004-01-01",
            frequency="1d",
        )
        data_1d.to_pickle(produces)
