
from app.llm.client import LLMClient
from app.logger.logger import get_logger
from app.core.base_answer_format import BaseAnswerFormat
import ollama

class OllamaClient(LLMClient):

    def generate(self, prompt, answer_format=BaseAnswerFormat):
        # self.logger.info(f"Calling Ollama LLM with answer format: {answer_format.model_json_schema()}")
        self.response = ollama.chat(
            model="llama3.2",
            messages=prompt,
            options={
                "temperature": 0.1,
                "max_tokens": 2000,
            },
            format=answer_format.model_json_schema()
        )

    def get_answer(self):
        # print("Raw response from Ollama:", self.response)
        return self.response["message"]["content"]
    
    def detect_domain(self, prompt):
        self.logger.info("Calling Ollama LLM for domain detection")
        self.response = ollama.chat(
            model="llama3.2",
            messages=prompt,
            options={
                "temperature": 0.1,
                "max_tokens": 10,
            },
        )
    
