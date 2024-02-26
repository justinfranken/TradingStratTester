"""Functions for indicating when to buy or sell."""

import math
import pickle

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tradingstrattester.config import STRATEGIES


def plot_asset_strategy(data, id, initial_depot_cash, depends_on):
    """Plot depot value for different strategies and asset price in the form of
    candlesticks.

    Parameters:
        data (DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.
        depends_on (list): A list of file paths to the simulated depots for each strategy.

    Returns:
        fig (go.Figure): The Plotly figure object containing annotated asset price candlesticks and simulated depot values for each strategy.

    """
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
        data (DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
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
        data (DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".

    """
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data.Open,
            high=data.High,
            low=data.Low,
            close=data.Close,
            name=f"{id.split('.')[0].split('_')[1]} price",
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


def plot_indicators(data, id, initial_depot_cash, depends_on):
    """Plot indicators for different strategies and no strategy (i.e. investing all the
    cash at the beginning of the investing period).

    Parameters:
        data (DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        id (str): The identifier for the asset including the ending "[...].pkl", e.g. "60m_DB.pkl".
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.
        depends_on (list): A list of file paths to the simulated depots for each strategy.

    Returns:
        fig (go.Figure): The Plotly figure object containing annotated indicator bars of all strategies and no strategy (i.e. investing all the cash at the beginning of the investing period).

    """
    fig = go.Figure()

    start_units = math.floor(initial_depot_cash / data.Close[1])
    rest_cash = initial_depot_cash - start_units * data.Close[1]

    _add_no_strategy_indicator(fig, data, start_units, rest_cash, initial_depot_cash)

    _add_strategy_indicators(
        fig,
        data,
        id,
        depends_on,
        start_units,
        rest_cash,
        initial_depot_cash,
    )

    _add_figure_layout_indicator(fig, id)

    return fig


def _add_no_strategy_indicator(fig, data, start_units, rest_cash, initial_depot_cash):
    """Add indicator for no strategy (i.e. investing all the cash at the beginning of
    the investing period).

    Parameters:
        fig (go.Figure): The Plotly figure object.
        data (DataFrame): The DataFrame containing asset opening, high, low, and closing data from the data_download() function.
        start_units (int): The number of units purchased at the start of the investing period.
        rest_cash (float): The remaining cash after purchasing units at the beginning of the investing period.
        initial_depot_cash (float): The initial depot cash value defined in the config.py file.

    """
    fig.add_trace(
        go.Indicator(
            mode="number+gauge+delta",
            value=start_units * data.Close[-1] + rest_cash,
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
    for _ in range(num_intervals):
        end = start + interval_width
        intervals.append([start, end])
        start = end + 0.09
    return intervals
