from retrieval.search import Search
from logger.logger import get_logger
from core.engine import RAGEngine
from guardtrail.confidence import return_with_confidence
from domains.router import DomainDetecter
from domains.router_llm import DomainDetectorLLM

class SearchingPipeline:
    def __init__(self, query: str, company: str):
        self.query = query.strip()
        self.companny = company.strip()
        self.logger = get_logger("pipeline.searching")
        self.router = DomainDetecter()
        self.llm_router = DomainDetectorLLM()
        self.rag_engine = RAGEngine()

    def validate(self):
        if not self.query:
            raise ValueError("Query missing")
        
        if not self.companny:
            raise ValueError("Company is require param")
        
    def run(self):
        self.validate()
        domain = self.llm_router.detect(self.query)
        context, confidence =  Search(self.query, self.companny, domain).search()
        self.logger.debug(f"detected domain {domain}")
        if not context:
            return {
                "answer": "No relevant information found in the documents.",
                "valid": False,
                "confidence": confidence
            }
        domain_handler = self.llm_router.get_domain(domain)
        answer = self.rag_engine.answer(question=self.query, context=context, domain_handler=domain_handler)
        self.logger.debug(f"LLM answer: {answer}")
        return return_with_confidence(
            answer,
            confidence,
            len(context)
        )

