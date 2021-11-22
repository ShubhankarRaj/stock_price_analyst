import yfinance as yf


def query_y_finance(symbol):
    return yf.Ticker(symbol)
