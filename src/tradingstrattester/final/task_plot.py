""""Tasks for creating all analysis plots."""


import pandas as pd
import pytask
from tradingstrattester.analysis.plotting_functions import (
    plot_asset_strategy,
    plot_indicators,
    plot_units_and_cash,
)
from tradingstrattester.config import _ID, BLD, INITIAL_DEPOT_CASH, STRATEGIES

# Preparing depending and producing paths
_dependencies = []
for strategy in STRATEGIES:
    _dependencies.append(BLD / "python" / "analysis" / f"sim_depot{strategy}.pkl")


_produce_paths = []
plot_names = ["asset_and_depot_value_plot", "indicator-bar_plot", "units_and_cash_plot"]
path_names = ["assets_and_depot_value", "indicator_bars", "units_and_cash"]
for id in _ID:
    for i in range(len(path_names)):
        _produce_paths.append(
            BLD / "plots" / path_names[i] / f"{plot_names[i]}_{id.split('.')[0]}.html",
        )

# Task function for plotting
index = -1
for id in _ID:
    index += 1
    index_start = index * 3
    index_end = index_start + 3

    @pytask.task(id=id.split(".")[0])
    def task_create_plots(
        id=id,
        depends_on=_dependencies,
        produces=_produce_paths[index_start:index_end],
    ):
        """Create all plots (asset+depot value, indicators, unit+cash)."""
        data = pd.read_pickle(BLD / "python" / "data" / id)

        # Plot asset and depot_value
        fig_asset_strat = plot_asset_strategy(data, id, INITIAL_DEPOT_CASH, depends_on)
        fig_asset_strat.write_html(produces[0])

        # Plot indicator bars
        fig_indicators = plot_indicators(data, id, INITIAL_DEPOT_CASH, depends_on)
        fig_indicators.write_html(produces[1])

        # Plot units and cash
        fig_units_cash = plot_units_and_cash(data, id, depends_on)
        fig_units_cash.write_html(produces[2])
