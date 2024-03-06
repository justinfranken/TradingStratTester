"""Function for simulating a depot to test strategies."""

import math

import numpy as np
import pandas as pd
from tradingstrattester.config import BLD


def simulated_depot(
    signal_dict,
    strategy,
    _id,
    initial_depot_cash,
    start_stock_prct,
    unit_strat,
    unit_var,
    tac,
):
    """Simulates a trading strategy on multiple assets specified in ASSETS from the
    config.py file.

    Args:
    - signal_dict (dict): A dictionary containing trading signals of the chosen strategy for each asset.
    - strategy (str): The name of the trading strategy to be used.
    - _id (list): A list of asset IDs specified in the config.py file.
    - initial_depot_cash (float): The initial depot cash value defined in the config.py file.
    - start_stock_prct (float): The percentage indicating the portion of the initial depot value to be invested in stocks.
    - unit_strat (str): Strategy for determining trade units. Supported strategies: 'fixed_trade_units',
                        'percentage_to_value_trades', 'volatility_unit_trades'.
    - unit_var (float): Variable used in the unit strategy calculation.

    Returns:
    - dict: A dictionary containing cash, units, and portfolio value balances for each asset specified in ASSET from the config.py file.

    """
    _handle_errors_in_input_variables(
        signal_dict,
        strategy,
        initial_depot_cash,
        start_stock_prct,
        unit_strat,
        unit_var,
    )

    cash_dict = {}
    unit_dict = {}
    value_dict = {}

    for id in _id:
        signal = signal_dict[strategy][f"signal_{id}"]
        data = pd.read_pickle(BLD / "python" / "data" / id)

        units, cash, value = _initialize_variables(
            data,
            initial_depot_cash,
            start_stock_prct,
        )

        for i in range(1, len(signal)):
            if signal[i] == 2:  # Sell signal
                _execute_sell_signal(
                    i,
                    value,
                    cash,
                    units,
                    data,
                    unit_strat,
                    unit_var,
                    tac,
                )
            elif signal[i] == 1:  # Buy signal
                _execute_buy_signal(
                    i,
                    value,
                    cash,
                    units,
                    data,
                    unit_strat,
                    unit_var,
                    tac,
                )
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


def _initialize_variables(data, initial_depot_cash, start_stock_prct):
    """Initializes variables for simulating the trading depot.

    Args:
    - data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
    - initial_depot_cash (float): The initial depot cash value defined in the config.py file.
    - start_stock_prct (float): The percentage indicating the portion of the initial depot value to be invested in stocks.

    Returns:
    - tuple: A tuple containing lists of units, cash, and portfolio value.

    """
    units = [math.floor((initial_depot_cash * start_stock_prct) / data.Close.iloc[0])]
    cash = [initial_depot_cash - units[0] * data.Close.iloc[0]]
    value = [units[0] * data.Close.iloc[0] + cash[0]]

    return units, cash, value


def _execute_sell_signal(i, value, cash, units, data, unit_strat, unit_var, tac):
    """Executes sell signal for a given time step.

    Args:
    - i (int): Index of the current time step.
    - value (list): List or array containing the value of the trading account at each time step.
    - cash (list): List containing cash values for each time step.
    - data (pd.DataFrame): DataFrame containing asset data.
    - units (list): List containing unit holdings for each time step.
    - unit_strat (str): Strategy for determining trade units. Supported strategies: 'fixed_trade_units',
                        'percentage_to_value_trades', 'volatility_unit_trades'.
    - unit_var (float): Variable used in the unit strategy calculation.

    """
    trade_units = _trade_units(i, data, value, unit_strat, unit_var)
    if units[i - 1] >= trade_units:
        cash.append(cash[i - 1] + data.Close.iloc[i] * trade_units * (1 - tac))
        units.append(units[i - 1] - trade_units)
    else:
        cash.append(cash[i - 1])
        units.append(units[i - 1])


def _execute_buy_signal(i, value, cash, units, data, unit_strat, unit_var, tac):
    """Executes buy signal for a given time step.

    Args:
    - i (int): Index of the current time step.
    - value (list): List or array containing the value of the trading account at each time step.
    - cash (list): List containing cash values for each time step.
    - units (list): List containing unit holdings for each time step.
    - data (pd.DataFrame): DataFrame containing asset data.
    - unit_strat (str): Strategy for determining trade units. Supported strategies: 'fixed_trade_units',
                        'percentage_to_value_trades', 'volatility_unit_trades'.
    - unit_var (float): Variable used in the unit strategy calculation.

    """
    trade_units = _trade_units(i, data, value, unit_strat, unit_var)
    cash_required = data.Close.iloc[i] * trade_units
    if cash[i - 1] >= cash_required:
        cash.append(cash[i - 1] - data.Close.iloc[i] * trade_units * (1 + tac))
        units.append(units[i - 1] + trade_units)
    else:
        cash.append(cash[i - 1])
        units.append(units[i - 1])


