"""Tests for the base retriever implementation."""

import pytest
from langchain_core.documents import Document

from .base import BaseRetriever, FallbackRetriever


class TestBaseRetriever:
    def test_base_retriever_abstract(self):
        with pytest.raises(TypeError):
            BaseRetriever()  # Should raise TypeError since it's abstract


class TestFallbackRetriever:
    @pytest.fixture
    def mock_retriever(self, mocker):
        retriever = mocker.Mock()
        retriever.get_relevant_documents.return_value = [Document(page_content="test")]
        return retriever

    def test_fallback_retriever_success(self, mock_retriever):
        fallback = FallbackRetriever([mock_retriever])
        results = fallback.get_relevant_documents("test")
        assert len(results) == 1
        assert results[0].page_content == "test"

    def test_fallback_retriever_failure(self, mocker):
        failing_retriever = mocker.Mock()
        failing_retriever.get_relevant_documents.side_effect = Exception("Failed")

        fallback = FallbackRetriever([failing_retriever])
        results = fallback.get_relevant_documents("test")
        assert len(results) == 0

    def test_fallback_retriever_multiple(self, mock_retriever, mocker):
        failing_retriever = mocker.Mock()
        failing_retriever.get_relevant_documents.side_effect = Exception("Failed")

        fallback = FallbackRetriever([failing_retriever, mock_retriever])
        results = fallback.get_relevant_documents("test")
        assert len(results) == 1
        assert results[0].page_content == "test"
