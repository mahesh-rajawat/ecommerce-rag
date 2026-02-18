from llm.ollama_client import OllamaClient
from config.settings import LLM_PROVIDER


def get_llm_client():

    if LLM_PROVIDER == "ollama":
        return OllamaClient()

    else:
        raise ValueError("Invalid LLM provider")