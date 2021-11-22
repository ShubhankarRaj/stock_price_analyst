from startup.create_db import check_for_database
from startup.sql_conn import SQLConnection
from configurations.get_config import get_sql_config


class DBHandle:
    def __init__(self):
        self.cursor = None
        self.connection = None
        self.sql_config = get_sql_config()

    def get_db_connection(self):
        sql_connection = SQLConnection()
        self.connection = sql_connection.connect_to_sql()
        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
        if self.cursor:
            pass
        else:
            self.cursor = self.connection.cursor()

        if check_for_database(self.cursor):
            self.cursor.execute(f"Use {self.sql_config.get('database')};")
            print(f"You're connected to database {self.sql_config.get('database')}!")
        else:
            print(f"You need to create the database: {self.sql_config.get('database')}")
            raise Exception("DataBase not created exception!")
        return self.connection

    def close_db_connection(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("DB connection is closed")

    def commit_connection_data(self):
        if self.connection.is_connected():
            self.connection.commit()