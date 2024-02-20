"""Functions for indicating when to buy or sell."""

import math

import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_asset_strategy(depot_out, df):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_scatter(
        x=df.index,
        y=depot_out,
        mode="lines",
        secondary_y=False,
    )

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df.Open,
            high=df.High,
            low=df.Low,
            close=df.Close,
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


def plot_indicators(strategy_dict, data, asset, initial_depot_cash, STRATEGIES):
    fig = go.Figure()

    start_units = math.floor(initial_depot_cash / data[f"{asset}.pkl"].Close[1])
    rest_cash = initial_depot_cash - start_units * data[f"{asset}.pkl"].Close[1]

    # Indicator bar indicating no strategy at all
    fig.add_trace(
        go.Indicator(
            mode="number+gauge+delta",
            value=start_units * data[f"{asset}.pkl"].Close[-1] + rest_cash,
            delta={"reference": initial_depot_cash},
            domain={"x": [0.20, 1], "y": _generate_intervals(len(STRATEGIES) + 1)[0]},
            title={"text": "No strategy"},
            gauge={
                "shape": "bullet",
                "axis": {
                    "range": [
                        (
                            math.ceil(
                                min(data[f"{asset}.pkl"].Close) * start_units
                                + rest_cash,
                            )
                            * 0.95
                        ),
                        (
                            math.ceil(
                                max(data[f"{asset}.pkl"].Close) * start_units
                                + rest_cash,
                            )
                            * 1.05
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
                            min(data[f"{asset}.pkl"].Close) * start_units + rest_cash,
                            initial_depot_cash,
                        ],
                        "color": "lightsalmon",
                    },
                    {
                        "range": [
                            initial_depot_cash,
                            max(data[f"{asset}.pkl"].Close) * start_units + rest_cash,
                        ],
                        "color": "lightgreen",
                    },
                ],
                "bar": {"color": "green"},
            },
        ),
    )

    # Indicator bars for each strategy for one asset at one frequency
    for index, strategies in enumerate(STRATEGIES, start=1):
        fig.add_trace(
            go.Indicator(
                mode="number+gauge+delta",
                value=strategy_dict[strategies]["value_dict"][asset][-1],
                delta={"reference": initial_depot_cash},
                domain={
                    "x": [0.20, 1],
                    "y": _generate_intervals(len(STRATEGIES) + 1)[index],
                },
                title={"text": strategies},
                gauge={
                    "shape": "bullet",
                    "axis": {
                        "range": [
                            math.ceil(
                                min(strategy_dict[strategies]["value_dict"][asset])
                                * 0.95,
                            ),
                            math.ceil(
                                max(strategy_dict[strategies]["value_dict"][asset])
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
                                min(strategy_dict[strategies]["value_dict"][asset]),
                                initial_depot_cash,
                            ],
                            "color": "lightsalmon",
                        },
                        {
                            "range": [
                                initial_depot_cash,
                                max(strategy_dict[strategies]["value_dict"][asset]),
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
