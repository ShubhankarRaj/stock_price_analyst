from configurations.get_config import get_sql_config
import mysql.connector as mysqlc
from mysql.connector import Error


class SQLConnection:
    def __init__(self):
        self.sql_config = get_sql_config()
        self.connection = None

    def connect_to_sql(self):
        if self.connection is not None:
            return self.connection
        else:
            try:
                self.connection = mysqlc.connect(host=self.sql_config.get('host'),
                                                 user=self.sql_config.get('user'),
                                                 password=self.sql_config.get('password'))
                return self.connection
            except Error as e:
                print("Error while connecting to MySQL", e)

