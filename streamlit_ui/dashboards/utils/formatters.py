import pandas as pd

from streamlit_ui.constants import *


def format_df_performance(df_performance: pd.DataFrame) -> pd.DataFrame:
    """
    Formats the performance DataFrame for display.

    Parameters
    ----------
    df_performance : pd.DataFrame
        The performance DataFrame to format.

    Returns
    -------
    pd.DataFrame
        The formatted performance DataFrame.
    """
    # Convert date column and set as index
    df_performance["date"] = pd.to_datetime(df_performance["date"])
    df_performance = df_performance.set_index("date").sort_index(ascending=False)
    df_performance.index.name = COLUMN_DATE

    # Drop unnecessary ID columns
    columns_to_drop = ["id", "portfolio_id", "portfolio_group_id", "asset_id"]
    df_performance = df_performance.drop(
        columns=[col for col in columns_to_drop if col in df_performance.columns],
        errors="ignore",
    )

    # Round numeric columns
    for col in df_performance.columns:
        if df_performance[col].dtype in ["float64", "int64"]:
            if any(k in col for k in ["pct", "percentage", "drawdown", "rate"]):
                df_performance[col] = (df_performance[col] * 100).round(2)
            elif "ratio" in col:
                df_performance[col] = df_performance[col].round(4)
            else:
                df_performance[col] = df_performance[col].round(2)

    # Define column mappings
    column_mapping = {
        "market_value": COLUMN_MARKET_VALUE,
        "cash_balance": COLUMN_CASH_BALANCE,
        "invested_amount": COLUMN_INVESTED_AMOUNT,
        "asset_disposal_income": COLUMN_ASSET_DISPOSAL_INCOME,
        "asset_holding_income": COLUMN_ASSET_HOLDING_INCOME,
        "interest_income": COLUMN_INTEREST_INCOME,
        "investment_income": COLUMN_INVESTMENT_INCOME,
        "profit": COLUMN_PROFIT,
        "profit_percentage": COLUMN_PROFIT_PERCENTAGE,
        "xirr_rate": COLUMN_XIRR_RATE,
        "drawdown_value": COLUMN_DRAWDOWN_VALUE,
        "drawdown_profit": COLUMN_DRAWDOWN_PROFIT,
        "drawdown": COLUMN_DRAWDOWN,
        "twrr_rate_daily": COLUMN_TWRR_RATE_DAILY,
        "twrr_rate_annualized": COLUMN_TWRR_RATE_ANNUALIZED,
        "sharpe_ratio_daily": COLUMN_SHARPE_RATIO_DAILY,
        "sharpe_ratio_annualized": COLUMN_SHARPE_RATIO_ANNUALIZED,
        "sortino_ratio_daily": COLUMN_SORTINO_RATIO_DAILY,
        "sortino_ratio_annualized": COLUMN_SORTINO_RATIO_ANNUALIZED,
    }

    # Add suffixes for delta and total columns
    final_mapping = {}
    for base_name, new_name in column_mapping.items():
        final_mapping[base_name] = new_name
        final_mapping[f"{base_name}_delta"] = f"{new_name} (Delta)"
        final_mapping[f"{base_name}_delta_pct"] = f"{new_name} (Delta %)"
        final_mapping[f"{base_name}_total"] = f"{new_name} Total"
        final_mapping[f"{base_name}_total_delta"] = f"{new_name} Total (Delta)"
        final_mapping[f"{base_name}_total_delta_pct"] = f"{new_name} Total (Delta %)"

    df_performance = df_performance.rename(columns=final_mapping)

    return df_performance


def get_ordinal_suffix(n: float) -> str:
    """
    Converts a number to its ordinal suffix string representation.

    Handles both integers and floats. For example, 1 becomes "1st", 2.5 becomes "2.5th".

    Parameters
    ----------
    n : float
        The number to convert.

    Returns
    -------
    str
        The number with its ordinal suffix (e.g., "1st Percentile", "2.5th Percentile").
    """
    if float(n).is_integer():
        n = int(n)
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix} Percentile"
    else:
        return f"{n}th Percentile"
