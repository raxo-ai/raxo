import vertica_python


class VerticaConnector:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def connect(self):
        # Establish the connection
        try:
            self.connection = vertica_python.connect(**self.config)
            print("Connection established successfully.")
        except vertica_python.errors.ConnectionError as e:
            print(f"Connection error: {e}")
            raise

    def close(self):
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
