from pydantic import BaseModel


class TransactionFilesModel(BaseModel):
    file_name: list[str]
    currency: list[str]
    portfolio_name: list[str]


class TransactionDataModel(BaseModel):
    date: list[str]
    asset_symbol: list[str]
    transaction_type: list[str]
    quantity: list[float]
    transaction_value: list[float]
    fee_amount: list[float]
    tax_amount: list[float]


class TransactionsModel(BaseModel):
    file_name: str
    transaction_data: TransactionDataModel


class TransactionsItemsModel(BaseModel):
    items: list[TransactionsModel]


class PortfolioGroupsModel(BaseModel):
    portfolio_name: list[str]
    group_name: list[str]
    group_weight: list[float]


class PortfolioGroupAssetsModel(BaseModel):
    portfolio_name: list[str]
    asset_symbol: list[str]
    group_name: list[str]


class SettingsDTO(BaseModel):
    analysis_currency: str
    ohlc_assets: str
    ohlc_currencies: str
    transaction_files: TransactionFilesModel
    transactions: TransactionsItemsModel
    portfolio_groups: PortfolioGroupsModel
    portfolio_group_assets: PortfolioGroupAssetsModel
