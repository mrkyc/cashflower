from src.domain.asset_pricings import AssetPricingService


def load_data_yfinance(asset_pricing_service: AssetPricingService, df_data, asset_id):
    asset_pricing_service.delete_many_by_asset_id_and_date(asset_id=asset_id)
    asset_pricing_service.create_many(
        asset_ids=df_data["asset_id"].values,
        dates=df_data["date"].values,
        open_prices=df_data["open_price"].values,
        high_prices=df_data["high_price"].values,
        low_prices=df_data["low_price"].values,
        close_prices=df_data["close_price"].values,
        adjusted_close_prices=df_data["adjusted_close_price"].values,
    )
