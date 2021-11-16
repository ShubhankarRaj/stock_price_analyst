from startup.db_connector import DBHandle


class GetColumns:
    def __init__(self):
        self.conn = DBHandle()
        self.cursor = self.conn.get_db_connection().cursor()

    def _get_cols_table(self, table_name):
        self.cursor.execute(f"SHOW COLUMNS FROM {table_name}")
        return [item[0] for item in self.cursor.fetchall()]

    def get_dividend_info_cols(self):
        return self._get_cols_table('dividend_info')

    def get_ticker_info_cols(self):
        return self._get_cols_table('ticker_info')

    def get_split_info_cols(self):
        return self._get_cols_table('split_info')

    def close_connection(self):
        self.conn.close_db_connection()






