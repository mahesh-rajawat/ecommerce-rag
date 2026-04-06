from app.logger.logger import get_logger

class LLMClient:

    def __init__(self):
        self.logger = get_logger("llm.client")

    def generate(self, prompt: str) -> str:
        raise NotImplementedError
    
    def get_answer():
        raise NotImplementedError