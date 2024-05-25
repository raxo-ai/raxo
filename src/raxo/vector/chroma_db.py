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
from chromadb.utils import embedding_functions


class ChromaStore:
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
                 metadata=None, n_result_sql=10, n_result_ddl=10, n_result_doc=10):
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

        if not self.em_function:
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
