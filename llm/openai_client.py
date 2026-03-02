import os
from dotenv import load_dotenv
from openai import OpenAI
from llm.client import LLMClient

class OpenAIClient(LLMClient):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
    
    def generate(self, prompt):
        self.logger.info("Calling OpenAI LLM")
        
        return super().generate(prompt)