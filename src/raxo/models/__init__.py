"""
Models Module

This module provides support for various Language Model (LLM) integrations.
Currently, it includes support for OpenAI and Azure OpenAI chat models.
More LLM models will be added in the future.

Modules:
    openai_chat: Contains the OpenAIChat class for interacting with the OpenAI chat service.
    azure_chat: Contains the AzureOpenAIChat class for interacting with the Azure OpenAI chat.
    llm: Defines the Llm abstract base class, which serves as a blueprint for LLM interactions.

Usage Example:
    from models.openai_chat import OpenAIChat
    from models.azure_chat import AzureOpenAIChat

    # OpenAI Chat example
    openai_chat = OpenAIChat(
        api_key="your_api_key",
        model="gpt-3.5-turbo"
    )
    response = openai_chat.invoke_prompt(
        prompt=[{"role": "user", "content": "Hello, how are you?"}],
        temperature=0.7,
        max_tokens=1000
    )
    print(response)

    # Azure OpenAI Chat example
    azure_chat = AzureOpenAIChat(
        api_key="your_api_key",
        api_version="your_api_version",
        azure_endpoint="your_azure_endpoint",
        deployment_name="your_deployment_name"
    )
    response = azure_chat.invoke_prompt(
        prompt=[{"role": "user", "content": "Hello, how are you?"}],
        temperature=0.7,
        max_tokens=1000
    )
    print(response)
"""

from .openai_chat import OpenAIChat
from .azure_chat import AzureOpenAIChat
from .llms import Llm
