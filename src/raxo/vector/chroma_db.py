import chromadb
from chromadb.utils import embedding_functions
from ..utils.base import RaxoBase


class ChromaStore(RaxoBase):
    def __int__(self, config):
        RaxoBase.__init__(config)

        path = self.config.get("path", "./db")
        self.embedding_function = self.config.get("embedding_function",
                                                  embedding_functions.DefaultEmbeddingFunction())
        client_type = self.config.get("chromadb_type", "persistent")
        collection_meta = self.config.get("collection_meta", None)
        n_result = self.config.get("n_result", 10)
        self.n_result_sql = self.config.get("n_result_sql", n_result)
        self.n_result_ddl = self.config.get("n_result_ddl", n_result)
        self.n_result_doc = self.config.get("n_result_doc", n_result)

        if client_type == "persistent":
            self.chroma_client = chromadb.PersistentClient(path=path)
        else:
            self.chroma_client = chromadb.Client()

        # creating collection for sql queries used for few shot
        self.sql_collection = self.chroma_client.get_or_create_collection(
            name="sql",
            embedding_function=self.embedding_function,
            metadata=collection_meta
        )

        self.ddl_collection = self.chroma_client.get_or_create_collection(
            name="ddl",
            embedding_function=self.embedding_function,
            metadata=collection_meta
        )

        self.doc_collection = self.chroma_client.get_or_create_collection(
            name="documentation",
            embedding_function=self.embedding_function,
            metadata=collection_meta
        )

    def run_query(self, sql):
        pass
