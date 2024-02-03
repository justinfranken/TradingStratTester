""""Tasks for creating all signal lists."""

import pickle

import pandas as pd
import pytask
from tradingstrattester.analysis.signaling_functions import signal_list
from tradingstrattester.config import ASSETS, BLD, FREQUENCIES, STRATEGIES

_id = [f"{frequency}_{asset}.pkl" for frequency in FREQUENCIES for asset in ASSETS]
_dependencies = []
for i in _id:
    _dependencies.append(BLD / "python" / "data" / i)


for signal_generator in STRATEGIES:

    @pytask.task(id=signal_generator)
    def task_signal_list(
        signal_generator=signal_generator,
        depends_on=_dependencies,
        produces=BLD / "python" / "analysis" / f"{signal_generator}.pkl",
    ):
        strategy_dict = {}
        for i in range(len(_id)):
            name = _id[i]
            data = pd.read_pickle(depends_on[i])
            strategy_dict[name] = signal_list(data, signal_generator)

        with open(produces, "wb") as file:
            pickle.dump(strategy_dict, file)
