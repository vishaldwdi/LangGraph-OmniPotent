"""Main agent module for the engineering agent.

This module contains the core agent implementation that coordinates
the various components (drafting, critique, etc.) to implement
a software engineering workflow using LangGraph.

Imports:
    - typing.Tuple: For type hints with fixed-length sequences
    - typing.Union: For type hints with multiple possible types
    - dotenv.load_dotenv: For loading environment variables
    - langchain_core.messages.BaseMessage: Base class for chat messages
    - langchain_core.prompts.chat.ChatPromptTemplate: For creating chat prompts
    - langchain_core.prompts.chat.MessagesPlaceholder: For placeholder messages
    - langchain_core.runnables.RunnableSerializable: For serializable runnables
    - langgraph.graph.Graph: For creating workflow graphs
    - langgraph.graph.StateGraph: For state-based workflow graphs
    - src.engineer_agent.check.code_check.CheckCode: For code checking
    - src.engineer_agent.config.EngineerAgentConfiguration: For agent config
    - src.engineer_agent.critique.CritiqueCode: For code critique
    - src.engineer_agent.draft.DraftCode: For code drafting
    - src.engineer_agent.gather_requirements.GatherRequirements: For requirements
    - src.engineer_agent.loader.LoadLocalFileTool: For loading local files
    - src.engineer_agent.model.ChatModel: For chat model interface
    - src.engineer_agent.retriever.KnowledgeBaseRetriever: For knowledge retrieval
    - src.engineer_agent.state.AgentState: For agent state management
    - src.shared_utils.document_utils.format_docs: For formatting documents
    - src.shared_utils.model_utils.load_chat_model: For loading chat models
"""

# Standard library imports
from typing import Tuple, Union

# Third party imports
from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSerializable
from langgraph.graph import Graph, StateGraph

# Local application imports
from src.engineer_agent.check.code_check import CheckCode
from src.engineer_agent.config import EngineerAgentConfiguration
from src.engineer_agent.model import ChatModel
from src.engineer_agent.state import AgentState


class CritiqueCode:
    """Class for critiquing code implementations."""

    @classmethod
    def from_llm(cls, llm: ChatModel) -> "CritiqueCode":
        """Create a critique chain from a language model."""
        return cls(llm)

    def __init__(self, llm: ChatModel):
        """Initialize with a language model."""
        self.llm = llm

    def invoke(self, state: AgentState) -> BaseMessage:
        """Critique the current code implementation."""
        # Implementation would go here
        return BaseMessage(content="Code critique placeholder")


class DraftCode:
    """Class for drafting code implementations."""

    @classmethod
    def from_llm(cls, llm: ChatModel) -> "DraftCode":
        """Create a draft chain from a language model."""
        return cls(llm)

    def __init__(self, llm: ChatModel):
        """Initialize with a language model."""
        self.llm = llm

    def invoke(self, state: AgentState) -> BaseMessage:
        """Draft the initial code implementation."""
        # Implementation would go here
        return BaseMessage(content="Code draft placeholder")


class GatherRequirements:
    """Class for gathering requirements."""

    @classmethod
    def from_llm(
        cls, llm: ChatModel, tool_descriptions: list[str]
    ) -> "GatherRequirements":
        """Create a requirements gathering chain from a language model."""
        return cls(llm, tool_descriptions)

    def __init__(self, llm: ChatModel, tool_descriptions: list[str]):
        """Initialize with a language model and tool descriptions."""
        self.llm = llm
        self.tool_descriptions = tool_descriptions

    def invoke(self, state: AgentState) -> BaseMessage:
        """Gather requirements for the code implementation."""
        # Implementation would go here
        return BaseMessage(content="Requirements gathering placeholder")


from src.engineer_agent.loader import LoadLocalFileTool
from src.engineer_agent.model import ChatModel
from src.engineer_agent.retriever import KnowledgeBaseRetriever
from src.engineer_agent.state import AgentState
from src.shared_utils.document_utils import format_docs
from src.shared_utils.model_utils import load_chat_model

load_dotenv()


