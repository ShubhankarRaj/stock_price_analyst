from configurations.get_config import get_new_stocks_list, get_stocks_list, get_historical_days
from operations.query_data import query_y_finance
from operations.insert_data import InsertOperations

stock_list = get_stocks_list()
insert_operations = InsertOperations()
new_stock_list = get_new_stocks_list()


def insert_info():
    for stock in stock_list:
        stock_data = query_y_finance(stock)
        print(stock_data.info)
        print("Adding Stock Details/Info!")
        insert_operations.insert_stock_info(info=stock_data.info)


def insert_hist():
    for stock in new_stock_list:
        stock_data = query_y_finance(stock)
        if not insert_operations.check_for_stock_already_present(symbol=stock):
            print("Fresh Stock!")
            insert_operations.insert_stock_history(history_df=stock_data.history(period=get_historical_days()))


insert_operations.close_db_connection()
print("All Updates for stock information completed!!")
