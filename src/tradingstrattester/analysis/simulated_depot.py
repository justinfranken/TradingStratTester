"""Function for simulating a depot to test strategies."""

import pandas as pd
from tradingstrattester.config import BLD


def process_strategy(
    signal_dict,
    strategy,
    _id,
    trade_units=100,
    start_stock=10,
    initial_portfolio_value=10_000,
):
    cash_dict = {}
    unit_dict = {}
    value_dict = {}

    for id in _id:
        signal = signal_dict[strategy][f"signal_{id}"]
        data = pd.read_pickle(BLD / "python" / "data" / id)

        units, cash, value = _initialize_variables(
            data,
            trade_units,
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

        cash_dict[id] = cash
        unit_dict[id] = units
        value_dict[id] = value

    return {
        "cash_dict": cash_dict,
        "unit_dict": unit_dict,
        "value_dict": value_dict,
    }


def _initialize_variables(data, trade_units, start_stock, initial_portfolio_value):
    units = [trade_units * start_stock]
    cash = [initial_portfolio_value - units[0] * data.Close.iloc[0]]
    value = [units[0] * data.Close.iloc[0] + cash[0]]

    return units, cash, value


def _execute_sell_signal(i, trade_units, cash, units, data):
    if units[i - 1] >= trade_units:
        cash.append(cash[i - 1] + data.Close.iloc[i] * trade_units)
        units.append(units[i - 1] - trade_units)
    else:
        cash.append(cash[i - 1])
        units.append(units[i - 1])


def _execute_buy_signal(i, trade_units, cash, units, data):
    cash_required = data.Close.iloc[i] * trade_units
    if cash[i - 1] >= cash_required:
        cash.append(cash[i - 1] - cash_required)
        units.append(units[i - 1] + trade_units)
    else:
        cash.append(cash[i - 1])
        units.append(units[i - 1])


def _execute_no_signal(i, cash, units):
    cash.append(cash[i - 1])
    units.append(units[i - 1])
