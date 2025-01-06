# src/enrichment_agent/graph.py
"""Graph definition for the enrichment agent."""
from typing import List

from langchain_core.messages import BaseMessage
from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph

from src.enrichment_agent.configuration import EnrichmentAgentConfiguration
from src.enrichment_agent.state import EnrichmentState
from src.shared_retrieval.retriever_factory import create_retriever
from src.shared_utils.model_utils import load_chat_model


def create_agent(
    config: EnrichmentAgentConfiguration,
) -> Runnable[EnrichmentState, List[BaseMessage]]:
    """Create the enrichment agent."""
    _ = load_chat_model(config.llm_model_name, temperature=config.llm_temperature)
    _ = create_retriever(config.knowledge_base)
    raise NotImplementedError


def get_relevant_context(state: EnrichmentState):
    """Get relevant context based on the current state."""
    raise NotImplementedError


def generate_enrichment(state: EnrichmentState):
    """Generate enrichment based on the context."""
    raise NotImplementedError


def decide_if_continue(state: EnrichmentState) -> str:
    """Decide whether to continue enriching or respond."""
    # If we've reached max loops or have sufficient enrichment, respond
    if state.loop_step >= 6 or len(state.enriched_data) >= 3:
        return "respond"
    return "continue"


def generate_response(state: EnrichmentState) -> dict:
    """Generate a final response."""
    return {"messages": [f"Final enriched data: {state.enriched_data}"]}


def create_graph() -> StateGraph:
    """Create the graph for the enrichment agent."""
    builder = StateGraph(EnrichmentState)
    builder.add_node("get_context", get_relevant_context)
    builder.add_node("generate_enrichment", generate_enrichment)
    builder.add_node("generate_response", generate_response)

    # Add conditional edges after all nodes are added
    builder.add_conditional_edges(
        "generate_enrichment",
        decide_if_continue,
        {"continue": "get_context", "respond": "generate_response"},
    )

    # Add normal edge from get_context to generate_enrichment
    builder.add_edge("get_context", "generate_enrichment")

    # Set the entry point and return the compiled graph
    builder.set_entry_point("get_context")
    return builder


# Create and expose the graph
graph = create_graph()
