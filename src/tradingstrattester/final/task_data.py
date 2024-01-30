""""Task to download the financial data and store it."""

import pytask
from tradingstrattester.config import ASSETS, BLD, FREQUENCIES
from tradingstrattester.data_management.data_functions import data_download

# Task function for "1d" frequency data for reproducibility of analysis and plots
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


# Task function for high frequency data from today - max possible length
FREQUENCIES = [freq for freq in FREQUENCIES if freq != "1d"]
_id = []

for frequency in FREQUENCIES:
    for asset in ASSETS:
        """Download financial data and store it in the bld folder."""
        state = FREQUENCIES.index(frequency) * len(ASSETS) + ASSETS.index(asset)
        _id.append(f"{frequency}_{asset}")

        @pytask.task(id=_id[state])
        def task_download_high_frequency_data(
            produces=BLD / "python" / "data" / f"{_id[state]}.pkl",
        ):
            high_frequency_data = data_download(asset, frequency=frequency)
            high_frequency_data.to_pickle(produces)