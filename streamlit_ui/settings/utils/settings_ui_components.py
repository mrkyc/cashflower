import streamlit as st
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile

from streamlit_ui.constants import *
from streamlit_ui.settings.utils.settings_session_variables_management import (
    load_portfolio_transactions,
    import_settings_from_file,
    save_settings_and_load_data,
    retrieve_settings_data,
    settings_data_exists,
    reset_settings,
    soft_database_reset,
    hard_database_reset,
)
from streamlit_ui.settings.utils.settings_input_validation import (
    validate_upload_files,
    validate_analysis_currency,
    validate_df_input,
    validate_df_input_portfolio_groups,
    validate_df_input_portfolio_group_assets,
)
from streamlit_ui.settings.utils.settings_df_input_filling import (
    fill_df_input_transaction_files,
    fill_df_input_portfolio_groups,
    fill_df_input_portfolio_group_assets,
)
from streamlit_ui.settings.utils.settings_other_utilities import (
    apply_data_editor_output,
    check_assets_in_transaction_files,
)


def display_transactions_tab_info() -> None:
    """Displays information about how to use the Transactions tab."""
    with st.expander("ℹ️ How to use this tab", expanded=False):
        st.write(
            """
            This tab is for managing your transaction data. You can upload, view, edit, add, and delete transaction files.

            **:warning: Important Note on Data Persistence:**  
            :sunflower: All data uploaded, added, or edited in this tab is **stored only for your current session**.  
            :sunflower: If you close or refresh your browser tab, these changes will be lost unless you save them.  
            :sunflower: To permanently save your data and settings for future use with your session ID, you must go to the **Settings** tab, configure everything, and then click the **"Save settings and load data"** button in the sidebar.

            **1. Upload Your Files:**  
            :sunflower: Use the "Upload your transaction files" button to upload one or more `.xlsx` or `.csv` files.  
            :sunflower: Ensure your files follow the structure of the provided template. You can have additional columns in your files; they will be ignored.  
            :sunflower: Uploading new files will add them to your current session.

            **2. Add or Delete Files:**  
            :sunflower: **Add:** If you need to start a new transaction list from scratch within the app, use the "Add empty transaction file" section. Provide a name and click "Add".  
            :sunflower: **Delete:** To remove files from your current session, select them from the multiselect box under "Delete transaction files" and click "Delete".

            **3. View and Edit Transactions:**  
            :sunflower: Select a file from the "Transaction file name" dropdown to see its contents in the table below.  
            :sunflower: You can directly edit the cells in the table. Changes are saved automatically (for the current session).  
            :sunflower: To add or delete rows, hover over the table to make a toolbar appear in the top-right corner. You can use it to add a row, or select one or more rows to delete them.
            """
        )


def display_upload_transaction_files_section() -> None:
    """Displays the section for uploading transaction files."""
    st.subheader(":card_file_box: Your transaction files")

    # Initialize a session state variable to control the file uploader widget's state
    if "clear_trx_files_uploader_widget" not in st.session_state:
        st.session_state["clear_trx_files_uploader_widget"] = False

    def uploader_on_change():
        """Callback function to process uploaded transaction files."""
        uploader_key = f"trx_files_uploader_widget{st.session_state.get('clear_trx_files_uploader_widget')}"
        uploaded_files = st.session_state.get(uploader_key, [])

        if validate_upload_files(uploaded_files):
            for uploaded_file in uploaded_files:
                loaded_transactions = load_portfolio_transactions(uploaded_file)
                file_name = uploaded_file.name.lower()
                st.session_state["transactions"][file_name] = loaded_transactions
            st.session_state["clear_trx_files_uploader_widget"] = True

    # File uploader for transaction files
    st.file_uploader(
        "Upload your transaction files",
        type=["xlsx", "csv"],
        accept_multiple_files=True,
        key=f"trx_files_uploader_widget{st.session_state.get('clear_trx_files_uploader_widget')}",
        on_change=uploader_on_change,
    )
    st.session_state["clear_trx_files_uploader_widget"] = False


