import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


def create_performance_chart(df: pd.DataFrame, performance_metric: str) -> go.Figure:
    """
    Creates a performance chart (line or area) based on the metric name.

    If the metric is a drawdown, it creates a filled area chart. Otherwise,
    it creates a line chart.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the performance data, with a DatetimeIndex.
    performance_metric : str
        The name of the column in the DataFrame to plot.

    Returns
    -------
    plotly.graph_objects.Figure
        The Plotly figure object for the chart.
    """
    if "drawdown" in performance_metric.lower():
        fig = px.area(
            df,
            labels={"value": performance_metric},
        )
    else:
        fig = px.line(
            df,
            labels={"value": performance_metric},
        )

    fig.update_layout(showlegend=False, hovermode="x unified")
    fig.update_traces(
        hovertemplate="<b>%{x|%d %b %Y}</b><br>"
        + f"{performance_metric}: %{{y}}<extra></extra>"
    )
    return fig
