from retrieval.search import Search
from logger.logger import get_logger
from core.engine import RAGEngine
from guardtrail.confidence import return_with_confidence
from domains.router import DomainDetecter

class SearchingPipeline:
    def __init__(self, query: str, company: str):
        self.query = query.strip()
        self.companny = company.strip()
        self.logger = get_logger("pipeline.searching")
        self.router = DomainDetecter()
        self.rag_engine = RAGEngine()

    def validate(self):
        if not self.query:
            raise ValueError("Query missing")
        
        if not self.companny:
            raise ValueError("Company is require param")
        
    def run(self):
        self.validate()
        domain = self.router.detect(self.query)
        context, confidence =  Search(self.query, self.companny, domain).search()
        
        if not context:
            return {
                "answer": "No relevant information found in the documents.",
                "valid": False,
                "confidence": confidence
            }
        domain_handler = self.router.get_domain(domain)
        answer = self.rag_engine.answer(question=self.query, context=context, domain_handler=domain_handler)
        
        return return_with_confidence(
            answer,
            confidence,
            len(context)
        )

