from retrieval.search import Search
from logs.logger import get_logger
from core.engine import RAGEngine
from guardtrail.confidence import return_with_confidence

class SearchingPipeline:
    def __init__(self, query: str, company: str):
        self.query = query.strip()
        self.companny = company.strip()
        self.logger = get_logger("pipeline.searching")
        self.rag_engine = RAGEngine()

    def validate(self):
        if not self.query:
            raise ValueError("Query missing")
        
        if not self.companny:
            raise ValueError("Company is require param")
        
    def run(self):
        self.validate()

        context, confidence =  Search(self.query, self.companny).search()
        
        if not context:
            return {
                "answer": "No relevant information found in the documents.",
                "valid": False,
                "confidence": confidence
            }
        answer = self.rag_engine.answer(domain='policy', question=self.query, context=context)
        
        return return_with_confidence(
            answer,
            confidence,
            len(context)
        )

