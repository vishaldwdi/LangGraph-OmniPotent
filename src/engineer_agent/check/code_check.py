"""Code checking functionality for the engineer agent."""

from typing import Any, Dict, Optional

from langchain_core.callbacks import Callbacks
from langchain_core.messages import BaseMessage
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSerializable

from src.engineer_agent.model import ChatModel
from src.engineer_agent.state import AgentState


class CheckCode(RunnableSerializable[AgentState, BaseMessage]):
    """Check code for errors and issues."""

    @classmethod
    def from_llm(cls, llm: ChatModel) -> "CheckCode":
        """Create a CheckCode instance from a language model."""
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a code quality checker. Analyze the provided code and identify any errors, "
                    "potential issues, or areas for improvement. Provide detailed feedback.",
                ),
                MessagesPlaceholder("messages"),
                MessagesPlaceholder("agent_scratchpad"),
            ]
        )
        chain = prompt | llm
        return cls(chain=chain)

    def invoke(
        self,
        state: AgentState,
        config: Optional[Dict[str, Any]] = None,
        callbacks: Callbacks = None,
        **kwargs: Any
    ) -> BaseMessage:
        """Invoke the code checker with the given state.

        Args:
            state: The current agent state containing code to check
            config: Optional configuration dictionary
            callbacks: Optional callbacks for the language model
            **kwargs: Additional keyword arguments

        Returns:
            BaseMessage containing the code analysis results
        """
        return self.chain.invoke(state, config=config, callbacks=callbacks, **kwargs)