def display_add_delete_transaction_files_section() -> None:
    """Displays the section for adding or deleting transaction files."""
    cols = st.columns(2)

    with cols[0]:
        st.subheader(":heavy_plus_sign: Add empty transaction file")

        # Initialize session state for new file name input
        if "clear_new_transaction_file_name_widget" not in st.session_state:
            st.session_state["clear_new_transaction_file_name_widget"] = False

        text_input_key = f"new_transaction_file_name_widget{st.session_state.get('clear_new_transaction_file_name_widget')}"
        new_file_name = st.text_input(
            "File name",
            max_chars=50,
            key=text_input_key,
            help="""Type the name of the new empty transaction file.""",
        )
        st.session_state["clear_new_transaction_file_name_widget"] = False

        def add_transaction_file_callback():
            """Callback function to add a new empty transaction file."""
            new_file_name_from_widget = st.session_state.get(text_input_key)
            if not new_file_name_from_widget:
                return

            df = pd.DataFrame(
                columns=[
                    "date",
                    "asset_symbol",
                    "transaction_type",
                    "quantity",
                    "transaction_value",
                    "fee_amount",
                    "tax_amount",
                ]
            )
            st.session_state["transactions"][new_file_name_from_widget.lower()] = df
            st.session_state["clear_new_transaction_file_name_widget"] = True

        # Button to add the new file
        st.button(
            "Add empty file",
            on_click=add_transaction_file_callback,
            disabled=not new_file_name,
            use_container_width=True,
        )

    with cols[1]:
        st.subheader(":heavy_minus_sign: Delete transaction files")

        # Multiselect to choose which files to delete
        keys_to_delete = st.multiselect(
            "Select transaction files to delete",
            options=st.session_state.get("transactions", {}).keys(),
            help="""Select the transaction files you want to delete.  
                    The files will be removed from the session state and will not be available for analysis.""",
        )

        # Function to remove selected transaction files
        def remove_transaction_files(keys_to_delete: list[str]) -> None:
            for key in keys_to_delete:
                st.session_state["transactions"].pop(key)

        # Button to delete the selected files
        st.button(
            "Delete",
            on_click=remove_transaction_files,
            args=(keys_to_delete,),
            use_container_width=True,
        )

    # Stop if no transaction files are provided
    if not st.session_state["transactions"]:
        st.error("Please provide transaction files.")
        st.stop()


def get_transaction_file_to_edit() -> str:
    """Displays a selectbox to choose a transaction file to edit."""
    dict_transactions = st.session_state["transactions"]
    return st.selectbox("Transaction file name", dict_transactions.keys())


def prepare_transactions_for_editing(df_transactions: pd.DataFrame) -> pd.DataFrame:
    """Prepares the transaction DataFrame for editing."""
    df_transactions["date"] = pd.to_datetime(df_transactions["date"]).dt.date
    df_transactions = df_transactions.sort_values(
        "date", ascending=False, ignore_index=True
    )
    return df_transactions.fillna(
        {
            "asset_symbol": "",
            "quantity": 0.0,
            "transaction_value": 0.0,
            "fee_amount": 0.0,
            "tax_amount": 0.0,
        }
    )


