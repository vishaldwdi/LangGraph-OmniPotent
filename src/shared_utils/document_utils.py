# src/shared_utils/document_utils.py
"""Shared document utility functions."""
from typing import List

from langchain_core.documents import Document


def format_docs(docs: List[Document]) -> str:
    """Format a list of documents into a string."""
    return "\\n\\n".join(doc.page_content for doc in docs)
