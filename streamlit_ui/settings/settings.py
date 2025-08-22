import streamlit as st

from streamlit_ui.settings.utils import *
from streamlit_ui.constants import *


# TABS LAYOUT

tabs = st.tabs(["Transactions", "Settings"])


# TRANSACTIONS TAB

with tabs[0]:
    display_transactions_tab_info()
    display_upload_transaction_files_section()
    display_add_delete_transaction_files_section()
    display_edit_transactions_section()


# SETTINGS TAB

with tabs[1]:
    display_settings_tab_info()
    display_load_settings_from_file_section()
    analysis_currency_validation = display_general_settings_section()
    df_input_transaction_files_validation = display_transaction_files_settings_section()
    df_input_portfolio_groups_validation = display_portfolio_groups_settings_section()
    df_input_portfolio_group_assets_validation = (
        display_portfolio_group_assets_settings_section()
    )


# SIDEBAR SETTINGS MANAGEMENT

with st.sidebar:
    display_sidebar_settings_management_section(
        analysis_currency_validation,
        df_input_transaction_files_validation,
        df_input_portfolio_groups_validation,
        df_input_portfolio_group_assets_validation,
    )
