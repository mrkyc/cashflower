import streamlit as st
import pandas as pd

from streamlit_ui.dashboards.utils.cache_data import get_df_portfolio_variants
from streamlit_ui.core.validation import (
    validate_session_id,
    validate_portfolio_variants,
    validate_analysis_currency,
)
from streamlit_ui.dashboards.utils.ui_components import (
    refresh_data_button,
    page_settings_header,
    common_sidebar_options,
    total_value_checkbox,
)


def setup_standard_dashboard() -> tuple:
    """
    Performs the standard initialization and sidebar setup for common dashboards.

    Returns
    -------
    tuple
        A tuple containing:
        - session_id (str): The ID of the current user session.
        - analysis_currency (str): The analysis currency (e.g., "USD", "EUR").
        - df_portfolio_variants (pd.DataFrame): DataFrame with portfolio variants data.
        - entity_selection_dict (dict): A dictionary with the selections made in the sidebar.
        - show_total_values (bool): A boolean indicating whether to show total values.
    """
    session_id, analysis_currency, df_portfolio_variants = initialize_dashboard()

    with st.sidebar:
        setup_common_sidebar_elements()
        entity_selection_dict = common_sidebar_options(df_portfolio_variants)
        show_total_values = total_value_checkbox()

    return (
        session_id,
        analysis_currency,
        df_portfolio_variants,
        entity_selection_dict,
        show_total_values,
    )


def initialize_dashboard() -> tuple[str, str, pd.DataFrame]:
    """
    Initializes the dashboard by getting and validating session data.

    Returns
    -------
    tuple[str, str, pd.DataFrame]
        A tuple containing:
        - session_id (str): The ID of the current user session.
        - analysis_currency (str): The analysis currency (e.g., "USD", "EUR").
        - df_portfolio_variants (pd.DataFrame): DataFrame with portfolio variants data.
    """
    session_id = st.session_state.get("session_id")
    validate_session_id(session_id)

    analysis_currency = st.session_state.get("analysis_currency")
    validate_analysis_currency(analysis_currency)
    analysis_currency = analysis_currency.upper()

    df_portfolio_variants = get_df_portfolio_variants(
        session_id, refresh_counter=st.session_state.get("refresh_counter")
    )
    validate_portfolio_variants(df_portfolio_variants)

    return session_id, analysis_currency, df_portfolio_variants


def setup_common_sidebar_elements() -> None:
    """
    Sets up the common elements in the sidebar for all dashboards.
    This includes the refresh data button and the page settings header.
    """
    refresh_data_button()
    page_settings_header()
