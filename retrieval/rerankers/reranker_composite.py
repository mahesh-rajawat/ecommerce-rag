

from email.mime import text

from retrieval.rerank import Reranker
from retrieval.rerankers.mmr_reranker import MMRReranker
from config.settings import TOP_K

stopwords = {"the", "is", "in", "and", "to", "of", "a", "that", "it", "with", "as", "for", "was", "on", "are", "by", "this", "be", "or"}


class RerankerComposite:
    def __init__(self, query:str, query_vector):
        self.query = query
        self.query_vector = query_vector
        self.reranker = Reranker(query, query_vector)
        self.mmr_reranker = MMRReranker()

    def re_rank(self, distance, indexes, documents, doc_embeddings):
    
        candidates = self.reranker.re_rank(distance, indexes, documents)
        if not candidates:
            return []
        indexes = [c['idx'] for c in candidates]
        print(f"Candidate indexes before MMR: {indexes}")
        doc_embeddings = doc_embeddings[indexes]
        mmr_reranked_idx = self.mmr_reranker.rerank(self.query_vector, doc_embeddings, top_k=TOP_K)
        reranked_candidates = [candidates[i] for i in mmr_reranked_idx]

        re_indexes = [c['idx'] for c in reranked_candidates]
        print(f"Reranked candidate indexes: {re_indexes}")

        return reranked_candidates
    
    def extract_keywords(self):
        words = self.query.lower().split()

        kewords = [
            w
            for w in words
            if len(w) > 2 and w not in stopwords
        ]
        
        return kewords