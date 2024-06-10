from abc import ABC, abstractmethod


class Embedding(ABC):
    def __int__(self, api_key: str | None = None, api_version: str | None = None,
                azure_endpoint: str | None = None,
                deployment_name: str | None = None, model: str | None = None):
        pass

    def check_missing_keys(self, required_keys):
        """
        Check for any missing keys required for the connection.

        This utility method checks for any missing required keys in the subclass instances.

        Args:
            required_keys (list): A list of required key names to check.

        Returns:
            list: A list of missing keys, if any.
        """
        missing_keys = [param for param in required_keys if getattr(self, param) is None]
        return missing_keys

    @abstractmethod
    def create_embedding(self, data):
        pass