def _execute_no_signal(i, cash, units):
    """Executes no signal action for a given time step.

    Args:
    - i (int): Index of the current time step.
    - cash (list): List containing cash values for each time step.
    - units (list): List containing unit holdings for each time step.

    """
    cash.append(cash[i - 1])
    units.append(units[i - 1])


# Determining the amount of units to trade


def _trade_units(i, data, value, unit_strat, unit_var):
    """Determine the number of units to trade based on the specified unit strategy.

    Args:
    - i (int): Index indicating the current time step.
    - data (pandas.DataFrame): DataFrame containing the data, with a 'Close' column representing closing prices.
    - value (list): List or array containing the value of the trading account at each time step.
    - unit_strat (str): Strategy for determining trade units. Supported strategies: 'fixed_trade_units',
                        'percentage_to_value_trades', 'volatility_unit_trades'.
    - unit_var (float): Variable used in the unit strategy calculation.

    Returns:
    - out (int): Number of units to trade based on the specified strategy.

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
    """Calculate the number of units to trade based on volatility of the past 10 trades
    and a percentage of the account value.

    Args:
    - i (int): Index indicating the current time step.
    - data (pandas.DataFrame): DataFrame containing the data, with a 'Close' column representing closing prices.
    - value (list or numpy.ndarray): List or array containing the value of the trading account at each time step.
    - unit_var (float): Percentage of the account value to allocate for trading.

    Returns:
    - int: Number of units to trade.

    """
    unit = math.floor((value[i - 1] * unit_var) / data.Close.iloc[i])

    return unit if i <= 10 else math.floor(np.std(data.Close.iloc[i - 10 : i]) * unit)


def _handle_errors_in_input_variables(
    signal_dict,
    strategy,
    initial_depot_cash,
    start_stock_prct,
    unit_strat,
    unit_var,
):
    if not isinstance(strategy, str):
        msg = f"'strategy' has to be of type str and not {type(strategy)}."
        raise TypeError(msg)
    og_strategies = [
        "_random_gen",
        "_crossover_gen",
        "_RSI_gen",
        "_BB_gen",
        "_MACD_gen",
    ]
    if strategy not in og_strategies:
        msg = f"Selected trading strategy ({strategy}) is not available. Please choose at least one from "
        raise ValueError(msg)

    if not isinstance(signal_dict, dict):
        msg = f"'signal_dict' has to be of type dict and not {type(signal_dict)}."
        raise TypeError(msg)
    if not signal_dict:
        msg = "'signal_dict' is empty. Please specify signal list for signal_dict."
        raise ValueError(msg)

    __handle_errors_in_sim_depot_config_vars(
        initial_depot_cash,
        start_stock_prct,
        unit_strat,
        unit_var,
    )


def __handle_errors_in_sim_depot_config_vars(
    initial_depot_cash,
    start_stock_prct,
    unit_strat,
    unit_var,
):
    """Handle type and value errors for sim depot input variables from config.py.

    Raises:
    - TypeError: Raises TypeErrors in case inputs have not the right type.
    - ValueError: Raises ValueErrors in case that inputs aren't in the correct format.

    """
    # initial_depot_cash
    if not isinstance(initial_depot_cash, int | float):
        msg = f"'initial_depot_cash' has the wrong type ({type(initial_depot_cash)}). '{initial_depot_cash}' has to be of type int or float."
        raise TypeError(msg)
    if initial_depot_cash <= 0:
        msg = f"Wrong input for 'initial_depot_cash' ({initial_depot_cash}). Input has to be greater than 0."
        raise ValueError(msg)

    # start_stock_prct
    if not isinstance(start_stock_prct, int | float):
        msg = f"'start_stock_prct' has the wrong type ({type(start_stock_prct)}). '{start_stock_prct}' has to be of type int or float."
        raise TypeError(msg)
    if start_stock_prct <= 0 or start_stock_prct > 1:
        msg = f"'start_stock_prct' has to be greaterthan or equal to 0 and smaller than or equal to 1, and not {start_stock_prct}."
        raise ValueError(msg)

    # unit_strat
    if not isinstance(unit_strat, str):
        msg = f"'unit_strat' has the wrong type ({type(unit_strat)}). '{unit_strat}' has to be of type str."
        raise TypeError(msg)
    og_unit_strats = [
        "fixed_trade_units",
        "percentage_to_value_trades",
        "volatility_unit_trades",
    ]
    if unit_strat not in og_unit_strats:
        msg = f"Input for 'unit_strat' ({unit_strat}) is not in {og_unit_strats}."
        raise ValueError(msg)

    # unit_var
    if not isinstance(unit_var, int | float):
        msg = f"'unit_var' has the wrong type ({type(unit_var)}). '{unit_var}' has to be of type int or float."
        raise TypeError(msg)
    if unit_var <= 0 or unit_var > 1:
        msg = f"'unit_var' has to be greater 0 and smaller or equal than 1, and not {unit_var}."
        raise ValueError(msg)
