"""Functions for indicating when to buy or sell."""


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
