""""Tasks for creating all analysis plots."""


import pandas as pd
import pytask
from tradingstrattester.analysis.plotting_functions import (
    plot_asset_strategy,
    plot_indicators,
)
from tradingstrattester.config import BLD, STRATEGIES, _id, initial_depot_cash

_dependencies = []
for strategy in STRATEGIES:
    _dependencies.append(BLD / "python" / "analysis" / f"sim_depot{strategy}.pkl")


for id in _id:

    @pytask.task(id=id)
    def task_plot_asset_and_strats(
        id=id,
        depends_on=_dependencies,
        produces=BLD
        / "python"
        / "analysis"
        / "plots"
        / f"asset_and_strat_plot_{id.split('.')[0]}.html",
    ):
        """Create plot of asset candles and strategy depot values."""
        data = pd.read_pickle(BLD / "python" / "data" / id)
        fig = plot_asset_strategy(data, id, initial_depot_cash, depends_on)
        fig.write_html(produces)

    @pytask.task(id=id)
    def task_plot_indicators(
        id=id,
        depends_on=_dependencies,
        produces=BLD
        / "python"
        / "analysis"
        / "plots"
        / f"indicator-bar_plot_{id.split('.')[0]}.html",
    ):
        """Create indicator bar plots for each asset at each frequency."""
        data = pd.read_pickle(BLD / "python" / "data" / id)
        fig = plot_indicators(data, id, initial_depot_cash, depends_on)
        fig.write_html(produces)
