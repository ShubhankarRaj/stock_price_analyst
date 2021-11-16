from __future__ import print_function
from startup.db_connector import DBHandle
from configurations.get_config import get_queries
from startup.get_columns import GetColumns


class InsertOperations:
    def __init__(self):
        self.conn = DBHandle()
        self.cursor = self.conn.get_db_connection().cursor()
        self.get_columns = GetColumns()

    def check_for_stock_already_present(self, symbol):
        QUERY = get_queries().get('check_for_stock_already_present').format(symbol)
        print(QUERY)
        self.cursor.execute(get_queries().get('check_for_stock_already_present').format(symbol))
        count = self.cursor.fetchone()[0]
        if count == 0:
            return False
        else:
            return True

    def insert_stock_info(self, symbol, info):
        cols = self.get_columns.get_ticker_info_cols()
        col_tuple = tuple(cols)
        value_list = []
        for key in cols:
            value_list.append(info.get(key))
        value_list.append('CURDATE()')
        QUERY = "Insert into ticker_info {}".format(col_tuple)
        # Removing quotes from the Query
        QUERY = QUERY.replace("'","")
        QUERY = "{} VALUES {}".format(QUERY, tuple(value_list))
        QUERY = QUERY.replace("None", "NULL")
        print(QUERY)

    def insert_stock_history(self, symbol, history_df):
        pass

    def close_db_connection(self):
        self.conn.close_db_connection()


# def insert_dividend_split_info(symbol, info):
#     cnx = DBHandle().get_db_connection()
#     cursor = cnx.cursor()
#
#     add_dividend = ("INSERT INTO dividend_info "
#                     "(share_symbol, dividend_date, div_percent) "
#                     "VALUES (%s, %s, %s)")
#
#     add_split_info = ("INSERT INTO split_info "
#                       "(split_date, split_ratio, share_symbol) "
#                       "VALUES (%s, %s, %s)")
#
#     info = info.to_dict()
#     date_dict = info["Open"].keys()
#     for i in date_dict:
#         if int(info["Dividends"][i]) > 0:
#             dividend_data = (symbol, i.to_pydatetime(), float(info["Dividends"][i]))
#             print(type(dividend_data))
#             cursor.execute(add_dividend, dividend_data)
#
#         if int(info["Stock Splits"][i]) > 0:
#             split_data = (i.to_pydatetime(), float(info["Stock Splits"][i]), symbol)
#             cursor.execute(add_split_info, split_data)
#     # Make sure data is committed to the database
#     cnx.commit()
#     cursor.close()
#     cnx.close()
#
#
# def insert_tick_info(data):
#     cnx = DBHandle().get_db_connection()
#     cursor = cnx.cursor()
#     cursor.execute(insert_statements['ticker_info'], data)
#     cnx.commit()
#     cursor.close()
#     cnx.close()


