import plotly.express as px
import streamlit as st
import pandas as pd

from streamlit_ui.constants import *
from streamlit_ui.dashboards.utils import *


(
    session_id,
    analysis_currency,
    df_portfolio_variants,
    entity_selection_dict,
    show_total_values,
) = setup_standard_dashboard()


# COLUMN NAME DEFINITIONS

# Get column lists depending on whether to show aggregated values
columns_all = get_columns_list(show_total_values)
columns_reduced = get_columns_list(show_total_values, reduced=True)


# PERFORMANCE DATA LOADING

# Load performance data based on the selected aggregation level
df_performance, analysis_entity = load_data_or_stop(
    load_performance_data,
    session_id,
    entity_selection_dict,
    df_portfolio_variants,
    error_message="No performance data found for the selected entity and date.",
    refresh_counter=st.session_state.get("refresh_counter", 0),
)


# MAIN PAGE CONTENT

st.header(f"Performance Overview: {analysis_entity}")

# General Chart Settings
st.subheader(":gear: Settings")

# Select the performance metric for analysis
data_aggregation_level = entity_selection_dict.get("data_aggregation_level")
performance_metric_options = (
    columns_all
    if data_aggregation_level in DATA_AGGREGATION_LEVELS[:2]
    else columns_reduced
)
performance_metric = st.selectbox(
    "Performance metric",
    options=performance_metric_options,
    index=performance_metric_options.index(COLUMN_MARKET_VALUE),
    help="Select the performance metric for detailed analysis.",
)

if performance_metric is None:
    performance_metric = performance_metric_options[0]

# Check if the metric is a percentage value
is_metric_percentage = performance_metric in performance_metric_options[-3:]

# Prepare data (remove missing values)
df_performance = df_performance[performance_metric].dropna()

if df_performance.empty:
    st.warning("No data to display.")
    st.stop()

# Component for selecting the data period
start_date, end_date = period_selection_widgets(df_performance.to_frame())
df_performance = filter_df_by_date_range(
    df_performance.to_frame(), start_date, end_date
)[performance_metric]

# Stop if no data is available for the selected period
if df_performance.empty:
    st.warning("No data available for the selected period.")
    st.stop()

# Determine the start and end dates
first_date = df_performance.index[-1].strftime("%Y-%m-%d")
last_date = df_performance.index[0].strftime("%Y-%m-%d")


# Data Over Time Chart
st.subheader(":chart_with_upwards_trend: Data Over Time")

smoothing_window = st.number_input(
    "Smoothing window (days)",
    min_value=1,
    value=1,
    step=1,
    help="Number of days to use for smoothing the data (rolling average).",
)
smoothed_df_performance = (
    df_performance.rolling(window=int(smoothing_window)).mean().dropna()
)

# Switch between chart and table view
show_chart_or_table_options = ["Chart", "Table"]
show_chart_or_table = st.segmented_control(
    "Show chart or table",
    show_chart_or_table_options,
    default=show_chart_or_table_options[0],
    key="data_in_time_chart_or_table",
    help="""Select whether to display the data in a chart or table format.""",
)

st.caption(
    f"Data from {first_date} to {last_date} | Currency {analysis_currency} | {performance_metric}"
)

if show_chart_or_table == show_chart_or_table_options[1]:
    # Display data in a table
    st.dataframe(smoothed_df_performance, use_container_width=True)
else:
    # Display data as a line chart
    fig = create_performance_chart(smoothed_df_performance, performance_metric)
    st.plotly_chart(fig, use_container_width=True, config={"showTips": False})


# Statistics
st.subheader(":abacus: Statistics")
st.caption(
    f"Data from {first_date} to {last_date} | Currency {analysis_currency} | {performance_metric}"
)

# Display basic descriptive statistics
cols = st.columns(3)
df_describe = df_performance.describe()
df_describe = (
    df_describe.round(4)
    if "ratio" in performance_metric.lower()
    else df_describe.round(2)
)

with cols[0]:
    st.metric("Count", f"{df_describe['count']:.0f}")
    st.metric("Max", f"{df_describe['max']}")

with cols[1]:
    st.metric("Average", f"{df_describe['mean']}")
    st.metric("Median", f"{df_describe['50%']}")

with cols[2]:
    st.metric("Standard Deviation", f"{df_describe['std']}")
    st.metric("Min", f"{df_describe['min']}")

# Violin plot to visualize data distribution
fig = px.violin(
    df_performance, y=performance_metric, box=True, points="all", height=550
)
fig.update_traces(hovertemplate=f"{performance_metric}: %{{y}}<extra></extra>")
st.plotly_chart(fig, config={"showTips": False})


# Periodic Performance
st.subheader(":bar_chart: Periodic Performance")

st.subheader(":gear: Aggregation Settings")

