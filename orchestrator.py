import defopt
from enum import Enum
from configurations.get_config import get_new_stocks_list, get_stocks_list, get_historical_days, get_daily_tweet_count_for_info
from operations.query_data import query_y_finance
from operations.insert_data import InsertOperations
from operations.sentiment_analyzer import get_datewise_sentiment
import pandas as pd

stock_list = get_stocks_list()
daily_tweet_cnt_for_info = get_daily_tweet_count_for_info()
insert_operations = InsertOperations()
new_stock_list = get_new_stocks_list()
pd.options.display.max_columns = None


def _get_sentiment_info(stock, day_count):
    QUERY = '#'+stock.replace(".NS","")
    return get_datewise_sentiment(QUERY, daily_tweet_cnt_for_info, day_count)


def _insert_info():
    for stock in stock_list:
        stock_data = query_y_finance(stock)
        stock_data_info = stock_data.info
        # Get Stock info
        sentiment_df = _get_sentiment_info(stock, 1)
        if sentiment_df.empty:
            stock_data_info['sentiment'] = None
            stock_data_info['sentiment_perc'] = 0
        else:
            stock_data_info['sentiment'] = sentiment_df.at[0, 'Sentiment']
            stock_data_info['sentiment_perc'] = sentiment_df.at[0, 'Percentage']
        print("Adding Stock Details/Info to data-base!")
        insert_operations.insert_stock_info(info=stock_data_info)


def _get_sentiment_hist():
    for stock in stock_list:
        sentiment_df = _get_sentiment_info(stock, 1000)
        insert_operations.insert_sentiment_history(sentiment_df, stock)


def _insert_hist():
    for stock in new_stock_list:
        stock_data = query_y_finance(stock)
        hist = get_historical_days()
        print(hist)
        insert_operations.insert_stock_history(stock, history_df=stock_data.history(period="max"))


def _dump_ticker_info():
    insert_operations.dump_ticker_info()


class RunType(Enum):
    info = "info"
    hist = "hist"
    dump = "dump"
    s_hist = "s_hist"


def orchestrate(
        runtype: RunType
):
    print(runtype)
    if runtype == RunType.info:
        _insert_info()
    elif runtype == RunType.hist:
        _insert_hist()
    elif runtype == RunType.dump:
        _dump_ticker_info()
    elif runtype == RunType.s_hist:
        _get_sentiment_hist()
    else:
        print("INVALID OPTION!")
    insert_operations.close_db_connection()
    print("All Updates for stock information completed!!")


if __name__ == "__main__":
    defopt.run(orchestrate)