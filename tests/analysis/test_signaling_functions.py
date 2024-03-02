""""Test for the signaling functions."""
import numpy as np
import pandas as pd
import pytest
from tradingstrattester.analysis.signaling_functions import (
    _random_signal_gen,
    signal_list,
)
from tradingstrattester.config import STRATEGIES
from tradingstrattester.data_management.data_functions import data_download


# Test signal_list
def test_data_error_in_signal_list():
    """Test if data error handling for signal_list() works."""
    data = pd.DataFrame()
    with pytest.raises(ValueError):
        signal_list(data, STRATEGIES[0])


def test_generator_error_in_signal_list():
    """Test if generator error handling for signal_list() works."""
    data = data_download("DB")
    with pytest.raises(ValueError):
        signal_list(data, "test")
    with pytest.raises(TypeError):
        signal_list(data, data)


# Test _simple_signal_generator
def test_simple_signal_generator_outcome():
    """Test if _simple_signal_generator outcomes are as expected."""
    df = pd.DataFrame(1, index=range(10), columns=["Open", "Close"])
    assert signal_list(df, STRATEGIES[0]) == list(np.zeros(10))


# Test_random_signal_gen
def test_probability_errors_in_random_signal_gen():
    """Test if probability error handling for _random_signal_gen() works."""
    with pytest.raises(ValueError):
        _random_signal_gen(0, 0, -0.5)
    with pytest.raises(ValueError):
        _random_signal_gen(0, 0, 2)
    with pytest.raises(ValueError):
        _random_signal_gen(0.5, 0.5, 0.5)


def test_random_signal_gen_outcome():
    """Test if _random_signal_gen() outcomes are as expected."""
    assert _random_signal_gen(1, 0, 0) == 0
    assert _random_signal_gen(0, 1, 0) == 1
    assert _random_signal_gen(0, 0, 1) == 2
