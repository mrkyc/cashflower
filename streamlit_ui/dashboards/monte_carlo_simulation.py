import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np

from streamlit_ui.constants import *
from streamlit_ui.dashboards.utils import *


# INITIALIZATION AND DATA LOADING

session_id, analysis_currency, df_portfolio_variants = initialize_dashboard()


# SIDEBAR SETTINGS

with st.sidebar:
    # Common sidebar elements
    setup_common_sidebar_elements()

    # Selectbox to choose the portfolio for analysis
    portfolio_id = portfolio_id_selectbox(df_portfolio_variants)


# DATA LOADING FOR SIMULATION

# Get statistics on percentage changes for the selected portfolio
pct_changes_stats = load_data_or_stop(
    get_pct_changes_stats,
    session_id,
    portfolio_id,
    error_message="Failed to load percentage changes statistics. Please try again later.",
    refresh_counter=st.session_state.get("refresh_counter", 0),
)


# Get historical market values for the portfolio
df_market_values = load_data_or_stop(
    get_df_market_values,
    session_id,
    portfolio_id,
    error_message="Failed to load market values. Please try again later.",
    refresh_counter=st.session_state.get("refresh_counter", 0),
)


# MAIN PAGE CONTENT

st.header("Monte Carlo simulation")
with st.expander("What is Monte Carlo simulation?"):
    st.markdown(
        """
        The Monte Carlo simulation is a computational algorithm that relies on repeated random sampling
        to obtain numerical results. In finance, it's often used to model the probability of different
        outcomes in a process that cannot be easily predicted due to the intervention of random variables.
        Here, we simulate future portfolio values based on historical daily returns.

        The simulation uses the Geometric Brownian Motion (GBM) model, which is commonly used for asset prices.
        The formula for the logarithmic returns (daily changes) is:

        $log\\_returns = (\\mu - 0.5 \\cdot \\sigma^2) + \\sigma \\cdot \\xi$

        Where:
        - $\\mu$ (mu): The expected daily return (mean).
        - $\\sigma$ (sigma): The daily volatility (standard deviation).
        - $\\xi$: A random variable drawn from a standard normal distribution.

        This formula helps to project how the portfolio value might evolve over time, considering both
        its average growth and its daily fluctuations.

        ---
        :warning: In this specific case, the Monte Carlo simulation shows the potential future value of the portfolio, assuming no deposits or withdrawals are made and that the portfolio's group weights remain identical to the model's.
        """
    )


# Simulation Settings


st.subheader(
    ":gear: Settings",
    help="""Adjust the parameters for the Monte Carlo simulation to explore different scenarios.""",
)


# User inputs for the simulation parameters
cols = st.columns(3)
with cols[0]:
    n_days = st.number_input(
        "Number of days",
        min_value=1,
        max_value=2520,
        value=252,
        step=1,
        help="""The number of future days to simulate. 252 is a common value for the number of trading days in a year.""",
    )
with cols[1]:
    n_sims = st.number_input(
        "Number of simulations",
        min_value=1,
        max_value=100000,
        value=10000,
        step=1,
        help="""The number of independent paths (scenarios) to simulate. A higher number increases accuracy but also computation time.""",
    )
with cols[2]:
    seed = st.number_input(
        "Random seed",
        min_value=0,
        value=42,
        help="""Set a seed for reproducible results. Use 0 for a random seed, which means each run will produce different results.""",
        step=1,
    )

cols = st.columns(2)
with cols[0]:
    mu = st.number_input(
        "Mean (mu)",
        value=pct_changes_stats.get("pct_change_avg"),
        format="%.8f",
        key="mu_input",
        help="""The average daily return (\\mu) of the portfolio. This value is calculated from historical data by default. It represents the expected growth rate in the GBM formula.""",
    )
with cols[1]:
    sigma = st.number_input(
        "Standard Deviation (sigma)",
        value=pct_changes_stats.get("pct_change_std"),
        format="%.8f",
        key="sigma_input",
        help="""The daily volatility (\\sigma) of the portfolio. This value is calculated from historical data by default. It represents the expected fluctuation (risk) in the GBM formula.""",
    )

percentile_options = [1, 2.5, 5, 10, 25, 75, 90, 95, 97.5, 99]
selected_percentiles = st.multiselect(
    "Select Percentiles to Display",
    options=percentile_options,
    default=[2.5, 97.5],
    help="""Select which percentiles of the simulated final values to display in the table and chart. Percentiles help understand the range of possible outcomes.""",
)


# Monte Carlo Simulation Logic

# Generate random standard normal variables
if seed != 0:
    np.random.seed(seed)
xi = np.random.normal(size=(n_days, n_sims))

