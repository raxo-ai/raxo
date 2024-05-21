from abc import ABC, abstractmethod
from ..databases import MySQLConnector, VerticaConnector
from ..utils.exceptions import InvalidKeysException


class RaxoBase(ABC):
    def __init__(self, config=None):
        if not config:
            config = {}
        self.config = config
        self.execute = None
        self.required_keys = ('host', 'user', 'password', 'database')

    def check_keys(self, db_creds):
        missing_keys = [key for key in self.required_keys if key not in db_creds]
        if missing_keys:
            raise InvalidKeysException(f"Missing keys: {', '.join(missing_keys)}")
        return True

    def vertica_connector(self, db_config):
        try:
            # check if creds have correct keys
            self.check_keys(db_config)

            # create Vertica connector
            vertica_connector = VerticaConnector(db_config)
            vertica_connector.connect()

            def run_query(query: str):
                # Perform your database operations here
                # query = "SELECT * FROM your_table LIMIT 10;"
                results = vertica_connector.execute_query(query)
                # for row in results:
                #     print(row)
                return results
            self.execute = run_query
        except InvalidKeysException:
            pass

    def mysql_connector(self, db_config):
        try:
            # # Defined required keys for the dictionary
            # required_keys = ('host', 'database', 'user', 'password')

            # Check if the dictionary has the correct keys
            self.check_keys(db_config)

            # Create and use the MySQL connector
            db_connector = MySQLConnector(**db_config)
            db_connector.connect()

            def run_query(query: str):
                # Example query
                # query = "SELECT * FROM your_table_name"
                results = db_connector.execute_query(query)

                # db_connector.disconnect()
                return results

            self.execute = run_query
        except InvalidKeysException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def sqlite_connector(self, db_config):
        pass

