from domains.base import BaseDomain

class PolicyDomain(BaseDomain):
    name = "policy"

    def get_prompt(self, context, question):
        context = "\n---\n".join(context)
        system = (
            "You are an e-commerce policy assistant. "
            "Answer strictly using the provided context. "
            "You must apply logical reasoning to interpret the rules. "
            "If a general rule covers a specific case, apply it. "
            "Do not invent information. "
            "Only say 'Not specified' if no relevant rule exists."
        )
        user = f"""
You are a policy and terms assistant.

Instructions:
- Use only the provided context.
- Apply rules logically to specific cases.
- If a rule clearly applies, explain it.
- Only answer "Not specified" if the context contains no related rule.
- If the product mentioned in the question does not appear in the provided context, you must answer:
 'The policy does not mention this product specifically.'
- Do not infer category membership.

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