def display_transactions_data_editor(
    df_transactions: pd.DataFrame, file_name: str
) -> None:
    """Displays the data editor for transactions."""
    st.data_editor(
        df_transactions,
        use_container_width=True,
        hide_index=True,
        column_config={
            "date": st.column_config.DateColumn(
                "Date",
                help="Type the date of the transaction in YYYY-MM-DD format.",
                required=True,
            ),
            "asset_symbol": st.column_config.TextColumn(
                "Asset symbol",
                help="Type the asset symbol for the transaction.",
                max_chars=10,
                validate="^.+$",
            ),
            "transaction_type": st.column_config.SelectboxColumn(
                "Transaction type",
                help="Select the type of transaction.",
                required=True,
                options=[
                    "buy",
                    "sell",
                    "deposit",
                    "withdrawal",
                    "distribution",
                    "interest",
                    "fee",
                ],
            ),
            "quantity": st.column_config.NumberColumn(
                "Quantity",
                help="Type the quantity of the asset in the transaction.",
                min_value=0.0,
            ),
            "transaction_value": st.column_config.NumberColumn(
                "Transaction value",
                help="Type the value of the transaction in the analysis currency.",
                min_value=0.0,
            ),
            "fee_amount": st.column_config.NumberColumn(
                "Fee amount",
                help="Type the fee amount for the transaction in the analysis currency.",
                min_value=0.0,
            ),
            "tax_amount": st.column_config.NumberColumn(
                "Tax amount",
                help="Type the tax amount for the transaction in the analysis currency.",
                min_value=0.0,
            ),
        },
        num_rows="dynamic",
        disabled=[0],
        key="df_transactions_widget",
        on_change=lambda: st.session_state["transactions"].update(
            {
                file_name: apply_data_editor_output(
                    df_transactions,
                    st.session_state.get("df_transactions_widget"),
                )
            }
        ),
    )


def display_edit_transactions_section() -> None:
    """Displays the section for editing transactions."""
    st.subheader(":pencil: Edit transactions")
    transaction_file_name = get_transaction_file_to_edit()
    df_transactions = st.session_state["transactions"].get(transaction_file_name)
    df_transactions = prepare_transactions_for_editing(df_transactions)
    display_transactions_data_editor(df_transactions, transaction_file_name)


def display_settings_tab_info() -> None:
    """Displays information about how to use the Settings tab."""
    with st.expander("ℹ️ How to use this tab", expanded=False):
        st.write(
            """
            This tab allows you to configure all the necessary settings for your analysis. Once configured, you must save them to be able to see the dashboards.

            **1. Load Settings from File:**  
            :sunflower: If you have a previously saved `settings.json` file, you can upload it here to quickly restore your configuration.

            **2. General Settings:**  
            :sunflower: **Analysis Currency:** Set the three-letter currency code (e.g., USD, EUR) for your reports.  
            :sunflower: **OHLC Assets/Currencies:** Choose the price type (Open, High, Low, Close, or an average) to be used for asset and currency valuations.

            **3. Set Transaction Files:**  
            :sunflower: For each uploaded transaction file, assign the correct currency and a portfolio name.  
            :sunflower: You can group multiple files under one portfolio by giving them the same portfolio name.

            **4. Define Portfolio Groups:**  
            :sunflower: Create custom groups for your assets (e.g., "Stocks", "Bonds", "Crypto").  
            :sunflower: Assign a target weight (in %) to each group. The sum of weights for each portfolio must equal 100%.

            **5. Match Assets to Portfolio Groups:**  
            :sunflower: Assign each asset from your transaction files to one of the portfolio groups you just defined.

            **:warning: Important Final Step:**  
            :sunflower: After you have configured everything, you **must** click the **"Save settings and load data"** button in the sidebar.  
            :sunflower: This action validates your settings, saves them permanently for your session ID, and loads all the data for analysis. Only after this step is successfully completed will you be able to access the dashboards.
            """
        )


def display_load_settings_from_file_section() -> None:
    """Displays the section for loading settings from a file."""
    with st.container(border=True):
        st.subheader(
            ":page_facing_up: Load settings from file",
            help="""Upload settings file to load settings from it.  
                    The settings file should be in JSON format.""",
        )

        # Initialize session state for settings file uploader
        if "clear_settings_file_uploader_widget" not in st.session_state:
            st.session_state["clear_settings_file_uploader_widget"] = False

        # File uploader for settings file
        uploaded_settings_file = st.file_uploader(
            "Load settings file",
            type=["json"],
            accept_multiple_files=False,
            key=f"settings_file_uploader_widget{st.session_state.get('clear_settings_file_uploader_widget')}",
            help="""Upload settings file to load settings from it.  
                    The settings file should be in JSON format.""",
            label_visibility="collapsed",
        )
        st.session_state["clear_settings_file_uploader_widget"] = False

        # Load settings from the uploaded file
        if uploaded_settings_file:
            import_settings_from_file(uploaded_settings_file)
            st.session_state["clear_settings_file_uploader_widget"] = True
            st.rerun()


