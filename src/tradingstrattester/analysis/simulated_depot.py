"""Function for simulating a depot to test strategies."""

import pandas as pd
from tradingstrattester.config import BLD, initial_depot_cash


def simulated_depot(
    signal_dict,
    strategy,
    _id,
    trade_units=100,
    start_stock=10,
    initial_portfolio_value=initial_depot_cash,
):
    """Simulates a trading strategy on multiple assets specified in ASSETS from the
    config.py file.

    Args:
        signal_dict (dict): A dictionary containing trading signals of the chosen strategy for each asset.
        strategy (str): The name of the trading strategy to be used.
        _id (list): A list of asset IDs specified in the config.py file.
        trade_units (int, optional): The number of units to trade per transaction. Default is 100.
        start_stock (int, optional): The initial number of stocks to start trading with. Default is 10.
        initial_portfolio_value (int, optional): The initial value of the portfolio. Default is 10,000.

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
            start_stock,
            initial_portfolio_value,
        )

        for i in range(1, len(signal)):
            if signal[i] == 2:  # Sell signal
                _execute_sell_signal(i, trade_units, cash, units, data)
            elif signal[i] == 1:  # Buy signal
                _execute_buy_signal(i, trade_units, cash, units, data)
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


def _initialize_variables(data, start_stock, initial_portfolio_value):
    """Initializes variables for simulating the trading depot.

    Args:
        data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        start_stock (int): The initial number of stocks to start trading with.
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.

    Returns:
        tuple: A tuple containing lists of units, cash, and portfolio value.

    """
    units = [start_stock]
    cash = [initial_portfolio_value - units[0] * data.Close.iloc[0]]
    value = [units[0] * data.Close.iloc[0] + cash[0]]

    return units, cash, value


def _execute_sell_signal(i, trade_units, cash, units, data):
    """Executes sell signal for a given time step.

    Args:
        i (int): Index of the current time step.
        trade_units (int): The number of units to trade per transaction.
        cash (list): List containing cash values for each time step.
        units (list): List containing unit holdings for each time step.
        data (pd.DataFrame): DataFrame containing asset data.

    """
    if units[i - 1] >= trade_units:
        cash.append(cash[i - 1] + data.Close.iloc[i] * trade_units)
        units.append(units[i - 1] - trade_units)
    else:
        cash.append(cash[i - 1])
        units.append(units[i - 1])


def _execute_buy_signal(i, trade_units, cash, units, data):
    """Executes buy signal for a given time step.

    Args:
        i (int): Index of the current time step.
        trade_units (int): The number of units to trade per transaction.
        cash (list): List containing cash values for each time step.
        units (list): List containing unit holdings for each time step.
        data (pd.DataFrame): DataFrame containing asset data.

    """
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
