"""Functions for indicating when to buy or sell."""

import math
import pathlib
import pickle

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tradingstrattester.config import _ID, STRATEGIES


def plot_asset_strategy(data, id, initial_depot_cash, depends_on):
    """Plot depot value for different strategies and asset price in the form of
    candlesticks.

    Parameters:
        data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.
        depends_on (list): A list of file paths to the simulated depots for each strategy.

    Returns:
        fig (go.Figure): The Plotly figure object containing annotated asset price candlesticks and simulated depot values for each strategy.

    """
    _handle_errors_in_plot_functions(
        data=data,
        id=id,
        initial_depot_cash=initial_depot_cash,
        depends_on=depends_on,
    )

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    _add_strategy_traces(fig, data, id, depends_on)
    _add_initial_depot_annotation(fig, initial_depot_cash)
    _add_asset_candlesticks(fig, data, id)

    _add_figure_layout_asset_strategy(fig, id)

    return fig


def _add_strategy_traces(fig, data, id, depends_on):
    """Add strategy traces to the plot.

    Parameters:
        fig (go.Figure): The Plotly figure object.
        data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".
        depends_on (list): A list of file paths to the simulated depots for each strategy.

    """
    depot_out = {}
    indicator = -1
    for strategy in STRATEGIES:
        indicator += 1
        with open(depends_on[indicator], "rb") as file:
            depot_out[strategy] = pickle.load(file)

        fig.add_scatter(
            x=data.index,
            y=depot_out[strategy]["value_dict"][id.split(".")[0]],
            mode="lines",
            name=strategy,
            line={"width": 1.5},
            secondary_y=True,
        )


def _add_initial_depot_annotation(fig, initial_depot_cash):
    """Add initial depot value as a horizontal line with annotations to the plot.

    Parameters:
        fig (go.Figure): The Plotly figure object.
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.

    """
    fig.add_hline(secondary_y=True, y=initial_depot_cash, line_dash="dot")

    fig.add_annotation(
        xref="paper",
        yref="y2",
        x=0.885,
        y=initial_depot_cash,
        text="Initial depot value",
        ax=0,
        ay=10,
    )


def _add_asset_candlesticks(fig, data, id):
    """Add asset candlesticks to the plot.

    Parameters:
        fig (go.Figure): The Plotly figure object.
        data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".

    """
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data.Open,
            high=data.High,
            low=data.Low,
            close=data.Close,
            name=f"{id.split('.')[0].split('_')[1]} OHLC",
        ),
        secondary_y=False,
    )


def _add_figure_layout_asset_strategy(fig, id):
    """Add layout to the asset strategy figure.

    Parameters:
        fig (go.Figure): The Plotly figure object.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".

    """
    fig.update_layout(
        title_text=f"<b>{id.split('.')[0]} Asset Price and Depot Value for Different Strategies<b>",
        xaxis_rangeslider_visible=False,
    )

    fig.update_xaxes(title_text="Dates")
    fig.update_yaxes(title_text="<b>Depot value</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Asset price</b>", secondary_y=False)


def plot_units_and_cash(data, id, depends_on):
    """Plot units count and cash value for each different strategies.

    Parameters:
        data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".
        depends_on (list): A list of file paths to the simulated depots for each strategy.

    Returns:
        fig (go.Figure): The Plotly figure object containing units count and cash value.

    """
    _handle_errors_in_plot_functions(data=data, id=id, depends_on=depends_on)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    _add_unit_and_cash_traces(fig, data, id, depends_on)

    _add_figure_layout_unit_and_cash(fig, id)

    return fig


def _add_unit_and_cash_traces(fig, data, id, depends_on):
    """Add units and cash traces to the plot.

    Parameters:
        fig (go.Figure): The Plotly figure object.
        data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".
        depends_on (list): A list of file paths to the simulated depots for each strategy.

    """
    depot_out = {}
    indicator = -1
    for strategy in STRATEGIES:
        indicator += 1
        with open(depends_on[indicator], "rb") as file:
            depot_out[strategy] = pickle.load(file)

        color = px.colors.qualitative.Plotly[
            indicator % len(px.colors.qualitative.Plotly)
        ]

        # Cash trace
        fig.add_scatter(
            x=data.index,
            y=depot_out[strategy]["cash_dict"][id.split(".")[0]],
            mode="lines",
            name=f"Cash{strategy}",
            line={"width": 1, "color": color},
            secondary_y=True,
        )

        # Unit trace
        fig.add_scatter(
            x=data.index,
            y=depot_out[strategy]["unit_dict"][id.split(".")[0]],
            mode="lines",
            name=f"Unit{strategy}",
            line={"shape": "linear", "dash": "dot", "width": 1.5, "color": color},
            secondary_y=False,
        )


