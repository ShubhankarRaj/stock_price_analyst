import defopt
from enum import Enum
from configurations.get_config import get_new_stocks_list, get_stocks_list, get_historical_days
from operations.query_data import query_y_finance
from operations.insert_data import InsertOperations


stock_list = get_stocks_list()
insert_operations = InsertOperations()
new_stock_list = get_new_stocks_list()

def _insert_info():
    for stock in stock_list:
        stock_data = query_y_finance(stock)
        print(stock_data.info)
        print("Adding Stock Details/Info!")
        insert_operations.insert_stock_info(info=stock_data.info)


def _insert_hist():
    for stock in new_stock_list:
        stock_data = query_y_finance(stock)
        hist = get_historical_days()
        print(hist)
        insert_operations.insert_stock_history(stock, history_df=stock_data.history(period="max"))


class RunType(Enum):
    info = "info"
    hist = "hist"


def orchestrate(
        runtype: RunType
):
    print(runtype)
    if runtype == RunType.info:
        _insert_info()
    elif runtype ==RunType.hist:
        _insert_hist()
    else:
        print("INVALID OPTION!")
    insert_operations.close_db_connection()
    print("All Updates for stock information completed!!")


if __name__ == "__main__":
    defopt.run(orchestrate)