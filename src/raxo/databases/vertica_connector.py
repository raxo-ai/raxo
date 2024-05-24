""" Vertica class """

import vertica_python
from ..utils.exceptions import InvalidKeysException


class VerticaConnector:
    required_keys = ('host', 'port', 'user', 'password', 'database')

    def __init__(self, config):
        self.config = config
        self.connection = None
        missing_keys = self.check_missing_keys()
        if missing_keys:
            raise InvalidKeysException(f"Missing required config keys: {', '.join(missing_keys)}")

    def check_missing_keys(self):
        missing_keys = [key for key in self.required_keys if key not in self.config]
        return missing_keys

    def connect(self):
        # Establish the connection
        try:
            self.connection = vertica_python.connect(**self.config)
            print("Connection established successfully.")
        except vertica_python.errors.ConnectionError as e:
            print(f"Connection error: {e}")
            raise

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Connection closed.")

    def execute_query(self, query):
        if not self.connection:
            raise ConnectionError("Connection is not established. Call the connect method first.")

        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error executing query: {e}")
            raise
        finally:
            cursor.close()


