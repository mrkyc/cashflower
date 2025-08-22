from .currency_pair_model import CurrencyPair


class CurrencyPairRepository:
    def __init__(self, session):
        self.session = session

    def create_one(self, currency_pair):
        self.session.add(currency_pair)
        self.session.flush()
        self.session.refresh(currency_pair)
        return currency_pair

    def get_one(self, id):
        return self.session.query(CurrencyPair).filter(CurrencyPair.id == id).first()

    def get_one_by_name(self, name):
        return (
            self.session.query(CurrencyPair).filter(CurrencyPair.name == name).first()
        )

    def get_one_by_symbol(self, symbol):
        return (
            self.session.query(CurrencyPair)
            .filter(CurrencyPair.symbol == symbol)
            .first()
        )

    def get_all(self):
        return self.session.query(CurrencyPair).all()

    def update_one(self, currency_pair):
        return self.session.merge(currency_pair)

    def delete_one(self, currency_pair):
        self.session.delete(currency_pair)
        self.session.flush()
        return currency_pair

    def delete_all(self):
        deleted_count = self.session.query(CurrencyPair).delete()
        self.session.flush()
        return deleted_count

    def execute_custom_query(self, query):
        result = self.session.execute(query)
        self.session.flush()
        return result

    def get_currency_pairs_last_pricing_dates(self):
        return self.session.query(
            CurrencyPair.name,
            CurrencyPair.symbol,
            CurrencyPair.last_pricing_date,
        ).all()
