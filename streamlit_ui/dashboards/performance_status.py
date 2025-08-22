import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from streamlit_ui.constants import *
from streamlit_ui.dashboards.utils import *


def create_sparkline(
    df: pd.DataFrame,
    column_name: str,
    currency: str = None,
    is_percentage: bool = False,
    rounding_places: int = 2,
) -> go.Figure:
    """
    Creates a compact sparkline chart for a given metric over time.

    The chart includes the main line, a filled area, and a dashed line for the average.
    It's designed to be displayed within a small container.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the historical data for the metric. Must have a DatetimeIndex.
    column_name : str
        The name of the column to plot.
    currency : str, optional
        The currency symbol to display in the hover tooltip. Defaults to None.
    is_percentage : bool, optional
        If True, formats the hover tooltip as a percentage. Defaults to False.
    rounding_places : int, optional
        The number of decimal places to show in the hover tooltip. Defaults to 2.

    Returns
    -------
    go.Figure
        A Plotly Figure object representing the sparkline chart.
    """
    fig = go.Figure()

    unit = ""
    if is_percentage:
        unit = "%"
    elif currency:
        unit = currency

    hover_template = (
        f"%{{y:,.{rounding_places}f}}{' ' + unit if unit else ''}<extra></extra>"
    )

    line_color = "#4682B4"
    fill_color = "rgba(70, 130, 180, 0.3)"  # A transparent version of the line color

    # Add a base trace at the minimum value for the fill
    min_val = df[column_name].min()
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=[min_val] * len(df),
            mode="lines",
            line=dict(width=0, color="rgba(0,0,0,0)"),  # Invisible line
            hoverinfo="none",
            showlegend=False,
        )
    )

    # Add the main data trace, filling down to the base trace
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[column_name],
            mode="lines",
            fill="tonexty",  # Fill to the previous trace
            fillcolor=fill_color,
            line=dict(width=2, color=line_color),
            hovertemplate=hover_template,
        )
    )

    # Add horizontal line for the average
    if not df.empty and column_name in df.columns:
        # Check if all values are the same to avoid floating point precision issues
        if df[column_name].nunique() == 1:
            mean_value = df[column_name].iloc[0]
        else:
            mean_value = df[column_name].mean()
        fig.add_hline(y=mean_value, line_dash="dash", line_color="darkgray")

    fig.update_layout(
        xaxis=dict(visible=False, showgrid=False, showticklabels=False),
        yaxis=dict(
            title=unit,
            visible=True,
            showgrid=True,
            gridcolor="gray",
            showticklabels=True,
            side="left",
            tickfont=dict(color="white"),
        ),
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=100,
        hovermode="x unified",
        hoverlabel=dict(bgcolor="black", font_color="white", font_size=12),
    )
    return fig


def display_metric_with_sparkline(
    label: str,
    value: str,
    delta: str,
    df_history: pd.DataFrame,
    column_name: str,
    currency: str = None,
    is_percentage: bool = False,
    rounding_places: int = 2,
):
    """
    Displays a Streamlit metric component along with a corresponding sparkline chart.

    This function creates a self-contained visual block for a single performance
    indicator, showing its current value, change, and a historical trend line.

    Parameters
    ----------
    label : str
        The label for the metric.
    value : str
        The main value of the metric to display.
    delta : str
        The change indicator (e.g., daily change) for the metric.
    df_history : pd.DataFrame
        A DataFrame with historical data for the sparkline.
    column_name : str
        The column in `df_history` to plot in the sparkline.
    currency : str, optional
        The currency symbol for the sparkline tooltip. Defaults to None.
    is_percentage : bool, optional
        Indicates if the metric is a percentage for formatting. Defaults to False.
    rounding_places : int, optional
        Number of decimal places for rounding in the sparkline. Defaults to 2.
    """
    with st.container(border=True):
        st.metric(label=label, value=value, delta=delta)
        if not df_history.empty and column_name in df_history.columns:
            sparkline = create_sparkline(
                df_history, column_name, currency, is_percentage, rounding_places
            )
            # Disable the modebar (toolbox)
            config = {"displayModeBar": False, "showTips": False}
            st.plotly_chart(
                sparkline,
                use_container_width=True,
                key=f"sparkline_{label}",
                config=config,
            )


