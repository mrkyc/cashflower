import pandas as pd


def fill_df_input_transaction_files(
    df_input_transaction_files: pd.DataFrame | None, dict_transactions: dict
) -> pd.DataFrame:
    """
    Fills the transaction files DataFrame with file names and their associated data.

    This function populates a DataFrame with transaction file names and retrieves
    their corresponding currency and portfolio name from the existing settings
    if available.

    Parameters
    ----------
    df_input_transaction_files : pd.DataFrame
        The DataFrame to be filled with transaction file data.
    dict_transactions : dict
        A dictionary where keys are file names.

    Returns
    -------
    pd.DataFrame
        The populated and sorted DataFrame.
    """
    file_names = []
    currencies = []
    portfolio_names = []

    # Iterate through transaction file names
    for file_name in dict_transactions.keys():
        file_names.append(file_name)

        # If the input DataFrame is empty, append None for currency and portfolio name
        if df_input_transaction_files is None or df_input_transaction_files.empty:
            currencies.append(None)
            portfolio_names.append(None)
        else:
            # Retrieve currency if it exists for the current file name
            currency = df_input_transaction_files.loc[
                df_input_transaction_files["file_name"] == file_name
            ]["currency"]
            currencies.append(None if currency.empty else currency.values[0])

            # Retrieve portfolio name if it exists for the current file name
            portfolio_name = df_input_transaction_files.loc[
                df_input_transaction_files["file_name"] == file_name
            ]["portfolio_name"]
            portfolio_names.append(
                None if portfolio_name.empty else portfolio_name.values[0]
            )

    # Create and sort the final DataFrame
    df_input_transaction_files = (
        pd.DataFrame(
            {
                "file_name": file_names,
                "currency": currencies,
                "portfolio_name": portfolio_names,
            },
            dtype=str,
        )
        .sort_values(by="file_name")
        .reset_index(drop=True)
    )

    return df_input_transaction_files


def fill_df_input_portfolio_groups(
    df_input_portfolio_groups: pd.DataFrame, portfolio_names: list[str]
) -> pd.DataFrame:
    """
    Fills the portfolio groups DataFrame with relevant data.

    This function filters the portfolio groups based on the provided portfolio names,
    converts the group weight to a float, and sorts the DataFrame.

    Parameters
    ----------
    df_input_portfolio_groups : pd.DataFrame
        The DataFrame containing portfolio group data.
    portfolio_names : list
        A list of portfolio names to filter by.

    Returns
    -------
    pd.DataFrame
        The filtered, converted, and sorted DataFrame.
    """
    # Filter the DataFrame to include only the specified portfolio names
    df_input_portfolio_groups = df_input_portfolio_groups.loc[
        df_input_portfolio_groups["portfolio_name"].isin(portfolio_names)
    ].copy()

    # Convert group_weight column to float
    df_input_portfolio_groups["group_weight"] = df_input_portfolio_groups[
        "group_weight"
    ].astype(float)

    # Sort the DataFrame
    df_input_portfolio_groups = df_input_portfolio_groups.sort_values(
        by=["portfolio_name", "group_weight", "group_name"],
        ascending=[True, False, True],
    ).reset_index(drop=True)

    return df_input_portfolio_groups


def fill_df_input_portfolio_group_assets(
    df_input_portfolio_group_assets: pd.DataFrame | None,
    assets_in_transaction_files: list[tuple[str, str]],
) -> pd.DataFrame:
    """
    Fills the portfolio group assets DataFrame.

    This function populates a DataFrame with assets from transaction files,
    matching them with their corresponding portfolio and group names.

    Parameters
    ----------
    df_input_portfolio_group_assets : pd.DataFrame
        The DataFrame to be filled.
    assets_in_transaction_files : list
        A list of tuples, where each tuple contains a portfolio name and an asset symbol.

    Returns
    -------
    pd.DataFrame
        The populated and sorted DataFrame.
    """
    portfolio_names = []
    asset_symbols = []
    group_names = []

    # Iterate through assets from transaction files
    for asset in assets_in_transaction_files:
        portfolio_name, asset_symbol = asset

        portfolio_names.append(portfolio_name)
        asset_symbols.append(asset_symbol)

        # If the input DataFrame is empty, append None for group name
        if (
            df_input_portfolio_group_assets is None
            or df_input_portfolio_group_assets.empty
        ):
            group_names.append(None)
        else:
            # Retrieve group name if it exists for the current asset
            group_name = df_input_portfolio_group_assets.loc[
                (df_input_portfolio_group_assets["portfolio_name"] == portfolio_name)
                & (df_input_portfolio_group_assets["asset_symbol"] == asset_symbol)
            ]["group_name"]
            group_names.append(None if group_name.empty else group_name.values[0])

    # Create and sort the final DataFrame
    df_input_portfolio_group_assets = (
        pd.DataFrame(
            {
                "portfolio_name": portfolio_names,
                "asset_symbol": asset_symbols,
                "group_name": group_names,
            },
            dtype=str,
        )
        .sort_values(by=["portfolio_name", "asset_symbol"])
        .reset_index(drop=True)
    )

    return df_input_portfolio_group_assets
