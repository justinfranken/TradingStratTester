""""Test for the simulating depot functions."""

from tradingstrattester.analysis.simulated_depot import simulated_depot
from tradingstrattester.config import (
    _id,
    initial_depot_cash,
    start_stock_prct,
    unit_strat,
    unit_var,
)


# Test config.py input variables
def test_simulated_depot_outcomes():
    """Test if simulated_depot outcomes are as expected."""
    # Testing sell signal
    signal = {}
    for id in _id:
        signal[f"signal_{id}"] = [2, 2]
    test_dict = {}
    test_dict["_simple_signal_gen"] = signal
    depot = simulated_depot(
        test_dict,
        "_simple_signal_gen",
        _id,
        initial_depot_cash,
        start_stock_prct,
        unit_strat,
        unit_var,
    )
    for id in _id:
        assert (
            depot["unit_dict"][id.split(".")[0]][1]
            <= depot["unit_dict"][id.split(".")[0]][0]
        )

    # Testing buy signal
    signal = {}
    for id in _id:
        signal[f"signal_{id}"] = [1, 1]
    test_dict = {}
    test_dict["_simple_signal_gen"] = signal
    depot = simulated_depot(
        test_dict,
        "_simple_signal_gen",
        _id,
        initial_depot_cash,
        start_stock_prct,
        unit_strat,
        unit_var,
    )
    for id in _id:
        assert (
            depot["unit_dict"][id.split(".")[0]][1]
            >= depot["unit_dict"][id.split(".")[0]][0]
        )

    # Testing do nothing signal
    signal = {}
    for id in _id:
        signal[f"signal_{id}"] = [0, 0]
    test_dict = {}
    test_dict["_simple_signal_gen"] = signal
    depot = simulated_depot(
        test_dict,
        "_simple_signal_gen",
        _id,
        initial_depot_cash,
        start_stock_prct,
        unit_strat,
        unit_var,
    )
    for id in _id:
        assert (
            depot["unit_dict"][id.split(".")[0]][1]
            == depot["unit_dict"][id.split(".")[0]][0]
        )

    # Test if initial depot value is correct
    signal = {}
    for id in _id:
        signal[f"signal_{id}"] = [0, 0]
    test_dict = {}
    test_dict["_simple_signal_gen"] = signal
    depot = simulated_depot(
        test_dict,
        "_simple_signal_gen",
        _id,
        initial_depot_cash,
        start_stock_prct,
        unit_strat,
        unit_var,
    )
    for id in _id:
        assert depot["value_dict"][id.split(".")[0]][0] == initial_depot_cash


# Test configuration variables from config.py file
