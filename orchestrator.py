from configurations.get_config import get_stocks_list, get_historical_days
from operations.query_data import query_y_finance
from operations.insert_data import InsertOperations

stock_list = get_stocks_list()
insert_operations = InsertOperations()
for stock in stock_list:
    stock_data = query_y_finance(stock)
    print(stock_data.info)
    if not insert_operations.check_for_stock_already_present(symbol=stock):
        print("Fresh Stock!")
        insert_operations.insert_stock_history(symbol=stock, history_df=stock_data.history(period=get_historical_days()))
    print("Adding Stock Details/Info!")
    insert_operations.insert_stock_info(symbol=stock, info=stock_data.info)

insert_operations.close_db_connection()
print("All Updates for stock information completed!!")


