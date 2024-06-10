"""
ChromaStore Module

This module provides the ChromaStore class for creating and managing a ChromaDB client and its collections.
The ChromaStore class initializes a ChromaDB client and sets up collections for SQL queries, DDL statements,
and documentation results. It supports both persistent storage using SQLite and in-memory storage.

Classes:
    ChromaStore: A class to create and manage a ChromaDB client and its collections.

Exceptions:
    InvalidKeysException: Exception raised for missing keys required for the Vertica connection.

Usage Example:
    chroma_store = ChromaStore(
        path="./db",
        persistent=True,
        em_function=my_embedding_function,
        metadata=my_metadata,
        n_result_sql=10,
        n_result_ddl=10,
        n_result_doc=10
    )
    chroma_store.connect()
    results = chroma_store.execute_query("SELECT * FROM my_table")
    chroma_store.disconnect()
"""

import chromadb
import uuid
from chromadb.utils import embedding_functions
from .vector import Vector


class ChromaStore(Vector):
    """
    A class to create and manage a ChromaDB client and its collections.

    This class initializes a ChromaDB client and sets up collections for SQL queries, DDL statements,
    and documentation results. It allows for either persistent storage using SQLite or in-memory storage.

    Attributes:
        em_function: The embedding function to use for vector embeddings.
        n_result_sql (int): The number of SQL results to retrieve from the vector database.
        n_result_ddl (int): The number of DDL results to retrieve from the vector database.
        n_result_doc (int): The number of documentation results to retrieve from the vector database.
        chroma_client: The ChromaDB client instance.
        sql_collection: The collection for storing and retrieving SQL query embeddings.
        ddl_collection: The collection for storing and retrieving DDL statement embeddings.
        doc_collection: The collection for storing and retrieving documentation embeddings.
    """

    def __init__(self, path: str | None = "./db", persistent: bool | None = True, em_function=None,
                 metadata=None, n_result_sql=5, n_result_ddl=5, n_result_doc=5):
        """
        Initialize an instance of the ChromaStore class.

        Args:
            path (str | None): The path for the SQLite database file. Default is "./db".
            persistent (bool | None): Whether to store embeddings in SQLite (True) or keep in-memory (False). Default is True.
            em_function: The embedding function to use. If None, the default embedding function is used.
            metadata: Additional metadata required by ChromaDB for the collections. Default is None.
            n_result_sql (int): The number of SQL results to retrieve from the vector database. Default is 10.
            n_result_ddl (int): The number of DDL results to retrieve from the vector database. Default is 10.
            n_result_doc (int): The number of documentation results to retrieve from the vector database. Default is 10.
        """
        Vector.__init__(self)

        self.em_function = em_function
        self.n_result_sql = n_result_sql
        self.n_result_ddl = n_result_ddl
        self.n_result_doc = n_result_doc

        print("check persistent", persistent)
        if persistent:
            print("creating persistent client")
            self.chroma_client = chromadb.PersistentClient(path=path)
        else:
            self.chroma_client = chromadb.Client()
        if self.em_function.embed_mode == "openai":
            self.em_function = embedding_functions.OpenAIEmbeddingFunction(api_key=self.em_function.api_key,
                                                                           model_name=self.em_function.model)
        else:
            self.em_function = embedding_functions.DefaultEmbeddingFunction()

        # creating collection for sql queries used for few shot
        self.sql_collection = self.chroma_client.get_or_create_collection(
            name="sql",
            embedding_function=self.em_function,
            metadata=metadata
        )

        self.ddl_collection = self.chroma_client.get_or_create_collection(
            name="ddl",
            embedding_function=self.em_function,
            metadata=metadata
        )

        self.doc_collection = self.chroma_client.get_or_create_collection(
            name="documentation",
            embedding_function=self.em_function,
            metadata=metadata
        )

    def add_ddl(self, ddl: str, embedding: list) -> str:
        ddl_id = f"{str(uuid.uuid4())}-ddl"
        self.ddl_collection.add(
            documents=ddl,
            embeddings=embedding,
            ids=ddl_id
        )
        return ddl_id

    def add_documentation(self, doc: str, embedding: list) -> str:
        doc_id = f"{str(uuid.uuid4())}-doc"
        self.doc_collection.add(
            documents=doc,
            embeddings=embedding,
            ids=doc_id
        )
        return doc_id

    def get_ddl(self, question_embed: str):
        print("question asked: ", question_embed)

        # Get the count of embeddings in the collection
        embedding_count = self.ddl_collection.count()

        # Adjust n_results if it exceeds the available embeddings
        if self.n_result_ddl > embedding_count:
            self.n_result_ddl = embedding_count

        return self.ddl_collection.query(
            query_embeddings=[question_embed],
            n_results=self.n_result_ddl
        )
