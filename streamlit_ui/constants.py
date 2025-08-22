"""
This module defines constants used throughout the Streamlit UI.

It includes API configuration, settings options, and column names for data display.
"""

import os

# API Configuration
URL = os.getenv("API_URL", "http://127.0.0.1:8000")
HEADER_SESSION_ID = "x-session-id"  # Header for session ID authentication

CACHE_TTL = 60 * 10  # 10 minutes in seconds

###################################################################
# SETTINGS CONSTANTS
###################################################################

# Options for Open, High, Low, Close (OHLC) data processing
OHLC_OPTIONS = [
    "open",
    "high",
    "low",
    "close",
    "average",
    "typical price",
    "weighted close price",
]

# Levels for data aggregation in dashboards
DATA_AGGREGATION_LEVELS = [
    "Aggregated portfolios",
    "Portfolio as a whole",
    "Model weight groups",
    "Assets",
]


###################################################################
# DASHBOARDS CONSTANTS
###################################################################

# Column names for performance metrics
COLUMN_MARKET_VALUE = "Market Value"
COLUMN_MARKET_VALUE_DELTA = "Market Value (Delta)"
COLUMN_MARKET_VALUE_DELTA_PCT = "Market Value (Delta %)"

COLUMN_CASH_BALANCE = "Cash Balance"
COLUMN_CASH_BALANCE_DELTA = "Cash Balance (Delta)"
COLUMN_CASH_BALANCE_DELTA_PCT = "Cash Balance (Delta %)"

COLUMN_INVESTED_AMOUNT = "Invested Amount"
COLUMN_INVESTED_AMOUNT_DELTA = "Invested Amount (Delta)"
COLUMN_INVESTED_AMOUNT_DELTA_PCT = "Invested Amount (Delta %)"

COLUMN_INVESTED_AMOUNT_TOTAL = "Invested Amount Total"
COLUMN_INVESTED_AMOUNT_TOTAL_DELTA = "Invested Amount Total (Delta)"
COLUMN_INVESTED_AMOUNT_TOTAL_DELTA_PCT = "Invested Amount Total (Delta %)"

COLUMN_ASSET_DISPOSAL_INCOME = "Asset Disposal Income"
COLUMN_ASSET_DISPOSAL_INCOME_DELTA = "Asset Disposal Income (Delta)"
COLUMN_ASSET_DISPOSAL_INCOME_DELTA_PCT = "Asset Disposal Income (Delta %)"

COLUMN_ASSET_DISPOSAL_INCOME_TOTAL = "Asset Disposal Income Total"
COLUMN_ASSET_DISPOSAL_INCOME_TOTAL_DELTA = "Asset Disposal Income Total (Delta)"
COLUMN_ASSET_DISPOSAL_INCOME_TOTAL_DELTA_PCT = "Asset Disposal Income Total (Delta %)"

COLUMN_ASSET_HOLDING_INCOME = "Asset Holding Income"
COLUMN_ASSET_HOLDING_INCOME_DELTA = "Asset Holding Income (Delta)"
COLUMN_ASSET_HOLDING_INCOME_DELTA_PCT = "Asset Holding Income (Delta %)"

COLUMN_ASSET_HOLDING_INCOME_TOTAL = "Asset Holding Income Total"
COLUMN_ASSET_HOLDING_INCOME_TOTAL_DELTA = "Asset Holding Income Total (Delta)"
COLUMN_ASSET_HOLDING_INCOME_TOTAL_DELTA_PCT = "Asset Holding Income Total (Delta %)"

COLUMN_INTEREST_INCOME = "Interest Income"
COLUMN_INTEREST_INCOME_DELTA = "Interest Income (Delta)"
COLUMN_INTEREST_INCOME_DELTA_PCT = "Interest Income (Delta %)"

COLUMN_INTEREST_INCOME_TOTAL = "Interest Income Total"
COLUMN_INTEREST_INCOME_TOTAL_DELTA = "Interest Income Total (Delta)"
COLUMN_INTEREST_INCOME_TOTAL_DELTA_PCT = "Interest Income Total (Delta %)"

