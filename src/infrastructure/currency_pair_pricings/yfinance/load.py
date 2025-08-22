from src.domain.currency_pair_pricings import CurrencyPairPricingService


def load_data_yfinance(
    currency_pair_pricing_service: CurrencyPairPricingService, df_data, currency_pair_id
):
    currency_pair_pricing_service.delete_many_by_currency_pair_id_and_date(
        currency_pair_id=currency_pair_id
    )
    currency_pair_pricing_service.create_many(
        currency_pair_ids=df_data["currency_pair_id"].values,
        dates=df_data["date"].values,
        open_prices=df_data["open_price"].values,
        high_prices=df_data["high_price"].values,
        low_prices=df_data["low_price"].values,
        close_prices=df_data["close_price"].values,
    )
