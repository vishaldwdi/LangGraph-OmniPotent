from typing import Any, Dict, List

from src.shared_retrieval.retriever_factory import create_retriever


class KnowledgeBaseRetriever:
    """Retriever for accessing knowledge base information."""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the retriever with configuration."""
        self.retriever = create_retriever(config)

    def retrieve(self, query: str) -> List[str]:
        """Retrieve relevant information from the knowledge base."""
        return self.retriever.retrieve(query)
