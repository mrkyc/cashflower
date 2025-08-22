from .adjusted_currency_pair_pricing_model import AdjustedCurrencyPairPricing


class AdjustedCurrencyPairPricingRepository:
    def __init__(self, session):
        self.session = session

    def get_one(self, id):
        return (
            self.session.query(AdjustedCurrencyPairPricing)
            .filter(AdjustedCurrencyPairPricing.id == id)
            .first()
        )

    def get_all(self):
        return self.session.query(AdjustedCurrencyPairPricing).all()

    def delete_one(self, adjusted_currency_pair_pricing):
        self.session.delete(adjusted_currency_pair_pricing)
        self.session.flush()
        return adjusted_currency_pair_pricing

    def delete_all(self):
        deleted_count = self.session.query(AdjustedCurrencyPairPricing).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
