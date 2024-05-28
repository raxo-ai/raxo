from abc import ABC, abstractmethod


class Llm(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def invoke_prompt(self, prompt, **kwargs):
        pass