(
    session_id,
    analysis_currency,
    df_portfolio_variants,
    entity_selection_dict,
    show_total_values,
) = setup_standard_dashboard()


# DATA FOR SIDEBAR

# Get available dates based on the selected entity
df_performance_history, _ = load_performance_data(
    session_id,
    entity_selection_dict,
    df_portfolio_variants,
    refresh_counter=st.session_state.get("refresh_counter", 0),
)

# Stop if no performance history data is found
if df_performance_history is None or df_performance_history.empty:
    st.error("No performance history data found for the selected entity.")
    st.stop()

available_dates = df_performance_history.index


# MAIN PAGE CONTENT

data_aggregation_level = entity_selection_dict["data_aggregation_level"]
st.header(f"Status for {data_aggregation_level}")

st.subheader(":gear: Settings")

# Date input for selecting the status date
status_date = st.date_input(
    "Status date",
    value=available_dates[0],
    min_value=available_dates[-1],
    max_value=available_dates[0],
    key="date_input",
)

# Load performance data based on the selected entity and date
df_performance_status, _ = load_data_or_stop(
    load_performance_status_data,
    session_id,
    entity_selection_dict,
    status_date,
    df_portfolio_variants,
    error_message="No performance data found for the selected entity and date.",
    refresh_counter=st.session_state.get("refresh_counter", 0),
)

df_performance_last_30d = df_performance_history.head(30)


# METRICS CONFIGURATION


def get_metric_config(show_total_values: bool) -> dict:
    """
    Returns a configuration dictionary for all metrics to be displayed.

    Parameters
    ----------
    show_total_values : bool
        Flag to determine whether to use total or net column names.

    Returns
    -------
    dict
        A dictionary containing the configuration for each metric section.
    """

    # Helper to get the correct column name
    def get_col(base_name):
        return get_column_name(base_name, show_total_values)

    return {
        "Value": {
            "icon": ":moneybag:",
            "cols": 2,
            "metrics": [
                {
                    "label": COLUMN_MARKET_VALUE,
                    "value_suffix": f" {analysis_currency}",
                },
                {
                    "label": COLUMN_CASH_BALANCE,
                    "value_suffix": f" {analysis_currency}",
                    "level": DATA_AGGREGATION_LEVELS[:2],
                },
            ],
        },
        "Investment Return": {
            "icon": ":trophy:",
            "cols": 2,
            "metrics": [
                {
                    "label": get_col(COLUMN_PROFIT),
                    "value_suffix": f" {analysis_currency}",
                    "full_width": True,
                },
                {
                    "label": get_col(COLUMN_PROFIT_PERCENTAGE),
                    "is_percentage": True,
                },
                {
                    "label": get_col(COLUMN_XIRR_RATE),
                    "is_percentage": True,
                },
                {
                    "label": COLUMN_TWRR_RATE_DAILY,
                    "is_percentage": True,
                },
                {
                    "label": COLUMN_TWRR_RATE_ANNUALIZED,
                    "is_percentage": True,
                },
            ],
        },
        "Drawdown": {
            "icon": ":chart_with_downwards_trend:",
            "cols": 2,
            "metrics": [
                {
                    "label": COLUMN_DRAWDOWN,
                    "is_percentage": True,
                    "full_width": True,
                },
                {
                    "label": get_col(COLUMN_DRAWDOWN_VALUE),
                    "is_percentage": True,
                },
                {
                    "label": get_col(COLUMN_DRAWDOWN_PROFIT),
                    "is_percentage": True,
                },
            ],
        },
        "Risk-Reward Ratios": {
            "icon": ":scales:",
            "cols": 2,
            "metrics": [
                {"label": COLUMN_SHARPE_RATIO_DAILY, "rounding": 4},
                {"label": COLUMN_SHARPE_RATIO_ANNUALIZED, "rounding": 4},
                {"label": COLUMN_SORTINO_RATIO_DAILY, "rounding": 4},
                {"label": COLUMN_SORTINO_RATIO_ANNUALIZED, "rounding": 4},
            ],
        },
        "Cash Flow Overview": {
            "icon": ":money_with_wings:",
            "cols": 2,
            "metrics": [
                {
                    "label": get_col(COLUMN_INVESTED_AMOUNT),
                    "value_suffix": f" {analysis_currency}",
                    "full_width": True,
                    "divider": True,
                },
                {
                    "label": get_col(COLUMN_INVESTMENT_INCOME),
                    "value_suffix": f" {analysis_currency}",
                },
                {
                    "label": get_col(COLUMN_ASSET_HOLDING_INCOME),
                    "value_suffix": f" {analysis_currency}",
                },
                {
                    "label": get_col(COLUMN_ASSET_DISPOSAL_INCOME),
                    "value_suffix": f" {analysis_currency}",
                },
                {
                    "label": get_col(COLUMN_INTEREST_INCOME),
                    "value_suffix": f" {analysis_currency}",
                    "level": DATA_AGGREGATION_LEVELS[:2],
                },
            ],
        },
    }


