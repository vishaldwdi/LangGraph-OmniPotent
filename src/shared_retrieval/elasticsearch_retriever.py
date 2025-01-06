import os
from typing import List

from elasticsearch import Elasticsearch
from elastic_transport import ConnectionError, ApiError
from langchain_core.documents import Document

from src.shared_retrieval.base import BaseRetriever


class ElasticsearchRetriever(BaseRetriever):
    """Retrieves documents from Elasticsearch."""

    def __init__(self):
        """Initializes the ElasticsearchRetriever with client configuration."""
        self.elasticsearch_url = os.getenv("ELASTICSEARCH_URL")
        self.elasticsearch_api_key = os.getenv("ELASTICSEARCH_API_KEY")
        if not self.elasticsearch_url or not self.elasticsearch_api_key:
            raise ValueError(
                "Elasticsearch URL and API key must be set in environment variables."
            )
        self.client = Elasticsearch(
            self.elasticsearch_url, api_key=self.elasticsearch_api_key
        )
        self.index_name = "langgraph-omnipotent-index"

    def get_relevant_documents(
        self,
        query: str,
        query_type: str = "multi_match",
        page_size: int = 10,
        page: int = 1,
    ) -> List[Document]:
        """Retrieves relevant documents from Elasticsearch based on the query.

        Args:
            query: The search query
            query_type: Type of query to execute (multi_match, match, term)
            page_size: Number of results per page
            page: Page number to retrieve

        Returns:
            A list of Document objects

        Raises:
            ValueError: If invalid query type is provided
            ConnectionError: For connection-related errors
            ApiError: For API-related errors
        """
        # Validate query type
        valid_query_types = ["multi_match", "match", "term"]
        if query_type not in valid_query_types:
            raise ValueError(f"Invalid query type. Must be one of: {valid_query_types}")

        try:
            # Build base query structure
            search_query = {
                "query": {
                    query_type: {
                        "query": query,
                        "fields": (
                            ["content", "title", "description"]
                            if query_type == "multi_match"
                            else None
                        ),
                    }
                },
                "from": (page - 1) * page_size,
                "size": page_size,
            }

            # Execute search with scroll for large result sets
            search_results = self.client.search(
                index=self.index_name,
                body=search_query,
                scroll="2m",  # Keep search context alive for 2 minutes
            )

            # Process results
            documents = []
            scroll_id = search_results.get("_scroll_id")

            while True:
                # Extract documents from current page
                hits = search_results["hits"]["hits"]
                if not hits:
                    break

                documents.extend(
                    [
                        Document(
                            page_content=hit["_source"]["content"],
                            metadata={
                                **hit["_source"],
                                "score": hit["_score"],
                                "id": hit["_id"],
                            },
                        )
                        for hit in hits
                    ]
                )

                # Get next page if available
                search_results = self.client.scroll(scroll_id=scroll_id, scroll="2m")

            return documents

        except (ConnectionError, ApiError) as e:
            raise ConnectionError(str(e)) from e
