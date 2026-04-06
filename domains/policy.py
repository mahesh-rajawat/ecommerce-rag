from app.domains.base import BaseDomain

from pydantic import BaseModel, Field
from typing import List, Optional


class PolicyResponse(BaseModel):

    product_identity_confirmed: bool

    detected_product: Optional[str]

    evidence: List[str] = Field(
        description="Exact sentences copied from the context that support the answer."
    )

    reasoning: str = Field(
        description="Explain the answer using ONLY the evidence."
    )

    final_answer: str

    is_permitted: bool

    sources_used: List[int]


class PolicyDomain(BaseDomain):
    name = "policy"

    

    def get_prompt(self, context, question):

        context_string = "\n\n---\n\n".join(
            [f"[ID: {doc['id']}]\n{doc['text']}" for doc in context]
        )
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

CONDITION MATCHING RULE

Before applying a policy rule, verify that the condition in the USER QUESTION
matches the condition in the policy text.

Do not treat similar phrases as equivalent.

Examples:

"opened package" ≠ "product put into use"
"damaged packaging" ≠ "used product"
"trying the product" ≠ "product in use"

If the policy condition does not exactly match the situation in the question,
do not apply the rule.

Instructions:
- Use only the provided context.
- Apply rules logically to specific cases.
- If a rule clearly applies, explain it.
- Only answer "Not specified" if the context contains no related rule.
- If the product mentioned in the question does not appear in the provided context, you must answer:
 'The policy does not mention this product specifically.'
- Do not infer category membership.

Context:
{context_string}

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

    def get_answer_format(self):
        return PolicyResponse