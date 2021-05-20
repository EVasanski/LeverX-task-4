import decimal

from mysql.connector import connect, Error, FieldType


class MyDatabase:

    def __init__(self, db_name, db_password, db_host='localhost', db_user='root'):
        self._host = db_host
        self._user = db_user
        self.__password = db_password
        self._dbname = db_name
        self.connection = self._connect_or_create_db()
        self.cursor = self.connection.cursor()

    def _connect_or_create_db(self):
        try:
            return connect(host=self._host, user=self._user, password=self.__password, database=self._dbname)
        except Error as err:
            if err.errno == 1049:
                connection = connect(host=self._host, user=self._user, password=self.__password)
                cursor = connection.cursor()
                cursor.execute(f'CREATE DATABASE IF NOT EXISTS {self._dbname}')
                cursor.close()
                connection.close()
                return connect(host=self._host, user=self._user, password=self.__password, database=self._dbname)
            else:
                raise err

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.fetchall()

    def headers(self):
        return [item[0] for item in self.cursor.description]

    def type(self):
        return enumerate([FieldType.get_info(item[1]) for item in self.cursor.description])

    def query_to_dict(self, query, params=None):
        data = []
        rows = self.query(query, params or ())
        headers = self.headers()
        row_types = {type(item[1]): item[0] for item in enumerate(rows[1])}
        decimal_index = row_types.get(decimal.Decimal)

        if decimal_index is not None:
            for row in rows:
                row = list(row)
                temp = row[decimal_index]
                row[decimal_index] = float(temp)
                data.append(dict(zip(headers, row)))
        else:
            for row in rows:
                data.append(dict(zip(headers, row)))
        return data
