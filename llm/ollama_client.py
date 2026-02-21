
from llm.client import LLMClient
from logger.logger import get_logger
import ollama

class OllamaClient(LLMClient):

    def generate(self, prompt):
        self.logger.info("Calling LLM")
        
        self.response = ollama.chat(
            model="llama3.2",
            messages=prompt,
            options={
                "temperature": 0.1,
            }
        )

    def get_answer(self):
        return self.response["message"]["content"]
    
