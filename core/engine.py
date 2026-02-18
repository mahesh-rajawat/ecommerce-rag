from llm.factory import get_llm_client
from prompts.factory import get_prompt

class RAGEngine:

    def __init__(self):
        self.llm = get_llm_client()

    def answer(self, domain, context, question):
        prompt_builder = get_prompt(domain)
        prompt = prompt_builder.generate(context, question)
        self.llm.generate(prompt)

        return self.llm.get_answer()