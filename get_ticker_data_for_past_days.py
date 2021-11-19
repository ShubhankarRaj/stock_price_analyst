import yfinance as yf
import pandas as pd
from stock_symbols import stock_symbols


pd.set_option('display.max_columns', None)
for symbol in stock_symbols:
    symbol = stock_symbols.get(symbol)
    yahoo_finance_api_data = yf.Ticker(symbol)

    # print(yahoo_finance_api_data.info.values())
    # Get the complete information and save in the DB in ticker_data table
    print(yahoo_finance_api_data.info)
    # data = tuple(yahoo_finance_api_data.info.values())
    # print(len(data))
    # insert_tick_info(data)

    # Get historical market data
    # historical_data = yahoo_finance_api_data.history(period="20d")
    # insert_dividend_split_info(symbol, historical_data)


