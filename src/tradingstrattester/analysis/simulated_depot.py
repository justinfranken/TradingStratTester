"""Function for simulating a depot to test strategies."""

import math

import numpy as np
import pandas as pd
from tradingstrattester.config import (
    BLD,
    initial_depot_cash,
    start_stock_prct,
    unit_strat,
    unit_var,
)


def simulated_depot(signal_dict, strategy, _id):
    """Simulates a trading strategy on multiple assets specified in ASSETS from the
    config.py file.

    Args:
        signal_dict (dict): A dictionary containing trading signals of the chosen strategy for each asset.
        strategy (str): The name of the trading strategy to be used.
        _id (list): A list of asset IDs specified in the config.py file.

    Returns:
        dict: A dictionary containing cash, units, and portfolio value balances for each asset specified in ASSET from the config.py file.

    """
    cash_dict = {}
    unit_dict = {}
    value_dict = {}

    for id in _id:
        signal = signal_dict[strategy][f"signal_{id}"]
        data = pd.read_pickle(BLD / "python" / "data" / id)

        units, cash, value = _initialize_variables(
            data,
            initial_depot_cash,
        )

        for i in range(1, len(signal)):
            if signal[i] == 2:  # Sell signal
                _execute_sell_signal(i, value, cash, units, data, unit_strat, unit_var)
            elif signal[i] == 1:  # Buy signal
                _execute_buy_signal(i, value, cash, units, data, unit_strat, unit_var)
            else:
                _execute_no_signal(i, cash, units)

            value.append(units[i] * data.Close.iloc[i] + cash[i])

        cash_dict[id.split(".")[0]] = cash
        unit_dict[id.split(".")[0]] = units
        value_dict[id.split(".")[0]] = value

    return {
        "cash_dict": cash_dict,
        "unit_dict": unit_dict,
        "value_dict": value_dict,
    }


def _initialize_variables(data, initial_depot_cash):
    """Initializes variables for simulating the trading depot.

    Args:
        data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.

    Returns:
        tuple: A tuple containing lists of units, cash, and portfolio value.

    """
    units = [math.floor((initial_depot_cash * start_stock_prct) / data.Close.iloc[0])]
    cash = [initial_depot_cash - units[0] * data.Close.iloc[0]]
    value = [units[0] * data.Close.iloc[0] + cash[0]]

    return units, cash, value


def _execute_sell_signal(i, value, cash, units, data, unit_strat, unit_var):
    """Executes sell signal for a given time step.

    Args:
        i (int): Index of the current time step.
        value (list): List or array containing the value of the trading account at each time step.
        cash (list): List containing cash values for each time step.
        data (pd.DataFrame): DataFrame containing asset data.
        units (list): List containing unit holdings for each time step.
        unit_strat (str): Strategy for determining trade units. Supported strategies: 'fixed_trade_units',
                        'percentage_to_value_trades', 'volatility_unit_trades'.
        unit_var (float): Variable used in the unit strategy calculation.

    """
    trade_units = _trade_units(i, data, value, unit_strat, unit_var)
    if units[i - 1] >= trade_units:
        cash.append(cash[i - 1] + data.Close.iloc[i] * trade_units)
        units.append(units[i - 1] - trade_units)
    else:
        cash.append(cash[i - 1])
        units.append(units[i - 1])


def _execute_buy_signal(i, value, cash, units, data, unit_strat, unit_var):
    """Executes buy signal for a given time step.

    Args:
        i (int): Index of the current time step.
        value (list): List or array containing the value of the trading account at each time step.
        cash (list): List containing cash values for each time step.
        units (list): List containing unit holdings for each time step.
        data (pd.DataFrame): DataFrame containing asset data.
        unit_strat (str): Strategy for determining trade units. Supported strategies: 'fixed_trade_units',
                        'percentage_to_value_trades', 'volatility_unit_trades'.
        unit_var (float): Variable used in the unit strategy calculation.

    """
    trade_units = _trade_units(i, data, value, unit_strat, unit_var)
    cash_required = data.Close.iloc[i] * trade_units
    if cash[i - 1] >= cash_required:
        cash.append(cash[i - 1] - cash_required)
        units.append(units[i - 1] + trade_units)
    else:
        cash.append(cash[i - 1])
        units.append(units[i - 1])


def _execute_no_signal(i, cash, units):
    """Executes no signal action for a given time step.

    Args:
        i (int): Index of the current time step.
        cash (list): List containing cash values for each time step.
        units (list): List containing unit holdings for each time step.

    """
    cash.append(cash[i - 1])
    units.append(units[i - 1])


# Determining the amount of units to trade


def _trade_units(i, data, value, unit_strat, unit_var):
    """Determine the number of units to trade based on the specified unit strategy.

    Args:
        i (int): Index indicating the current time step.
        data (pandas.DataFrame): DataFrame containing the data, with a 'Close' column representing closing prices.
        value (list): List or array containing the value of the trading account at each time step.
        unit_strat (str): Strategy for determining trade units. Supported strategies: 'fixed_trade_units',
                        'percentage_to_value_trades', 'volatility_unit_trades'.
        unit_var (float): Variable used in the unit strategy calculation.

    Returns:
        out (int): Number of units to trade based on the specified strategy.

    """
    if unit_strat == "fixed_trade_units":
        out = unit_var

    if unit_strat == "percentage_to_value_trades":
        out = __percentage_to_value_trades(i, data, value, unit_var)

    if unit_strat == "volatility_unit_trades":
        out = __volatility_unit_trades(i, data, value, unit_var)

    return out


def __percentage_to_value_trades(i, data, value, unit_var):
    """Calculate the number of units to trade based on a percentage of the account
    value.

    Args:
    - i (int): Index indicating the current time step.
    - data (pandas.DataFrame): DataFrame containing the data, with a 'Close' column representing closing prices.
    - value (list or numpy.ndarray): List or array containing the value of the trading account at each time step.
    - unit_var (float): Percentage of the account value to allocate for trading.

    Returns:
    - int: Number of units to trade.

    """
    return math.floor((value[i - 1] * unit_var) / data.Close.iloc[i])


def __volatility_unit_trades(i, data, value, unit_var):
    """Calculate the number of units to trade based on volatility and a percentage of
    the account value.

    Args:
    - i (int): Index indicating the current time step.
    - data (pandas.DataFrame): DataFrame containing the data, with a 'Close' column representing closing prices.
    - value (list or numpy.ndarray): List or array containing the value of the trading account at each time step.
    - unit_var (float): Percentage of the account value to allocate for trading.

    Returns:
    - int: Number of units to trade.

    """
    unit = math.floor((value[i - 1] * unit_var) / data.Close.iloc[i])

    return unit if i <= 50 else math.floor(np.std(data.Close.iloc[i - 50 : i]) * unit)
