from domains.policy import PolicyDomain
from domains.base import BaseDomain

POLICY_WORDS = {
    "vat", "tax", "terms", "policy", "refund", "return", "warranty", "delivery", "sell"
}

PRODUCT_WORDS = {
    "price", "cost", "buy", "purchase", "model", "spec", "feature"
}

class DomainDetecter:
    def __init__(self):
        self.domains = {
            "policy": PolicyDomain()
        }

    def detect(self, query: str) -> str:
        q = query.lower()
        p_words = [w in q for w in POLICY_WORDS]
        print("matched policy words", p_words)
        policy_score = sum(w in q for w in POLICY_WORDS)
        pr_words = sum(w in q for w in PRODUCT_WORDS)
        print("matched product words", pr_words)
        product_score = sum(w in q for w in PRODUCT_WORDS)

        if policy_score >= product_score:
            return "policy"
        return "product"
    
    def get_domain(self, name: str) -> BaseDomain:
        return self.domains.get(name, self.domains.get("policy"))