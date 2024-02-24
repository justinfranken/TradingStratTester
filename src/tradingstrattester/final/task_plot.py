""""Tasks for creating all analysis plots."""


import pandas as pd
import pytask
from tradingstrattester.analysis.plotting_functions import plot_asset_strategy
from tradingstrattester.config import ASSETS, BLD, FREQUENCIES, STRATEGIES

_id = [f"{frequency}_{asset}.pkl" for frequency in FREQUENCIES for asset in ASSETS]
_dependencies = []
for strategy in STRATEGIES:
    _dependencies.append(BLD / "python" / "analysis" / f"sim_depot{strategy}.pkl")

for id in _id:

    @pytask.task(id=id)
    def task_create_plots(
        id=id,
        depends_on=_dependencies,
        produces=BLD
        / "python"
        / "analysis"
        / "plots"
        / f"asset+strat_plot_{id.split('.')[0]}.html",
    ):
        data = pd.read_pickle(BLD / "python" / "data" / id)
        fig = plot_asset_strategy(data, id, depends_on)
        fig.write_html(produces)
