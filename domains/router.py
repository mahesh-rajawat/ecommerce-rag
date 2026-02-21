from domains.policy import PolicyDomain
from domains.base import BaseDomain

class DomainDetecter:
    def __init__(self):
        self.domains = {
            "policy": PolicyDomain()
        }

    def detect(self, query: str) -> str:
        q = query.lower()

        if "vat" in q or "terms" in q:
            return "policy"
        
        if "price" in q or "buy" in q:
            return "product"
        
        return "policy"
    
    def get_domain(self, name: str) -> BaseDomain:
        return self.domains.get(name, self.domains.get("policy"))