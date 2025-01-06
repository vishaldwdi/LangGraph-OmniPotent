# src/shared_utils/model_utils.py
"""Shared model utility functions."""
import os

import google.generativeai as genai
from deepseek import DeepSeekAPI
from langchain_anthropic import ChatAnthropic
from langchain_community.llms import Ollama
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI


def load_chat_model(model_name: str, temperature: float):
    """Load a chat model based on the model name."""

    def validate_api_key(key_name: str):
        api_key = os.getenv(key_name)
        if not api_key:
            raise ValueError(f"{key_name} environment variable is required")
        return api_key

    if model_name == "openai":
        return ChatOpenAI(temperature=temperature, model_name="gpt-4o-2024-08-06")
    elif model_name == "anthropic":
        return ChatAnthropic(
            temperature=temperature, model_name="claude-3-5-sonnet-20240620"
        )
    elif model_name == "gemini":
        genai.configure(api_key=validate_api_key("GEMINI_API_KEY"))
        return genai.GenerativeModel(model_name="gemini-pro")
    elif model_name == "groq":
        return ChatGroq(
            temperature=temperature, groq_api_key=validate_api_key("GROQ_API_KEY")
        )
    elif model_name == "lmstudio":
        return ChatOpenAI(
            temperature=temperature,
            openai_api_base=validate_api_key("LM_STUDIO_API_BASE"),
            api_key=validate_api_key("OPENAI_API_KEY"),
        )
    elif model_name == "deepseek":
        api_client = DeepSeekAPI(api_key=validate_api_key("DEEPSEEK_API_KEY"))
        return {
            "chat": lambda prompt: api_client.chat_completion(
                prompt=prompt, temperature=temperature
            )
        }
    elif model_name == "ollama":
        base_url = validate_api_key("OLLAMA_BASE_URL")
        return Ollama(base_url=base_url, model=model_name)
    else:
        raise ValueError(f"Unsupported model name: {model_name}")
