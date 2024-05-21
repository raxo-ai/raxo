import mysql.connector
from mysql.connector import Error


class MySQLConnector:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
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
