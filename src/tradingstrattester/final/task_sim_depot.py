""""Tasks for simulating a depot for the strategies."""

import pickle

import pytask
from tradingstrattester.analysis.simulated_depot import simulated_depot
from tradingstrattester.config import (
    _ID,
    BLD,
    INITIAL_DEPOT_CASH,
    START_STOCK_PRCT,
    STRATEGIES,
    TAC,
    UNIT_STRAT,
    UNIT_VAR,
)

for strategy in STRATEGIES:

    @pytask.task(id=f"{strategy}_depot")
    def task_simulating_depot(
        strategy=strategy,
        depends_on=BLD / "python" / "analysis" / f"{strategy}.pkl",
        produces=BLD / "python" / "analysis" / f"sim_depot{strategy}.pkl",
    ):
        """Create the simulated depot for each strategy."""
        signal_dict = {}
        with open(depends_on, "rb") as file:
            signal_dict[strategy] = pickle.load(file)

        sim_depot_out = simulated_depot(
            signal_dict,
            strategy,
            _ID,
            INITIAL_DEPOT_CASH,
            START_STOCK_PRCT,
            UNIT_STRAT,
            UNIT_VAR,
            TAC,
        )

        with open(produces, "wb") as file:
            pickle.dump(sim_depot_out, file)
