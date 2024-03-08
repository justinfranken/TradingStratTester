""""Tasks for creating all signal lists."""

import pickle

import pandas as pd
import pytask
from tradingstrattester.analysis.signaling_functions import signal_list
from tradingstrattester.config import _ID, BLD, STRATEGIES

_dependencies = []
for i in _ID:
    _dependencies.append(BLD / "python" / "data" / i)


for strategy in STRATEGIES:

    @pytask.task(id=strategy)
    def task_signal_list(
        signal_generator=strategy,
        depends_on=_dependencies,
        produces=BLD / "python" / "analysis" / f"{strategy}.pkl",
    ):
        """Create a dictionary of signal lists for each strategy."""
        strategy_dict = {}
        for i in range(len(_ID)):
            name = f"signal_{_ID[i]}"
            data = pd.read_pickle(depends_on[i])
            strategy_dict[name] = signal_list(data, signal_generator)

        with open(produces, "wb") as file:
            pickle.dump(strategy_dict, file)
