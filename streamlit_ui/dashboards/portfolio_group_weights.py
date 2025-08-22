import plotly.express as px
import streamlit as st

from streamlit_ui.constants import *
from streamlit_ui.dashboards.utils import *


# INITIALIZATION AND DATA LOADING

session_id, _, df_portfolio_variants = initialize_dashboard()


# SIDEBAR SETTINGS

with st.sidebar:
    # Common sidebar elements
    setup_common_sidebar_elements()

    # Selectbox to choose the portfolio for analysis
    portfolio_id = portfolio_id_selectbox(df_portfolio_variants)
    portfolio_name = (
        df_portfolio_variants.loc[
            df_portfolio_variants["portfolio_id"] == portfolio_id, "portfolio_name"
        ].iloc[0]
        if not df_portfolio_variants.empty
        else "Unknown Portfolio"
    )


# DATA LOADING

# Load portfolio group weights
df_portfolio_group_weights = get_df_portfolio_group_weights(
    session_id=session_id,
    portfolio_id=portfolio_id,
    refresh_counter=st.session_state.get("refresh_counter", 0),
)
if df_portfolio_group_weights.empty:
    st.error("No portfolio group weights found for the selected portfolio.")
    st.stop()

# Load portfolio assets status
df_portfolio_assets = get_df_portfolio_assets_status(
    session_id=session_id,
    portfolio_id=portfolio_id,
    refresh_counter=st.session_state.get("refresh_counter", 0),
)
if df_portfolio_assets.empty:
    st.error("No portfolio assets found for the selected portfolio.")
    st.stop()

# Load portfolio groups
df_portfolio_groups = load_data_or_stop(
    get_df_portfolio_groups,
    session_id=session_id,
    portfolio_id=portfolio_id,
    error_message="No portfolio groups found for the selected portfolio.",
    refresh_counter=st.session_state.get("refresh_counter", 0),
)


# MAIN PAGE CONTENT

# Portfolio Group Weights

with st.container(border=True):
    st.header(f"Portfolio group weights for {portfolio_name}")
    col1, col2 = st.columns([1, 1], gap="large")

    # Model Weights Pie Chart
    with col1:
        st.subheader(
            ":scales: Model Weights",
            help="""The 'Model Weights' pie chart displays the share of each portfolio group in the model portfolio.  
                    The model portfolio is the defined target portfolio with the desired weights for each portfolio group.""",
        )
        fig_model_weights = px.pie(
            df_portfolio_groups,
            values=COLUMN_MODEL_WEIGHT,
            names=COLUMN_PORTFOLIO_GROUP_NAME,
        )
        fig_model_weights.update_layout(showlegend=False)
        fig_model_weights.update_traces(
            sort=False,
            textinfo="percent+label",
            textfont_size=12,
            textposition="inside",
            pull=[0.05] * len(df_portfolio_groups),
            hovertemplate="<b>%{label}</b><br>Weight: %{percent}",
        )
        st.plotly_chart(
            fig_model_weights, use_container_width=True, config={"showTips": False}
        )

    # Current Weights Pie Chart
    with col2:
        st.subheader(
            ":weight_lifter: Current Weights",
            help="""The 'Current Weights' pie chart displays the share of each portfolio group in the real portfolio.  
                    The real portfolio is the actual portfolio with the current weights for each portfolio group.""",
        )
        df_current_weights = df_portfolio_group_weights.loc[
            df_portfolio_group_weights.index[0]
        ].sort_values(
            by=[COLUMN_MODEL_WEIGHT, COLUMN_PORTFOLIO_GROUP_NAME],
            ascending=[False, True],
        )
        fig_current_weights = px.pie(
            df_current_weights,
            values=COLUMN_WEIGHT,
            names=COLUMN_PORTFOLIO_GROUP_NAME,
        )
        fig_current_weights.update_layout(showlegend=False)
        fig_current_weights.update_traces(
            sort=False,
            textinfo="percent+label",
            textfont_size=12,
            textposition="inside",
            pull=[0.05] * len(df_current_weights),
            hovertemplate="<b>%{label}</b><br>Weight: %{percent}",
        )
        st.plotly_chart(
            fig_current_weights, use_container_width=True, config={"showTips": False}
        )

