import os
from openai import OpenAI
from src.raxo.utils.base import RaxoBase


class OpenAIChat(RaxoBase):
    def __init__(self, client=None, config=None):
        RaxoBase.__init__(self, config)

        self.temperature = self.config.get("temperature", 0.75)
        self.max_tokens = self.config.get("max_tokens", 500)

        if client is not None:
            self.client = client

        if self.config.get("api_key") is None and os.environ.get("OPENAI_API_KEY") is None:
            raise KeyError("Did not find openai api_key, please add an environment variable"
                           " `OPENAI_API_KEY` which contains it, or pass `api_key` as"
                           " a named parameter")

        self.client = OpenAI(api_key=self.config.get("api_key", os.environ.get("OPENAI_API_KEY")))

    def invoke_prompt(self, prompt, **kwargs):
        if not prompt or len(prompt) == 0:
            raise Exception("Please provide prompt to generate sql!")

        data = self.client.chat.completions.create(messages=prompt,
                                                   model=kwargs.get("model", "gpt-3.5-turbo"))

        return data.choices[0].message.content
