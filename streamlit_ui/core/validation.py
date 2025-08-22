import streamlit as st
import pandas as pd


def validate_session_id(session_id: str) -> None:
    """
    Validates the session ID, stopping the app if it's not set.

    Parameters
    ----------
    session_id : str
        The session ID to validate.
    """
    if not session_id:
        st.error(
            "Session ID is not set. Please go to the entry page to set the session ID."
        )
        st.stop()


def validate_portfolio_variants(df_portfolio_variants: pd.DataFrame) -> None:
    """
    Validates the portfolio variants DataFrame, stopping the app if it's empty.

    Parameters
    ----------
    df_portfolio_variants : pd.DataFrame
        The DataFrame to validate.
    """
    if df_portfolio_variants is None or df_portfolio_variants.empty:
        st.error(
            "Portfolio variants not found. Please go to the settings page and load all necessary data properly."
        )
        st.stop()


def validate_analysis_currency(analysis_currency: str) -> None:
    """
    Validates the analysis currency, stopping the app if it's not set.

    Parameters
    ----------
    analysis_currency : str
        The analysis currency to validate.
    """
    if not analysis_currency:
        st.error(
            "Analysis currency not found. Please go to the settings page and load all necessary data properly."
        )
        st.stop()