# Weights Balancing

with st.container(border=True):
    st.header(f"Weights balancing for {portfolio_name}")

    # Units Adjustment
    st.subheader(
        ":straight_ruler: Units Adjustment",
        help="""Enter the units in the 'Units Change' column to adjust the portfolio weights.  
                It can be positive or negative depending on the direction of the adjustment (potentially buy or sell).""",
    )
    df_portfolio_assets.insert(5, "Units Change", 0.0)
    df_portfolio_assets = st.data_editor(
        df_portfolio_assets,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Units Change": st.column_config.NumberColumn(required=True, default=0.0)
        },
        disabled=[1, 2, 3, 4, 5],
    )

    # Adjustment Value
    st.subheader(
        ":abacus: Adjustment Value",
        help="""The 'Change Value' column shows the value change in the portfolio assets based on the 'Units Change' column.  
                It is calculated as the product of the 'Unit Price' and 'Units Change' columns.""",
    )
    df_portfolio_assets["Change Value"] = (
        df_portfolio_assets[COLUMN_UNIT_PRICE] * df_portfolio_assets["Units Change"]
    ).round(2)
    df_portfolio_assets_grouped = (
        df_portfolio_assets.groupby("Portfolio Group Name", sort=False)["Change Value"]
        .sum()
        .reset_index()
    )
    df_portfolio_assets_grouped.loc[len(df_portfolio_assets_grouped)] = [
        COLUMN_GRAND_TOTAL,
        df_portfolio_assets_grouped["Change Value"].sum(),
    ]
    st.dataframe(df_portfolio_assets_grouped, use_container_width=True, hide_index=True)

    # Adjusted Weights Deviation
    st.subheader(
        ":ocean: Adjusted Weights Deviation",
        help="""The 'Weight Deviation' column shows the difference between the weights after the adjustment and the model weights.  
                It is calculated as the difference between the 'Adjusted Weight' and 'Model Weight' columns.""",
    )
    df_portfolio_assets["Adjusted Value"] = (
        df_portfolio_assets[COLUMN_MARKET_VALUE] + df_portfolio_assets["Change Value"]
    )
    df_portfolio_assets_grouped_by_value = (
        df_portfolio_assets.groupby("Portfolio Group Name")["Adjusted Value"]
        .sum()
        .reset_index()
    )
    total_adjusted_value = df_portfolio_assets_grouped_by_value["Adjusted Value"].sum()
    df_portfolio_assets_grouped_by_value[COLUMN_WEIGHT] = (
        df_portfolio_assets_grouped_by_value["Adjusted Value"]
        / total_adjusted_value
        * 100
    ).round(2)
    df_portfolio_assets = df_portfolio_assets_grouped_by_value.merge(
        df_portfolio_groups, on=COLUMN_PORTFOLIO_GROUP_NAME
    )
    df_portfolio_assets[COLUMN_WEIGHT_DEVIATION] = (
        df_portfolio_assets[COLUMN_WEIGHT] - df_portfolio_assets[COLUMN_MODEL_WEIGHT]
    ).round(2)
    df_portfolio_assets = df_portfolio_assets.sort_values(
        by=[COLUMN_WEIGHT_DEVIATION, COLUMN_PORTFOLIO_GROUP_NAME], ascending=True
    )

    # Chart or Table view for Adjusted Weights Deviation
    show_chart_or_table_options = ["Chart", "Table"]
    show_chart_or_table = st.segmented_control(
        "Show chart or table",
        show_chart_or_table_options,
        default=show_chart_or_table_options[0],
        key="rebalanced_weights_chart_or_table",
        help="""Select whether to display the data in a chart or table format.""",
    )
    if show_chart_or_table == show_chart_or_table_options[1]:
        st.dataframe(df_portfolio_assets, use_container_width=True, hide_index=True)
    else:
        fig = px.bar(
            df_portfolio_assets,
            x=COLUMN_WEIGHT_DEVIATION,
            y=COLUMN_PORTFOLIO_GROUP_NAME,
            color=COLUMN_WEIGHT_DEVIATION,
            color_continuous_scale="RdYlGn_r",
            orientation="h",
            labels={COLUMN_WEIGHT_DEVIATION: "Weight Deviation [% pts]"},
            text=COLUMN_WEIGHT_DEVIATION,
            category_orders={
                COLUMN_PORTFOLIO_GROUP_NAME: df_portfolio_assets[
                    COLUMN_PORTFOLIO_GROUP_NAME
                ].tolist()
            },
        )
        fig.update_traces(
            hovertemplate="<b>%{y}</b><br>Weight Deviation: %{x:.2f}%<extra></extra>"
        )
        st.plotly_chart(fig, use_container_width=True, config={"showTips": False})

