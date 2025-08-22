from .currency_pair_pricing_model import CurrencyPairPricing


class CurrencyPairPricingRepository:
    def __init__(self, session):
        self.session = session

    def create_many(self, currency_pair_pricings):
        self.session.add_all(currency_pair_pricings)
        self.session.flush()
        for currency_pair_pricing in currency_pair_pricings:
            self.session.refresh(currency_pair_pricing)
        return currency_pair_pricings

    def get_one(self, id):
        return (
            self.session.query(CurrencyPairPricing)
            .filter(CurrencyPairPricing.id == id)
            .first()
        )

    def get_all(self):
        return self.session.query(CurrencyPairPricing).all()

    def update_one(self, currency_pair_pricing):
        return self.session.merge(currency_pair_pricing)

    def delete_one(self, currency_pair_pricing):
        self.session.delete(currency_pair_pricing)
        self.session.flush()
        return currency_pair_pricing

    def delete_all(self):
        deleted_count = self.session.query(CurrencyPairPricing).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result
