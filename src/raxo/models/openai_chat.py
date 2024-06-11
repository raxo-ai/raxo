"""
OpenAI Chat Module

This module provides the OpenAIChat class for creating and managing chat interactions using
    the OpenAI service.
It extends the Llm class and integrates with the OpenAI API to generate responses
  based on provided prompts.

Classes:
    OpenAIChat: A class to handle interactions with the OpenAI chat service.

Dependencies:
    - os: Standard library for accessing environment variables.
    - openai.OpenAI: OpenAI client for making API requests.
    - utils.exceptions.InvalidKeysException: Custom exception for handling missing keys.

OpenAIChat Usage Example:
    openai_chat = OpenAIChat(
        api_key="your_api_key",
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1000
    )
    response = openai_chat.invoke_prompt(
        prompt=[{"role": "user", "content": "Hello, how are you?"}]
    )
    print(response)
"""


import os
from openai import OpenAI
from typing import List
from .llms import Llm
from ..utils.exceptions import InvalidKeysException, PromptError


class OpenAIChat(Llm):
    """
    A class to handle interactions with the OpenAI chat service.

    This class extends the Llm class and integrates with the OpenAI API to generate responses
        based on provided prompts.
    It manages the connection to the OpenAI service using the provided API key and model.

    Attributes:
        model (str): The model to use for generating responses.
        client (OpenAI): The OpenAI client for making API requests.
    """

    required_keys = ('api_key', 'model')

    def __init__(self, api_key: str | None = None,
                 model: str | None = None):
        """
        Initialize an instance of the OpenAIChat class.

        This method initializes the OpenAIChat instance with the provided API key and model.
        If any of these parameters are not provided, it attempts to retrieve them from
            environment variables.
        It also initializes the OpenAI client and checks for any missing required keys.

        Args:
            api_key (str | None): The API key for accessing the OpenAI service. Default is None.
            model (str | None): The model to use for generating responses. Default is None.

        Raises:
            InvalidKeysException: If any of the required keys are missing.
        """

        Llm.__init__(self)

        self.model = model
        self.api_key = api_key

        missing_keys = self.check_missing_keys(self.required_keys)
        if missing_keys:
            raise InvalidKeysException(f"""Missing keys: {', '.join(missing_keys)}\n
                                       please add an environment variable
                                       `OPENAI_API_KEY` and `MODEL` which contains it, or pass `api_key` and  `model`
                                       as a named parameter""")

        self.client = OpenAI(api_key=self.api_key or os.environ.get("OPENAI_API_KEY", None))

    def invoke_prompt(self, prompt, temperature: float = 0.5, max_tokens: int = 700, **kwargs):
        """
        Generate a response from the OpenAI chat model based on the provided prompt.

        This method sends the given prompt to the OpenAI model and returns the generated response.
        Additional parameters can be passed through kwargs to customize the request.

        Args:
            prompt (list): A list of dictionaries representing the conversation history.
             Each dictionary should have a 'role'
                (e.g., 'user', 'system', 'assistant') and 'content' (the message content).
            temperature (float): The temperature for the chat model's response. Default is 0.5.
            max_tokens (int): The maximum number of tokens in the response. Default is 700.
            **kwargs: Additional parameters to customize the request, such as the model to use.

        Returns:
            str: The content of the generated response from the OpenAI chat model.

        Raises:
            Exception: If the prompt is not provided or is empty.
            openai.error.OpenAIError: If there is an error during the API request.
        """
        if not prompt or len(prompt) == 0:
            raise PromptError("Please provide prompt to generate sql!")

        data = self.client.chat.completions.create(messages=prompt,
                                                   model=self.model,
                                                   temperature=temperature,
                                                   max_tokens=max_tokens,
                                                   **kwargs)
        
        print("Data got from chat gpt: ", data)

        return data.choices[0].message.content

    def create_embedding(self, data: str) -> List[float]:
        embedding = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=data,
            encoding_format="float"
        )
        return embedding.data[0].embedding
