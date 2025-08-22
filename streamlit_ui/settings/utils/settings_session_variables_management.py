import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import pandas as pd
import requests
import json

from streamlit_ui.constants import *


def get_settings_data(session_id: str) -> dict | None:
    """
    Retrieves settings data from the API for a given session ID.

    Parameters
    ----------
    session_id : str
        The session ID for which to retrieve settings.

    Returns
    -------
    dict | None
        A dictionary containing settings data if the request is successful,
        otherwise None.
    """
    response = requests.get(
        f"{URL}/settings",
        headers={HEADER_SESSION_ID: session_id},
    )
    return response.json() if response.ok else None


def initialize_settings_session_variables() -> None:
    """
    Initializes settings in the session state.

    Tries to load settings from the database. If that fails, it resets
    the settings to their default values.
    """
    settings_data = get_settings_data(st.session_state.get("session_id"))
    if settings_data is not None:
        load_settings_from_database(settings_data)
    else:
        reset_settings()


def settings_data_exists() -> bool:
    """
    Checks if settings data exists in the database for the current session.

    Returns
    -------
    bool
        True if settings data exists, False otherwise.
    """
    return get_settings_data(st.session_state.get("session_id")) is not None


def retrieve_settings_data() -> str:
    """
    Retrieves current settings from the session state and formats them as a JSON string.

    Returns
    -------
    str
        A JSON string representing the current settings.
    """
    settings = {
        "analysis_currency": st.session_state.get("analysis_currency"),
        "ohlc_assets": st.session_state.get("ohlc_assets"),
        "ohlc_currencies": st.session_state.get("ohlc_currencies"),
        "transaction_files": st.session_state.get("df_input_transaction_files").to_dict(
            orient="list"
        ),
        "portfolio_groups": st.session_state.get("df_input_portfolio_groups").to_dict(
            orient="list"
        ),
        "portfolio_group_assets": st.session_state.get(
            "df_input_portfolio_group_assets"
        ).to_dict(orient="list"),
    }
    return json.dumps(settings, indent=4)


def load_settings_from_database(settings_data: dict) -> None:
    """
    Loads settings from a dictionary (from the database) into the session state.

    Parameters
    ----------
    settings_data : dict
        A dictionary containing the settings data.
    """
    if settings_data:
        st.session_state["analysis_currency"] = settings_data["analysis_currency"]
        st.session_state["ohlc_assets"] = settings_data["ohlc_assets"]
        st.session_state["ohlc_currencies"] = settings_data["ohlc_currencies"]
        st.session_state["df_input_transaction_files"] = pd.DataFrame.from_dict(
            settings_data["transaction_files"], dtype=str
        )

        dict_transactions = {}
        for item in settings_data.get("transactions", {}).get("items", []):
            file_name = item.get("file_name")
            df = pd.DataFrame.from_dict(item.get("transaction_data", {}))
            df = df.astype(
                {
                    "date": "object",
                    "asset_symbol": "object",
                    "transaction_type": "object",
                    "quantity": "float",
                    "transaction_value": "float",
                    "fee_amount": "float",
                    "tax_amount": "float",
                }
            )
            df["date"] = pd.to_datetime(df["date"])
            dict_transactions[file_name] = df.sort_values("date", ascending=False)

        st.session_state["transactions"] = dict_transactions
        st.session_state["df_input_portfolio_groups"] = pd.DataFrame.from_dict(
            settings_data["portfolio_groups"], dtype=str
        )
        st.session_state["df_input_portfolio_group_assets"] = pd.DataFrame.from_dict(
            settings_data["portfolio_group_assets"], dtype=str
        )


def import_settings_from_file(uploaded_settings_file: UploadedFile) -> None:
    """
    Imports settings from an uploaded JSON file into the session state.

    Parameters
    ----------
    uploaded_settings_file : UploadedFile
        The file uploaded by the user.
    """
    settings_data = json.loads(uploaded_settings_file.read().decode("utf-8"))
    st.session_state["analysis_currency"] = settings_data["analysis_currency"]
    st.session_state["ohlc_assets"] = settings_data["ohlc_assets"]
    st.session_state["ohlc_currencies"] = settings_data["ohlc_currencies"]
    st.session_state["df_input_transaction_files"] = pd.DataFrame.from_dict(
        settings_data["transaction_files"], dtype=str
    )
    st.session_state["df_input_portfolio_groups"] = pd.DataFrame.from_dict(
        settings_data["portfolio_groups"], dtype=str
    )
    st.session_state["df_input_portfolio_group_assets"] = pd.DataFrame.from_dict(
        settings_data["portfolio_group_assets"], dtype=str
    )