COLUMN_INVESTMENT_INCOME = "Investment Income"
COLUMN_INVESTMENT_INCOME_DELTA = "Investment Income (Delta)"
COLUMN_INVESTMENT_INCOME_DELTA_PCT = "Investment Income (Delta %)"

COLUMN_INVESTMENT_INCOME_TOTAL = "Investment Income Total"
COLUMN_INVESTMENT_INCOME_TOTAL_DELTA = "Investment Income Total (Delta)"
COLUMN_INVESTMENT_INCOME_TOTAL_DELTA_PCT = "Investment Income Total (Delta %)"

COLUMN_PROFIT = "Profit"
COLUMN_PROFIT_DELTA = "Profit (Delta)"
COLUMN_PROFIT_DELTA_PCT = "Profit (Delta %)"

COLUMN_PROFIT_TOTAL = "Profit Total"
COLUMN_PROFIT_TOTAL_DELTA = "Profit Total (Delta)"
COLUMN_PROFIT_TOTAL_DELTA_PCT = "Profit Total (Delta %)"

COLUMN_PROFIT_PERCENTAGE = "Profit Percentage"
COLUMN_PROFIT_PERCENTAGE_DELTA = "Profit Percentage (Delta)"
COLUMN_PROFIT_PERCENTAGE_DELTA_PCT = "Profit Percentage (Delta %)"

COLUMN_PROFIT_PERCENTAGE_TOTAL = "Profit Percentage Total"
COLUMN_PROFIT_PERCENTAGE_TOTAL_DELTA = "Profit Percentage Total (Delta)"
COLUMN_PROFIT_PERCENTAGE_TOTAL_DELTA_PCT = "Profit Percentage Total (Delta %)"

COLUMN_XIRR_RATE = "XIRR Rate"
COLUMN_XIRR_RATE_DELTA = "XIRR Rate (Delta)"
COLUMN_XIRR_RATE_DELTA_PCT = "XIRR Rate (Delta %)"

COLUMN_XIRR_RATE_TOTAL = "XIRR Rate Total"
COLUMN_XIRR_RATE_TOTAL_DELTA = "XIRR Rate Total (Delta)"
COLUMN_XIRR_RATE_TOTAL_DELTA_PCT = "XIRR Rate Total (Delta %)"

COLUMN_DRAWDOWN_VALUE = "Drawdown Value"
COLUMN_DRAWDOWN_VALUE_DELTA = "Drawdown Value (Delta)"
COLUMN_DRAWDOWN_VALUE_DELTA_PCT = "Drawdown Value (Delta %)"

COLUMN_DRAWDOWN_VALUE_TOTAL = "Drawdown Value Total"
COLUMN_DRAWDOWN_VALUE_TOTAL_DELTA = "Drawdown Value Total (Delta)"
COLUMN_DRAWDOWN_VALUE_TOTAL_DELTA_PCT = "Drawdown Value Total (Delta %)"

COLUMN_DRAWDOWN_PROFIT = "Drawdown Profit"
COLUMN_DRAWDOWN_PROFIT_DELTA = "Drawdown Profit (Delta)"
COLUMN_DRAWDOWN_PROFIT_DELTA_PCT = "Drawdown Profit (Delta %)"

COLUMN_DRAWDOWN_PROFIT_TOTAL = "Drawdown Profit Total"
COLUMN_DRAWDOWN_PROFIT_TOTAL_DELTA = "Drawdown Profit Total (Delta)"
COLUMN_DRAWDOWN_PROFIT_TOTAL_DELTA_PCT = "Drawdown Profit Total (Delta %)"

COLUMN_DRAWDOWN = "Drawdown"
COLUMN_DRAWDOWN_DELTA = "Drawdown (Delta)"
COLUMN_DRAWDOWN_DELTA_PCT = "Drawdown (Delta %)"

