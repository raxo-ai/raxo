"""
MySQLConnector Module

This module provides the MySQLConnector class for creating and managing MySQL database connections.
The MySQLConnector class initializes a connection to a MySQL database using provided credentials and
supports executing SQL queries and closing the connection.

Classes:
    MySQLConnector: A class to handle MySQL database connections.
    InvalidKeysException: Exception raised for missing keys required for the MySQL connection.

Usage Example:
    mysql_connector = MySQLConnector(
        host="localhost",
        database="my_database",
        user="my_user",
        password="my_password"
    )
    mysql_connector.connect()
    results = mysql_connector.execute_query("SELECT * FROM my_table")
    mysql_connector.disconnect()
"""

import mysql.connector
from mysql.connector import Error
from ..utils.exceptions import InvalidKeysException


class MySQLConnector:
    """
    A class to handle MySQL database connections.

    This class provides methods to connect to a MySQL database using the provided
    credentials and maintains the connection for executing queries.

    Attributes:
        required_keys (tuple): A tuple of required keys for the connection.
             Defaults to ('host', 'database', 'user', 'password').
        host (str | None): The hostname of the MySQL server. Default is None.
        database (str | None): The name of the database to connect to. Default is None.
        user (str | None): The username to use for authentication. Default is None.
        password (str | None): The password to use for authentication. Default is None.
        connection: The connection object. Default is None.
    """

    required_keys = ('host', 'database', 'user', 'password')

    def __init__(self, host: str | None = None, database: str | None = None,
                 user: str | None = None, password: str | None = None):
        """
        Initialize the MySQLConnector with the given credentials.

        Args:
            host (str | None): The hostname of the MySQL server. Default is None.
            database (str | None): The name of the database to connect to. Default is None.
            user (str | None): The username to use for authentication. Default is None.
            password (str | None): The password to use for authentication. Default is None.

        Raises:
            InvalidKeysException: If any of the required keys are missing.
        """
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.dialect = "MySQL"
        missing_keys = self.check_missing_keys()
        if missing_keys:
            raise InvalidKeysException(f"Missing keys: {', '.join(missing_keys)}")

    def check_missing_keys(self):
        """
        Check for any missing keys required for the connection.

        Returns:
            list: A list of missing keys, if any.
        """
        missing_keys = [param for param in self.required_keys if getattr(self, param) is None]
        return missing_keys

    def connect(self):
        """
        Establish a connection to the MySQL database.

        This method uses the provided host, database, user, and password attributes
        to establish a connection to the MySQL database. The connection object is stored
        in the `connection` attribute of the class.

        Raises:
            ConnectionError: If the connection to the database fails.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")
            self.connection = None

    def disconnect(self):
        """
        Close the connection to the MySQL database.

        This method closes the connection to the MySQL database if it is currently open.
        It sets the `connection` attribute to None after closing the connection.

        Raises:
            ConnectionError: If there is an error closing the connection.
        """
        if self.connection is not None and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def execute_query(self, query, params=None):
        """
        Execute a SQL query on the MySQL database.

        This method executes the provided SQL query using the current database connection.
        It supports passing additional parameters to the query.

        Args:
            query (str): The SQL query to be executed.
            params (tuple, optional): A tuple of parameters to pass to the query. Default is None.

        Returns:
            list: The result of the query.

        Raises:
            ConnectionError: If there is no active connection to the database.
            RuntimeError: If there is an error executing the query.
        """
        if self.connection is None or not self.connection.is_connected():
            print("Connection is not established")
            return None

        cursor = self.connection.cursor()
        try:
            cursor.execute(query, params)
            return cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            return None
        finally:
            cursor.close()
