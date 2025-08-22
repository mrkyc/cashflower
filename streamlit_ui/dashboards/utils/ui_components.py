import streamlit as st
import pandas as pd

from streamlit_ui.constants import *
from streamlit_ui.settings.utils.settings_session_variables_management import (
    save_settings_and_load_data,
)


def refresh_data_button() -> None:
    """Displays a button in the sidebar to refresh all cached data."""
    st.button(
        ":material/autorenew: Refresh data",
        on_click=save_settings_and_load_data,
        use_container_width=True,
    )


def page_settings_header() -> None:
    """Displays the 'Page Settings' header in the sidebar."""
    st.header(":material/settings: Page Settings")


def _portfolio_selectbox(
    df_portfolio_variants: pd.DataFrame, data_aggregation_level: str
) -> str | None:
    """
    Creates a selectbox for choosing a portfolio, internal helper.

    Parameters
    ----------
    df_portfolio_variants : pd.DataFrame
        DataFrame with portfolio variants to populate the selectbox.
    data_aggregation_level : str
        The currently selected data aggregation level.

    Returns
    -------
    str | None
        The selected portfolio ID, or None if 'Aggregated portfolios' is selected.
    """
    portfolios = df_portfolio_variants[
        ["portfolio_id", "portfolio_name"]
    ].drop_duplicates()
    return st.selectbox(
        "Portfolio",
        options=(
            None
            if data_aggregation_level == DATA_AGGREGATION_LEVELS[0]
            else portfolios["portfolio_id"]
        ),
        format_func=lambda x: portfolios.loc[
            portfolios["portfolio_id"] == x, "portfolio_name"
        ].values[0],
        help="Select a specific portfolio for analysis.",
    )


def _portfolio_group_selectbox(
    df_portfolio_variants: pd.DataFrame, portfolio_id: int
) -> str | None:
    """
    Creates a selectbox for choosing a portfolio group, internal helper.

    Parameters
    ----------
    df_portfolio_variants : pd.DataFrame
        DataFrame with portfolio variants to populate the selectbox.
    portfolio_id : int
        The ID of the selected portfolio.

    Returns
    -------
    str | None
        The selected portfolio group ID, or None if no group is selected.
    """
    portfolio_groups = df_portfolio_variants[
        df_portfolio_variants["portfolio_id"] == portfolio_id
    ][["portfolio_group_id", "portfolio_group_name"]].drop_duplicates()
    return st.selectbox(
        "Model weight group",
        options=portfolio_groups["portfolio_group_id"],
        format_func=lambda x: portfolio_groups.loc[
            portfolio_groups["portfolio_group_id"] == x, "portfolio_group_name"
        ].values[0],
        help="Select a specific portfolio group.",
    )


def _portfolio_asset_selectbox(
    df_portfolio_variants: pd.DataFrame, portfolio_id: int
) -> str | None:
    """
    Creates a selectbox for choosing an asset, internal helper.

    Parameters
    ----------
    df_portfolio_variants : pd.DataFrame
        DataFrame with portfolio variants to populate the selectbox.
    portfolio_id : int
        The ID of the selected portfolio.

    Returns
    -------
    str | None
        The selected asset ID, or None if no asset is selected.
    """
    portfolio_assets = df_portfolio_variants[
        df_portfolio_variants["portfolio_id"] == portfolio_id
    ][["asset_id", "asset_name"]].drop_duplicates()
    return st.selectbox(
        "Asset",
        options=portfolio_assets["asset_id"],
        format_func=lambda x: portfolio_assets.loc[
            portfolio_assets["asset_id"] == x, "asset_name"
        ].values[0],
        help="Select a specific asset within the portfolio.",
    )


