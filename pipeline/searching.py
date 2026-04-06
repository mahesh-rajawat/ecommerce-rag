from app.retrieval.search import Search
from app.logger.logger import get_logger
from app.core.engine import RAGEngine
from app.guardtrail.confidence import return_with_confidence
from app.domains.router import DomainDetecter
from app.domains.router_llm import DomainDetectorLLM

class SearchingPipeline:
    def __init__(self, query: str, company: str):
        self.query = self.clear_query(query)
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
        self.logger.info(f"Detected domain: {domain} for {self.companny}")
        context, confidence =  Search(self.query, self.companny, domain).search()
        # print(f"Search returned context {context}")
        self.logger.info(f"Detected domain {domain}")
        if not context:
            return {
                "answer": "No relevant information found in the documents.",
                "valid": False,
                "confidence": confidence,
            }
        domain_handler = self.llm_router.get_domain(domain)
        answer = self.rag_engine.answer(question=self.query, context=context, domain_handler=domain_handler)
        self.logger.debug(f"LLM answer: {answer}")
        return return_with_confidence(
            answer,
            confidence,
            len(context)
        )
    
    def clear_query(self, query):
        return query.strip().replace("\n", " ").replace("?", "").replace("!", "")

