"""
VerticaConnector Module

This module provides the VerticaConnector class for creating and managing Vertica database connections.
The VerticaConnector class initializes a connection to a Vertica database using provided credentials
 and supports executing SQL queries and closing the connection.

Classes:
    VerticaConnector: A class to handle Vertica database connections.
    InvalidKeysException: Exception raised for missing keys required for the Vertica connection.

Usage Example:
    vertica_connector = VerticaConnector(
        host="localhost",
        port=5433,
        user="my_user",
        password="my_password",
        database="my_database"
    )
    vertica_connector.connect()
    results = vertica_connector.execute_query("SELECT * FROM my_table")
    vertica_connector.disconnect()
"""

import vertica_python
from ..utils.exceptions import InvalidKeysException


class VerticaConnector:
    """
    A class to handle Vertica database connections.

    This class provides methods to connect to a Vertica database using the provided
    credentials and maintains the connection for executing queries.

    Attributes:
        required_keys (tuple): A tuple of required keys for the connection.
            Defaults to ('host', 'port', 'user', 'password', 'database').
        host (str): The hostname of the Vertica server.
        port (int): The port number to connect to the Vertica server.
        user (str): The username to use for authentication.
        password (str): The password to use for authentication.
        database (str): The name of the database to connect to.
        connection: The connection object. Default is None.
    """

    required_keys = ('host', 'port', 'user', 'password', 'database')

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        """
        Initialize the VerticaConnector with the given credentials.

        Args:
            host (str): The hostname of the Vertica server.
            port (int): The port number to connect to the Vertica server.
            user (str): The username to use for authentication.
            password (str): The password to use for authentication.
            database (str): The name of the database to connect to.

        Raises:
            InvalidKeysException: If any of the required keys are missing.
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.dialect = "Vertica"
        missing_keys = self.check_missing_keys()
        if missing_keys:
            raise InvalidKeysException(f"Missing required keys: {', '.join(missing_keys)}")

    def check_missing_keys(self):
        """
        Check for any missing keys required for the connection.

        Returns:
            list: A list of missing keys, if any.
        """
        missing_keys = [key for key in self.required_keys if not getattr(self, key)]
        return missing_keys

    def connect(self):
        """
        Establish a connection to the Vertica database.

        This method uses the provided credentials to establish a connection to the Vertica database.
        The connection object is stored in the `connection` attribute of the class.

        Raises:
            vertica_python.errors.ConnectionError: If the connection to the database fails.
        """
        try:
            self.connection = vertica_python.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connection established successfully.")
        except vertica_python.errors.ConnectionError as e:
            print(f"Connection error: {e}")
            raise

    def disconnect(self):
        """
        Close the connection to the Vertica database.

        This method closes the connection to the Vertica database if it is currently open.
        It sets the `connection` attribute to None after closing the connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Connection closed.")

    def execute_query(self, query):
        """
        Execute a SQL query on the Vertica database.

        This method executes the provided SQL query using the current database connection.
        It returns the result of the query.

        Args:
            query (str): The SQL query to be executed.

        Returns:
            list: The result of the query.

        Raises:
            ConnectionError: If there is no active connection to the database.
            RuntimeError: If there is an error executing the query.
        """
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