# Weights in Time

with st.container(border=True):
    st.header(f"Weights over time for {portfolio_name}")
    st.subheader(":gear: Settings")

    # Multiselect for portfolio groups
    groups_in_order = df_portfolio_groups[COLUMN_PORTFOLIO_GROUP_NAME]
    analysis_entities = st.multiselect(
        "Portfolio groups",
        options=groups_in_order,
        default=groups_in_order,
        help="""Select the portfolio groups to display the weights data in time.  
                You can select multiple groups to compare the weights in time.  
                By default, all groups are selected.""",
    )
    analysis_entities = [
        group for group in groups_in_order.tolist() if group in analysis_entities
    ]

    # Segmented control for weight metric
    weight_metric_options = [COLUMN_GROUP_WEIGHTS, COLUMN_GROUP_WEIGHT_DEVIATIONS]
    weight_metric = st.segmented_control(
        "Weight metric",
        weight_metric_options,
        default=weight_metric_options[0],
        key="weight_metric",
        help="""Select the weight metric to display.  
                The 'Group Weights' option displays the group weights in time.  
                The 'Group Weight Deviations' option displays the group weight deviations in time
                (as a difference in percentage points from the model weights).""",
    )

    # Prepare data for the chart
    df_weights_in_time = df_portfolio_group_weights[
        df_portfolio_group_weights[COLUMN_PORTFOLIO_GROUP_NAME].isin(analysis_entities)
    ]
    df_weights_in_time = df_weights_in_time.reset_index(names=COLUMN_DATE)

    if weight_metric == weight_metric_options[1]:
        weight_metric_column = COLUMN_WEIGHT_DEVIATION
        y_label = COLUMN_WEIGHT_DEVIATION + " [%]"
    else:
        weight_metric_column = COLUMN_WEIGHT
        y_label = COLUMN_WEIGHT + " [%]"

    df_weights_in_time = df_weights_in_time.pivot(
        index=COLUMN_DATE,
        columns=COLUMN_PORTFOLIO_GROUP_NAME,
        values=weight_metric_column,
    ).sort_index(ascending=False)[analysis_entities]

    # Period input for the chart
    start_date, end_date = period_selection_widgets(df_weights_in_time)
    df_weights_in_time = filter_df_by_date_range(
        df_weights_in_time, start_date, end_date
    )

    # Stop if no data is available for the selected period
    if df_weights_in_time.empty:
        st.warning("No data available for the selected period.")
        st.stop()

    if weight_metric == weight_metric_options[1]:
        st.subheader(":wavy_dash: Weight Deviations Over Time")
    else:
        st.subheader(":wavy_dash: Weights Over Time")

    # Chart or Table view for Weights in Time
    show_chart_or_table_options = ["Chart", "Table"]
    show_chart_or_table = st.segmented_control(
        "Show chart or table",
        show_chart_or_table_options,
        default=show_chart_or_table_options[0],
        key="data_in_time_chart_or_table",
        help="""Select whether to display the data in a chart or table format.""",
    )

    first_date = df_weights_in_time.index[-1].strftime("%Y-%m-%d")
    last_date = df_weights_in_time.index[0].strftime("%Y-%m-%d")
    st.caption(f"Data from {first_date} to {last_date} | {weight_metric}")

    if show_chart_or_table == show_chart_or_table_options[1]:
        st.dataframe(df_weights_in_time, use_container_width=True)
    else:
        fig = px.line(
            df_weights_in_time,
            labels={"value": y_label},
        )
        fig.update_layout(hovermode="x unified")
        fig.update_traces(
            hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:.2f}%<extra></extra>"
        )
        st.plotly_chart(fig, use_container_width=True, config={"showTips": False})
