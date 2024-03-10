""""Test for the signaling functions."""
import pandas as pd
import pytest
from tradingstrattester.analysis.signaling_functions import (
    _bollinger_bands_signal_gen,
    _crossover_signal_gen,
    _handle_errors_bb,
    _handle_errors_macd_gen,
    _handle_errors_rsi,
    _macd_signal_gen,
    _random_signal_gen,
    _rsi_signal_gen,
    signal_list,
)
from tradingstrattester.config import STRATEGIES
from tradingstrattester.data_management.data_functions import data_download

# Test signal_list
value_error_data_list = [
    pd.DataFrame(),
    pd.DataFrame(1, range(2), columns=["Open", "High", "Low", "Wrong_Close"]),
    pd.DataFrame(1, range(2), columns=["High", "Low", "Close"]),
]
type_error_data_list = [
    "data",
    range(10),
]
value_error_generator_list = [
    "typo",
    "random_gen",
]
type_error_generator_list = [
    {"_random_gen"},
    ["_random_gen"],
]


@pytest.mark.parametrize(
    (
        "value_error_data",
        "type_error_data",
        "value_error_generator",
        "type_error_generator",
    ),
    zip(
        value_error_data_list,
        type_error_data_list,
        value_error_generator_list,
        type_error_generator_list,
    ),
)
def test_error_handling_in_signal_list(
    value_error_data,
    type_error_data,
    value_error_generator,
    type_error_generator,
):
    """Test if data error handling for signal_list() works."""
    with pytest.raises(ValueError):
        signal_list(value_error_data, STRATEGIES[0])
    with pytest.raises(TypeError):
        signal_list(type_error_data, STRATEGIES[0])
    with pytest.raises(ValueError):
        signal_list(
            pd.DataFrame(1, range(2), columns=["Open", "High", "Low", "Close"]),
            value_error_generator,
        )
    with pytest.raises(TypeError):
        signal_list(
            pd.DataFrame(1, range(2), columns=["Open", "High", "Low", "Close"]),
            type_error_generator,
        )


def test_generator_error_in_signal_list():
    """Test if generator error handling for signal_list() works."""
    data = data_download("DB", "60m")
    with pytest.raises(ValueError):
        signal_list(data, "test")
    with pytest.raises(TypeError):
        signal_list(data, data)


# Test signaling strategies
columns = ["Open", "High", "Low", "Close"]
co_in = [
    pd.DataFrame([[-1, 0, 0, 0], [2, 0, 0, -2]], range(2), columns=columns),
    pd.DataFrame([[0, 0, 0, -1], [-1, 0, 0, 2]], range(2), columns=columns),
    pd.DataFrame([[0, 0, 0, 0], [0, 0, 0, 0]], range(2), columns=columns),
]
co_out = [
    [0, 1],
    [0, 2],
    [0, 0],
]
rsi_in = [
    pd.DataFrame(
        [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 2]],
        range(3),
        columns=columns,
    ),
    pd.DataFrame(
        [[0, 0, 0, 2], [0, 0, 0, 1], [0, 0, 0, 0]],
        range(3),
        columns=columns,
    ),
    pd.DataFrame(
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        range(3),
        columns=columns,
    ),
]
rsi_out = [
    [0, 1, 1],
    [0, 2, 2],
    [0, 0, 0],
]
bb_in = [
    pd.DataFrame(
        [[0, 0, 0, 2], [0, 0, 0, 1], [0, 0, 0, 0]],
        range(3),
        columns=columns,
    ),
    pd.DataFrame(
        [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 2]],
        range(3),
        columns=columns,
    ),
    pd.DataFrame(
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        range(3),
        columns=columns,
    ),
]
bb_out = [
    [0, 1, 1],
    [0, 2, 2],
    [0, 0, 0],
]
macd_in = [
    pd.DataFrame(
        [[0, 0, 0, 2], [0, 0, 0, 1], [0, 0, 0, 0]],
        range(3),
        columns=columns,
    ),
    pd.DataFrame(
        [[0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 0, 2]],
        range(3),
        columns=columns,
    ),
    pd.DataFrame(
        [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
        range(3),
        columns=columns,
    ),
]
macd_out = [
    [0, 0, 1],
    [0, 0, 2],
    [0, 0, 0],
]


@pytest.mark.parametrize(
    ("co_1", "co_2", "rsi_1", "rsi_2", "bb_1", "bb_2", "macd_1", "macd_2"),
    zip(co_in, co_out, rsi_in, rsi_out, bb_in, bb_out, macd_in, macd_out),
)
def test_strategy_signal_generator_outcomes(
    co_1,
    co_2,
    rsi_1,
    rsi_2,
    bb_1,
    bb_2,
    macd_1,
    macd_2,
):
    """Test outcomes of all strategies except random_signal_generator()."""
    assert _crossover_signal_gen(co_1) == co_2
    assert _rsi_signal_gen(rsi_1) == rsi_2
    assert _bollinger_bands_signal_gen(bb_1, window=2, num_std_dev=0.5) == bb_2
    assert _macd_signal_gen(macd_1, 2, 1, 2, 0) == macd_2


# Test_random_signal_gen outcomes
def test_random_signal_gen_outcome():
    """Test if _random_signal_gen() outcomes are as expected."""
    df = pd.DataFrame(1, index=range(1), columns=["Open", "High", "Low", "Close"])
    assert _random_signal_gen(df, 1, 0, 0) == [0]
    assert _random_signal_gen(df, 0, 1, 0) == [1]
    assert _random_signal_gen(df, 0, 0, 1) == [2]


# Test signaling functions error handling
def test_probability_errors_in_random_signal_gen():
    """Test if probability error handling for _random_signal_gen() works."""
    df = pd.DataFrame(1, index=range(1), columns=["Open", "High", "Low", "Close"])
    with pytest.raises(ValueError):
        _random_signal_gen(df, 0, 0, -0.5)
    with pytest.raises(ValueError):
        _random_signal_gen(df, 0, 0, 2)
    with pytest.raises(ValueError):
        _random_signal_gen(df, 0.5, 0.5, 0.5)


def test_rsi_error_handling():
    """Test rsi_signal_gen error handling."""
    with pytest.raises(ValueError):
        _handle_errors_rsi(-30, 70, 10)
        _handle_errors_rsi(70, 30, 10)
        _handle_errors_rsi(30, 70, -10)
    with pytest.raises(TypeError):
        _handle_errors_rsi("30", 70, 10)
        _handle_errors_rsi(30, 70, 10.5)


def test_bb_error_handling():
    """Test bb_signal_gen error handling."""
    with pytest.raises(ValueError):
        _handle_errors_bb(-10, 1.5)
        _handle_errors_bb(10, -1.5)
    with pytest.raises(TypeError):
        _handle_errors_bb(10.5, 1.5)
        _handle_errors_bb(10, "1.5")


def test_macd_error_handling():
    """Test macd_signal_gen error handling."""
    with pytest.raises(ValueError):
        _handle_errors_macd_gen(-10, 10, 10, 2)
        _handle_errors_macd_gen(10, 10, 10, -2)
    with pytest.raises(TypeError):
        _handle_errors_macd_gen(10.5, 10, 10, 2)
        _handle_errors_macd_gen(10, 10, 10, "2")