def _add_figure_layout_unit_and_cash(fig, id):
    """Add layout to the asset strategy figure.

    Parameters:
        fig (go.Figure): The Plotly figure object.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".

    """
    fig.update_layout(
        title_text=f"<b>Development of Units and Cash for {id.split('.')[0]}<b>",
        xaxis_rangeslider_visible=False,
    )

    fig.update_xaxes(title_text="Dates")
    fig.update_yaxes(title_text="<b>Cash value</b>", secondary_y=True)
    fig.update_yaxes(title_text="<b>Units count</b>", secondary_y=False)


def plot_indicators(data, id, initial_depot_cash, depends_on):
    """Plot indicators for different strategies and no strategy (i.e. investing all the
    cash at the beginning of the investing period).

    Parameters:
        data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.
        depends_on (list): A list of file paths to the simulated depots for each strategy.

    Returns:
        fig (go.Figure): The Plotly figure object containing annotated indicator bars of all strategies and no strategy (i.e. investing all the cash at the beginning of the investing period).

    """
    _handle_errors_in_plot_functions(
        data=data,
        id=id,
        initial_depot_cash=initial_depot_cash,
        depends_on=depends_on,
    )
    fig = go.Figure()

    start_units = math.floor(initial_depot_cash / data.Close.iloc[1])
    rest_cash = initial_depot_cash - start_units * data.Close.iloc[1]

    _add_no_strategy_indicator(fig, data, start_units, rest_cash, initial_depot_cash)

    _add_strategy_indicators(fig, id, depends_on, initial_depot_cash)

    _add_figure_layout_indicator(fig, id)

    return fig


def _add_no_strategy_indicator(fig, data, start_units, rest_cash, initial_depot_cash):
    """Add indicator for no strategy (i.e. investing all the cash at the beginning of
    the investing period).

    Parameters:
        fig (go.Figure): The Plotly figure object.
        data (pd.DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        start_units (int): The number of units purchased at the start of the investing period.
        rest_cash (float): The remaining cash after purchasing units at the beginning of the investing period.
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.

    """
    fig.add_trace(
        go.Indicator(
            mode="number+gauge+delta",
            value=start_units * data.Close.iloc[-1] + rest_cash,
            delta={"reference": initial_depot_cash},
            domain={"x": [0.15, 1], "y": _generate_intervals(len(STRATEGIES) + 1)[0]},
            title={"text": "No strategy"},
            gauge={
                "shape": "bullet",
                "axis": {
                    "range": [
                        (math.ceil(min(data.Close) * start_units + rest_cash) * 0.95),
                        (math.ceil(max(data.Close) * start_units + rest_cash) * 1.05),
                    ],
                },
                "threshold": {
                    "line": {"color": "grey", "width": 2},
                    "thickness": 0.75,
                    "value": initial_depot_cash,
                },
                "steps": [
                    {
                        "range": [
                            min(data.Close) * start_units + rest_cash,
                            initial_depot_cash,
                        ],
                        "color": "lightsalmon",
                    },
                    {
                        "range": [
                            initial_depot_cash,
                            max(data.Close) * start_units + rest_cash,
                        ],
                        "color": "lightgreen",
                    },
                ],
                "bar": {"color": "green"},
            },
        ),
    )


def _add_strategy_indicators(fig, id, depends_on, initial_depot_cash):
    """Add indicators for each strategy.

    Parameters:
        fig (go.Figure): The Plotly figure object.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".
        depends_on (list): A list of file paths to the simulated depots for each strategy.
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.

    """
    depot_out = {}
    indicator = -1
    for index, strategy in enumerate(STRATEGIES, start=1):
        indicator += 1
        with open(depends_on[indicator], "rb") as file:
            depot_out[strategy] = pickle.load(file)

        fig.add_trace(
            go.Indicator(
                mode="number+gauge+delta",
                value=depot_out[strategy]["value_dict"][id.split(".")[0]][-1],
                delta={"reference": initial_depot_cash},
                domain={
                    "x": [0.15, 1],
                    "y": _generate_intervals(len(STRATEGIES) + 1)[index],
                },
                title={"text": strategy},
                gauge={
                    "shape": "bullet",
                    "axis": {
                        "range": [
                            math.ceil(
                                min(
                                    depot_out[strategy]["value_dict"][id.split(".")[0]],
                                )
                                * 0.95,
                            ),
                            math.ceil(
                                max(
                                    depot_out[strategy]["value_dict"][id.split(".")[0]],
                                )
                                * 1.05,
                            ),
                        ],
                    },
                    "threshold": {
                        "line": {"color": "grey", "width": 2},
                        "thickness": 0.75,
                        "value": initial_depot_cash,
                    },
                    "steps": [
                        {
                            "range": [
                                min(
                                    depot_out[strategy]["value_dict"][id.split(".")[0]],
                                ),
                                initial_depot_cash,
                            ],
                            "color": "lightsalmon",
                        },
                        {
                            "range": [
                                initial_depot_cash,
                                max(
                                    depot_out[strategy]["value_dict"][id.split(".")[0]],
                                ),
                            ],
                            "color": "lightgreen",
                        },
                    ],
                    "bar": {"color": "green"},
                },
            ),
        )


