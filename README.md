# Cashflower

Portfolio analytics platform that processes transaction data and user settings to generate performance metrics, asset allocation insights, and cash flow analysis with API and web interface.

## Demo

A live demo version is currently deployed on a VPS using:
- Docker containerization
- nginx as reverse proxy
- SQLite database (chosen for limited resources and development simplicity) with custom extensions ([XIRR](https://github.com/mrkyc/sqlite-xirr-extension), [Standard Deviation](https://github.com/mrkyc/sqlite-stddev-extension))
- FastAPI backend with SQLAlchemy ORM
- Streamlit frontend interface

**Demo URL:** [https://cashflower.online](https://cashflower.online)

*Note: Project is still in active development. Source code will be published once the codebase is properly organized and refactored.*
