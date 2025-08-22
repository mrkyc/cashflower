import streamlit as st

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
df_performance, _ = load_data_or_stop(
    load_performance_data,
    session_id,
    entity_selection_dict,
    df_portfolio_variants,
    error_message="No performance data found for the selected entity and date.",
    refresh_counter=st.session_state.get("refresh_counter", 0),
)


# MAIN PAGE CONTENT

st.header("All Data Table")

# Determine which columns to display based on the selected aggregation level
data_aggregation_level = entity_selection_dict.get("data_aggregation_level")
use_reduced_columns = data_aggregation_level not in DATA_AGGREGATION_LEVELS[:2]
columns_to_display = get_columns_list(show_total_values, reduced=use_reduced_columns)
df_performance_to_display = df_performance[columns_to_display]

# Component for selecting the data period
start_date, end_date = period_selection_widgets(df_performance_to_display)
df_performance_to_display = filter_df_by_date_range(
    df_performance_to_display, start_date, end_date
)

# Stop if no data is available for the selected period
if df_performance_to_display.empty:
    st.warning("No data available for the selected period.")
    st.stop()

# Display the data table with a caption
st.caption(
    f"Displaying data from {df_performance_to_display.index[-1].strftime('%Y-%m-%d')} to {df_performance_to_display.index[0].strftime('%Y-%m-%d')} in {analysis_currency} currency."
)
st.dataframe(df_performance_to_display, use_container_width=True)
