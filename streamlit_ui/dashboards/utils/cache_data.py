import requests
import pandas as pd
import streamlit as st

from streamlit_ui.constants import *
from .formatters import format_df_performance


def fetch_data(
    endpoint: str, session_id: str, params: dict | None = None
) -> pd.DataFrame:
    """
    Fetches data from a specified API endpoint and returns a DataFrame.

    This function sends a GET request to the given endpoint with the session ID in the headers.
    It's cached using Streamlit's caching mechanism to avoid redundant API calls.

    Parameters
    ----------
    endpoint : str
        The API endpoint to fetch data from (e.g., "portfolio-variants").
    session_id : str
        The session ID for authentication.
    params : dict, optional
        A dictionary of query parameters to include in the request, by default None.

    Returns
    -------
    pd.DataFrame
        A DataFrame containing the fetched data. Returns an empty DataFrame if the
        request fails or returns a non-OK status code.
    """
    response = requests.get(
        f"{URL}/{endpoint}",
        headers={HEADER_SESSION_ID: session_id},
        params=params,
    )
    return pd.DataFrame(response.json()) if response.ok else pd.DataFrame()


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_variants(session_id: str, refresh_counter: int) -> pd.DataFrame:
    """
    Retrieves portfolio variants data, which includes details about all available
    portfolios, their groups, and assets.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A DataFrame with portfolio variants data.
    """
    return fetch_data("portfolio-variants", session_id)


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_aggregate_performance(
    session_id: str, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats the historical performance data for all portfolios aggregated.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with aggregated performance data, indexed by date.
    """
    df = fetch_data("portfolio-aggregate-performance", session_id)
    return format_df_performance(df) if not df.empty else df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_performance(
    session_id: str, portfolio_id: int, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats historical performance data for a specific portfolio.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_id : int
        The unique identifier for the portfolio.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with performance data for the specified portfolio.
    """
    df = fetch_data(f"portfolio-performance/{portfolio_id}", session_id)
    return format_df_performance(df) if not df.empty else df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_group_performance(
    session_id: str, portfolio_group_id: int, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats historical performance data for a specific portfolio group.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_group_id : int
        The unique identifier for the portfolio group.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with performance data for the specified portfolio group.
    """
    df = fetch_data(f"portfolio-group-performance/{portfolio_group_id}", session_id)
    return format_df_performance(df) if not df.empty else df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_asset_performance(
    session_id: str, portfolio_id: int, asset_id: int, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats historical performance data for a specific asset within a portfolio.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_id : int
        The unique identifier for the portfolio containing the asset.
    asset_id : int
        The unique identifier for the asset.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with performance data for the specified asset.
    """
    df = fetch_data(
        f"portfolio-asset-performance/{portfolio_id}/{asset_id}",
        session_id,
    )
    return format_df_performance(df) if not df.empty else df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_aggregate_performance_status(
    session_id: str, status_date: str, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats the aggregated performance status for all portfolios on a specific date.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    status_date : str
        The date for which to retrieve the status (format: 'YYYY-MM-DD').
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with the aggregated performance status.
    """
    df = fetch_data(
        "portfolio-aggregate-performance-status",
        session_id,
        params={"status_date": status_date},
    )
    return format_df_performance(df) if not df.empty else df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_performance_status(
    session_id: str, portfolio_id: int, status_date: str, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats the performance status for a specific portfolio on a given date.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_id : int
        The unique identifier for the portfolio.
    status_date : str
        The date for which to retrieve the status (format: 'YYYY-MM-DD').
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with the performance status for the specified portfolio.
    """
    df = fetch_data(
        f"portfolio-performance-status/{portfolio_id}",
        session_id,
        params={"status_date": status_date},
    )
    return format_df_performance(df) if not df.empty else df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_group_performance_status(
    session_id: str, portfolio_group_id: int, status_date: str, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats performance status for a specific portfolio group on a given date.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_group_id : int
        The unique identifier for the portfolio group.
    status_date : str
        The date for which to retrieve the status (format: 'YYYY-MM-DD').
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with the performance status for the specified group.
    """
    df = fetch_data(
        f"portfolio-group-performance-status/{portfolio_group_id}",
        session_id,
        params={"status_date": status_date},
    )
    return format_df_performance(df) if not df.empty else df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_asset_performance_status(
    session_id: str,
    portfolio_id: int,
    asset_id: int,
    status_date: str,
    refresh_counter: int,
) -> pd.DataFrame:
    """
    Retrieves and formats performance status for a specific asset in a portfolio on a given date.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_id : int
        The unique identifier for the portfolio containing the asset.
    asset_id : int
        The unique identifier for the asset.
    status_date : str
        The date for which to retrieve the status (format: 'YYYY-MM-DD').
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with the performance status for the specified asset.
    """
    df = fetch_data(
        f"portfolio-asset-performance-status/{portfolio_id}/{asset_id}",
        session_id,
        params={"status_date": status_date},
    )
    return format_df_performance(df) if not df.empty else df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_group_weights(
    session_id: str, portfolio_id: int, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats historical portfolio group weights for a given portfolio.

    The formatting includes:
    - Converting 'date' to datetime and setting it as a sorted index.
    - Rounding weight-related columns.
    - Renaming columns to user-friendly names.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_id : int
        The unique identifier for the portfolio.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with portfolio group weights over time.
    """
    df = fetch_data(f"portfolio-group-weights/{portfolio_id}", session_id)
    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"]).dt.date
    df = df.set_index("date").sort_index(ascending=False)
    df.index.name = COLUMN_DATE
    df[["weight", "weight_deviation"]] = df[["weight", "weight_deviation"]].round(2)
    df = df.rename(
        columns={
            "portfolio_group_name": COLUMN_PORTFOLIO_GROUP_NAME,
            "model_weight": COLUMN_MODEL_WEIGHT,
            "weight": COLUMN_WEIGHT,
            "weight_deviation": COLUMN_WEIGHT_DEVIATION,
        }
    )
    return df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_assets_status(
    session_id: str, portfolio_id: int, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats the current status of all assets for a given portfolio.

    The formatting includes:
    - Sorting assets by model weight, group name, and asset name.
    - Rounding numeric columns.
    - Renaming columns to user-friendly names.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_id : int
        The unique identifier for the portfolio.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with the status of portfolio assets.
    """
    df = fetch_data(f"portfolio-assets-status/{portfolio_id}", session_id)
    if df.empty:
        return df

    df = df.sort_values(
        by=["model_weight", "portfolio_group_name", "asset_name"],
        ascending=[False, True, True],
    ).drop(columns="model_weight")
    df[["unit_price", "quantity", "market_value"]] = df[
        ["unit_price", "quantity", "market_value"]
    ].round(2)
    df = df.rename(
        columns={
            "portfolio_group_name": COLUMN_PORTFOLIO_GROUP_NAME,
            "asset_name": COLUMN_ASSET_NAME,
            "unit_price": COLUMN_UNIT_PRICE,
            "quantity": COLUMN_QUANTITY,
            "market_value": COLUMN_MARKET_VALUE,
        }
    )
    return df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_portfolio_groups(
    session_id: str, portfolio_id: int, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats the portfolio groups for a given portfolio.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_id : int
        The unique identifier for the portfolio.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with portfolio group details.
    """
    df = fetch_data(f"portfolio-groups/{portfolio_id}", session_id)
    if df.empty:
        return df

    df = df.sort_values(by=["weight", "name"], ascending=[False, True])
    df = df.rename(
        columns={
            "name": COLUMN_PORTFOLIO_GROUP_NAME,
            "weight": COLUMN_MODEL_WEIGHT,
        }
    )
    return df


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_pct_changes_stats(
    session_id: str, portfolio_id: int, refresh_counter: int
) -> dict:
    """
    Retrieves statistical data on percentage changes for a model portfolio,
    used for Monte Carlo simulations.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_id : int
        The unique identifier for the portfolio.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    dict
        A dictionary containing statistics like 'pct_change_avg' (mean) and
        'pct_change_std' (standard deviation). Returns an empty dict on failure.
    """
    response = requests.get(
        f"{URL}/model-portfolio-stats/{portfolio_id}",
        headers={HEADER_SESSION_ID: session_id},
    )
    return response.json() if response.ok else {}


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def get_df_market_values(
    session_id: str, portfolio_id: int, refresh_counter: int
) -> pd.DataFrame:
    """
    Retrieves and formats historical market values for a given portfolio.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    portfolio_id : int
        The unique identifier for the portfolio.
    refresh_counter : int
        Used to load refreshed data into the cache.

    Returns
    -------
    pd.DataFrame
        A formatted DataFrame with historical market values, sorted chronologically.
    """
    df = fetch_data(f"portfolio-market-values/{portfolio_id}", session_id)
    return format_df_performance(df).sort_index(ascending=True) if not df.empty else df
