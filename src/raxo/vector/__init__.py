"""
Vector Module

This module provides classes for creating and managing connections to various vector databases.
Currently, it includes support for ChromaDB, with plans to add support for Qdrant and
    other vector databases.

Classes:
    ChromaStore: A class to create and manage a ChromaDB client and its collections.
    (Future classes for Qdrant and other vector databases will be added here.)

ChromaStore Usage Example:
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

(Future usage examples for Qdrant and other vector databases will be added here.)
"""

from .chroma_db import ChromaStore