# DISPLAYING PERFORMANCE METRICS

metric_config = get_metric_config(show_total_values)

for section_title, config in metric_config.items():
    # Check if the section should be displayed based on the aggregation level
    if "level" in config and data_aggregation_level not in config["level"]:
        continue

    with st.container(border=True):
        st.subheader(f"{config['icon']} {section_title}")

        # Create columns for the metrics
        columns = st.columns(config["cols"])
        col_idx = 0

        for metric in config["metrics"]:
            # Check if the metric should be displayed
            if "level" in metric and data_aggregation_level not in metric["level"]:
                continue

            label = metric["label"]
            base_name = label.split(" (")[0].replace(" Total", "")

            # Prepare parameters for display_metric_with_sparkline
            is_percentage = metric.get("is_percentage", False)
            value_suffix = "%" if is_percentage else metric.get("value_suffix", "")
            delta_suffix = " pp" if is_percentage else ""

            value = df_performance_status[label].values[0]
            delta_pct = df_performance_status[f"{label} (Delta %)"].values[0]
            delta_abs = df_performance_status[f"{label} (Delta)"].values[0]

            if metric.get("full_width"):
                # If full_width, call the display function directly
                display_metric_with_sparkline(
                    label=label.replace(" [%]", ""),
                    value=f"{value}{value_suffix}",
                    delta=f"{delta_pct} % | {delta_abs}{delta_suffix}",
                    df_history=df_performance_last_30d,
                    column_name=label,
                    currency=analysis_currency if not is_percentage else None,
                    is_percentage=is_percentage,
                    rounding_places=metric.get("rounding", 2),
                )

                if metric.get("divider"):
                    st.divider()

                columns = st.columns(config["cols"])
                col_idx = 0  # Reset column index after a full-width metric
            else:
                # Otherwise, use the column context
                target_col = columns[col_idx % config["cols"]]
                with target_col:
                    display_metric_with_sparkline(
                        label=label.replace(" [%]", ""),
                        value=f"{value}{value_suffix}",
                        delta=f"{delta_pct} % | {delta_abs}{delta_suffix}",
                        df_history=df_performance_last_30d,
                        column_name=label,
                        currency=analysis_currency if not is_percentage else None,
                        is_percentage=is_percentage,
                        rounding_places=metric.get("rounding", 2),
                    )
                col_idx += 1
