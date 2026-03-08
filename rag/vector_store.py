"""
Vector store module for the Autonomous QA Platform.

This module provides vector database functionality for storing and retrieving
embeddings using ChromaDB.
"""

import os
from typing import List, Dict, Any, Optional
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from rag.embeddings import embedding_service
from config import get_config


class VectorStore:
    """Vector database for storing and retrieving document embeddings."""

    def __init__(self):
        """Initialize the vector store with ChromaDB."""
        config = get_config()

        # Ensure directories exist
        os.makedirs(config.database.chromadb_path, exist_ok=True)

        # Initialize ChromaDB client
        self.client = PersistentClient(path=config.database.chromadb_path)

        # Use OpenAI embeddings
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=config.openai.api_key,
            model_name="text-embedding-3-small"
        )

    def create_collection(self, name: str, metadata: Optional[Dict[str, Any]] = None):
        """
        Create a new collection in the vector store.

        Args:
            name: Name of the collection
            metadata: Optional metadata for the collection
        """
        return self.client.create_collection(
            name=name,
            embedding_function=self.embedding_function,
            metadata=metadata
        )

    def get_collection(self, name: str):
        """
        Get an existing collection.

        Args:
            name: Name of the collection

        Returns:
            ChromaDB collection object
        """
        return self.client.get_collection(
            name=name,
            embedding_function=self.embedding_function
        )

    def add_documents(self, collection_name: str, documents: List[str],
                     metadatas: Optional[List[Dict[str, Any]]] = None,
                     ids: Optional[List[str]] = None):
        """
        Add documents to a collection.

        Args:
            collection_name: Name of the collection
            documents: List of document texts
            metadatas: Optional metadata for each document
            ids: Optional IDs for each document
        """
        collection = self.get_collection(collection_name)
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, collection_name: str, query: str, n_results: int = 5) -> Dict[str, Any]:
        """
        Search for similar documents.

        Args:
            collection_name: Name of the collection to search
            query: Search query
            n_results: Number of results to return

        Returns:
            Dictionary containing search results
        """
        collection = self.get_collection(collection_name)
        return collection.query(
            query_texts=[query],
            n_results=n_results
        )

    def delete_collection(self, name: str):
        """
        Delete a collection.

        Args:
            name: Name of the collection to delete
        """
        self.client.delete_collection(name)

    def list_collections(self):
        """
        List all collections in the store.

        Returns:
            List of collection names
        """
        return [col.name for col in self.client.list_collections()]


# Global instance for easy access
vector_store = VectorStore()
