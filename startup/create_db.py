import mysql
from startup.sql_conn import SQLConnection
from configurations.get_config import get_sql_config

sql_config = get_sql_config()
DB_NAME = sql_config.get('database')


def check_for_database(cursor):
    # Check for Database
    cursor.execute("SHOW DATABASES")
    record = [item[0] for item in cursor.fetchall()]
    if DB_NAME in record:
        return True
    else:
        return False


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
        print(f"Database {DB_NAME} created!")
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)

try:
    sql_conn = SQLConnection()
    connection = sql_conn.connect_to_sql()
    if connection.is_connected():
        cursor = connection.cursor()
        if check_for_database(cursor):
            print(f"DATABASE {DB_NAME} already existing")
        else:
            create_database(cursor)
    connection.close()
except Exception as e:
    print(e)
    exit(1)