def display_general_settings_section() -> bool:
    """Displays the general settings section and returns analysis_currency_validation."""
    with st.container(border=True):
        st.subheader(":gear: General settings")

        # Input for analysis currency
        analysis_currency = st.text_input(
            "Analysis currency",
            value=st.session_state.get("analysis_currency").upper(),
            max_chars=3,
            key="analysis_currency_widget",
            help="""Type the currency in the text box.  
                    The currency should be in ISO 4217 format (3 letters).""",
            on_change=lambda: st.session_state.update(
                {
                    "analysis_currency": st.session_state.get(
                        "analysis_currency_widget"
                    ).lower()
                }
            ),
        ).lower()
        analysis_currency_validation = validate_analysis_currency(analysis_currency)

        # Segmented control for OHLC assets
        st.segmented_control(
            "OHLC assets",
            OHLC_OPTIONS,
            default=st.session_state.get("ohlc_assets"),
            format_func=lambda x: x.upper(),
            key="ohlc_assets_widget",
            help="""Select the type of asset pricing data you want to use.  
                    You have the following options:  
                    - One of the simple OHLC (Open, High, Low, Close) prices.  
                    - Average (Open + High + Low + Close) / 4.  
                    - Typical price (Open + High + Low) / 3.  
                    - Weighted close price (2 * Close + High + Low) / 4.""",
            on_change=lambda: st.session_state.update(
                {"ohlc_assets": st.session_state.get("ohlc_assets_widget")}
            ),
        )

        # Segmented control for OHLC currencies
        st.segmented_control(
            "OHLC currencies",
            OHLC_OPTIONS,
            default=st.session_state.get("ohlc_currencies"),
            format_func=lambda x: x.upper(),
            key="ohlc_currencies_widget",
            help="""Select the type of currency pricing data you want to use.  
                    You have the following options:  
                    - One of the simple OHLC (Open, High, Low, Close) prices.  
                    - Average (Open + High + Low + Close) / 4.  
                    - Typical price (Open + High + Low) / 3.  
                    - Weighted close price (2 * Close + High + Low) / 4.""",
            on_change=lambda: st.session_state.update(
                {"ohlc_currencies": st.session_state.get("ohlc_currencies_widget")}
            ),
        )
    return analysis_currency_validation


def display_transaction_files_settings_section() -> pd.DataFrame:
    """Displays the transaction files settings section and returns df_input_transaction_files_validation."""
    with st.container(border=True):
        st.subheader(":card_file_box: Set transaction files")

        # Get transaction files settings from session state
        df_input_transaction_files = st.session_state.get("df_input_transaction_files")

        # Fill the transaction files DataFrame if not loaded from the database
        df_input_transaction_files = fill_df_input_transaction_files(
            df_input_transaction_files, st.session_state["transactions"]
        )
        st.session_state["df_input_transaction_files"] = df_input_transaction_files

        # Data editor for transaction files settings
        df_input_transaction_files = st.data_editor(
            df_input_transaction_files,
            height=len(df_input_transaction_files) * 35 + 38,
            use_container_width=True,
            hide_index=True,
            column_config={
                "file_name": st.column_config.TextColumn(
                    "File name",
                    width="large",
                    help="Name of the uploaded transaction file",
                    disabled=True,
                ),
                "currency": st.column_config.TextColumn(
                    "Currency",
                    width="small",
                    help="Type the currency of the transaction file",
                    required=True,
                    max_chars=3,
                    validate="^[a-zA-Z]{3}$",
                ),
                "portfolio_name": st.column_config.TextColumn(
                    "Portfolio name",
                    width="large",
                    help="""Type the name of the portfolio for the corresponding transaction file.  
                            The name will be used to group the transactions in the portfolio.  
                            It can be the same for all transaction files or different for each file.""",
                    required=True,
                    max_chars=30,
                    validate="^.+$",
                ),
            },
            key="df_input_transaction_files_widget",
            on_change=lambda: st.session_state.update(
                {
                    "df_input_transaction_files": apply_data_editor_output(
                        df_input_transaction_files,
                        st.session_state.get("df_input_transaction_files_widget"),
                    )
                }
            ),
        )

        # Validate transaction files settings
        df_input_transaction_files_validation = validate_df_input(
            df_input_transaction_files
        )
    return df_input_transaction_files_validation


