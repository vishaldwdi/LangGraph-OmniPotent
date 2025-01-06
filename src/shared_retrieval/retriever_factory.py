"""Factory for creating retriever instances."""

import os
from typing import Any, Dict

from langchain_core.retrievers import BaseRetriever

from src.shared_retrieval.elasticsearch_retriever import ElasticsearchRetriever
from src.shared_retrieval.mongodb_retriever import MongoRetriever
from src.shared_retrieval.pinecone_retriever import PineconeRetriever


def create_retriever(config: Dict[str, Any]) -> BaseRetriever:
    """Create a retriever instance based on the configuration."""
    retriever_type = config.get("type", "elasticsearch")

    if retriever_type == "elasticsearch":
        return ElasticsearchRetriever(
            url=os.getenv("ELASTICSEARCH_URL"),
            api_key=os.getenv("ELASTICSEARCH_API_KEY"),
            index_name=config.get("index_name"),
        )
    elif retriever_type == "pinecone":
        return PineconeRetriever(
            api_key=os.getenv("PINECONE_API_KEY"),
            index_name=os.getenv("PINECONE_INDEX_NAME"),
        )
    elif retriever_type == "mongodb":
        return MongoRetriever(
            connection_string=os.getenv("MONGODB_URI"),
            database_name=config.get("database_name"),
            collection_name=config.get("collection_name"),
        )
    else:
        raise ValueError(f"Unsupported retriever type: {retriever_type}")
