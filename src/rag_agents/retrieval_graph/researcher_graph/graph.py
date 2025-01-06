# src/rag_agents/retrieval_graph/researcher_graph/graph.py
"""Graph definition for the research agent."""
from typing import List

from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph

from src.rag_agents.retrieval_graph.configuration import RetrievalAgentConfiguration
from src.rag_agents.retrieval_graph.researcher_graph.state import ResearcherState
from src.shared_retrieval.retriever_factory import create_retriever
from src.shared_utils.model_utils import load_chat_model


def create_agent(
    config: RetrievalAgentConfiguration,
) -> Runnable[ResearcherState, List[BaseMessage]]:
    """Create the research agent."""
    _ = load_chat_model(config.llm_model_name, temperature=config.llm_temperature)
    _ = create_retriever(config.knowledge_base)
    raise NotImplementedError


def generate_research_query(state: ResearcherState):
    """Generate a research query based on the current state."""
    raise NotImplementedError


def retrieve_relevant_documents(state: ResearcherState):
    """Retrieve relevant documents based on the query."""
    raise NotImplementedError


def generate_report(state: ResearcherState):
    """Generate a report based on the retrieved documents."""
    raise NotImplementedError


def should_continue_researching(state: ResearcherState):
    """Determine whether to continue researching or report."""
    raise NotImplementedError


def create_graph() -> StateGraph[ResearcherState]:
    """Create the graph for the research agent."""
    builder = StateGraph(ResearcherState)
    builder.add_node("generate_query", generate_research_query)
    builder.add_node("retrieve_docs", retrieve_relevant_documents)
    builder.add_node("generate_report", generate_report)
    builder.add_conditional_edges(
        should_continue_researching,
        {"continue": "generate_query", "report": "generate_report"},
    )
    builder.set_entry_point("generate_query")
    return builder
