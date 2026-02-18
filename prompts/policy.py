from prompts.base import BasePrompt

class PolicyPrompt(BasePrompt):

    def generate(self, context, question):

        return [
            
                {"role": "system", "content": self._system_prompts()},
                {"role": "user", "content": self._build_prompt(question, context)},
                {
                    "role": "user",
                    "content": f"Question: {question}"
                }
        ]


    def _system_prompts(self):
        return (
            "You are a strict e-commerce policy assistant. "
            "Answer ONLY using the provided context. "
            "You may use logical reasoning if the meaning is clear. "
            "Do NOT use external knowledge. "
            "If the answer cannot be derived from the context, say: "
            "'I don't know based on the given information.'"
        )
    
    def _build_prompt(self, question, context):
        joined = "\n---\n".join(context)

        return f"""
You are a strict policy assistant.
Answer ONLY from context.

Context:
{joined}

Question:
{question}

Answer:
"""
