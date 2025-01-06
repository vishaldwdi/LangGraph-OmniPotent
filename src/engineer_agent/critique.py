"""Critique module for the engineering agent.

This module handles the critique functionality, including
acceptance criteria evaluation and code review.
"""

from langchain_core.messages import AIMessage
from langchain_core.pydantic_v1 import BaseModel

from engineer_agent.loader import load_github_file
from engineer_agent.model import _get_model
from engineer_agent.state import AgentState


class CritiqueCode:
    """Class for code critique functionality."""

    def __init__(self, model_name: str):
        """Initialize the critique component."""
        self.model = _get_model(model_name)

    def critique(self, code: str) -> str:
        """Provide critique for the given code."""
        # Implementation of critique logic
        return self.model(f"Critique this code: {code}")


critique_prompt = """You are tasked with critiquing a junior developers first attempt at building a LangGraph application. \
Here is a long unit test file for LangGraph. This should contain a lot (but possibly not all) \
relevant information on how to use LangGraph.

<unit_test_file>
{file}
</unit_test_file>

Based on the conversation below, attempt to critique the developer. If it seems like the written solution is fine, then call the `Accept` tool.

Do NOT critique the internal logic of the nodes too much - just make sure the flow (the nodes and edges) are correct and make sense. \
It's totally fine to use dummy LLMs or dummy retrieval steps."""


class Accept(BaseModel):
    """Model representing acceptance criteria for code review.

    Attributes:
        logic: The reasoning behind the acceptance decision
        accept: Boolean indicating whether the code is accepted
    """

    logic: str
    accept: bool


def _swap_messages(messages):
    new_messages = []
    for m in messages:
        if isinstance(m, AIMessage):
            new_messages.append({"role": "user", "content": m.content})
        else:
            new_messages.append({"role": "assistant", "content": m.content})
    return new_messages


def critique(state: AgentState, config):
    """Evaluate and critique the current code implementation.

    Args:
        state: The current agent state containing messages and requirements
        config: Configuration parameters for the critique process

    Returns:
        dict: Contains critique messages and acceptance status
    """
    github_url = "https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/tests/test_pregel.py"
    file_contents = load_github_file(github_url)
    messages = [
        {"role": "user", "content": critique_prompt.format(file=file_contents)},
        {"role": "assistant", "content": state.get("requirements")},
    ] + _swap_messages(state["messages"])
    model = _get_model(config, "openai", "critique_model").with_structured_output(
        Accept
    )
    response = model.invoke(messages)
    accepted = response.accept
    if accepted:
        return {
            "messages": [
                {"role": "user", "content": response.logic},
                {"role": "assistant", "content": "okay, sending to user"},
            ],
            "accepted": True,
        }
    else:
        return {
            "messages": [
                {"role": "user", "content": response.logic},
            ],
            "accepted": False,
        }
