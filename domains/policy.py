from domains.base import BaseDomain

class PolicyDomain(BaseDomain):
    name = "policy"

    def get_prompt(self, context, question):
        context = "\n---\n".join(context)
        system = (
            "You are a strict e-commerce policy assistant. "
            "Answer ONLY using the provided context. "
            "You may use logical reasoning if the meaning is clear. "
            "Do NOT use external knowledge. "
            "If the answer cannot be derived from the context, say: "
            "'I don't know based on the given information.'"    
        )
        user = f"""
You are a policy and terms assistant.

Rules:
- Answer only from context
- Do NOT guess
- If unclear, say: "Not specified"

Context:
{context}

Question:
{question}

Answer:
"""
        return [
            {"role": "system", "content": system.strip()},
            {"role": "user", "content": user.strip()},
            {"role": "user", "content": f"Question: {question}"}
        ]

    def get_threshold(self):
        return 0.45

    def get_min_confidence(self):
        return 0.35