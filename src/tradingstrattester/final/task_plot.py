""""Tasks for creating all analysis plots."""

import pickle

import pandas as pd
import pytask
from tradingstrattester.analysis.plotting_functions import plot_asset_strategy
from tradingstrattester.config import ASSETS, BLD, FREQUENCIES, STRATEGIES

_id = [f"{frequency}_{asset}.pkl" for frequency in FREQUENCIES for asset in ASSETS]

for strategy in STRATEGIES:
    for id in _id:

        @pytask.task(id=id)
        def task_plotting_assets_and_strats(
            id=id,
            depends_on=BLD / "python" / "analysis" / f"sim_depot{strategy}.pkl",
            produces=BLD
            / "python"
            / "analysis"
            / "plots"
            / f"asset+strat_plot_{id.split('.')[0]}.html",
        ):
            # Preparing asset and strategy output data
            data = {}
            data[id] = pd.read_pickle(BLD / "python" / "data" / id)
            with open(depends_on, "rb") as file:
                depot_out = pickle.load(file)

            # Make plot and store it as HTML
            fig = plot_asset_strategy(
                depot_out["value_dict"][id.split(".")[0]],
                data[id],
            )
            fig.write_html(produces)
