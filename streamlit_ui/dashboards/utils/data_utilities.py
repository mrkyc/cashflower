import streamlit as st
import pandas as pd
from typing import Callable, Any

from streamlit_ui.constants import *
from .cache_data import (
    get_df_portfolio_aggregate_performance,
    get_df_portfolio_performance,
    get_df_portfolio_group_performance,
    get_df_portfolio_asset_performance,
    get_df_portfolio_aggregate_performance_status,
    get_df_portfolio_performance_status,
    get_df_portfolio_group_performance_status,
    get_df_portfolio_asset_performance_status,
    get_df_portfolio_performance,
)


def _get_safe_name(
    df: pd.DataFrame, by_col: str, by_val: any, get_col: str, default: str
) -> str:
    """
    Safely retrieves a single value from a DataFrame column based on a condition.

    This is a helper function to avoid errors when trying to access a value that
    might not exist.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to search in.
    by_col : str
        The column to filter by.
    by_val : any
        The value to match in `by_col`.
    get_col : str
        The column from which to retrieve the value.
    default : str
        The default value to return if no match is found or `by_val` is None.

    Returns
    -------
    str
        The retrieved value or the default.
    """
    if by_val is None:
        return default
    result = df.loc[df[by_col] == by_val, get_col]
    return result.iloc[0] if not result.empty else default


def _get_safe_asset_name(
    df: pd.DataFrame, p_id: str | None, a_id: str | None, get_col: str, default: str
) -> str:
    """
    Safely retrieves an asset's value from the variants DataFrame based on portfolio and asset IDs.

    This is a specialized version of `_get_safe_name` for assets, which require a composite key.

    Parameters
    ----------
    df : pd.DataFrame
        The portfolio variants DataFrame.
    p_id : int
        The portfolio ID.
    a_id : int
        The asset ID.
    get_col : str
        The column from which to retrieve the value.
    default : str
        The default value to return if no match is found or IDs are None.

    Returns
    -------
    str
        The retrieved value or the default.
    """
    if p_id is None or a_id is None:
        return default
    result = df.loc[(df["portfolio_id"] == p_id) & (df["asset_id"] == a_id), get_col]
    return result.iloc[0] if not result.empty else default


