"""
Exceptions Module

This module defines custom exception classes used across the project.
 These exceptions provide more specific
error messages and handling mechanisms for various error scenarios,
 improving the readability and maintainability
of the code.

Classes:
    APIError: Exception raised for errors occurring in the API.
    PromptError: Exception raised for errors related to prompts.
    InvalidKeysException: Exception raised for missing keys required for the database connection.
    NoTextProvided: Exception raised when no text is provided as input.

Usage Example:
    try:
        # Code that may raise an APIError
        raise APIError("Custom error message")
    except APIError as e:
        print(e)

    try:
        # Code that may raise an InvalidKeysException
        raise InvalidKeysException()
    except InvalidKeysException as e:
        print(e)
"""


class APIError(Exception):
    """
    Exception raised for errors occurring in the API.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="An error occurred in the API"):
        self.message = message
        super().__init__(self.message)


class PromptError(Exception):
    """
    Exception raised for errors related to prompts.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="An error occurred with the prompt"):
        self.message = message
        super().__init__(self.message)


class InvalidKeysException(Exception):
    """
    Exception raised for missing keys required for the database connection.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Invalid keys provided in the dictionary"):
        self.message = message
        super().__init__(self.message)


class NoTextProvided(Exception):
    """
    Exception raised when no text is provided as input.

    Attributes:
        message (str): Explanation of the error.
    """
    def __init__(self, message="Please provide a valid input"):
        self.message = message
        super().__init__(self.message)