def _add_figure_layout_indicator(fig, id):
    """Add layout to the indicator bar figure.

    Parameters:
        fig (go.Figure): The Plotly figure object.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".

    """
    fig.update_layout(
        title_text=f"<b>Comparison of {id.split('.')[0]} Strategy Indicator Bars and Immediately Investing Approach (No strategy)<b>",
        xaxis_rangeslider_visible=False,
    )


def _generate_intervals(num_intervals):
    """Generate intervals for positioning indicators in a vertical arrangement.

    Parameters:
        num_intervals (int): The number of intervals to generate.

    Returns:
        list: A list of intervals represented as pairs of start and end values.

    """
    total_gap = 0.09 * (num_intervals - 1)
    interval_width = (1 - total_gap) / num_intervals
    intervals = []
    start = 0
    for _i in range(num_intervals):
        end = start + interval_width
        intervals.append([start, end])
        start = end + 0.09
    return intervals


def _handle_errors_in_plot_functions(
    data=None,
    id=None,
    initial_depot_cash=None,
    depends_on=None,
):
    """Helper function to handle errors in the plot functions.

    Raises:
        ValueError: If data-related errors occur, such as empty data or missing columns.
        TypeError: If type-related errors occur, such as incorrect types for id, initial_depot_cash, or depends_on.

    """
    _handle_data_errors(data)
    _handle_id_errors(id)
    _handle_initial_depot_cash_errors(initial_depot_cash)
    _handle_depends_on_errors(depends_on)


def _handle_data_errors(data):
    """Helper function to handle errors related to input data.

    Raises:
        ValueError: If data is empty or if required columns are missing.
        TypeError: If data is not a DataFrame.

    """
    if not isinstance(data, pd.core.frame.DataFrame):
        msg = f"Data has to be of type 'pd.DataFrame' and not {type(data)}."
        raise TypeError(msg)

    if data.empty:
        msg = f"Input data is empty ({data}). Please use data_download() with valid inputs as input data."
        raise ValueError(
            msg,
        )

    columns = ["Open", "High", "Low", "Close"]
    for col in columns:
        if col not in data.columns:
            msg = f"Input data columns are ({data.columns}) and is therefore missing required column '{col}'. Please provide complete data."
            raise ValueError(
                msg,
            )


def _handle_id_errors(id):
    """Helper function to handle errors related to identifier.

    Raises:
        ValueError: If the provided id is not available in the predefined list of strategies.
        TypeError: If id is not a string.

    """
    if not isinstance(id, str):
        msg = f"The identifier 'id' must be a string and not {type(id)}."
        raise TypeError(msg)

    if id not in _ID:
        msg = f"Selected identifier '{id}' is not available. Please choose from {_ID}."
        raise ValueError(
            msg,
        )


def _handle_initial_depot_cash_errors(initial_depot_cash):
    """Helper function to handle errors related to initial deposit cash.

    Raises:
        ValueError: If initial_depot_cash is not a positive value.
        TypeError: If initial_depot_cash is not an integer or float.

    """
    if initial_depot_cash is None:
        initial_depot_cash = 100

    if not isinstance(initial_depot_cash, int | float):
        msg = f"Initial deposit cash must be an integer or float and not {type(initial_depot_cash)}."
        raise TypeError(
            msg,
        )

    if initial_depot_cash <= 0:
        msg = f"Initial deposit cash is ({initial_depot_cash}) but must be greater than zero."
        raise ValueError(
            msg,
        )


def _handle_depends_on_errors(depends_on):
    """Helper function to handle errors related to depends_on parameter.

    Raises:
        TypeError: If depends_on is not a list or if its elements are not instances of pathlib.WindowsPath.

    """
    if not isinstance(depends_on, list):
        msg = f"The 'depends_on' parameter must be a list and not {type(depends_on)}."
        raise TypeError(msg)

    for item in depends_on:
        if not isinstance(item, pathlib.WindowsPath):
            msg = f"Each element in 'depends_on' must be an instance of pathlib.WindowsPath and not {type(depends_on[item])}."
            raise TypeError(
                msg,
            )
