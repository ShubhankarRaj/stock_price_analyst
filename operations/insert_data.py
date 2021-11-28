from __future__ import print_function
from startup.db_connector import DBHandle
from configurations.get_config import get_queries, get_stock_dump_file
from startup.get_columns import GetColumns
from enum import Enum
from pandas import DataFrame
import os, csv

CUSTOM_KEY = 'date_of_trade'


class TableType(Enum):
    ticker = "ticker"
    dividend = "dividend"
    split = "split"


class InsertOperations:
    def __init__(self):
        self.conn = DBHandle()
        self.cursor = self.conn.get_db_connection().cursor()
        self.get_columns = GetColumns()

    def _check_for_stock_already_present(self, table_type: TableType, symbol):
        if table_type == TableType.ticker:
            QUERY = get_queries().get('check_for_stock_in_ticker_info').format(symbol)
            self.cursor.execute(get_queries().get('check_for_stock_in_ticker_info').format(symbol))
        elif table_type == TableType.dividend:
            QUERY = get_queries().get('check_for_stock_in_dividend_info').format(symbol)
            self.cursor.execute(get_queries().get('check_for_stock_in_dividend_info').format(symbol))
        elif table_type == TableType.split:
            QUERY = get_queries().get('check_for_stock_in_split_info').format(symbol)
            self.cursor.execute(get_queries().get('check_for_stock_in_split_info').format(symbol))
        else:
            print("Invalid value for checking stock")
            return None

        print(f"Check for Stock already present query:\n{QUERY}")
        count = self.cursor.fetchone()[0]
        if count == 0:
            return False
        else:
            return True

    def _query_ticker_info_table(self):
        QUERY = get_queries().get('dump_ticker_info')
        try:
            self.cursor.execute(QUERY)
            columns = [desc[0] for desc in self.cursor.description]
            result = DataFrame(self.cursor.fetchall(), columns=columns)
            print(result.head())
        except Exception as e:
            print(f"SQL Result dump failed. Exception: {e}")

        return result

    def dump_ticker_info(self):
        result = self._query_ticker_info_table()
        if os.path.exists(get_stock_dump_file()):
            os.remove(get_stock_dump_file())
        result.to_csv(get_stock_dump_file(), index=False)

    def _insert_map_to_table(self, table_type: TableType, col_tuple, value_list):
        if table_type == TableType.ticker:
            QUERY = "Insert into ticker_info {}".format(col_tuple)
        elif table_type == TableType.dividend:
            QUERY = "Insert into dividend_info {}".format(col_tuple)
        elif table_type ==TableType.split:
            QUERY = "Insert into split_info {}".format(col_tuple)
        # Removing quotes from the Query
        QUERY = QUERY.replace("'", "")
        QUERY = "{} VALUES {}".format(QUERY, tuple(value_list))
        QUERY = QUERY.replace("None", "NULL")
        QUERY = QUERY.replace("'CURDATE()'", "CURDATE()")
        print(f"Stock Info Insert Query: \n{QUERY}")
        try:
            print("Executing QUERY!")
            self.cursor.execute(QUERY)
        except Exception as e:
            print(f"Query execution for Inserting Stock info to DB failed. EXCEPTION: {e}")
        self.commit_transaction()

    def _update_table(self, table_type: TableType, table_col_map, history_df, stock):
        """
        Using the same function to update for all the different types of tables:
        ticker_info/dividend_info/split_info
        :param table_type:
        :param table_col_map:
        :param history_df:
        :param stock:
        :return:
        """
        if table_type == TableType.ticker:
            cols = self.get_columns.get_ticker_info_cols()
        elif table_type == TableType.dividend:
            cols = self.get_columns.get_dividend_info_cols()
        elif table_type == TableType.split:
            cols = self.get_columns.get_split_info_cols()
        col_tuple = tuple(cols)
        if not self._check_for_stock_already_present(table_type, stock):
            print(f"Fresh {table_type.value} Info for {stock}!!")
            for index, row in history_df.iterrows():
                value_list = []
                table_dict = {}

                for k, v in table_col_map.items():
                    if k in history_df.columns:
                        table_dict[table_col_map.get(k)] = row[k]
                # Adding the Date of Record
                table_dict[table_col_map.get("Date")] = index
                # Adding the symbol of the stock
                table_dict['symbol'] = stock

                for key in cols:
                    value_list.append(table_dict.get(key))
                self._insert_map_to_table(table_type, col_tuple, value_list)
        else:
            print(f"{stock} already present in {table_type.value} Info table.")
        self.commit_transaction()

    def insert_stock_info(self, info):
        cols = self.get_columns.get_ticker_info_cols()
        col_tuple = tuple(cols)
        value_list = []
        for key in cols:
            if key == CUSTOM_KEY:
                # Adding the value for the CUSTOM_KEY
                value_list.append('CURDATE()')
            else:
                value_list.append(info.get(key))

        self._insert_map_to_table(TableType.ticker, col_tuple, value_list)

    def insert_stock_history(self, stock, history_df):
        # Mapping the Columns that we get in historical data's dataframe to info, dividends, stock-split
        info_col_map = {"Date":"date_of_trade","Open":"open","High":"dayHigh", "Low":"dayLow", "Close":"regularMarketPrice", "Volume":"regularMarketVolume"}
        dividend_col_map = {"Date":"dividend_date", "Dividends":"div_percent"}
        split_col_map = {"Date":"split_date","Stock Splits": "split_ratio"}

        self._update_table(TableType.ticker, info_col_map, history_df, stock)
        self._update_table(TableType.dividend, dividend_col_map, history_df, stock)
        self._update_table(TableType.split, split_col_map, history_df, stock)

    def insert_sentiment_history(self,sentiment, stock):
        for index,senti in sentiment.iterrows():
            sentiment_dict = dict(senti)
            QUERY = 'update ticker_info set sentiment = "'+sentiment_dict['Sentiment']+'",sentiment_perc = "'+str(sentiment_dict['Percentage'])+'"  where symbol= "'+stock+'" and date_of_trade = "'+str(sentiment_dict['Date'])+'"'
            print(QUERY)
            self.cursor.execute(QUERY)

        self.commit_transaction()

    def close_db_connection(self):
        self.conn.close_db_connection()

    def commit_transaction(self):
        self.conn.commit_connection_data()
