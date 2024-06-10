import os
from typing import List
from openai import OpenAI
from .embedding import Embedding
from ..utils.exceptions import InvalidKeysException


class OpenAiEmbeddings(Embedding):
    required_keys = ('api_key', 'model')

    def __init__(self, api_key: str | None = None, model: str | None = None):
        Embedding.__init__(self)

        self.api_key = api_key
        self.model = model
        self.embed_mode = "openai"

        missing_keys = self.check_missing_keys(self.required_keys)
        if missing_keys:
            raise InvalidKeysException(f"""Missing keys: {', '.join(missing_keys)}\n
                                               please add an environment variable
                                               `OPENAI_API_KEY` and `MODEL` which contains it, or pass `api_key` and
                                                 `model` as a named parameter""")
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY", None))
        # openai_ef = embedding_functions.OpenAIEmbeddingFunction(api_key="",
        #                                                         model_name="text-embedding-ada-002")

    def create_embedding(self, data: str) -> List[float]:
        embedding = self.client.embeddings.create(
            model=self.model,
            input=data,
            encoding_format="float"
        )
        return embedding.data[0].embedding
