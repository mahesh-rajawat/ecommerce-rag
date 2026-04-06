from app.llm.factory import get_llm_client


class RAGEngine:

    def __init__(self):
        self.llm = get_llm_client()

    def answer(self, context, question, domain_handler):

        prompt = domain_handler.get_prompt(context, question)
        answer_format = domain_handler.get_answer_format()
        self.llm.generate(prompt, answer_format=answer_format)

        return self.llm.get_answer()