# Time aggregation and summary method settings
cols = st.columns(2)
with cols[0]:
    time_aggregation = st.selectbox(
        "Time aggregation",
        options=["Yearly", "Quarterly", "Monthly", "Weekly", "Daily"],
        help="""Select the time aggregation for the performance data.""",
    )
with cols[1]:
    summary_method = st.selectbox(
        "Summary method",
        options=["Last", "Average", "Median", "Maximum", "Minimum"],
        help="""Select the method to summarize the performance data over the selected time periods.""",
    )

# Map user selection to Pandas frequency codes and aggregation functions
freq_map = {
    "Yearly": "YE",
    "Quarterly": "QE",
    "Monthly": "ME",
    "Weekly": "W",
    "Daily": "D",
}
agg_map = {
    "Last": "last",
    "Average": "mean",
    "Median": "median",
    "Maximum": "max",
    "Minimum": "min",
}

# Data processing: resampling, calculating differences
df_performance.index = pd.to_datetime(df_performance.index)
summary_values = df_performance.resample(freq_map[time_aggregation]).agg(
    agg_map[summary_method]
)
absolute_diff = summary_values.diff()
absolute_diff = (
    absolute_diff.round(4)
    if "ratio" in performance_metric.lower()
    else absolute_diff.round(2)
)

percent_change = (summary_values.pct_change() * 100).round(2)

# Prepare a DataFrame for visualization
difference_column = "Absolute Change"
difference_percentage_column = "Relative Change"
df_values = pd.DataFrame(
    {
        performance_metric: summary_values,
        difference_column: absolute_diff,
        difference_percentage_column: percent_change,
    },
    index=summary_values.index,
).dropna()

# Switch between chart and table for periodic data
show_chart_or_table = st.segmented_control(
    "Show chart or table",
    show_chart_or_table_options,
    default=show_chart_or_table_options[0],
    key="performance_in_time_chart_or_table",
    help="""Select whether to display the data in a chart or table format.""",
)

st.caption(
    f"Data from {first_date} to {last_date} | Currency {analysis_currency} | {performance_metric}"
)

if show_chart_or_table == show_chart_or_table_options[1]:
    # Display data in a table
    difference_columns = (
        difference_column
        if is_metric_percentage
        else [difference_column, difference_percentage_column]
    )
    st.dataframe(df_values[difference_columns], use_container_width=True)
else:
    st.subheader(
        "Inter-Period Performance",
        help="Shows the performance metric changes between selected time periods, highlighting absolute or relative differences (compared to the previous period).",
    )

    # Display data in charts
    show_difference_percentage = st.toggle(
        "Show Relative Change",
        disabled=is_metric_percentage,
        help="Toggle to show the relative change.",
    )
    y_column = (
        difference_percentage_column
        if show_difference_percentage
        else difference_column
    )
    if y_column == "Relative Change":
        y_label = f"Relative Change of {performance_metric}"
    else:
        y_label = f"Absolute Change of {performance_metric}"

    # Color bars based on value (positive/negative)
    df_values["color"] = df_values[y_column].apply(
        lambda x: "red" if x < 0 else "green"
    )

    # Create period labels for the x-axis and sort
    df_values = df_values.sort_index().reset_index()
    period_code = freq_map[time_aggregation][0]
    df_values["period"] = df_values[COLUMN_DATE].dt.to_period(period_code).astype(str)
    period_order = df_values["period"].tolist()

    # Bar chart showing differences between periods
    fig = (
        px.bar(
            df_values,
            x="period",
            y=y_column,
            color="color",
            color_discrete_map={"red": "red", "green": "green"},
            labels={y_column: y_label, "period": time_aggregation},
            text=y_column,
            category_orders={"period": period_order},
        )
        .update_layout(showlegend=False)
        .update_xaxes(type="category")
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>" + f"{y_label}: %{{y}}<extra></extra>"
    )
    st.plotly_chart(fig, use_container_width=True, config={"showTips": False})

    # Prepare data for the violin plot
    df_period = df_performance.reset_index().copy()
    df_period = df_period.sort_values(by=COLUMN_DATE)

    # Create period labels, ensuring uniqueness and order
    df_period["period"] = df_period[COLUMN_DATE].dt.to_period(period_code).astype(str)
    period_order = df_period["period"].unique().tolist()

    st.subheader(
        "Distribution of Values by Period",
        help="Shows the distribution of performance metric values within each selected time period using a violin plot, highlighting density and quartiles.",
    )

    st.caption(
        f"Data from {first_date} to {last_date} | Currency {analysis_currency} | {performance_metric}"
    )

    # Violin plot showing the distribution of values in each period
    fig = px.violin(
        df_period,
        x="period",
        y=performance_metric,
        box=True,
        labels={"period": time_aggregation},
        category_orders={"period": period_order},
    ).update_xaxes(type="category")
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>" + f"{performance_metric}: %{{y}}<extra></extra>"
    )
    st.plotly_chart(fig, config={"showTips": False})
