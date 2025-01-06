# src/rag_agents/index_graph/graph.py
"""Graph definition for the indexing agent."""
from typing import List

from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langgraph.graph import END, StateGraph

from src.rag_agents.index_graph.configuration import IndexConfiguration
from src.rag_agents.index_graph.state import IndexState
from src.shared_retrieval.retriever_factory import create_retriever
from src.shared_utils.model_utils import load_chat_model


def create_agent(
    config: IndexConfiguration,
) -> Runnable[IndexState, List[BaseMessage]]:
    """Create the indexing agent."""
    _ = load_chat_model(config.llm_model_name, temperature=config.llm_temperature)
    _ = create_retriever(config.knowledge_base)
    raise NotImplementedError


def decide_if_add_knowledge(state: IndexState):
    """Decide whether to add more knowledge."""
    return {
        "get_relevant_knowledge": state.should_add_knowledge,
        "END": not state.should_add_knowledge,
    }


def get_relevant_knowledge(state: IndexState):
    """Get relevant knowledge based on the current state."""
    raise NotImplementedError


def generate_response(state: IndexState):
    """Generate a response based on the current state."""
    raise NotImplementedError


def update_knowledge_base(state: IndexState):
    """Update the knowledge base with new information."""
    raise NotImplementedError


def create_graph():
    """Create the graph for the indexing agent."""
    builder = StateGraph(IndexState)
    builder.add_node("get_relevant_knowledge", get_relevant_knowledge)
    builder.add_node("generate_response", generate_response)
    builder.add_node("update_knowledge_base", update_knowledge_base)
    builder.add_conditional_edges(
        "get_relevant_knowledge",
        {
            "update_knowledge_base": lambda state: state.should_add_knowledge,
            "generate_response": lambda state: not state.should_add_knowledge,
        },
    )
    builder.add_edge("update_knowledge_base", "generate_response")
    builder.add_edge("generate_response", END)
    builder.set_entry_point("get_relevant_knowledge")
    return builder


graph = create_graph()