def _load_data(
    session_id: str,
    entity_selection: dict,
    df_portfolio_variants: pd.DataFrame,
    status_date: str | None = None,
    refresh_counter: int = 0,
) -> tuple[pd.DataFrame, str]:
    """
    Loads performance or performance status data based on the selected entity.

    This is a generic data loading function that uses a mapping to call the correct
    data-fetching function from `cache_data.py` based on the aggregation level
    and whether a `status_date` is provided.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    entity_selection : dict
        A dictionary containing the user's selection (aggregation level, IDs).
    df_portfolio_variants : pd.DataFrame
        DataFrame with portfolio variants, used to retrieve entity names.
    status_date : str, optional
        If provided, fetches performance status for this date. Otherwise, fetches
        historical performance data. Defaults to None.
    refresh_counter : int, optional
        A counter to bust the cache. Defaults to 0.

    Returns
    -------
    tuple[pd.DataFrame, str]
        A tuple containing:
        - The loaded data as a DataFrame.
        - The name of the analyzed entity as a string.
    """
    level = entity_selection.get("data_aggregation_level")
    p_id = entity_selection.get("portfolio_id")
    g_id = entity_selection.get("portfolio_group_id")
    a_id = entity_selection.get("portfolio_asset_id")

    # Determine which set of functions to use (status or historical)
    if status_date:
        func_map = {
            DATA_AGGREGATION_LEVELS[0]: (
                lambda: get_df_portfolio_aggregate_performance_status(
                    session_id, status_date, refresh_counter
                ),
                "aggregated portfolios",
            ),
            DATA_AGGREGATION_LEVELS[1]: (
                lambda: (
                    get_df_portfolio_performance_status(
                        session_id, p_id, status_date, refresh_counter
                    )
                    if p_id
                    else pd.DataFrame()
                ),
                "portfolio",
            ),
            DATA_AGGREGATION_LEVELS[2]: (
                lambda: (
                    get_df_portfolio_group_performance_status(
                        session_id, g_id, status_date, refresh_counter
                    )
                    if g_id
                    else pd.DataFrame()
                ),
                _get_safe_name(
                    df_portfolio_variants,
                    "portfolio_group_id",
                    g_id,
                    "portfolio_group_name",
                    "",
                ),
            ),
            DATA_AGGREGATION_LEVELS[3]: (
                lambda: (
                    get_df_portfolio_asset_performance_status(
                        session_id, p_id, a_id, status_date, refresh_counter
                    )
                    if p_id and a_id
                    else pd.DataFrame()
                ),
                _get_safe_asset_name(
                    df_portfolio_variants, p_id, a_id, "asset_name", ""
                ),
            ),
        }
    else:
        func_map = {
            DATA_AGGREGATION_LEVELS[0]: (
                lambda: get_df_portfolio_aggregate_performance(
                    session_id, refresh_counter
                ),
                "aggregated portfolios",
            ),
            DATA_AGGREGATION_LEVELS[1]: (
                lambda: (
                    get_df_portfolio_performance(session_id, p_id, refresh_counter)
                    if p_id
                    else pd.DataFrame()
                ),
                "portfolio",
            ),
            DATA_AGGREGATION_LEVELS[2]: (
                lambda: (
                    get_df_portfolio_group_performance(
                        session_id, g_id, refresh_counter
                    )
                    if g_id
                    else pd.DataFrame()
                ),
                _get_safe_name(
                    df_portfolio_variants,
                    "portfolio_group_id",
                    g_id,
                    "portfolio_group_name",
                    "",
                ),
            ),
            DATA_AGGREGATION_LEVELS[3]: (
                lambda: (
                    get_df_portfolio_asset_performance(
                        session_id, p_id, a_id, refresh_counter
                    )
                    if p_id and a_id
                    else pd.DataFrame()
                ),
                _get_safe_asset_name(
                    df_portfolio_variants, p_id, a_id, "asset_name", ""
                ),
            ),
        }

    loader, name = func_map.get(level, (lambda: pd.DataFrame(), "unknown"))
    return loader(), name


def load_performance_data(
    session_id: str,
    entity_selection: dict,
    df_portfolio_variants: pd.DataFrame,
    refresh_counter: int = 0,
) -> tuple[pd.DataFrame, str]:
    """
    Loads historical performance data based on the selected entity.

    This is a wrapper around `_load_data` for fetching time-series performance data.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    entity_selection : dict
        A dictionary containing the user's selection (aggregation level, IDs).
    df_portfolio_variants : pd.DataFrame
        DataFrame with portfolio variants, used to retrieve entity names.
    refresh_counter : int, optional
        A counter to bust the cache. Defaults to 0.

    Returns
    -------
    tuple[pd.DataFrame, str]
        A tuple containing the loaded DataFrame and the entity name.
    """
    return _load_data(
        session_id,
        entity_selection,
        df_portfolio_variants,
        refresh_counter=refresh_counter,
    )


def load_performance_status_data(
    session_id: str,
    entity_selection: dict,
    status_date: str,
    df_portfolio_variants: pd.DataFrame,
    refresh_counter: int = 0,
) -> tuple[pd.DataFrame, str]:
    """
    Loads performance status data for a specific date based on the selected entity.

    This is a wrapper around `_load_data` for fetching point-in-time status data.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    entity_selection : dict
        A dictionary containing the user's selection (aggregation level, IDs).
    status_date : str
        The date for which to retrieve the status (format: 'YYYY-MM-DD').
    df_portfolio_variants : pd.DataFrame
        DataFrame with portfolio variants, used to retrieve entity names.
    refresh_counter : int, optional
        A counter to bust the cache. Defaults to 0.

    Returns
    -------
    tuple[pd.DataFrame, str]
        A tuple containing the loaded DataFrame and the entity name.
    """
    return _load_data(
        session_id,
        entity_selection,
        df_portfolio_variants,
        status_date=status_date,
        refresh_counter=refresh_counter,
    )


