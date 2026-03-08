"""
Embeddings module for the Autonomous QA Platform.

This module provides text embedding functionality using various embedding models.
Currently supports OpenAI embeddings for document and query processing.
"""

from typing import List, Optional
from langchain_openai import OpenAIEmbeddings
from config import get_config


class EmbeddingService:
    """Service for generating text embeddings."""

    def __init__(self):
        """Initialize the embedding service with configuration."""
        config = get_config()
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=config.openai.api_key
        )

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embeddings for a single text string.

        Args:
            text: The text to embed

        Returns:
            List of float values representing the embedding vector
        """
        return self.embeddings.embed_query(text)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple text strings.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        return self.embeddings.embed_documents(texts)

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embeddings for a search query.

        Args:
            query: The search query text

        Returns:
            Embedding vector for the query
        """
        return self.embeddings.embed_query(query)


# Global instance for easy access
embedding_service = EmbeddingService()
