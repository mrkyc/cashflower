import pandas as pd


def apply_data_editor_output(
    df: pd.DataFrame, dict_data_editor_output: dict
) -> pd.DataFrame:
    """
    Applies changes from Streamlit's data_editor to a DataFrame.

    This function takes a DataFrame and a dictionary of changes from the
    data_editor widget and applies the edits, additions, and deletions.

    Parameters
    ----------
    df : pd.DataFrame
        The original DataFrame.
    dict_data_editor_output : dict
        The dictionary of changes from `st.data_editor`.

    Returns
    -------
    pd.DataFrame
        The updated DataFrame.
    """
    updated_data = df.copy()

    # Apply edited rows
    if "edited_rows" in dict_data_editor_output:
        for index, inner_dict in dict_data_editor_output["edited_rows"].items():
            for column, value in inner_dict.items():
                updated_data.loc[int(index), column] = value

    # Apply added rows
    if "added_rows" in dict_data_editor_output:
        for row in dict_data_editor_output["added_rows"]:
            updated_data.loc[len(updated_data)] = row

    # Apply deleted rows
    if "deleted_rows" in dict_data_editor_output:
        updated_data = updated_data.drop(index=dict_data_editor_output["deleted_rows"])

    # Convert all string columns to lowercase
    return updated_data.map(lambda x: x.lower() if isinstance(x, str) else x)


def check_assets_in_transaction_files(
    df_input_transaction_files: pd.DataFrame, dict_transactions: dict[str, pd.DataFrame]
) -> set[tuple[str, str]]:
    """
    Identifies all unique assets within the transaction files.

    This function iterates through transaction files, extracts unique asset symbols,
    and pairs them with their corresponding portfolio name.

    Parameters
    ----------
    df_input_transaction_files : pd.DataFrame
        A DataFrame containing transaction file metadata.
    dict_transactions : dict
        A dictionary of DataFrames, where keys are file names.

    Returns
    -------
    set
        A set of tuples, where each tuple is (portfolio_name, asset_symbol).
    """
    set_of_asset_symbols = set()

    # Iterate through each transaction file
    for row in df_input_transaction_files.itertuples():
        file_name = row.file_name
        portfolio_name = row.portfolio_name
        df_transactions = dict_transactions.get(file_name)

        # Get unique, non-null asset symbols
        asset_symbols = df_transactions["asset_symbol"].dropna().unique().tolist()

        # Create a list of (portfolio_name, asset_symbol) tuples
        portfolio_asset_symbols = [
            (portfolio_name, asset_symbol.lower())
            for asset_symbol in asset_symbols
            if asset_symbol != ""
        ]
        set_of_asset_symbols.update(portfolio_asset_symbols)

    return set_of_asset_symbols
