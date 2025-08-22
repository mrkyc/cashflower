from .currency_pair_model import CurrencyPair
from .currency_pair_repository import CurrencyPairRepository


class CurrencyPairService:
    def __init__(self, currency_pair_repository: CurrencyPairRepository):
        self.currency_pair_repository = currency_pair_repository

    def create_one(
        self,
        symbol,
        name,
        first_currency_name,
        second_currency_name,
    ):
        currency_pair = CurrencyPair(
            symbol=symbol,
            name=name,
            first_currency_name=first_currency_name,
            second_currency_name=second_currency_name,
        )
        return self.currency_pair_repository.create_one(currency_pair=currency_pair)

    def get_one(self, id):
        return self.currency_pair_repository.get_one(id=id)

    def get_one_by_symbol(self, symbol):
        return self.currency_pair_repository.get_one_by_symbol(symbol=symbol)

    def get_one_by_name(self, name):
        return self.currency_pair_repository.get_one_by_name(name=name)

    def get_all(self):
        return self.currency_pair_repository.get_all()

    def update_one(
        self,
        id,
        first_pricing_date=None,
        last_pricing_date=None,
    ):
        currency_pair = self.get_one(id=id)
        if currency_pair is None:
            return None
        else:
            if first_pricing_date is not None:
                currency_pair.first_pricing_date = first_pricing_date
            if last_pricing_date is not None:
                currency_pair.last_pricing_date = last_pricing_date
            return self.currency_pair_repository.update_one(currency_pair=currency_pair)

    def upsert_one(self, symbol, name, first_currency_name, second_currency_name):
        currency_pair = self.get_one_by_symbol(symbol=symbol)
        if currency_pair:
            return currency_pair
        else:
            return self.create_one(
                symbol=symbol,
                name=name,
                first_currency_name=first_currency_name,
                second_currency_name=second_currency_name,
            )

    def delete_one(self, id):
        currency_pair = self.get_one(id=id)
        if currency_pair is None:
            return None
        else:
            return self.currency_pair_repository.delete_one(currency_pair=currency_pair)

    def delete_all(self):
        return self.currency_pair_repository.delete_all()

    def get_currency_pairs_last_pricing_dates(self):
        return self.currency_pair_repository.get_currency_pairs_last_pricing_dates()
