from llm.factory import get_llm_client
from domains.router import DomainDetecter
from logger.logger import get_logger

class DomainDetectorLLM(DomainDetecter):
    def __init__(self):
        super().__init__()
        self.llm = get_llm_client()
        self.logger = get_logger('llm_domain_detector')
        self.domain = 'general'
        
    def detect(self, query):
        prompt = self.get_prompt(query)
        self.logger.debug("Calling llm from domain detector")
        self.llm.generate(prompt)
        self.domain = self.llm.get_answer()
        self.logger.debug(f"Detected domain from llm {self.domain}")
        return self.domain
    

    def get_prompt(self, query):
        return [
            {
                "role": "system", "content": f"""
                    You are a Senior Routing Assistant for an E-commerce system. 
                    Classify the user query into exactly ONE of these categories:

                    1. 'product': Questions about item features, prices, stock levels, or technical specs.
                    2. 'policy': Questions about shipping, taxes (VAT), returns, age limits, legal eligibility, or terms of service.
                    3. 'general': Greetings, small talk, or gratitude.

                    Constraint: Reply with ONLY the category name in lowercase. Do not explain your choice.
                """
                
            },
            {"role": "user", "content": f" Query: {query}" }
        ]
    