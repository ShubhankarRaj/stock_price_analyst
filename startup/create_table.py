import mysql
from mysql.connector import errorcode
from configurations.get_config import get_table_queries
from db_connector import DBHandle


db_handle = DBHandle()
cnx = db_handle.get_db_connection()
cursor = cnx.cursor()
TABLE_QUERIES = get_table_queries()
for query in TABLE_QUERIES:
    try:
        cursor.execute(query)
        print(f"Successfully executed: \n{query}")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Table already exists.")
        else:
            print(err.msg)

# Closing the Cursor object and the Connection
db_handle.close_db_connection()
