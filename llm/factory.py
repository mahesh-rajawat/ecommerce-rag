from app.llm.ollama_client import OllamaClient
from app.config.settings import LLM_PROVIDER


def get_llm_client():

    if LLM_PROVIDER == "ollama":
        return OllamaClient()

    else:
        raise ValueError("Invalid LLM provider")