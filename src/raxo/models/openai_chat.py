"""
   OpenAIChat class will be used to create client for openai connect and then
   further used to ask any query
"""

import os
from openai import OpenAI
from src.raxo.utils.base import RaxoBase
from ..utils.exceptions import PromptError


class OpenAIChat(RaxoBase):
    """
        class to create openai client
    """
    def __init__(self, client=None):

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
        """ this function will use to invoke prompt, format a proper prompt,
         it will call openai chat completion api and get the inference
         """
        if not prompt or len(prompt) == 0:
            raise PromptError("Please provide prompt to generate sql!")

        data = self.client.chat.completions.create(messages=prompt,
                                                   model=kwargs.get("model", "gpt-3.5-turbo"))

        return data.choices[0].message.content
