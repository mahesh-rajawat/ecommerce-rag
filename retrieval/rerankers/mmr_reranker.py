            # semantic = cosine(self.query_vector, doc['embedding'])
import numpy as np
from logger.logger import get_logger 

MMR_TOP_K = 8

class MMRReranker:
    def __init__(self, lambda_param=0.6):
        self.lambda_param = lambda_param
        self.logger = get_logger("search.mmr_reranker")

    def rerank(self, query_vec, doc_embeddings, top_k):
        """
        query_vec: shape (d,)
        doc_embeddings: shape (n, d)
        """

        selected = []
        print(f"MMR Reranker: Starting reranking with {doc_embeddings.shape} documents")
        candidate_indices = list(range(len(doc_embeddings)))
        print(f"MMR Reranker: Starting with {len(candidate_indices)} candidates")
        self.logger.debug("Starting MMR reranking with %d candidates", len(candidate_indices))

        query_sims = np.dot(doc_embeddings, query_vec[0])  # shape (n,)
        self.logger.debug(f"Query similarities: {query_sims}")

        doc_sims = np.dot(doc_embeddings, doc_embeddings.T)
        self.logger.debug(f"Document similarities shape: {doc_sims.shape}")

        while len(selected) < MMR_TOP_K and candidate_indices:

            mmr_scores = []

            for idx in candidate_indices:

                relevance = query_sims[idx]

                if not selected:
                    diversity_penalty = 0
                else:
                    max_sim = max(doc_sims[idx][sel] for sel in selected)
                    diversity_penalty = max_sim

                score = (
                    self.lambda_param * relevance
                    - (1 - self.lambda_param) * diversity_penalty
                )
                # self.logger.debug(f"MMR score for idx {idx}: relevance={relevance}, diversity_penalty={diversity_penalty}, score={score}")
                mmr_scores.append((idx, score))

            best_idx = max(mmr_scores, key=lambda x: x[1])[0]

            selected.append(best_idx)
            candidate_indices.remove(best_idx)
            
        self.logger.info(f"Selected indices after MMR reranking: {len(selected)}")
        print(f"Selected indices after MMR reranking: {selected}")
        return selected