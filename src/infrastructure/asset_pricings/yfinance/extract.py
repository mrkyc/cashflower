from contextlib import redirect_stdout, redirect_stderr
import yfinance as yf
import io


def extract_data_yfinance(symbols, start_date):
    # download data from Yahoo Finance API for the ticker for the period from the last date in the table to the latest possible date
    # if the ticker table is empty, download data for the whole available period
    # redirect stdout and stderr to the buffer to avoid printing the data to the console
    buffer = io.StringIO()
    with redirect_stdout(buffer), redirect_stderr(buffer):
        df_data = yf.download(
            symbols, start=start_date, auto_adjust=False, group_by="ticker"
        )
    buffer.close()

    return df_data
