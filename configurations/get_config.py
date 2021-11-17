from configurations.load_config import Config

SQL_KEY = 'sql'
TABLES_KEY = 'tables'
STOCKS_KEY = 'stocks'
NEW_STOCKS_KEY = 'new_stocks'
HISTORY = 'days_in_history'
QUERIES = 'queries'

config_obj = Config()
config = config_obj.load_conf()


def get_sql_config():
    return config.get(SQL_KEY)


def get_table_lists():
    table_configs = get_sql_config().get(TABLES_KEY)
    return list(table_configs.keys())


def get_table_queries():
    table_configs = get_sql_config().get(TABLES_KEY)
    return [query for table,query in table_configs.items()]


def get_stocks_list():
    return config.get(STOCKS_KEY)


def get_new_stocks_list():
    return config.get(NEW_STOCKS_KEY)


def get_historical_days():
    return config.get(HISTORY)


def get_queries():
    return config.get(QUERIES)

