from streamlit_ui.constants import *


def get_column_name(base_name: str, total_values: bool) -> str:
    """
    Gets the appropriate column name based on whether to show total values.

    Parameters
    ----------
    base_name : str
        The base name of the column.
    total_values : bool
        Flag to determine if the total version of the column name is needed.

    Returns
    -------
    str
        The full column name.
    """
    if total_values:
        if "(" in base_name and base_name.endswith(")"):
            # Insert 'Total' before the last parenthesis
            parts = base_name.rsplit("(", 1)
            return f"{parts[0]}Total ({parts[1]}"
        else:
            return f"{base_name} Total"
    return base_name


def get_columns_list(show_total_values: bool, reduced: bool = False) -> list[str]:
    """
    Determines the list of columns to display based on user selections.

    Parameters
    ----------
    show_total_values : bool
        Flag to include total values.
    reduced : bool, optional
        Flag to exclude certain columns for a reduced view, by default False.

    Returns
    -------
    list
        A list of column names for display.
    """

    column_definitions = [
        {"name": COLUMN_MARKET_VALUE, "in_reduced": True, "supports_total": False},
        {"name": COLUMN_PROFIT, "in_reduced": True, "supports_total": True},
        {"name": COLUMN_PROFIT_PERCENTAGE, "in_reduced": True, "supports_total": True},
        {"name": COLUMN_XIRR_RATE, "in_reduced": True, "supports_total": True},
        {"name": COLUMN_DRAWDOWN_VALUE, "in_reduced": True, "supports_total": True},
        {"name": COLUMN_DRAWDOWN_PROFIT, "in_reduced": True, "supports_total": True},
        {"name": COLUMN_DRAWDOWN, "in_reduced": True, "supports_total": False},
        {"name": COLUMN_TWRR_RATE_DAILY, "in_reduced": True, "supports_total": False},
        {
            "name": COLUMN_TWRR_RATE_ANNUALIZED,
            "in_reduced": True,
            "supports_total": False,
        },
        {
            "name": COLUMN_SHARPE_RATIO_DAILY,
            "in_reduced": True,
            "supports_total": False,
        },
        {
            "name": COLUMN_SHARPE_RATIO_ANNUALIZED,
            "in_reduced": True,
            "supports_total": False,
        },
        {
            "name": COLUMN_SORTINO_RATIO_DAILY,
            "in_reduced": True,
            "supports_total": False,
        },
        {
            "name": COLUMN_SORTINO_RATIO_ANNUALIZED,
            "in_reduced": True,
            "supports_total": False,
        },
        {"name": COLUMN_CASH_BALANCE, "in_reduced": False, "supports_total": False},
        {"name": COLUMN_INVESTED_AMOUNT, "in_reduced": True, "supports_total": True},
        {
            "name": COLUMN_ASSET_DISPOSAL_INCOME,
            "in_reduced": True,
            "supports_total": True,
        },
        {
            "name": COLUMN_ASSET_HOLDING_INCOME,
            "in_reduced": True,
            "supports_total": True,
        },
        {"name": COLUMN_INTEREST_INCOME, "in_reduced": False, "supports_total": True},
        {"name": COLUMN_INVESTMENT_INCOME, "in_reduced": True, "supports_total": True},
    ]

    # Filter columns based on the 'reduced' flag
    if reduced:
        base_columns = [c for c in column_definitions if c["in_reduced"]]
    else:
        base_columns = column_definitions

    # Apply total values transformation if needed
    if show_total_values:
        transformed_columns = []
        for col_def in base_columns:
            if col_def["supports_total"]:
                transformed_columns.append(get_column_name(col_def["name"], True))
            else:
                transformed_columns.append(col_def["name"])
        return transformed_columns
    else:
        return [c["name"] for c in base_columns]
