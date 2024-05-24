import os
from openai import OpenAI
from .llms import Llm


class OpenAIChat(Llm):
    def __init__(self, api_key: str | None = None,
                 model: str | None = None,
                 temperature: float = 0.5, max_tokens: int = 700):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", None)
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.model = model

        if self.api_key is None:
            raise KeyError("Did not find openai api_key, please add an environment variable"
                           " `OPENAI_API_KEY` which contains it, or pass `api_key` as"
                           " a named parameter")
        if self.model is None:
            raise KeyError("Did not find openai model name, please add an environment variable"
                           " `MODEL` which contains it, or pass `model` as"
                           " a named parameter")
        self.client = OpenAI(
            api_key=self.api_key)

    def invoke_prompt(self, prompt, **kwargs):
        if not prompt or len(prompt) == 0:
            raise Exception("Please provide prompt to generate sql!")

        data = self.client.chat.completions.create(messages=prompt,
                                                   model=self.model,
                                                   temperature=self.temperature,
                                                   max_tokens=self.max_tokens,
                                                   **kwargs)

        return data.choices[0].message.content
