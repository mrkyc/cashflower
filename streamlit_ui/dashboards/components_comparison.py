import plotly.express as px
import streamlit as st
import pandas as pd

from streamlit_ui.constants import *
from streamlit_ui.dashboards.utils import *


# INITIALIZATION AND DATA LOADING

session_id, analysis_currency, df_portfolio_variants = initialize_dashboard()

# Create combined names for portfolio groups and assets for easier display
df_portfolio_variants["portfolio_group_name"] = df_portfolio_variants.apply(
    lambda row: f'{row["portfolio_name"]} - {row["portfolio_group_name"]}', axis=1
)
df_portfolio_variants["portfolio_asset_name"] = df_portfolio_variants.apply(
    lambda row: f'{row["portfolio_name"]} - {row["asset_name"]}', axis=1
)


# SIDEBAR SETTINGS

with st.sidebar:
    setup_common_sidebar_elements()

    data_aggregation_level = st.radio(
        "Data aggregation level",
        DATA_AGGREGATION_LEVELS[1:],
        index=0,
        help="Select the level of data aggregation (e.g., portfolios, groups, or assets).",
    )
    show_total_values = total_value_checkbox()


# COLUMN NAME DEFINITIONS

# Get column lists depending on whether to show aggregated values
columns_all = get_columns_list(show_total_values)
columns_reduced = get_columns_list(show_total_values, reduced=True)


# PERFORMANCE DATA LOADING

# Load data for the selected category
dict_of_df_performances = load_data_or_stop(
    load_data_for_category,
    session_id,
    data_aggregation_level,
    df_portfolio_variants,
    columns_all,
    columns_reduced,
    error_message=f"No performance data found for the selected category. Please check your data sources.",
    refresh_counter=st.session_state.get("refresh_counter", 0),
)

# Additional check for empty entities within the dictionary
empty_entities = [name for name, df in dict_of_df_performances.items() if df.empty]
if empty_entities:
    st.error(
        f"No performance data found for the following entities: {', '.join(empty_entities)}. Please check your data sources."
    )
    st.stop()


# MAIN PAGE CONTENT

# Set the header and relevant columns based on the selected category
header_map = {
    DATA_AGGREGATION_LEVELS[1]: "Portfolio comparison",
    DATA_AGGREGATION_LEVELS[2]: "Portfolio group comparison",
    DATA_AGGREGATION_LEVELS[3]: "Portfolio asset comparison",
}
st.header(header_map.get(data_aggregation_level, "Component Comparison"))

if data_aggregation_level == DATA_AGGREGATION_LEVELS[1]:
    relevant_columns = columns_all
else:
    relevant_columns = columns_reduced


# General Chart Settings

st.subheader(":gear: Settings")

# Multiselect to choose which entities to compare
comparison_entities = st.multiselect(
    "Comparison entities",
    dict_of_df_performances.keys(),
    default=list(dict_of_df_performances.keys()),
    help="Choose the specific entities to include in the comparison.",
)
# Selectbox to choose the performance metric
performance_metric = st.selectbox(
    "Performance metric",
    options=relevant_columns,
    help="Select the performance metric to compare across entities.",
)

# Stop if no entities are selected
if not comparison_entities:
    st.warning("Please select at least one comparison entity.")
    st.stop()

# Combine the performance data of selected entities into a single DataFrame
df_performances = pd.concat(
    (
        dict_of_df_performances[entity][performance_metric].rename(entity)
        for entity in comparison_entities
    ),
    axis=1,
)

# Drop rows where all values are missing
df_performances = df_performances.dropna(how="all")

# Stop if there's no data to display for any of the selected entities
if df_performances.empty or df_performances.isna().all().any():
    st.warning(
        "No data to display. Please check if the selected entities have data for the chosen metric."
    )
    st.stop()

# Ensure the DataFrame is sorted by date in descending order for period selection
df_performances = df_performances.sort_index(ascending=False)

# Component for selecting the data period
start_date, end_date = period_selection_widgets(df_performances)
df_performances = filter_df_by_date_range(df_performances, start_date, end_date)

# Stop if no data is available for the selected period
if df_performances.empty:
    st.warning("No data available for the selected period.")
    st.stop()

# Determine the start and end dates
first_date = df_performances.index[-1].strftime("%Y-%m-%d")
last_date = df_performances.index[0].strftime("%Y-%m-%d")


# Data Over Time Chart

# Switch between chart and table view
show_chart_or_table_options = ["Chart", "Table"]
show_chart_or_table = st.segmented_control(
    "Show chart or table",
    show_chart_or_table_options,
    default=show_chart_or_table_options[0],
    key="data_in_time_chart_or_table",
    help="""Select whether to display the data in a chart or table format.""",
)

if show_chart_or_table == show_chart_or_table_options[1]:
    # Display data in a table
    if len(df_performances.columns) > 1 and performance_metric in columns_all[:5]:
        df_performances.insert(0, COLUMN_GRAND_TOTAL, df_performances.sum(axis=1))

    st.caption(
        f"Data from {first_date} to {last_date} | Currency {analysis_currency} | {performance_metric}"
    )

    st.dataframe(df_performances, use_container_width=True)
else:
    # Display data as a line chart with enhanced customization
    y_label = (
        f"{performance_metric} ({analysis_currency.upper()})"
        if performance_metric in columns_all[:5]
        else f"{performance_metric} ([%])"
    )
    title_text = f"Comparison of {performance_metric} from {first_date} to {last_date}"

    fig = px.line(
        df_performances,
        labels={
            "index": "Date",
            "value": y_label,
            "variable": "Entity",
        },
        title=title_text,
    )
    fig.update_layout(
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title=y_label,
    )
    fig.update_traces(hovertemplate="%{y}<extra></extra>")
    st.plotly_chart(fig, use_container_width=True, config={"showTips": False})
