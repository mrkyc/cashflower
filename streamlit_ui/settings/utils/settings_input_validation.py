import streamlit as st
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile


def _validate_dataframe(
    df: pd.DataFrame,
    table_name: str,
    columns_to_check: list[str] | None = None,
) -> tuple[bool, str]:
    """
    Generic function to perform common validation checks on a DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to validate.
    table_name : str
        The name of the table for use in error messages.
    columns_to_check : list[str] | None, optional
        A list of columns to check for NA values and empty strings.
        If None, all columns are checked. Defaults to None.

    Returns
    -------
    tuple[bool, str]
        A tuple containing a boolean indicating success and an error message string.
    """
    if df.empty:
        return False, f"The table '{table_name}' is empty."

    check_df = df[columns_to_check] if columns_to_check else df

    if check_df.isnull().any().any():
        return (
            False,
            f"The table '{table_name}' contains NA values in required columns.",
        )
    if (check_df.astype(str) == "").any().any():
        return (
            False,
            f"The table '{table_name}' contains empty strings in required columns.",
        )

    return True, ""


def validate_upload_files(uploaded_files: list[UploadedFile]) -> bool:
    """
    Validates uploaded files.

    Checks if a list of uploaded files is not empty and if all file names
    (excluding extensions) are unique.
    """
    if not uploaded_files:
        return False

    uploaded_file_names = [file.name.split(".")[0] for file in uploaded_files]
    if len(uploaded_file_names) != len(set(uploaded_file_names)):
        st.error("Please provide transaction files with unique names.")
        return False
    return True


def validate_analysis_currency(analysis_currency: str) -> bool:
    """
    Validates the analysis currency format (must be 3 characters).
    """
    if len(analysis_currency) != 3:
        st.error("Currency name must have 3 characters.")
        return False
    return True


def validate_df_input(df_input: pd.DataFrame) -> bool:
    """
    Validates a generic DataFrame input using the common validation function.
    """
    is_valid, error_message = _validate_dataframe(df_input, "input")
    if not is_valid:
        st.error(error_message)
    return is_valid


def validate_df_input_portfolio_groups(df_input_portfolio_groups: pd.DataFrame) -> bool:
    """
    Validates the portfolio groups DataFrame.
    """
    is_valid, error_message = _validate_dataframe(
        df_input_portfolio_groups,
        "portfolio groups",
        ["portfolio_name", "group_name", "group_weight"],
    )
    if not is_valid:
        st.error(error_message)
        return False

    if (
        df_input_portfolio_groups.groupby("portfolio_name")["group_weight"].sum() != 100
    ).any():
        st.error(
            "The sum of the group weights must be equal to 100 for each portfolio."
        )
        return False

    return True


def validate_df_input_portfolio_group_assets(
    df_input_portfolio_group_assets: pd.DataFrame,
    df_input_portfolio_groups: pd.DataFrame,
) -> bool:
    """
    Validates the portfolio group assets DataFrame.
    """
    is_valid, error_message = _validate_dataframe(
        df_input_portfolio_group_assets, "portfolio group assets"
    )
    if not is_valid:
        st.error(error_message)
        return False

    # Check for consistency between group assets and group definitions
    defined_groups = set(
        df_input_portfolio_groups[["portfolio_name", "group_name"]].itertuples(
            index=False, name=None
        )
    )
    assigned_groups = set(
        df_input_portfolio_group_assets[["portfolio_name", "group_name"]].itertuples(
            index=False, name=None
        )
    )

    if not assigned_groups.issubset(defined_groups):
        st.error(
            "Group names must be related to the portfolio names as defined in the table about portfolio groups."
        )
        return False

    return True