COLUMN_TWRR_RATE_DAILY = "TWRR Rate Daily"
COLUMN_TWRR_RATE_DAILY_DELTA = "TWRR Rate Daily (Delta)"
COLUMN_TWRR_RATE_DAILY_DELTA_PCT = "TWRR Rate Daily (Delta %)"

COLUMN_TWRR_RATE_ANNUALIZED = "TWRR Rate Annualized"
COLUMN_TWRR_RATE_ANNUALIZED_DELTA = "TWRR Rate Annualized (Delta)"
COLUMN_TWRR_RATE_ANNUALIZED_DELTA_PCT = "TWRR Rate Annualized (Delta %)"

COLUMN_SHARPE_RATIO_DAILY = "Sharpe Ratio Daily"
COLUMN_SHARPE_RATIO_DAILY_DELTA = "Sharpe Ratio Daily (Delta)"
COLUMN_SHARPE_RATIO_DAILY_DELTA_PCT = "Sharpe Ratio Daily (Delta %)"

COLUMN_SHARPE_RATIO_ANNUALIZED = "Sharpe Ratio Annualized"
COLUMN_SHARPE_RATIO_ANNUALIZED_DELTA = "Sharpe Ratio Annualized (Delta)"
COLUMN_SHARPE_RATIO_ANNUALIZED_DELTA_PCT = "Sharpe Ratio Annualized (Delta %)"

COLUMN_SORTINO_RATIO_DAILY = "Sortino Ratio Daily"
COLUMN_SORTINO_RATIO_DAILY_DELTA = "Sortino Ratio Daily (Delta)"
COLUMN_SORTINO_RATIO_DAILY_DELTA_PCT = "Sortino Ratio Daily (Delta %)"

COLUMN_SORTINO_RATIO_ANNUALIZED = "Sortino Ratio Annualized"
COLUMN_SORTINO_RATIO_ANNUALIZED_DELTA = "Sortino Ratio Annualized (Delta)"
COLUMN_SORTINO_RATIO_ANNUALIZED_DELTA_PCT = "Sortino Ratio Annualized (Delta %)"

# Other general column names
COLUMN_GRAND_TOTAL = "Grand Total"
COLUMN_UNIT_PRICE = "Unit Price"
COLUMN_QUANTITY = "Quantity"
COLUMN_WEIGHT = "Weight"
COLUMN_MODEL_WEIGHT = "Model Weight"
COLUMN_GROUP_WEIGHTS = "Group Weights"
COLUMN_GROUP_WEIGHT_DEVIATIONS = "Group Weight Deviations"
COLUMN_WEIGHT_DEVIATION = "Weight Deviation"
COLUMN_PORTFOLIO_GROUP_NAME = "Portfolio Group Name"
COLUMN_ASSET_NAME = "Asset Name"
COLUMN_DATE = "Date"
COLUMN_MEAN = "Mean"
COLUMN_MEDIAN = "Median"


###################################################################
# TIME PERIOD CONSTANTS
###################################################################

# Number of days for standard time periods
W1 = 7
M1 = 30
M3 = 91
M6 = 182
Y1 = 365
Y2 = 730
Y3 = 1095
Y5 = 1826
Y10 = 3652
Y15 = 5479
Y20 = 7305

# Dictionary mapping predefined period labels to days
PREDIFINED_PERIODS_DICT = {
    "1W": W1,
    "1M": M1,
    "3M": M3,
    "6M": M6,
    "1Y": Y1,
    "2Y": Y2,
    "3Y": Y3,
    "5Y": Y5,
    "10Y": Y10,
    "All": 0,  # Represents the entire available period
}

# Dictionary for chart-specific predefined periods
PREDIFINED_PERIODS_FOR_CHART_DICT = {
    "1W": W1,
    "1M": M1,
    "3M": M3,
    "6M": M6,
    "1Y": Y1,
    "2Y": Y2,
    "3Y": Y3,
    "5Y": Y5,
    "10Y": Y10,
    "15Y": Y15,
    "20Y": Y20,
}
