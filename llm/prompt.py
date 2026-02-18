
class HandlePrompt:

    def __init__(self, context):
        self.context = context

    def build_user_prompt(self):

        joined = "\n---\n".join(self.context)

        return f"""
    Context:
    {joined}
    """

    def get_system_prompt(self):
        # print("Document in context:", self.context)
        # if self.context[0]['document'] == 'sales_and_delivery_terms':
            
        return self.get_policy_system_prompt()
    
    def get_policy_system_prompt(self):
        return (
            "You are a strict e-commerce policy assistant. "
            "Answer ONLY using the provided context. "
            "You may use logical reasoning if the meaning is clear. "
            "Do NOT use external knowledge. "
            "If the answer cannot be derived from the context, say: "
            "'I don't know based on the given information.'"
        )
