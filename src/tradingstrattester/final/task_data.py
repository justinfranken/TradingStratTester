""""Task to download the financial data and store it."""

import pytask
from tradingstrattester.config import BLD, _id, end_date, start_date
from tradingstrattester.data_management.data_functions import data_download

for id in _id:

    @pytask.task(id=id.split(".")[0])
    def task_download_data(
        symbol=id.split(".")[0].split("_")[1],
        frequency=id.split(".")[0].split("_")[0],
        produces=BLD / "python" / "data" / id,
    ):
        """Download financial data and store it in the bld folder."""
        data = data_download(
            symbol,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
        )
        data.to_pickle(produces)
