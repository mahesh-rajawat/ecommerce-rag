import numpy as np
from config.settings import DIM, MAX_CONTEXT, TOP_K
from retrieval.rerank import Reranker
from retrieval.rerankers.reranker_composite import RerankerComposite
from preprocess.cleaner import clean_text
from index.embedder import Embedder
from guardtrail.validation import validate_distance_index, validate_retirived_docs
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
        query_vector = self.embeder.embed(self.query)
        reranker = RerankerComposite(self.query, query_vector)
        
        keywords = reranker.extract_keywords()
        index, docs, embeddings = self.vector_handler.load_company_data_and_index(
            get_domain_dir(self.company, self.domain)
        )
        D, I = self.search_vector(index, query_vector)
        is_valid = validate_distance_index(D, I)
        if (is_valid == False):
            return False
        
        safe_dis, safe_indexes, safe_docs = validate_retirived_docs(D, I, docs, self.company, self.domain)
        self.logger.info(f"Found %d safe documents after validation", len(safe_docs))
        print(f"Found {safe_indexes} safe documents after validation")

        # Rerank candidates
        candidates = reranker.re_rank(safe_dis, safe_indexes, documents=safe_docs, doc_embeddings=embeddings)

        context = self.__get_context(candidates, docs)

        confidence = ConfidenceScorer().score(candidates, self.query, query_vector, keywords=keywords)
        if not context:
            return False

        return context, confidence

    def search_vector(self, index, vector):
        self.logger.debug("Running vector search")
        self.vector_handler.normalize_embeddings(vector)
        
        D, I = index.search(vector, k=TOP_K)
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
    