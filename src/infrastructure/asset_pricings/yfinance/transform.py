import pandas as pd


def transform_data_yfinance(
    df_data,
    asset_id,
):
    ohlc = ["Open", "High", "Low", "Close", "Adj Close"]
    df_data = df_data[ohlc].reset_index()
    df_data.insert(0, "asset_id", asset_id)
    df_data = df_data.rename(
        columns={
            "Date": "date",
            "Open": "open_price",
            "High": "high_price",
            "Low": "low_price",
            "Close": "close_price",
            "Adj Close": "adjusted_close_price",
        }
    )
    df_data["date"] = pd.to_datetime(df_data["date"]).dt.date

    return df_data
