import numpy as np
from config.settings import DIM, MAX_CONTEXT
from retrieval.rerank import Reranker
from preprocess.cleaner import clean_text
from index.embedder import Embedder
from guardtrail.validation import validate_distance_index
from retrieval.confidence import ConfidenceScorer
from vector_handlers.factory import get_vector_handler
from logger.logger import get_logger
from utils.paths import get_domain_dir

class Search:
    def __init__(self, query, company, domain):
        self.query = clean_text(query)
        self.company = company
        self.domain = domain
        self.embeder = Embedder()
        self.vector_handler = get_vector_handler()
        self.logger = get_logger("search")

    def search(self):
        reranker = Reranker(self.query)
        query_vector = self.embeder.embed_query(self.query)
        kewords = reranker.extract_keywords()
        index, docs = self.vector_handler.load_company_data_and_index(
            get_domain_dir(self.company, self.domain)
        )
        D, I = self.search_vector(index, query_vector)
        is_valid = validate_distance_index(D, I)
        if (is_valid == False):
            return False
        
        candidates = reranker.re_rank(D, I, documents=docs)
        context = self.__get_context(candidates, docs)
        confidence = ConfidenceScorer().score(candidates, len(kewords))
        if not context:
            return False
        
        return context, confidence

    def search_vector(self, index, vector):
        self.logger.debug("Running vector search")
        q_np_array = np.array([vector]).astype("float32")

        if q_np_array.ndim != 2 or q_np_array.shape[1] != DIM:
            raise ValueError("Invalid embedding dimension")
        
        D, I = index.search(q_np_array, k=15)
        self.logger.info("Vector search returned %d Indexes", len(I[0]))

        return [D, I]
    
    def __get_context(self, candidates, documents):
        context = []

        # Limit Total context length
        totalc_length = 0

        for c in candidates:
            text = documents[c['idx']]["text"]

            if totalc_length + len(text) > MAX_CONTEXT:
                break

            context.append(text)
            totalc_length += len(text)
        return context
    