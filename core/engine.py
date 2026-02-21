from llm.factory import get_llm_client


class RAGEngine:

    def __init__(self):
        self.llm = get_llm_client()

    def answer(self, context, question, domain_handler):

        prompt = domain_handler.get_prompt(context, question)
        self.llm.generate(prompt)

        return self.llm.get_answer()