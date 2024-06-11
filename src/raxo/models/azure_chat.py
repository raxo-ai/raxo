"""
Azure OpenAI Chat Module

This module provides the AzureOpenAIChat class for creating and managing chat interactions
 using the Azure OpenAI.
It extends the Llm class and integrates with the Azure OpenAI API to generate responses based
 on provided prompts.

Classes:
    AzureOpenAIChat: A class to handle interactions with the Azure OpenAI chat service.

Dependencies:
    - os: Standard library for accessing environment variables.
    - openai.AzureOpenAI: Azure OpenAI client for making API requests.
    - utils.exceptions.InvalidKeysException: Custom exception for handling missing keys.

AzureOpenAIChat Usage Example:
    azure_chat = AzureOpenAIChat(
        api_key="your_api_key",
        api_version="your_api_version",
        azure_endpoint="your_azure_endpoint",
        deployment_name="your_deployment_name",
        temperature=0.7,
        max_tokens=1000
    )
    response = azure_chat.invoke_prompt(
        prompt=[{"role": "user", "content": "Hello, how are you?"}]
    )
    print(response)
"""

import os
from openai import AzureOpenAI
from .llms import Llm
from ..utils.exceptions import InvalidKeysException


class AzureOpenAIChat(Llm):
    """
    A class to handle interactions with the Azure OpenAI chat service.

    This class extends the Llm class and integrates with the Azure OpenAI API to generate responses
     based on prompts.
    It manages the connection to the Azure OpenAI service using the provided API key,
     version, endpoint, and deployment name.

    Attributes:
        api_key (str): The API key for accessing the Azure OpenAI service.
        api_version (str): The API version for the Azure OpenAI service.
        azure_endpoint (str): The endpoint URL for the Azure OpenAI service.
        deployment_name (str): The deployment name for the Azure OpenAI service.
        client (AzureOpenAI): The Azure OpenAI client for making API requests.
    """
    required_keys = ('api_key', 'api_version', 'azure_endpoint', 'deployment_name')

    def __init__(self, api_key: str | None = None, api_version: str | None = None,
                 azure_endpoint: str | None = None,
                 deployment_name: str | None = None):
        """
        Initialize an instance of the AzureOpenAIChat class.

        This method initializes the AzureOpenAIChat instance with the provided API key,
         version, endpoint, and deployment name.
        If any of these parameters are not provided, it attempts to retrieve them from
        environment variables.
        It also initializes the Azure OpenAI client and checks for any missing required keys.

        Args:
            api_key (str | None): The API key for accessing the Azure OpenAI service.
                Default is None.
            api_version (str | None): The API version for the Azure OpenAI service.
                Default is None.
            azure_endpoint (str | None): The endpoint URL for the Azure OpenAI service.
                Default is None.
            deployment_name (str | None): The deployment name for the Azure OpenAI service.
                Default is None.

        Raises:
            InvalidKeysException: If any of the required keys are missing.
        """

        Llm.__init__(self)

        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", None)
        self.api_version = api_version or os.environ.get("API_VERSION", None)
        self.azure_endpoint = azure_endpoint or os.environ.get("AZURE_ENDPOINT", None)
        self.deployment_name = deployment_name
        missing_keys = self.check_missing_keys(self.required_keys)
        if missing_keys:
            raise InvalidKeysException(f"""Missing keys: {', '.join(missing_keys)}\n
                                       Please add an environment variable
                                       `AZURE_API_KEY`, `API_VERSION`, `AZURE_ENDPOINT` and `DEPLOYMENT_NAME`
                                        which contains it, or pass `azure_key`, `api_version`, `azure_endpoint`
                                        and 'deployment_name as a named parameter.""")

        self.client = AzureOpenAI(api_key=self.api_key,
                                  azure_endpoint=self.azure_endpoint,
                                  api_version=self.api_version
                                  )

    def invoke_prompt(self, prompt, temperature: float = 0.5, max_tokens: int = 700, **kwargs):
        """
         Generate a response from the Azure OpenAI chat model based on the provided prompt.

         This method sends the given prompt to the Azure OpenAI chat model
            and returns the generated response.
         Additional parameters can be passed through kwargs to customize the request.

         Args:
             prompt (list): A list of dictionaries representing the conversation history.
                Each dictionary should have
                a 'role' (e.g., 'user', 'system', 'assistant') and 'content' (the message content).
             temperature (float): The temperature for the chat model's response.
                Default is 0.5.
             max_tokens (int): The maximum number of tokens in the response.
                Default is 700.
             **kwargs: Additional parameters to customize the request, such as the model to use.

         Returns:
             str: The content of the generated response from the Azure OpenAI chat model.

         Raises:
             openai.error.OpenAIError: If there is an error during the API request.
         """
        data = self.client.chat.completions.create(messages=prompt,
                                                   model=kwargs.get("model", "gpt-3.5-turbo"),
                                                   temperature=temperature,
                                                   max_tokens=max_tokens,
                                                   **kwargs)

        return data.choices[0].message.content

    def create_embedding(self, data):
        pass
