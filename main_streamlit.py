import streamlit as st
import logging
import atexit
import shutil

logging.basicConfig(level=logging.INFO)


def main():
    # atexit.register(shutil.rmtree, "databases", ignore_errors=True)

    # st.logo() TODO: Add logo

    st.set_page_config(layout="wide")

    pages = {
        "Dashboard Pages": [
            st.Page(
                "streamlit_ui/dashboards/performance_status.py",
                title="Performance Status",
                icon=":material/speed:",
            ),
            st.Page(
                "streamlit_ui/dashboards/performance_overview.py",
                title="Performance Overview",
                icon=":material/query_stats:",
            ),
            st.Page(
                page="streamlit_ui/dashboards/portfolio_group_weights.py",
                title="Portfolio Group Weights",
                icon=":material/balance:",
            ),
            st.Page(
                page="streamlit_ui/dashboards/components_comparison.py",
                title="Components Comparison",
                icon=":material/compare_arrows:",
            ),
            st.Page(
                page="streamlit_ui/dashboards/all_data_table.py",
                title="All Data Table",
                icon=":material/table:",
            ),
            st.Page(
                page="streamlit_ui/dashboards/monte_carlo_simulation.py",
                title="Monte Carlo Simulation",
                icon=":material/event_upcoming:",
            ),
        ],
        "Settings Pages": [
            st.Page(
                page="streamlit_ui/settings/entry_page.py",
                title="Entry Page",
                icon=":material/home:",
                default=True,
            ),
            st.Page(
                page="streamlit_ui/settings/settings.py",
                title="Global Settings",
                icon=":material/settings:",
            ),
        ],
    }

    st.navigation(pages).run()


if __name__ == "__main__":
    main()
