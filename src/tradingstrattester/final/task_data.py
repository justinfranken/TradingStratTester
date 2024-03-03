""""Task to download the financial data and store it."""

import pytask
from tradingstrattester.config import ASSETS, BLD, FREQUENCIES, end_date, start_date
from tradingstrattester.data_management.data_functions import data_download

# Task function for "1d" frequency data to facilitate reproducibility
for asset in ASSETS:

    @pytask.task(id=asset)
    def task_download_1d_data(
        symbol=asset,
        produces=BLD / "python" / "data" / f"1d_{asset}.pkl",
    ):
        """Download financial data and store it in the bld folder."""
        data_1d = data_download(
            symbol,
            end_date=end_date,
            start_date=start_date,
            frequency="1d",
        )
        data_1d.to_pickle(produces)


# Task function for high frequency data from today - max possible length
FREQUENCIES = [freq for freq in FREQUENCIES if freq != "1d"]
_id = []

for frequency in FREQUENCIES:
    for asset in ASSETS:
        state = FREQUENCIES.index(frequency) * len(ASSETS) + ASSETS.index(asset)
        _id.append(f"{frequency}_{asset}")

        @pytask.task(id=_id[state])
        def task_download_high_frequency_data(
            symbol=asset,
            frequency=frequency,
            produces=BLD / "python" / "data" / f"{_id[state]}.pkl",
        ):
            """Download financial data and store it in the bld folder."""
            high_frequency_data = data_download(symbol, frequency=frequency)
            high_frequency_data.to_pickle(produces)
