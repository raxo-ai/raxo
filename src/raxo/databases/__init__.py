"""
Databases Module

This module provides classes for creating and managing database connections.
Currently, it includes support for MySQL and Vertica databases.

Classes:
    MySQLConnector: A class to handle MySQL database connections.
    VerticaConnector: A class to handle Vertica database connections.
    InvalidKeysException: Exception raised for missing keys required for the database connection.

MySQLConnector Usage Example:
    mysql_connector = MySQLConnector(
        host="localhost",
        database="my_database",
        user="my_user",
        password="my_password"
    )
    mysql_connector.connect()
    results = mysql_connector.execute_query("SELECT * FROM my_table")
    mysql_connector.disconnect()

VerticaConnector Usage Example:
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

from .mysql_connector import MySQLConnector
from .vertica_connector import VerticaConnector
