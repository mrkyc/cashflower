import yfinance as yf


def fetch_asset_info(symbol: str) -> dict:
    info = yf.Ticker(symbol).info
    currency = info.get("currency")
    full_name = info.get("longName") or info.get("symbol")

    return {"currency": currency, "full_name": full_name}
