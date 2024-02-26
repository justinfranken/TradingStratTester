""""Tasks for simulating a depot for the strategies."""

import pickle

import pytask
from tradingstrattester.analysis.simulated_depot import simulated_depot
from tradingstrattester.config import ASSETS, BLD, FREQUENCIES, STRATEGIES

for strategy in STRATEGIES:

    @pytask.task(id=f"{strategy}_depot")
    def task_simulating_depot(
        strategy=strategy,
        depends_on=BLD / "python" / "analysis" / f"{strategy}.pkl",
        produces=BLD / "python" / "analysis" / f"sim_depot{strategy}.pkl",
    ):
        """Create the simulated depot for each strategy."""
        _id = [
            f"{frequency}_{asset}.pkl" for frequency in FREQUENCIES for asset in ASSETS
        ]

        signal_dict = {}
        with open(depends_on, "rb") as file:
            signal_dict[strategy] = pickle.load(file)

        sim_depot_out = simulated_depot(
            signal_dict,
            strategy,
            _id,
        )

        with open(produces, "wb") as file:
            pickle.dump(sim_depot_out, file)