def load_portfolio_transactions(uploaded_file: UploadedFile) -> pd.DataFrame:
    """
    Loads portfolio transactions from an uploaded file (XLSX or CSV).

    Parameters
    ----------
    uploaded_file : UploadedFile
        The file containing transaction data.

    Returns
    -------
    pd.DataFrame
        A DataFrame with the loaded and formatted transaction data.
    """
    extension = uploaded_file.name.lower().split(".")[-1]
    dtype = {
        "date": str,
        "asset_symbol": str,
        "transaction_type": str,
        "quantity": float,
        "transaction_value": float,
        "fee_amount": float,
        "tax_amount": float,
    }

    if extension == "xlsx":
        df = pd.read_excel(uploaded_file, usecols=dtype.keys(), dtype=dtype)
    elif extension == "csv":
        df = pd.read_csv(uploaded_file, usecols=dtype.keys(), dtype=dtype)
    else:
        raise ValueError(f"Unsupported file type: {extension}")

    df = df.map(lambda x: x.lower() if isinstance(x, str) else x)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=False)
    df["asset_symbol"] = df["asset_symbol"].fillna("")
    df[["quantity", "transaction_value", "fee_amount", "tax_amount"]] = df[
        ["quantity", "transaction_value", "fee_amount", "tax_amount"]
    ].abs()

    return df


def save_settings_and_load_data() -> None:
    """
    Saves current settings and triggers data processing.

    This function sends the current settings to the backend to be saved,
    and then initiates the data processing pipeline.
    It also increments a session-specific counter to force a refresh of cached data.
    """
    # Increment refresh counter to invalidate session-specific cache
    if "refresh_counter" not in st.session_state:
        st.session_state.refresh_counter = 0
    st.session_state.refresh_counter += 1

    transactions_serializable = []
    for file_name, df in st.session_state.get("transactions", {}).items():
        df_copy = df.copy()
        df_copy["date"] = pd.to_datetime(df_copy["date"]).dt.strftime("%Y-%m-%d")
        df_copy = df_copy.fillna(
            {
                "asset_symbol": "",
                "quantity": 0.0,
                "transaction_value": 0.0,
                "fee_amount": 0.0,
                "tax_amount": 0.0,
            }
        )
        transactions_serializable.append(
            {
                "file_name": file_name,
                "transaction_data": df_copy.to_dict(orient="list"),
            }
        )

    settings = {
        "analysis_currency": st.session_state.get("analysis_currency"),
        "ohlc_assets": st.session_state.get("ohlc_assets"),
        "ohlc_currencies": st.session_state.get("ohlc_currencies"),
        "transaction_files": st.session_state.get("df_input_transaction_files").to_dict(
            orient="list"
        ),
        "transactions": {"items": transactions_serializable},
        "portfolio_groups": st.session_state.get("df_input_portfolio_groups").to_dict(
            orient="list"
        ),
        "portfolio_group_assets": st.session_state.get(
            "df_input_portfolio_group_assets"
        ).to_dict(orient="list"),
    }

    response = requests.post(
        f"{URL}/settings",
        json=settings,
        headers={HEADER_SESSION_ID: st.session_state.get("session_id")},
    )
    if not response.ok:
        st.error(f"Failed to save settings. Error: {response.text}")
        st.stop()

    response = requests.post(
        f"{URL}/run-processing",
        headers={HEADER_SESSION_ID: st.session_state.get("session_id")},
    )
    if not response.ok:
        st.error(f"Failed to run data processing. Error: {response.text}")
        st.stop()


def reset_settings() -> None:
    """
    Resets all settings in the session state to their default values.
    """
    st.session_state["analysis_currency"] = "USD"
    st.session_state["ohlc_assets"] = OHLC_OPTIONS[3].lower()
    st.session_state["ohlc_currencies"] = OHLC_OPTIONS[3].lower()
    st.session_state["df_input_transaction_files"] = pd.DataFrame(
        {"file_name": [], "currency": [], "portfolio_name": []}, dtype=str
    )
    st.session_state["transactions"] = {}
    st.session_state["df_input_portfolio_groups"] = pd.DataFrame(
        {"portfolio_name": [], "group_name": [], "group_weight": []}, dtype=str
    )
    st.session_state["df_input_portfolio_group_assets"] = pd.DataFrame(
        {"portfolio_name": [], "asset_symbol": [], "group_name": []}, dtype=str
    )


def soft_database_reset() -> None:
    """
    Performs a soft reset of the database.

    This resets the data processing checkpoint, forcing a full reload of transformations.
    """
    response = requests.post(
        f"{URL}/reset-checkpoint-date",
        headers={HEADER_SESSION_ID: st.session_state.get("session_id")},
    )
    if response.ok:
        st.success("Database soft reset successful.")
    else:
        st.error("Failed to reset checkpoint date.")


def hard_database_reset() -> None:
    """
    Performs a hard reset of the user's data in the database.

    This action truncates all tables associated with the user's session.
    """
    response = requests.post(
        f"{URL}/reset-user",
        headers={HEADER_SESSION_ID: st.session_state.get("session_id")},
    )
    if response.ok:
        st.success("User data hard reset successful.")
    else:
        st.error("Failed to reset user data.")