def filter_df_by_date_range(
    df: pd.DataFrame, start_date: pd.Timestamp, end_date: pd.Timestamp
) -> pd.DataFrame:
    """
    Filters a DataFrame to a given date range, assuming a descending sorted index.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to filter. Must have a DatetimeIndex sorted in descending order.
    start_date : pd.Timestamp
        The start date of the period.
    end_date : pd.Timestamp
        The end date of the period.

    Returns
    -------
    pd.DataFrame
        A view of the original DataFrame filtered to the specified date range.
    """
    # Ensure dates are in the correct order for slicing
    start, end = sorted(
        [pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()]
    )
    # Slice the DataFrame using the sorted dates. Assumes descending index.
    return df.loc[end:start]


@st.cache_data(ttl=CACHE_TTL, show_spinner=False)
def load_data_for_category(
    session_id: str,
    category: str,
    df_portfolio_variants: pd.DataFrame,
    columns_all: list[str],
    columns_reduced: list[str],
    refresh_counter: int = 0,
) -> dict[str, pd.DataFrame]:
    """
    Loads performance data for all entities within a given category and returns a dictionary.

    This function iterates through portfolios, groups, or assets based on the selected
    category and fetches their performance data.

    Parameters
    ----------
    session_id : str
        The session ID for authentication.
    category : str
        The category of entities to load (e.g., 'Portfolios', 'Portfolio groups').
    df_portfolio_variants : pd.DataFrame
        DataFrame with all portfolio variants to get entity IDs and names.
    columns_all : list
        The list of all columns to be loaded for portfolio-level data.
    columns_reduced : list
        The list of reduced columns for group and asset-level data.
    refresh_counter : int, optional
        A counter to bust the cache. Defaults to 0.

    Returns
    -------
    dict[str, pd.DataFrame]
        A dictionary where keys are entity names and values are their performance DataFrames.
    """
    dict_of_df_performances = {}

    if category == DATA_AGGREGATION_LEVELS[1]:
        for row in (
            df_portfolio_variants[["portfolio_id", "portfolio_name"]]
            .drop_duplicates()
            .itertuples()
        ):
            df_performance = get_df_portfolio_performance(
                session_id, row.portfolio_id, refresh_counter
            )[columns_all]
            dict_of_df_performances[row.portfolio_name] = df_performance

    elif category == DATA_AGGREGATION_LEVELS[2]:
        for row in (
            df_portfolio_variants[["portfolio_group_id", "portfolio_group_name"]]
            .drop_duplicates()
            .itertuples()
        ):
            df_performance = get_df_portfolio_group_performance(
                session_id, row.portfolio_group_id, refresh_counter
            )[columns_reduced]
            dict_of_df_performances[row.portfolio_group_name] = df_performance

    elif category == DATA_AGGREGATION_LEVELS[3]:
        for row in (
            df_portfolio_variants[["portfolio_id", "asset_id", "portfolio_asset_name"]]
            .drop_duplicates()
            .itertuples()
        ):
            df_performance = get_df_portfolio_asset_performance(
                session_id, row.portfolio_id, row.asset_id, refresh_counter
            )[columns_reduced]
            dict_of_df_performances[row.portfolio_asset_name] = df_performance

    return dict_of_df_performances


def load_data_or_stop(
    fetch_function: Callable[..., Any],
    *args,
    error_message: str = "Failed to load data.",
    **kwargs
) -> Any:
    """
    Fetches data using the provided function and stops the app on failure.

    This helper function simplifies data loading by wrapping the fetch call
    in a check that ensures the data is not None or empty. If the check fails,
    it displays an error message and stops the Streamlit execution.

    Args:
        fetch_function (Callable[..., Any]): The function to call to fetch the data.
        *args: Positional arguments to pass to the `fetch_function`.
        error_message (str, optional): The error message to display on failure.
            Defaults to "Failed to load data.".
        **kwargs: Keyword arguments to pass to the `fetch_function`.

    Returns:
        Any: The data returned by the `fetch_function` if it's valid.
    """
    data = fetch_function(*args, **kwargs)
    is_empty = data is None
    if hasattr(data, "empty"):
        is_empty = data.empty
    elif isinstance(data, (dict, list, str)):
        is_empty = not data

    if is_empty:
        st.error(error_message)
        st.stop()
    return data
