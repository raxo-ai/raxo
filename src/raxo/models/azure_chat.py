import os
from openai import OpenAI
from src.raxo.utils.base import RaxoBase


class AzureOpenAIChat(RaxoBase):
    def __init__(self, client=None, config=None):
        RaxoBase.__init__(self, config)

        self.temperature = self.config.get("temperature", 0.75)
        self.max_tokens = self.config.get("max_tokens", 500)

        if client is not None:
            self.client = client

        if self.config.get("api_key") is None and os.environ.get("OPENAI_API_KEY") is None:
            raise KeyError("Did not find azure api_key, please add an environment variable"
                           " `AZURE_API_KEY` which contains it, or pass `azure_key` as"
                           " a named parameter")

        if self.config.get("api_version") is None:
            raise KeyError("Did not find azure api_version, please add an environment variable"
                           " `API_VERSION` which contains it, or pass `api_version` as"
                           " a named parameter")

        if self.config.get("azure_endpoint") is None:
            raise KeyError("Did not find azure azure_endpoint, please add an environment variable"
                           " `AZURE_ENDPOINT` which contains it, or pass `azure_endpoint` as"
                           " a named parameter")

        self.client = OpenAI(api_key=self.config.get("azure_key", os.environ.get("AZURE_API_KEY")))

    def invoke_prompt(self, prompt, **kwargs):
        print("parameters: ", self.config)
        data = self.client.chat.completions.create(messages=prompt,
                                                   model=kwargs.get("model", "gpt-3.5-turbo"))

        return data.choices[0].message.content
