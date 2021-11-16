from get_config import TickerConfig
import mysql.connector as mysqlc
from mysql.connector import Error

# PRE-REQUISITE : Create the Ticker datababse  in MySQL
SQL_KEY = "sql"


class SqlConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def _get_sql_config(self):
        config_obj = TickerConfig()
        config = config_obj.get_config()
        return config.get(SQL_KEY)

    def get_sql_connection(self):
        if self.connection != None:
            return self.connection
        else:
            sql_config = self._get_sql_config()
            try:
                self.connection = mysqlc.connect(host=sql_config.get('host'),
                                            database=sql_config.get('database'),
                                            user=sql_config.get('user'),
                                            password=sql_config.get('password'))

                if self.connection.is_connected():
                    db_Info = self.connection.get_server_info()
                    print("Connected to MySQL Server version ", db_Info)
                    self.cursor = self.connection.cursor()
                    self.cursor.execute("select database();")
                    record = self.cursor.fetchone()
                    print("You're connected to database: ", record)
                    return self.connection

            except Error as e:
                print("Error while connecting to MySQL", e)

    def close_sql_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("MySQL connection is closed")



new_connection = SqlConnection()
new_connection.get_sql_connection()
new_connection.close_sql_connection()