"""Functions for indicating when to buy or sell."""

import math
import pickle

import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tradingstrattester.config import STRATEGIES

6


def plot_asset_strategy(data, id, depends_on):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add strategy traces
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
            secondary_y=False,
        )

    # Add asset candle sticks
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data.Open,
            high=data.High,
            low=data.Low,
            close=data.Close,
        ),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Double Y Axis Example",
        xaxis_rangeslider_visible=False,
    )

    # Set x-axis title
    fig.update_xaxes(title_text="xaxis title")

    # Set y-axes titles
    fig.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
    fig.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

    return fig


def plot_indicators(data, id, initial_depot_cash, depends_on):
    fig = go.Figure()

    start_units = math.floor(initial_depot_cash / data.Close[1])
    rest_cash = initial_depot_cash - start_units * data.Close[1]

    # Add indicator for no strategy
    fig.add_trace(
        go.Indicator(
            mode="number+gauge+delta",
            value=start_units * data.Close[-1] + rest_cash,
            delta={"reference": initial_depot_cash},
            domain={"x": [0.20, 1], "y": _generate_intervals(len(STRATEGIES) + 1)[0]},
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

    # Add indicators for each strategy
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
                    "x": [0.20, 1],
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

    return fig


def _generate_intervals(num_intervals):
    total_gap = 0.09 * (num_intervals - 1)
    interval_width = (1 - total_gap) / num_intervals
    intervals = []
    start = 0
    for _ in range(num_intervals):
        end = start + interval_width
        intervals.append([start, end])
        start = end + 0.09
    return intervals
