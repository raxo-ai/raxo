""" MySQL class """
import mysql.connector
from mysql.connector import Error
from ..utils.exceptions import InvalidKeysException


class MySQLConnector:
    required_keys = ('host', 'database', 'user', 'password')

    def __init__(self, config):
        self.config = config
        self.connection = None
        missing_keys = self.check_missing_keys()
        if missing_keys:
            raise InvalidKeysException(f"Missing keys: {', '.join(missing_keys)}")

    def check_missing_keys(self):
        missing_keys = [key for key in self.required_keys if key not in self.config]
        return missing_keys

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def execute_query(self, query, params=None):
        if self.connection is None or not self.connection.is_connected():
            print("Connection is not established")
            return None

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            # self.connection.commit()
            # print("Query executed successfully")
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
