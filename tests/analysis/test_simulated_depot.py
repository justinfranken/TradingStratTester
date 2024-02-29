""""Test for the simulating depot functions."""

import pytest
from tradingstrattester.analysis.simulated_depot import (
    _handle_errors_in_sim_depot_config_vars,
    simulated_depot,
)
from tradingstrattester.config import (
    _id,
    initial_depot_cash,
    start_stock_prct,
    unit_strat,
    unit_var,
)

# Test simulated_depot outcomes

signals_list = [[2, 2], [1, 1], [0, 0]]
pattern_list = ["sell", "buy", "nothing"]


@pytest.mark.parametrize(
    ("signals", "pattern"),
    zip(signals_list, pattern_list),
)
def test_simulated_depot_outcomes(signals, pattern):
    """Test if simulated_depot outcomes are as expected."""

    signal = {}
    for id in _id:
        signal[f"signal_{id}"] = signals
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

    # Testing sell signal
    if pattern == "sell":
        for id in _id:
            assert (
                depot["unit_dict"][id.split(".")[0]][1]
                <= depot["unit_dict"][id.split(".")[0]][0]
            )

    # Testing buy signal
    if pattern == "buy":
        for id in _id:
            assert (
                depot["unit_dict"][id.split(".")[0]][1]
                >= depot["unit_dict"][id.split(".")[0]][0]
            )

    # Testing do nothing signal
    if pattern == "nothing":
        for id in _id:
            assert (
                depot["unit_dict"][id.split(".")[0]][1]
                == depot["unit_dict"][id.split(".")[0]][0]
            )


def test_initial_depot_cash_in_simulated_depot():
    """Test if start value of simulated_depot() is equal to initial_depot_cash."""
    signal = {}
    for id in _id:
        signal[f"signal_{id}"] = [0, 0]
    test_dict = {}
    test_dict["_simple_signal_gen"] = signal
    depot = simulated_depot(
        test_dict,
        "_simple_signal_gen",
        _id,
        100,
        start_stock_prct,
        unit_strat,
        unit_var,
    )
    for id in _id:
        assert depot["value_dict"][id.split(".")[0]][0] == 100


# Test configuration variables from config.py file

type_error_inputs = [
    # wrong initial_depot_cash
    ["1000", 0.25, "fixed_trade_units", 0.1],
    # wrong start_stock_prct
    [1000, "0.25", "fixed_trade_units", 0.1],
    # wrong unit_strat
    [1000, 0.25, initial_depot_cash, 0.1],
    # wrong unit_var
    [1000, 0.25, "fixed_trade_units", "0.1"],
]


@pytest.mark.parametrize("type_inputs", type_error_inputs)
def test_handle_errors_in_sim_depot_config_vars_type_error(type_inputs):
    """Test if _handle_errors_in_sim_depot_config_vars raises correct type errors."""
    with pytest.raises(TypeError):
        _handle_errors_in_sim_depot_config_vars(type_inputs)


def test_handle_errors_in_sim_depot_config_vars_value_errors():
    with pytest.raises(ValueError):
        _handle_errors_in_sim_depot_config_vars(-1000, 0.25, "fixed_trade_units", 0.1)
        _handle_errors_in_sim_depot_config_vars(1000, -0.25, "fixed_trade_units", 0.1)
        _handle_errors_in_sim_depot_config_vars(1000, 1.25, "fixed_trade_units", 0.1)
        _handle_errors_in_sim_depot_config_vars(1000, 0.25, "test", 0.1)
        _handle_errors_in_sim_depot_config_vars(1000, 0.25, "fixed_trade_units", -0.1)
        _handle_errors_in_sim_depot_config_vars(1000, 0.25, "fixed_trade_units", 1.1)
