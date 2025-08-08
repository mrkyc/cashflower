## ⚠️ UNDER DEVELOPMENT ⚠️
This project is currently under active development. Features and functionalities may change.

**Access the online version here: [www.cashflower.online](www.cashflower.online)**

This application uses **Streamlit** for the frontend. The backend is built with **FastAPI**, **SQLAlchemy**, and **SQLite**. SQLite was chosen for its quick setup, minimal resource usage, and ease of local deployment, as each user is provisioned with a separate database. To further enhance calculation performance and simplify the codebase, the project utilizes two custom-built SQLite extensions for calculating the key financial metrics: [XIRR](https://github.com/mrkyc/sqlite-xirr-extension) (Extended Internal Rate of Return) and [STDDEV](https://github.com/mrkyc/sqlite-stddev-extension) (Standard Deviation). This approach allows complex calculations to be performed directly within the database using SQL, eliminating the need to transfer datasets out of the database for processing. The extensions themselves implement more functionality than is currently required by the application, but they were included to provide a robust foundation for future enhancements.

While the database schema was designed to allow for a single, shared database, the current implementation utilizes separate SQLite databases per user. This per-user database approach offers better isolation and scalability compared to a single shared database, potentially deferring the need for a more robust solution like PostgreSQL and making deployment on a VPS easier and more cost-effective.

The deployed online version runs on **Docker**, uses **Nginx** as a reverse proxy, and features fully encrypted connections via **Cloudflare**.

# 💸🌻 CashFlower - Investment Portfolio Analysis Platform

## 🚀 Introduction

CashFlower is a powerful and interactive Streamlit-based application designed to provide comprehensive financial portfolio analysis and visualization. It serves as a central hub for managing your investment transaction data, configuring detailed portfolio settings, and gaining deep insights into your investment performance through a suite of analytical dashboards. The platform aims to empower individual investors and financial enthusiasts with the ability to track, analyze, and understand their portfolios with precision and clarity.

As a portfolio analytics platform, CashFlower processes transaction data and user settings to generate performance metrics, asset allocation insights, and cash flow analysis, accessible via its web interface and API.

### 💡 What CashFlower Does:

*   **Centralized Transaction Management:** Easily import your investment transaction history from various sources (XLSX and CSV files). The application provides intuitive interfaces to view, edit, add new transactions, or delete existing ones, ensuring your data is always accurate and up-to-date.
*   **Flexible Portfolio Customization:** Go beyond basic tracking by defining how your portfolio is structured and analyzed. You can set a primary analysis currency, specify how asset and currency prices are calculated (e.g., Open, High, Low, Close, or various averages), and map your transaction files to specific portfolios. Crucially, CashFlower allows you to create custom portfolio groups (e.g., 'Stocks', 'Bonds', 'Crypto', 'Tech stocks', 'Government bonds') with target allocation weights, and then assign individual assets to these groups, enabling sophisticated model portfolio analysis.
*   **In-depth Performance Analytics:** Access a rich set of dashboards that transform raw transaction data into actionable insights. From high-level performance overviews and current status checks to detailed comparisons between different portfolio components and Monte Carlo simulations for future forecasting, CashFlower provides a 360-degree view of your investments.
*   **Seamless Configuration Management:** Your detailed settings and configurations can be easily saved to and loaded from JSON files, allowing for quick setup across sessions or sharing configurations.
*   **Persistent Session Management:** Each user session is assigned a unique ID, enabling you to resume your work exactly where you left off by simply using a generated session link.

## ✨ Features

*   **Transaction Management:** Loading, editing, adding, and deleting transaction files in XLSX and CSV formats.
*   **Flexible Portfolio Configuration:**
    *   Defining the analysis currency.
    *   Setting preferred price types (OHLC) for assets and and currencies.
    *   Mapping transaction files to specific portfolios and currencies.
    *   Creating custom portfolio groups with target weights.
    *   Assigning assets to defined portfolio groups.
*   **Detailed Analytical Dashboards:**
    *   **Performance Overview:** Comprehensive analysis of performance metrics over time.
    *   **Performance Status:** Current status of key portfolio indicators.
    *   **Components Comparison:** Comparing the performance of different portfolios, groups, or assets.
    *   **Portfolio Group Weights:** Analysis and simulation of portfolio group weights.
    *   **All Data Table:** 📋 Detailed table of all performance data.
    *   **Monte Carlo Simulation:** Forecasting future portfolio value.
*   **Settings Management:** Ability to load and export configuration settings to a JSON file.
*   **Session Management:** Unique session ID allowing for session resumption.

## 📊 Dashboards

### <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M418-340q24 24 62 23.5t56-27.5l224-336-336 224q-27 18-28.5 55t22.5 61Zm62-460q59 0 113.5 16.5T696-734l-76 48q-33-17-68.5-25.5T480-720q-133 0-226.5 93.5T160-400q0 42 11.5 83t32.5 77h552q23-38 33.5-79t10.5-85q0-36-8.5-70T766-540l48-76q30 47 47.5 100T880-406q1 57-13 109t-41 99q-11 18-30 28t-40 10H204q-21 0-40-10t-30-28q-26-45-40-95.5T80-400q0-83 31.5-155.5t86-127Q252-737 325-768.5T480-800Zm7 313Z"/></svg> Performance Status

This dashboard presents the current status of key performance indicators for the selected portfolio, portfolio group, or asset.

*   **Key Metrics:** Displays market value, profit, rates of return (XIRR, TWRR), risk indicators (Sharpe, Sortino), and cash flows.
*   **Changes and Sparklines:** For each metric, it shows its value, percentage and absolute change, as well as a small line chart (sparkline) illustrating the trend over the last 30 days.
*   **Detailed Sections:** Divided into sections: Status, Investment Returns, Drawdown, Risk-Reward Ratios, Cash Flow Overview.

### <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m105-399-65-47 200-320 120 140 160-260 120 180 135-214 65 47-198 314-119-179-152 247-121-141-145 233Zm475 159q42 0 71-29t29-71q0-42-29-71t-71-29q-42 0-71 29t-29 71q0 42 29 71t71 29ZM784-80 676-188q-21 14-45.5 21t-50.5 7q-75 0-127.5-52.5T400-340q0-75 52.5-127.5T580-520q75 0 127.5 52.5T760-340q0 26-7 50.5T732-244l108 108-56 56Z"/></svg> Performance Overview

This dashboard offers a detailed insight into a selected performance metric for the entire portfolio, a single portfolio, a portfolio group, or a specific asset.

*   **Time-series Visualization:** Line charts showing the evolution of the selected metric, with data smoothing options.
*   **Descriptive Statistics:** Basic statistics (mean, median, min, max, standard deviation) for the selected metric.
*   **Periodic Performance:** Analysis of metric changes across different time intervals (yearly, quarterly, monthly, weekly, daily) with the ability to choose the aggregation method (last value, average, median, maximum, minimum).
*   **Distribution Visualization:** Violin plots showing the distribution of metric values within each period.

### <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M80-120v-80h360v-447q-26-9-45-28t-28-45H240l120 280q0 50-41 85t-99 35q-58 0-99-35t-41-85l120-280h-80v-80h247q12-35 43-57.5t70-22.5q39 0 70 22.5t43 57.5h247v80h-80l120 280q0 50-41 85t-99 35q-58 0-99-35t-41-85l120-280H593q-9 26-28 45t-45 28v447h360v80H80Zm585-320h150l-75-174-75 174Zm-520 0h150l-75-174-75 174Zm335-280q17 0 28.5-11.5T520-760q0-17-11.5-28.5T480-800q-17 0-28.5 11.5T440-760q0 17 11.5 28.5T480-720Z"/></svg> Portfolio Group Weights

This dashboard is used for analyzing and managing portfolio group weights.

*   **Model vs. Current Weights:** Pie charts illustrating the target portfolio group weights (model) and their current actual weights.
*   **Weight Balancing:** Functionality allowing simulation of weight changes by manually adjusting asset units. It shows how these changes affect deviations from model weights.
*   **Weights Over Time:** Line charts showing the evolution of portfolio group weights or their deviations from model weights over time.

### <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m320-160-56-57 103-103H80v-80h287L264-503l56-57 200 200-200 200Zm320-240L440-600l200-200 56 57-103 103h287v80H593l103 103-56 57Z"/></svg> Components Comparison

This dashboard allows for comparing the performance of different portfolios, portfolio groups, or individual assets.

*   **Category Selection:** Users can choose whether to compare portfolios, portfolio groups, or assets.
*   **Metric Selection:** Ability to select the performance metric for comparison.
*   **Visualization:** Data is presented on line charts, facilitating visual comparison of trends. An option to display data in a table format is also available.

### <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M200-120q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm240-240H200v160h240v-160Zm80 0v160h240v-160H520Zm-80-80v-160H200v160h240Zm80 0h240v-160H520v160ZM200-680h560v-80H200v80Z"/></svg> All Data Table

This dashboard displays all available performance data in a tabular format.

*   **Detailed Data:** Presents full historical data for the selected aggregation level (overall portfolio, single portfolio, portfolio group, single asset).
*   **Filtering:** Ability to filter data by date range.
*   **Configurable Columns:** Displays appropriate columns depending on the selected aggregation level.

### <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M600-80v-80h160v-400H200v160h-80v-320q0-33 23.5-56.5T200-800h40v-80h80v80h320v-80h80v80h40q33 0 56.5 23.5T840-720v560q0 33-23.5 56.5T760-80H600ZM320 0l-56-56 103-104H40v-80h327L264-344l56-56 200 200L320 0ZM200-640h560v-80H200v80Zm0 0v-80 80Z"/></svg> Monte Carlo Simulation

This dashboard allows for performing Monte Carlo simulations to forecast the future value of a selected portfolio.

*   **Simulation Parameters:** Users can configure the number of simulation days, number of simulations, random seed, mean (mu), and standard deviation (sigma) of daily returns.
*   **Results Visualization:**
    *   Table of final values with key statistics (mean, median, selected percentiles).
    *   Histogram of the distribution of final values.
    *   Line chart showing historical and simulated portfolio value paths.

## 📈 Key Performance Metrics

CashFlower provides a comprehensive set of metrics to analyze your investment portfolio's performance, risk, and cash flows. Below are the definitions and interpretations of the key metrics used across the dashboards:

*   **Market Value:** The current total value of all assets in the portfolio, calculated based on their latest available prices.
*   **Profit:** The absolute gain or loss on your investments, calculated as the difference between the current market value (plus any withdrawals/disposals) and the total invested amount (plus any deposits).
*   **Profit Percentage:** The percentage return on your investments, indicating the profitability relative to the invested capital.
*   **XIRR Rate (Extended Internal Rate of Return):** A sophisticated metric that calculates the annualized effective compounded return for a series of cash flows occurring at irregular intervals. It provides a more accurate measure of investment performance than simple return calculations, especially for portfolios with ongoing contributions and withdrawals.
*   **TWRR Rate (Time-Weighted Rate of Return):** A measure of the compound rate of growth of an investment portfolio over a specified period. It eliminates the distorting effects on growth rates created by cash inflows and outflows, making it suitable for comparing the performance of investment managers.
    *   **Daily:** The daily time-weighted rate of return.
    *   **Annualized:** The annualized time-weighted rate of return, calculated by compounding the daily TWRR.
*   **Drawdown:** The peak-to-trough decline in the value of an investment portfolio during a specific period, calculated based on daily changes in portfolio value, similar to TWRR, and thus excluding the impact of cash flows. It measures the downside risk of an investment.
    *   **Drawdown Value:** The absolute monetary value of the drawdown, calculated based on the actual market value of the portfolio, adjusted for the value of assets already sold. This adjustment prevents the drawdown from artificially increasing due to asset sales, ensuring that only market fluctuations impact the metric. It's important to note that new purchases can also reduce or eliminate an existing drawdown, as they increase the portfolio's overall value, potentially pushing it above a previous peak.
    *   **Drawdown Profit:** The drawdown calculated specifically on the portfolio's profit, showing the peak-to-trough decline in accumulated profit.
*   **Sharpe Ratio:** A measure of risk-adjusted return. It describes how much excess return you receive for the volatility you endure. A higher Sharpe ratio indicates a better risk-adjusted return.
    *   **Daily:** Calculated using daily returns and daily standard deviation.
    *   **Annualized:** Calculated by annualizing the daily Sharpe Ratio.
    *   *Note: For simplification, the risk-free rate used in Sharpe Ratio calculations is currently assumed to be 0%. This may be configurable in future updates.*
*   **Sortino Ratio:** Similar to the Sharpe Ratio, but it only considers downside volatility (standard deviation of negative returns), making it a better measure for investors concerned specifically with downside risk. A higher Sortino ratio indicates a better return for each unit of downside risk.
    *   **Daily:** Calculated using daily returns and daily downside deviation.
    *   **Annualized:** Calculated by annualizing the daily Sortino Ratio.
    *   *Note: For simplification, the risk-free rate used in Sortino Ratio calculations is currently assumed to be 0%. This may be configurable in future updates.*
*   **Cash Balance:** The current amount of cash held within the portfolio.
*   **Invested Amount:** The total cumulative amount of capital invested into the portfolio through deposits and asset purchases.
*   **Asset Disposal Income:** Income generated from selling assets.
*   **Asset Holding Income:** Income earned from owning or holding financial assets, including dividends, bond coupons, and other distributions.
*   **Interest Income:** Income earned from interest on cash or deposit holdings.
*   **Investment Income:** The total income generated from investments, including asset disposals, asset holdings, and interest.

## 🛠️ How to Use

### 💻 Local Running

To run the CashFlower application locally, ensure you have Python and pip installed. The application consists of a FastAPI backend and a Streamlit frontend, which must be run separately from the main `cashflower/` directory.

First, install the required dependencies from the main `cashflower/` directory:
```bash
# Navigate to the project's root directory
cd /path/to/cashflower

# Install dependencies
pip install -r requirements.txt
```

Next, you need to run both the backend and the frontend from the `cashflower/` directory.

1.  **Run the FastAPI Backend:**
    Open a terminal in the `cashflower/` directory and run:
    ```bash
    uvicorn main:app --reload
    ```

2.  **Run the Streamlit Frontend:**
    Open a second terminal in the `cashflower/` directory and run:
    ```bash
    streamlit run main_streamlit.py
    ```
The application should now be accessible in your browser.

### 🌐 Online Version

The CashFlower application is also deployed and accessible online at [www.cashflower.online](www.cashflower.online).

### ⚠️ Transaction File Structure ⚠️

Before uploading your transaction files, it's crucial to prepare your data according to the required structure. To ensure your transaction data is correctly processed, your transaction files (XLSX or CSV) must adhere to a specific structure. The following columns are required:

*   **date:** Date of the transaction (YYYY-MM-DD format).
*   **asset_symbol:** Symbol of the asset (e.g., "AAPL", "SPY", "SAP.DE", "MC.PA"). This must be a symbol recognized by Yahoo Finance. Always verify the exact quote symbol for your asset on Yahoo Finance to ensure correct data retrieval.
*   **transaction_type:** Type of transaction. Supported types are: "buy", "sell", "deposit", "withdrawal", "distribution", "interest", "fee".
    Here is a detailed description of each transaction type and when to use it:
    *   **buy**: Use when purchasing an asset (e.g., stocks, bonds, crypto).
    *   **sell**: Use when selling an asset.
    *   **deposit**: Use when adding cash to your investment account from an external source (e.g., a bank transfer).
    *   **withdrawal**: Use when removing cash from your investment account to an external destination.
    *   **distribution**: Use for receiving payments generated by assets you hold, such as dividends from stocks, bond coupons, or fund distributions.
    *   **interest**: Use for interest earned on cash held within your investment account.
    *   **fee**: Use for any standalone fees charged to your account that are not directly associated with another transaction (e.g., account maintenance fees, advisory fees).
*   **quantity:** Quantity of the asset involved in the transaction.
*   **transaction_value:** Value of the transaction in the analysis currency.
*   **fee_amount:** Any fees associated with the transaction in the analysis currency.
*   **tax_amount:** Any taxes associated with the transaction in the analysis currency.

The interpretation of the `quantity`, `transaction_value`, `fee_amount`, and `tax_amount` fields depends on the `transaction_type`. The system automatically handles the sign of the values (positive or negative), so you can provide either absolute values or values with signs in your file. Below is a detailed breakdown of how each field is interpreted for different transaction types:
*   **quantity:**
    *   `buy`: The quantity will be treated as positive.
    *   `sell`: The quantity will be treated as negative.
*   **transaction_value:**
    *   `deposit`, `sell`, `distribution`, `interest`: The value will be treated as positive.
    *   `withdrawal`, `buy`: The value will be treated as negative.
*   **fee_amount:**
    *   `deposit`, `withdrawal`, `sell`, `distribution`, `interest`, `buy`, `fee`: The amount will be treated as negative.
*   **tax_amount:**
    *   `sell`, `distribution`, `interest`: The amount will be treated as negative.

You can find a detailed template and demo data here:

*   [Template File](https://docs.google.com/spreadsheets/d/1D1UPDEMOIYgjHCLJvjvrMlhq0v3ie5grjZa3lSH6Nb4/edit?usp=sharing)
*   [Demo Data](https://drive.google.com/drive/folders/1uLS6gbX2ieore1bGZZ6mKqRa5DYx4zUg?usp=sharing)

### <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M240-200h120v-240h240v240h120v-360L480-740 240-560v360Zm-80 80v-480l320-240 320 240v480H520v-240h-80v240H160Zm320-350Z"/></svg> Entry Page

After launching the application, you will be redirected to the entry page.

*   **Session ID:** A unique link with your session ID will be generated. Save it to resume your session later.
*   **How It Works:** A section explaining the basic functionality of the application.
*   **Template File:** A link to download the transaction template file, which shows the required column names and data types.
*   **Demo Data:** A link to a folder with demo data (sample transaction files and a `settings.json` file). Instructions on how to load demo data to explore the application's features.

### <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m370-80-16-128q-13-5-24.5-12T307-235l-119 50L78-375l103-78q-1-7-1-13.5v-27q0-6.5 1-13.5L78-585l110-190 119 50q11-8 23-15t24-12l16-128h220l16 128q13 5 24.5 12t22.5 15l119-50 110 190-103 78q1 7 1 13.5v27q0 6.5-2 13.5l103 78-110 190-118-50q-11 8-23 15t-24 12L590-80H370Zm70-80h79l14-106q31-8 57.5-23.5T639-327l99 41 39-68-86-65q5-14 7-29.5t2-31.5q0-16-2-31.5t-7-29.5l86-65-39-68-99 42q-22-23-48.5-38.5T533-694l-13-106h-79l-14 106q-31 8-57.5 23.5T321-633l-99-41-39 68 86 64q-5 15-7 30t-2 32q0 16 2 31t7 30l-86 65 39 68 99-42q22 23 48.5 38.5T427-266l13 106Zm42-180q58 0 99-41t41-99q0-58-41-99t-99-41q-59 0-99.5 41T342-480q0 58 40.5 99t99.5 41Zm-2-140Z"/></svg> Settings

To start the analysis, you need to configure your data and settings in the "Settings" tab.

#### "Transactions" Tab

1.  🗃️ **Uploading Transaction Files:**
    *   Use the "Upload your transaction files" button to upload one or more `.xlsx` or `.csv` files.
    *   Ensure that the files comply with the template structure.
    *   All transaction files must be uploaded simultaneously.
2.  ➕ **Adding an Empty Transaction File:**
    *   In the "Add empty transaction file" section, you can add a new, empty transaction file by providing its name.
3.  ➖ **Deleting Transaction Files:**
    *   In the "Delete transaction files" section, you can select and remove transaction files from the current session.
4.  📝 **Editing Transactions:**
    *   Select a file from the "Transaction file name" dropdown to view and edit its content in the table.
    *   Changes are saved automatically. You can add new rows or delete existing ones.

#### "Settings" Tab

1.  📄 **Loading Settings from File:**
    *   If you have a previously saved `settings.json` file, you can upload it here to quickly restore your configuration.
2.  ⚙️ **General Settings:**
    *   **Analysis currency:** Enter the three-letter currency code (e.g., USD, EUR) for your reports.
    *   **OHLC assets/currencies:** Select the price type to be used for asset and currency valuation. This determines how the daily price of an asset or currency is calculated. Options include:
    *   **Open:** The price at which the asset first traded during the day.
    *   **High:** The highest price at which the asset traded during the day.
    *   **Low:** The lowest price at which the asset traded during the day.
    *   **Close:** The last price at which the asset traded during the day. This is often considered the most important price as it reflects the market's sentiment at the end of the trading period.
    *   **Average:** A simple average of the Open, High, Low, and Close prices: `(Open + High + Low + Close) / 4`.
    *   **Typical Price:** The average of the High, Low, and Close prices: `(High + Low + Close) / 3`. This is often used in technical analysis.
    *   **Weighted Close Price:** A weighted average that gives more importance to the Close price: `(Close * 2 + High + Low) / 4`. This emphasizes the closing price's significance.
3.  🗃️ **Setting Transaction Files:**
    *   For each uploaded transaction file, assign the appropriate currency and portfolio name.
    *   You can group multiple files under one portfolio name.
4.  📚 **Defining Portfolio Groups:**
    *   Create custom groups for your assets (e.g., "Stocks", "Bonds", "Crypto", "Tech stocks", "Government bonds").
    *   Assign a target weight (in %) to each group. The sum of weights for each portfolio must equal 100%.
5.  🔗 **Matching Assets to Portfolio Groups:**
    *   Assign each asset symbol from the transaction files to one of the defined portfolio groups.

**After configuring all settings, click the "<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M840-680v480q0 33-23.5 56.5T760-120H200q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h480l160 160Zm-80 34L646-760H200v560h560v-446ZM480-240q50 0 85-35t35-85q0-50-35-85t-85-35q-50 0-85 35t-35 85q0 50 35 85t85 35ZM240-560h360v-160H240v160Zm-40-86v446-560 114Z"/></svg> Save settings and load data" button in the sidebar to save the configuration and load the data.**

### <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M686-132 444-376q-20 8-40.5 12t-43.5 4q-100 0-170-70t-70-170q0-36 10-68.5t28-61.5l146 146 72-72-146-146q29-18 61.5-28t68.5-10q100 0 170 70t70 170q0 23-4 43.5T584-516l244 242q12 12 12 29t-12 29l-84 84q-12 12-29 12t-29-12Zm29-85 27-27-256-256q18-20 26-46.5t8-53.5q0-60-38.5-104.5T386-758l74 74q12 12 12 28t-12 28L332-500q-12 12-28 12t-28-12l-74-74q9 57 53.5 95.5T360-440q26 0 52-8t47-25l256 256ZM472-488Z"/></svg> Sidebar Settings Management

In the sidebar, you'll find additional options for managing your settings and data:

*   <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M840-680v480q0 33-23.5 56.5T760-120H200q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h480l160 160Zm-80 34L646-760H200v560h560v-446ZM480-240q50 0 85-35t35-85q0-50-35-85t-85-35q-50 0-85 35t-35 85q0 50 35 85t85 35ZM240-560h360v-160H240v160Zm-40-86v446-560 114Z"/></svg> **Save settings and load data:** Click this button to apply your configured settings and load the corresponding data for analysis. This button is disabled until all required settings are valid.
*   <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m400-570 80-40 80 40v-190H400v190ZM280-280v-80h200v80H280Zm-80 160q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200Zm0-640v560-560Zm0 560h560v-560H640v320l-160-80-160 80v-320H200v560Z"/></svg> **Export settings to file:** Download your current settings as a `settings.json` file. This allows you to easily back up your configuration or share it with others.
*   <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M280-200v-80h284q63 0 109.5-40T720-420q0-60-46.5-100T564-560H312l104 104-56 56-200-200 200-200 56 56-104 104h252q97 0 166.5 63T800-420q0 94-69.5 157T564-200H280Z"/></svg> **Reset settings:** Reset all your current settings to their default values. Use with caution as this will clear your configuration.
*   <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M480-120q-151 0-255.5-46.5T120-280v-400q0-66 105.5-113T480-840q149 0 254.5 47T840-680v400q0 67-104.5 113.5T480-120Zm0-479q89 0 179-25.5T760-679q-11-29-100.5-55T480-760q-91 0-178.5 25.5T200-679q14 30 101.5 55T480-599Zm0 199q42 0 81-4t74.5-11.5q35.5-7.5 67-18.5t57.5-25v-120q-26 14-57.5 25t-67 18.5Q600-528 561-524t-81 4q-42 0-82-4t-75.5-11.5Q287-543 256-554t-56-25v120q25 14 56 25t66.5 18.5Q358-408 398-404t82 4Zm0 200q46 0 93.5-7t87.5-18.5q40-11.5 67-26t32-29.5v-98q-26 14-57.5 25t-67 18.5Q600-328 561-324t-81 4q-42 0-82-4t-75.5-11.5Q287-343 256-354t-56-25v99q5 15 31.5 29t66.5 25.5q40 11.5 88 18.5t94 7Z"/></svg> **Database management:** Options for managing the application's internal database:
    *   <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M480-120q-138 0-240.5-91.5T122-440h82q14 104 92.5 172T480-200q117 0 198.5-81.5T760-480q0-117-81.5-198.5T480-760q-69 0-129 32t-101 88h110v80H120v-240h80v94q51-64 124.5-99T480-840q75 0 140.5 28.5t114 77q48.5 48.5 77 114T840-480q0 75-28.5 140.5t-77 114q-48.5 48.5-114 77T480-120Zm112-192L440-464v-216h80v184l128 128-56 56Z"/></svg> **Soft database reset:** The application does not recalculate all performance data from scratch every time. Instead, it saves a checkpoint and refreshes the data from that point, making subsequent calculations much faster than the initial one. This option allows you to force the application to recalculate all performance data from the beginning, clearing only the loaded data while keeping your settings intact. For example, if you add new or modified transactions with dates prior to the last calculation, you should use this option to ensure accurate recalculation of historical performance.
    *   <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="m376-300 104-104 104 104 56-56-104-104 104-104-56-56-104 104-104-104-56 56 104 104-104 104 56 56Zm-96 180q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520Zm-400 0v520-520Z"/></svg> **Hard database reset:** This action removes all data except essential session information, allowing you to restore the session without loaded settings or calculations. It is primarily used in case of unexpected errors, such as incorrect data loading or retrieval. Use with extreme caution.

### Navigating Dashboards

Once the data is loaded, you can navigate between different dashboards using the sidebar on the left. Each dashboard offers unique views and analyses of your portfolio.

### Common Sidebar Options

Most dashboards have common sidebar options that allow you to customize the displayed data:

*   <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#e3e3e3"><path d="M204-318q-22-38-33-78t-11-82q0-134 93-228t227-94h7l-64-64 56-56 160 160-160 160-56-56 64-64h-7q-100 0-170 70.5T240-478q0 26 6 51t18 49l-60 60ZM481-40 321-200l160-160 56 56-64 64h7q100 0 170-70.5T720-482q0-26-6-51t-18-49l60-60q22 38 33 78t11 82q0 134-93 228t-227 94h-7l64 64-56 56Z"/></svg> **Refresh data:** Button to refresh data.
*   **Data aggregation level:** Choose whether to analyze:
    *   **Aggregated portfolios:** All portfolios combined.
    *   **Portfolio as a whole:** A single, selected portfolio.
    *   **Model weight groups:** Data aggregated by model weight groups.
    *   **Assets:** Data for a single, selected asset.
*   **Show total values:** Option to enable/disable the display of total values including the sum of paid fees and taxes.
