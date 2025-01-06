"""Abstract base class for retrievers."""

from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


class BaseRetriever(ABC):
    """Abstract base class for retrievers."""

    @abstractmethod
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get relevant documents based on a query."""
        raise NotImplementedError


class FallbackRetriever(BaseRetriever):
    """Fallback retriever."""

    def __init__(self, retrievers: List[BaseRetriever]):
        """Initialize the fallback retriever."""
        self.retrievers = retrievers

    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get relevant documents based on a query."""
        for retriever in self.retrievers:
            try:
                results = retriever.get_relevant_documents(query)
                if results:
                    return results
            except Exception:
                continue
        return []


def create_fallback_retriever(retrievers: List[BaseRetriever]) -> FallbackRetriever:
    """Create a fallback retriever."""
    return FallbackRetriever(retrievers=retrievers)