def create_agent(
    llm: ChatModel,
    retriever: KnowledgeBaseRetriever,
    config: EngineerAgentConfiguration,
) -> RunnableSerializable[AgentState, Union[BaseMessage, Tuple[str, str]]]:
    """Create and configure the software engineering agent.

    Args:
        llm: The language model to use for the agent
        retriever: The knowledge base retriever for code context
        config: Configuration for the agent

    Returns:
        A runnable agent that processes AgentState and returns either a BaseMessage
        or a tuple of (code, explanation)
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a software engineer. When asked to build something, "
                "you will gather requirements, then draft the code, then critique "
                "the code, then check the code for errors. If the code passes "
                "the checks, you will respond with the final code. If the code "
                "does not pass the checks, you will revise the code and repeat "
                "the process.",
            ),
            MessagesPlaceholder("messages"),
            MessagesPlaceholder("agent_scratchpad"),
        ]
    )
    # define tools
    tools = [
        LoadLocalFileTool(),
        # KnowledgeBaseTool(retriever=retriever),
        # CodeCheckTool(),
    ]
    # bind tools to the llm
    llm_with_tools = llm.bind_tools(tools)
    # define the agent
    agent = (
        {
            "messages": lambda x: x["messages"],
            "agent_scratchpad": lambda x: format_docs(x["steps"]),
        }
        | prompt
        | llm_with_tools
    )
    return agent


def create_llm(config: EngineerAgentConfiguration) -> ChatModel:
    """Create and configure the language model for the agent.

    Args:
        config: Configuration containing model name and temperature

    Returns:
        Configured ChatModel instance
    """
    return load_chat_model(
        config.llm_model_name,
        temperature=config.llm_temperature,
    )


def gather_requirements(state: AgentState) -> AgentState:
    """Execute the requirements gathering phase of the engineering workflow.

    Args:
        state: Current agent state containing messages and context

    Returns:
        Updated state with gathered requirements
    """
    config = state["config"]
    llm = create_llm(config)
    tool_descriptions = [
        "load_local_file: useful for when you need to load a local file to understand its content",
        # "knowledge_base: useful for when you need to retrieve information about the codebase",
        # "code_check: useful for when you need to check the code for errors",
    ]
    gather_requirements_chain = GatherRequirements.from_llm(
        llm=llm, tool_descriptions=tool_descriptions
    )
    result = gather_requirements_chain.invoke(state)
    return {"messages": state["messages"] + [result]}


def draft_code(state: AgentState) -> AgentState:
    """Execute the code drafting phase of the engineering workflow.

    Args:
        state: Current agent state containing messages and context

    Returns:
        Updated state with drafted code
    """
    config = state["config"]
    llm = create_llm(config)
    draft_code_chain = DraftCode.from_llm(llm=llm)
    result = draft_code_chain.invoke(state)
    return {"messages": state["messages"] + [result]}


def critique_code(state: AgentState) -> AgentState:
    """Execute the code critique phase of the engineering workflow.

    Args:
        state: Current agent state containing messages and context

    Returns:
        Updated state with code critique
    """
    config = state["config"]
    llm = create_llm(config)
    critique_code_chain = CritiqueCode.from_llm(llm=llm)
    result = critique_code_chain.invoke(state)
    return {"messages": state["messages"] + [result]}


def check_code(state: AgentState) -> AgentState:
    """Execute the code checking phase of the engineering workflow.

    Args:
        state: Current agent state containing messages and context

    Returns:
        Updated state with code check results
    """
    config = state["config"]
    llm = create_llm(config)
    check_code_chain = CheckCode.from_llm(llm=llm)
    result = check_code_chain.invoke(state)
    return {"messages": state["messages"] + [result]}


def decide_next_step(state: AgentState) -> str:
    """Determine the next step in the engineering workflow based on current state.

    Args:
        state: Current agent state containing messages and context

    Returns:
        Name of the next node to execute in the workflow graph
    """
    if "check_code" not in state["messages"][-1].content.lower():
        return "critique_code"
    elif "passes" in state["messages"][-1].content.lower():
        return "respond_to_user"
    else:
        return "draft_code"


def respond_to_user(state: AgentState) -> BaseMessage:
    """Generate final response to the user with the completed code.

    Args:
        state: Current agent state containing messages and context

    Returns:
        Final message containing the completed code solution
    """
    return state["messages"][-1]


def create_graph(
    config: EngineerAgentConfiguration,
) -> Graph:
    """Create and configure the state machine graph for the engineering agent.

    Args:
        config: Configuration for the agent

    Returns:
        Compiled state machine graph that implements the engineering workflow
    """
    builder = StateGraph(AgentState)
    builder.add_node("gather_requirements", gather_requirements)
    builder.add_node("draft_code", draft_code)
    builder.add_node("critique_code", critique_code)
    builder.add_node("check_code", check_code)
    builder.add_node("respond_to_user", respond_to_user)
    builder.add_edge("gather_requirements", "draft_code")
    builder.add_edge("draft_code", "critique_code")
    builder.add_edge("critique_code", "check_code")
    builder.add_conditional_edges(
        "check_code",
        decide_next_step,
        {
            "respond_to_user": "respond_to_user",
            "draft_code": "draft_code",
        },
    )
    builder.set_entry_point("gather_requirements")
    return builder.compile()


# Create and expose the graph
graph: Graph = create_graph(EngineerAgentConfiguration())
"""The compiled state machine graph that implements the engineering workflow.

This graph coordinates the various phases of the engineering process:
1. Requirements gathering
2. Code drafting
3. Code critique
4. Code checking
5. Final response generation
"""