# Logarithmic returns for Geometric Brownian Motion (GBM)
# Formula: log_returns = (mu - 0.5 * sigma**2) + sigma * xi
# - We use log returns because GBM assumes that asset prices follow a lognormal distribution.
# - The term (-0.5 * sigma**2) is the "Jensen's inequality correction":
#   - Since we model log returns, the expectation of e^(log return) should match the expected return.
#   - This correction ensures that the expected price follows the correct mean.
# - We do NOT divide sigma * xi by 252 because:
#   - We are already working with **daily** mu and sigma.
#   - If mu and sigma were **annualized**, we would need to scale them by (1/252) and (sqrt(1/252)) respectively.
log_returns = (mu - 0.5 * sigma**2) + sigma * xi

# Calculate simulated asset prices using NumPy for performance
latest_market_value = df_market_values.iloc[-1, 0]
cumulative_log_returns = log_returns.cumsum(axis=0)
mc_values_np = (latest_market_value * np.exp(cumulative_log_returns)).round(2)

# Calculate statistics for the simulated values
quantiles_to_calculate = sorted([p / 100.0 for p in selected_percentiles])
quantile_results = np.quantile(mc_values_np, q=quantiles_to_calculate, axis=1)


# Create column names for the new DataFrame
column_names = [get_ordinal_suffix(p) for p in selected_percentiles]

# Create the DataFrame from NumPy results
df_mc_values_stats = pd.DataFrame(
    quantile_results.T,
    index=pd.RangeIndex(start=0, stop=n_days, step=1),
    columns=column_names,
)

# Always add Median to the stats
median_np = np.median(mc_values_np, axis=1)
df_mc_values_stats.insert(0, COLUMN_MEDIAN, median_np)


# Displaying Final Values

st.subheader(
    ":checkered_flag: Final Values Table",
    help="""This table summarizes the key statistics of the simulated portfolio values at the end of the simulation period.""",
)

# Get final statistics for the table
final_stats_dict = {COLUMN_MARKET_VALUE: latest_market_value}
final_stats_dict[COLUMN_MEAN] = mc_values_np[-1].mean().round(2)

# Add selected percentiles and median to the dictionary
for col in df_mc_values_stats.columns:
    final_stats_dict[col] = df_mc_values_stats[col].iloc[-1].round(2)

# Display final values statistics in a table
st.dataframe(
    pd.DataFrame(final_stats_dict, index=[0]),
    use_container_width=True,
    hide_index=True,
)


# Final Value Distribution Chart

st.subheader(
    ":bar_chart: Final Value Distribution",
    help="""This histogram visualizes the distribution of the simulated final portfolio values, showing the probability of different outcomes.""",
)

n_bins = st.slider(
    "Number of bins",
    min_value=1,
    max_value=1000,
    value=100,
    help="""Number of bins for the histogram. Adjust to see more or fewer bars in the distribution.""",
)

# Histogram of the final simulated values
fig = px.histogram(
    mc_values_np[-1],
    nbins=n_bins,
    histnorm="probability",
)
# Add vertical lines for key statistics
fig.add_vline(
    x=final_stats_dict[COLUMN_MARKET_VALUE],
    line_dash="dash",
    line_color="green",
    annotation_text=COLUMN_MARKET_VALUE,
    annotation_position="top right",
)
fig.add_vline(
    x=final_stats_dict[COLUMN_MEAN],
    line_dash="dash",
    line_color="orange",
    annotation_text=COLUMN_MEAN,
    annotation_position="top right",
)

# Loop through the calculated final stats for percentiles and median
for col_name in df_mc_values_stats.columns:
    value = final_stats_dict[col_name]
    fig.add_vline(
        x=value,
        line_dash="dash",
        line_color="purple" if col_name == COLUMN_MEDIAN else "red",
        annotation_text=col_name,
        annotation_position="top left",
    )

fig.update_layout(
    xaxis_title=f"Final Value [{analysis_currency}]",
    yaxis_title="Probability",
    showlegend=False,
)
fig.update_traces(
    hovertemplate="<b>Range:</b> %{x}<br><b>Probability:</b> %{y}<extra></extra>"
)
st.plotly_chart(fig, use_container_width=True, config={"showTips": False})


# Simulation Results Chart

st.subheader(
    ":chart_with_upwards_trend: Monte Carlo Simulation Results",
    help="""This chart displays the historical portfolio values along with the simulated future paths, including selected percentiles.""",
)

# Prepare data for the simulation chart
df_mc_values_stats.index = pd.date_range(
    start=df_market_values.index[-1] + pd.DateOffset(days=1), periods=n_days, freq="B"
)
df_simulated_portfolio_values = pd.concat([df_market_values, df_mc_values_stats])

# Line chart showing historical and simulated portfolio values
fig = px.line(
    df_simulated_portfolio_values,
    labels={"index": "Day", "value": f"Value [{analysis_currency}]"},
)
fig.update_layout(hovermode="x unified")
fig.update_traces(hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y}<extra></extra>")
st.plotly_chart(fig, use_container_width=True, config={"showTips": False})
