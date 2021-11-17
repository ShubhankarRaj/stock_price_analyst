from __future__ import print_function
from startup.db_connector import DBHandle
from configurations.get_config import get_queries
from startup.get_columns import GetColumns

CUSTOM_KEY = 'currentDate'

class InsertOperations:
    def __init__(self):
        self.conn = DBHandle()
        self.cursor = self.conn.get_db_connection().cursor()
        self.get_columns = GetColumns()

    def check_for_stock_already_present(self, symbol):
        QUERY = get_queries().get('check_for_stock_already_present').format(symbol)
        print(f"Check for Stock already present query:\n{QUERY}")
        self.cursor.execute(get_queries().get('check_for_stock_already_present').format(symbol))
        count = self.cursor.fetchone()[0]
        if count == 0:
            return False
        else:
            return True

    def insert_stock_info(self, info):
        cols = self.get_columns.get_ticker_info_cols()
        col_tuple = tuple(cols)
        value_list = []
        for key in cols:
            if key != CUSTOM_KEY:
                value_list.append(info.get(key))
        # Adding the value for the CUSTOM_KEY
        value_list.append('CURDATE()')
        QUERY = "Insert into ticker_info {}".format(col_tuple)
        # Removing quotes from the Query
        QUERY = QUERY.replace("'","")
        QUERY = "{} VALUES {}".format(QUERY, tuple(value_list))
        QUERY = QUERY.replace("None", "NULL")
        QUERY = QUERY.replace("'CURDATE()'", "CURDATE()")
        print(f"Stock Info Insert Query: \n{QUERY}")
        try:
            print("Executing QUERY!")
            self.cursor.execute(QUERY)
        except Exception as e:
            print(f"Query execution for Inserting Stock info to DB failed. EXCEPTION: {e}")

    def insert_stock_history(self, history_df):
        # Mapping the Columns that we get in historical data's dataframe to info
        print(history_df)

    def close_db_connection(self):
        self.conn.close_db_connection()