def common_sidebar_options(df_portfolio_variants: pd.DataFrame) -> dict:
    """
    Creates a set of common sidebar widgets for selecting the analysis entity.

    This function dynamically displays radio buttons and selectboxes to allow the
    user to drill down from an aggregated view to a specific portfolio, group, or asset.

    Parameters
    ----------
    df_portfolio_variants : pd.DataFrame
        DataFrame with all portfolio variants, used to populate the selectboxes.

    Returns
    -------
    dict
        A dictionary containing the selected entity information:
        - 'data_aggregation_level': The level of aggregation selected.
        - 'portfolio_id': The selected portfolio ID (or None).
        - 'portfolio_group_id': The selected group ID (or None).
        - 'portfolio_asset_id': The selected asset ID (or None).
    """
    data_aggregation_level = st.radio(
        "Data aggregation level",
        options=DATA_AGGREGATION_LEVELS,
        help="Select the level of data aggregation (e.g., aggregated portfolios, single portfolio, portfolio group, or individual asset).",
    )

    portfolio_id = _portfolio_selectbox(df_portfolio_variants, data_aggregation_level)

    portfolio_group_id = None
    if data_aggregation_level == DATA_AGGREGATION_LEVELS[2]:
        portfolio_group_id = _portfolio_group_selectbox(
            df_portfolio_variants, portfolio_id
        )

    portfolio_asset_id = None
    if data_aggregation_level == DATA_AGGREGATION_LEVELS[3]:
        portfolio_asset_id = _portfolio_asset_selectbox(
            df_portfolio_variants, portfolio_id
        )

    return {
        "data_aggregation_level": data_aggregation_level,
        "portfolio_id": portfolio_id,
        "portfolio_group_id": portfolio_group_id,
        "portfolio_asset_id": portfolio_asset_id,
    }


def portfolio_id_selectbox(df_portfolio_variants: pd.DataFrame) -> str | None:
    """
    Creates a selectbox in the sidebar for choosing a single portfolio.

    Parameters
    ----------
    df_portfolio_variants : pd.DataFrame
        DataFrame with portfolio variants to populate the selectbox.

    Returns
    -------
    str | None
        The selected portfolio ID, or None if no portfolio is selected.
    """
    portfolios = df_portfolio_variants[
        ["portfolio_id", "portfolio_name"]
    ].drop_duplicates()
    return st.selectbox(
        "Portfolio",
        options=portfolios["portfolio_id"],
        format_func=lambda x: portfolios.loc[
            portfolios["portfolio_id"] == x, "portfolio_name"
        ].values[0],
        help="Select a specific portfolio for analysis.",
    )


def total_value_checkbox() -> bool:
    """Creates a checkbox in the sidebar to toggle between total and net values."""
    return st.checkbox(
        "Show total values",
        value=True,
        help="When checked, calculations will include the sum of paid fees and taxes. Uncheck to show values without considering them.",
    )


def _set_period_to_custom():
    """Callback function to set the period selector to 'Custom'."""
    st.session_state.predefined_period_selector = "Custom"


def period_selection_widgets(df: pd.DataFrame) -> tuple[pd.Timestamp, pd.Timestamp]:
    """
    Displays period selection widgets and returns the selected start and end dates.

    This function provides a set of predefined period buttons (e.g., '1M', '1Y')
    and custom date input fields. The state is managed via `st.session_state` to
    ensure interactivity between the widgets.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame whose index is used to determine the minimum and maximum
        available dates for the selection.

    Returns
    -------
    tuple[pd.Timestamp, pd.Timestamp]
        A tuple containing the selected start and end dates.
    """
    # Determine the full available date range from the DataFrame
    min_date, max_date = df.index[-1], df.index[0]

    period_options = ["Custom"] + [
        k for k, v in PREDIFINED_PERIODS_DICT.items() if v <= len(df)
    ]
    selected_period = st.segmented_control(
        "Period",
        options=period_options,
        key="predefined_period_selector",
        help="Select a predefined period or choose 'Custom' to specify your own date range.",
    )

    # Date Range Calculation
    if selected_period == "Custom":
        # If "Custom" is selected, use dates from date_input widgets
        start_date = st.session_state.get("custom_period_start", min_date)
        end_date = st.session_state.get("custom_period_end", max_date)
    else:
        # For predefined periods, calculate the date range
        days = PREDIFINED_PERIODS_DICT.get(selected_period, 0)
        if days > 0:
            start_date = max_date - pd.Timedelta(days=days - 1)
            end_date = max_date
        else:  # "All time"
            start_date, end_date = min_date, max_date

    # Custom Period Date Inputs
    # These widgets are always visible but their values are driven by the selection
    custom_period_cols = st.columns(2)
    with custom_period_cols[0]:
        final_start_date = st.date_input(
            "Start date",
            value=start_date,
            min_value=min_date,
            max_value=max_date,
            key="custom_period_start",
            on_change=_set_period_to_custom,
        )
    with custom_period_cols[1]:
        final_end_date = st.date_input(
            "End date",
            value=end_date,
            min_value=min_date,
            max_value=max_date,
            key="custom_period_end",
            on_change=_set_period_to_custom,
        )

    return final_start_date, final_end_date
