"""
LLM Abstract Base Class Module

This module defines the Llm abstract base class, which serves as a blueprint for concrete
  implementations of language model clients.
It enforces the implementation of the `invoke_prompt` method and provides a utility method
  for checking missing required keys.

Classes:
    Llm: An abstract base class for Language Model (LLM) interactions.
        Subclasses must implement the `invoke_prompt` method.

Usage Example:
    from llm import Llm

    class MyLlm(Llm):
        def invoke_prompt(self, prompt, **kwargs):
            # Implementation for invoking a prompt
            pass

    my_llm = MyLlm()
    missing_keys = my_llm.check_missing_keys(['api_key', 'model'])
    if missing_keys:
        print(f"Missing keys: {', '.join(missing_keys)}")
"""

from abc import ABC, abstractmethod


class Llm(ABC):
    """
    An abstract base class for Language Model (LLM) interactions.

    This class serves as a blueprint for concrete implementations of language model clients,
    such as OpenAIChat and AzureOpenAIChat. It enforces the implementation of the `invoke_prompt`
     method and provides a utility method for checking missing required keys.

    Methods:
        __init__: Initializes the Llm instance.
        invoke_prompt: An abstract method to be implemented by subclasses to invoke a prompt and
            generate a response.
        check_missing_keys: Checks for any missing required keys in the subclass instances.

    Usage Example:
        class MyLlm(Llm):
            def invoke_prompt(self, prompt, **kwargs):
                # Implementation for invoking a prompt
                pass

        my_llm = MyLlm()
        missing_keys = my_llm.check_missing_keys(['api_key', 'model'])
    """
    def __int__(self):
        """
        Initialize an instance of the Llm class.

        This constructor initializes the Llm instance. It can be used by subclasses to
            ensure proper initialization.
        """

    @abstractmethod
    def invoke_prompt(self, prompt, temperature=0.5, max_tokens=700, **kwargs):
        """
        Abstract method to invoke a prompt and generate a response.

        Subclasses must implement this method to send a prompt to the language model and
            return the generated response.

        Args:
            prompt (list): A list of dictionaries representing the conversation history.
             Each dictionary should have a 'role'
                (e.g., 'user', 'system', 'assistant') and 'content' (the message content).
            temperature (float): The temperature for the chat model's response. Default is 0.5.
            max_tokens (int): The maximum number of tokens in the response. Default is 700.
            **kwargs: Additional parameters to customize the request.

        Returns:
            str: The content of the generated response from the language model.
        """

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

    def create_embedding(self, data):
        pass