def display_portfolio_groups_settings_section() -> pd.DataFrame:
    """Displays the portfolio groups settings section and returns df_input_portfolio_groups_validation."""
    with st.container(border=True):
        st.subheader(":books: Define portfolio groups")

        # Get portfolio groups settings from session state
        df_input_portfolio_groups = st.session_state.get("df_input_portfolio_groups")

        # Get unique portfolio names
        df_input_transaction_files = st.session_state.get("df_input_transaction_files")
        portfolio_names_unique = df_input_transaction_files["portfolio_name"].unique()

        # Fill the portfolio groups DataFrame
        df_input_portfolio_groups = fill_df_input_portfolio_groups(
            df_input_portfolio_groups, portfolio_names_unique
        )
        st.session_state["df_input_portfolio_groups"] = df_input_portfolio_groups

        # Data editor for portfolio groups settings
        df_input_portfolio_groups = st.data_editor(
            df_input_portfolio_groups,
            height=len(df_input_portfolio_groups) * 35 + 35 + 38,
            use_container_width=True,
            hide_index=True,
            disabled=[0],
            column_config={
                "portfolio_name": st.column_config.SelectboxColumn(
                    "Portfolio name",
                    width="large",
                    help="Select the portfolio name for which the group is defined.",
                    options=portfolio_names_unique,
                    required=True,
                ),
                "group_name": st.column_config.TextColumn(
                    "Group name",
                    width="large",
                    help="Type the name of the portfolio group.",
                    required=True,
                    max_chars=30,
                    validate="^.+$",
                ),
                "group_weight": st.column_config.NumberColumn(
                    "Group weight",
                    width="small",
                    help="""Type the weight of the portfolio group in the portfolio.  
                            The weight should be between 0 and 100.  
                            The sum of the weights of all portfolio groups in a portfolio should be equal to 100.""",
                    required=True,
                    min_value=0,
                    max_value=100,
                    step=0.1,
                ),
            },
            num_rows="dynamic",
            key="df_input_portfolio_groups_widget",
            on_change=lambda: st.session_state.update(
                {
                    "df_input_portfolio_groups": apply_data_editor_output(
                        df_input_portfolio_groups,
                        st.session_state.get("df_input_portfolio_groups_widget"),
                    )
                }
            ),
        )

        # Validate portfolio groups settings
        df_input_portfolio_groups_validation = validate_df_input_portfolio_groups(
            df_input_portfolio_groups
        )
    return df_input_portfolio_groups_validation


