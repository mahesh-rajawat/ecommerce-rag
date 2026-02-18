class BasePrompt:
    def generate(self, context, question):
        raise NotImplementedError