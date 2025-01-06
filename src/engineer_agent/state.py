"""State management module for the engineering agent.

This module defines the state classes and types used throughout
the agent's execution graph, including message states and configuration.

Imports:
    - typing.Literal: For type hints with specific literal values
    - typing.TypedDict: For defining dictionary types with specific key-value pairs
    - langgraph.graph.MessagesState: Base state class for message-based workflows
"""

from typing import Literal, TypedDict

from langgraph.graph import MessagesState


class AgentState(MessagesState):
    """Main state class representing the agent's current state.

    Attributes:
        requirements: Current requirements being processed
        code: Current code implementation
        accepted: Whether the current implementation has been accepted
    """

    requirements: str
    code: str
    accepted: bool


class OutputState(TypedDict):
    """State representing the final output of the agent.

    Attributes:
        code: The final generated code
    """

    code: str


class GraphConfig(TypedDict):
    """Configuration for the agent's execution graph.

    Attributes:
        gather_model: Model to use for requirements gathering
        draft_model: Model to use for code drafting
        critique_model: Model to use for code critique
    """

    gather_model: Literal[
        "openai", "anthropic", "gemini", "groq", "lmstudio", "deepseek", "ollama"
    ]
    draft_model: Literal[
        "openai", "anthropic", "gemini", "groq", "lmstudio", "deepseek", "ollama"
    ]
    critique_model: Literal[
        "openai", "anthropic", "gemini", "groq", "lmstudio", "deepseek", "ollama"
    ]
