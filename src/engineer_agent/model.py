from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI


def _get_model(model_name: str, temperature: float = 0.7) -> BaseChatModel:
    """Get a chat model instance based on the model name."""
    if "gpt" in model_name.lower():
        return ChatOpenAI(model_name=model_name, temperature=temperature)
    elif "claude" in model_name.lower():
        return ChatAnthropic(model_name=model_name, temperature=temperature)
    raise ValueError(f"Unsupported model: {model_name}")


class ChatModel(BaseChatModel):
    """Wrapper class for chat models."""

    def __init__(self, model_name: str, temperature: float = 0.7):
        """Initialize the chat model."""
        if "gpt" in model_name.lower():
            self.model = ChatOpenAI(model_name=model_name, temperature=temperature)
        elif "claude" in model_name.lower():
            self.model = ChatAnthropic(model_name=model_name, temperature=temperature)
        else:
            raise ValueError(f"Unsupported model: {model_name}")

    def __call__(self, *args, **kwargs):
        """Delegate calls to the underlying model."""
        return self.model(*args, **kwargs)

    def bind_tools(self, tools):
        """Bind tools to the model."""
        return self.model.bind_tools(tools)