def display_portfolio_group_assets_settings_section() -> pd.DataFrame:
    """Displays the portfolio group assets settings section and returns df_input_portfolio_group_assets_validation."""
    with st.container(border=True):
        st.subheader(":link: Match assets to portfolio groups")

        # Get portfolio group assets settings from session state
        df_input_portfolio_group_assets = st.session_state.get(
            "df_input_portfolio_group_assets"
        )

        # Check assets in transaction files
        df_input_transaction_files = st.session_state.get("df_input_transaction_files")
        assets_in_transaction_files = check_assets_in_transaction_files(
            df_input_transaction_files, st.session_state["transactions"]
        )

        # Fill the portfolio group assets DataFrame
        df_input_portfolio_group_assets = fill_df_input_portfolio_group_assets(
            df_input_portfolio_group_assets, assets_in_transaction_files
        )
        st.session_state["df_input_portfolio_group_assets"] = (
            df_input_portfolio_group_assets
        )

        # Data editor for portfolio group assets settings
        df_input_portfolio_group_assets = st.data_editor(
            df_input_portfolio_group_assets,
            height=len(df_input_portfolio_group_assets) * 35 + 38,
            use_container_width=True,
            hide_index=True,
            column_config={
                "portfolio_name": st.column_config.TextColumn(
                    "Portfolio name",
                    help="Portfolio name for a given asset.",
                    disabled=True,
                ),
                "asset_symbol": st.column_config.TextColumn(
                    "Asset symbol",
                    help="Asset included in the portfolio.",
                    disabled=True,
                ),
                "group_name": st.column_config.SelectboxColumn(
                    "Group name",
                    help="Select the group name for a given asset.",
                    options=st.session_state.get("df_input_portfolio_groups")[
                        "group_name"
                    ].unique(),
                    required=True,
                ),
            },
            key="df_input_portfolio_group_assets_widget",
            on_change=lambda: st.session_state.update(
                {
                    "df_input_portfolio_group_assets": apply_data_editor_output(
                        df_input_portfolio_group_assets,
                        st.session_state.get("df_input_portfolio_group_assets_widget"),
                    ),
                }
            ),
        )

        # Validate portfolio group assets settings
        df_input_portfolio_group_assets_validation = (
            validate_df_input_portfolio_group_assets(
                df_input_portfolio_group_assets,
                st.session_state.get("df_input_portfolio_groups"),
            )
        )
    return df_input_portfolio_group_assets_validation


def display_save_export_section(
    analysis_currency_validation: bool,
    df_input_transaction_files_validation: bool,
    df_input_portfolio_groups_validation: bool,
    df_input_portfolio_group_assets_validation: bool,
) -> None:
    """Displays the save and export settings section in the sidebar."""
    st.header(":material/build: Settings management")

    save_settings_and_load_data_button_disabled = (
        not analysis_currency_validation
        or not df_input_transaction_files_validation
        or not df_input_portfolio_groups_validation
        or not df_input_portfolio_group_assets_validation
    )

    if st.button(
        ":material/save: Save settings and load data",
        on_click=save_settings_and_load_data,
        disabled=save_settings_and_load_data_button_disabled,
        use_container_width=True,
    ):
        pass

    st.download_button(
        label=":material/package: Export settings to file",
        data=retrieve_settings_data(),
        file_name="settings.json",
        mime="application/json",
        disabled=not settings_data_exists(),
        use_container_width=True,
    )


def display_reset_section() -> None:
    """Displays the reset settings section in the sidebar."""
    with st.expander(":material/undo: Reset settings"):
        st.button(
            "Confirm reset",
            on_click=reset_settings,
            type="primary",
            use_container_width=True,
        )


def display_database_management_section() -> None:
    """Displays the database management section in the sidebar."""
    st.header(":material/database: Database management")

    with st.expander(":material/restore: Soft database reset"):
        st.button(
            "Confirm soft reset",
            on_click=soft_database_reset,
            type="primary",
            use_container_width=True,
        )

    with st.expander(":material/delete_forever: Hard database reset"):
        st.button(
            "Confirm hard reset",
            on_click=hard_database_reset,
            type="primary",
            use_container_width=True,
        )


def display_sidebar_settings_management_section(
    analysis_currency_validation: bool,
    df_input_transaction_files_validation: bool,
    df_input_portfolio_groups_validation: bool,
    df_input_portfolio_group_assets_validation: bool,
) -> None:
    """Displays the sidebar settings management section."""
    display_save_export_section(
        analysis_currency_validation,
        df_input_transaction_files_validation,
        df_input_portfolio_groups_validation,
        df_input_portfolio_group_assets_validation,
    )
    display_reset_section()
    display_database_management_section()
