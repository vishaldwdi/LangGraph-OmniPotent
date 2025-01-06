"""Configuration module for the engineering agent.

This module defines the configuration models and settings used by the engineering agent,
including LLM model parameters, execution limits, and debugging options.
"""

from pydantic import BaseModel


class EngineerAgentConfiguration(BaseModel):
    """Configuration for the Engineer Agent.

    Attributes:
        llm_model_name: Name of the language model to use (default: "gpt-4")
        llm_temperature: Temperature parameter for model generation (default: 0.7)
        knowledge_base: Dictionary containing knowledge base configuration
        max_iterations: Maximum number of iterations for the engineering workflow
        debug_mode: Whether to enable debug logging and output
    """

    llm_model_name: str = "gpt-4"
    llm_temperature: float = 0.7
    knowledge_base: dict = {}
    max_iterations: int = 5
    debug_mode: bool = False
