import streamlit as st

from streamlit_ui.core.session_management import initialize_session_id
from streamlit_ui.settings.utils import initialize_settings_session_variables


###################################################################
# PART 1: SESSION INITIALIZATION
###################################################################

# Initialize a new session ID if one doesn't exist
session_id = initialize_session_id()

# Initialize session state variables for settings if they haven't been set up
if "settings_session_variables_initialized" not in st.session_state:
    st.session_state["settings_session_variables_initialized"] = True
    initialize_settings_session_variables()


###################################################################
# PART 2: MAIN PAGE CONTENT
###################################################################

# Display welcome header
st.header(":sparkles: Welcome to CashFlower :money_with_wings: :sunflower:")

# Display session ID information
st.subheader(":id: Your session ID")
st.write(
    """:sunflower: Your session link is below - save it to resume your session later."""
)
st.code(f"https://cashflower.online/?session_id={session_id}", language=None)

st.divider()

# Display "How It Works" section
st.header(":sparkles: How It Works")

with st.expander("ℹ️ Quick Start Guide", expanded=True):
    st.markdown(
        """
        This page helps you get started with CashFlower. Here's the typical workflow:

        1.  **Familiarize yourself with the data format.** Use the template file linked below to see the required columns.  
            :sunflower: **Tip:** Your transaction files can contain additional columns; they will simply be ignored.
        2.  **Upload your data.** Navigate to the **Settings** page. In the **Transactions** tab, upload your transaction files.  
            :sunflower: **Important:** Uploaded data is temporary and only lasts for your current session (until you close or refresh the tab).
        3.  **Configure your settings.** In the **Settings** tab, either configure your analysis settings manually or upload a `settings.json` file from a previous session.
        4.  **Save your work.** To make your data and settings permanent for this session, you **must** click the **"Save settings and load data"** button in the sidebar. This will allow you to return to your analysis later using your session ID.
        5.  **Explore.** Once your data is loaded, you can explore the dashboards.

        For a hands-on example, check out the demo data below.
        """
    )

# Section for viewing the template file
st.subheader(":page_facing_up: View the template file")
st.write(
    """
    :sunflower: You can download it using the link below.  
    :sunflower: The template shows the required column names and data types for transaction files.
    """
)
st.link_button(
    "Template file on Google Drive",
    "https://docs.google.com/spreadsheets/d/1D1UPDEMOIYgjHCLJvjvrMlhq0v3ie5grjZa3lSH6Nb4/edit?usp=sharing",
    use_container_width=True,
)

# Section for checking out the demo data
st.subheader(":bulb: Check out the demo data")
st.write(
    """
    :sunflower: The demo data includes sample transaction files and a settings file, all ready to be uploaded to the application.  
    :sunflower: It allows you to explore the application's features and see how it works.
    
    **To get started with the demo data:**
    1. Click the button below to download the demo data files.
    2. Navigate to the **Settings** page from the sidebar.
    3. In the **Transactions** tab, upload the downloaded `.xlsx` transaction files.
    4. Switch to the **Settings** tab and upload the `settings.json` file.
    5. Finally, click the **Save settings and load data** button in the sidebar to load and process the data.
    """
)
st.link_button(
    "Folder with demo data on Google Drive",
    "https://drive.google.com/drive/folders/1uLS6gbX2ieore1bGZZ6mKqRa5DYx4zUg?usp=sharing",
    use_container_width=True,
)
