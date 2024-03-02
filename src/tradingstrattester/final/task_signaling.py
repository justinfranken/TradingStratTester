""""Tasks for creating all signal lists."""

import pickle

import pandas as pd
import pytask
from tradingstrattester.analysis.signaling_functions import signal_list
from tradingstrattester.config import BLD, STRATEGIES, _id

_dependencies = []
for i in _id:
    _dependencies.append(BLD / "python" / "data" / i)


for strategy in STRATEGIES:

    @pytask.task(id=strategy)
    def task_signal_list(
        signal_generator=strategy,
        depends_on=_dependencies,
        produces=BLD / "python" / "analysis" / f"{strategy}.pkl",
    ):
        """Create a dictionary of signal lists for each strategy."""
        if not _dependencies:
            msg = f"No data available for the file path {BLD / 'python' / 'data'}. Please state at least one entry in 'ASSETS' and 'FREQUENCIES' in the config.py file because they are empty."
            raise ValueError(msg)

        if not STRATEGIES:
            msg = "'STRATEGIES' is empty. Please specify at least one strategy for 'STRATEGIES' in the config.py file."

        strategy_dict = {}
        for i in range(len(_id)):
            name = f"signal_{_id[i]}"
            data = pd.read_pickle(depends_on[i])
            strategy_dict[name] = signal_list(data, signal_generator)

        with open(produces, "wb") as file:
            pickle.dump(strategy_dict, file)
