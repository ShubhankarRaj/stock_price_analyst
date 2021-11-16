from __future__ import print_function

from turtle import pd

from insert_statements import insert_statements
from sql_connector import SqlConnection


def insert_dividend_split_info(symbol, info):
    cnx = SqlConnection().get_sql_connection()
    cursor = cnx.cursor()

    add_dividend = ("INSERT INTO dividend_info "
                    "(share_symbol, dividend_date, div_percent) "
                    "VALUES (%s, %s, %s)")

    add_split_info = ("INSERT INTO split_info "
                      "(split_date, split_ratio, share_symbol) "
                      "VALUES (%s, %s, %s)")

    info = info.to_dict()
    date_dict = info["Open"].keys()
    for i in date_dict:
        if int(info["Dividends"][i]) > 0:
            dividend_data = (symbol, i.to_pydatetime(), float(info["Dividends"][i]))
            print(type(dividend_data))
            cursor.execute(add_dividend, dividend_data)

        if int(info["Stock Splits"][i]) > 0:
            split_data = (i.to_pydatetime(), float(info["Stock Splits"][i]), symbol)
            cursor.execute(add_split_info, split_data)
    # Make sure data is committed to the database
    cnx.commit()
    cursor.close()
    cnx.close()


def insert_tick_info(data):
    cnx = SqlConnection().get_sql_connection()
    cursor = cnx.cursor()
    cursor.execute(insert_statements['ticker_info'], data)
    cnx.commit()
    cursor.close()
    cnx.close()


