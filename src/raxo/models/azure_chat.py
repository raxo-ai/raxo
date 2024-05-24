import os
from .llms import Llm
from openai import AzureOpenAI


class AzureOpenAIChat(Llm):
    def __init__(self, api_key: str | None = None, api_version: str | None = None,
                 azure_endpoint: str | None = None,
                 deployment_name: str | None = None,
                 temperature: float = 0.5, max_tokens: int = 700):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", None)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_version = api_version or os.environ.get("API_VERSION", None)
        self.azure_endpoint = azure_endpoint or os.environ.get("AZURE_ENDPOINT", None)
        self.deployment_name = deployment_name
        if self.api_key is None:
            raise KeyError("Did not find azure api_key, please add an environment variable"
                           " `AZURE_API_KEY` which contains it, or pass `azure_key` as"
                           " a named parameter")

        if self.api_version is None:
            raise KeyError("Did not find azure api_version, please add an environment variable"
                           " `API_VERSION` which contains it, or pass `api_version` as"
                           " a named parameter")

        if self.azure_endpoint is None:
            raise KeyError("Did not find azure azure_endpoint, please add an environment variable"
                           " `AZURE_ENDPOINT` which contains it, or pass `azure_endpoint` as"
                           " a named parameter")

        self.client = AzureOpenAI(api_key=self.api_key,
                                  azure_endpoint=self.azure_endpoint,
                                  api_version=self.api_version
                                  )

    def invoke_prompt(self, prompt, **kwargs):
        data = self.client.chat.completions.create(messages=prompt,
                                                   model=kwargs.get("model", "gpt-3.5-turbo"),
                                                   temperature=self.temperature,
                                                   max_tokens=self.max_tokens,
                                                   **kwargs)

        return data.choices[0].message.content
