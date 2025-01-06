from engineer_agent.model import _get_model


class GatherRequirements:
    """Class for gathering requirements functionality."""

    @classmethod
    def from_llm(cls, llm, tool_descriptions):
        """Create a GatherRequirements instance from an LLM."""
        return cls(llm, tool_descriptions)

    def __init__(self, model_name: str, tool_descriptions: list):
        """Initialize the requirements gathering component."""
        self.model = _get_model(model_name)
        self.tool_descriptions = tool_descriptions

    def gather(self, initial_input: str) -> str:
        """Gather requirements based on initial input."""
        prompt = f"Based on this input: {initial_input}\nAnd these available tools: {self.tool_descriptions}\nWhat are the requirements?"
        return self.model(prompt)
