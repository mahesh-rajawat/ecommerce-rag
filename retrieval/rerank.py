from config.settings import DISTANCE_THRESHOLD
from logger.logger import get_logger
from utils.math import cosine

class Reranker:
    stopwords = {"the", "is", "in", "and", "to", "of", "a", "that", "it", "with", "as", "for", "was", "on", "are", "by", "this", "be", "or"}

    def __init__(self, query, query_vector):
        self.query = query
        self.query_vector = query_vector
        self.logger = get_logger("search.rerank")

    def re_rank(self, distance, indexes, documents):
        self.logger.info("Reranking candidates")
        keywords = self.extract_keywords()
        candidates = []
        for dis, idx in zip(distance, indexes):
        # index saftey, else index not found error
            if idx < 0 or idx >= len(documents):
                continue
        
            doc = documents[idx]
            k_score = self.keyword_score(doc['text'], keywords)
            # semantic = cosine(self.query_vector, doc['embedding'])
            semantic = 1 - (dis / 2)

            #self.logger.debug(f"semantic={semantic}")
            keyword = min(k_score / 5, 1.0)
            final_score = (
                0.7 * semantic +
                0.3 * keyword
            )
            
            self.logger.debug(f"RE-RANK idx={idx} dist={dis} semantic={semantic} k-score={k_score} final_score={final_score}")

            if final_score < 0.3:
                continue
            

            if dis < DISTANCE_THRESHOLD or k_score > 0:
                candidates.append({
                    'idx': int(idx),
                    "distance": float(dis),
                    "semantic": semantic,
                    "k_score": int(k_score),
                    "text": doc['text'],
                    "final_score": final_score
                })
            

        #Rank results
        candidates.sort(
            key=lambda x: x["final_score"],
            reverse=True
        )

        self.logger.info("Final candidates: %d", len(candidates))

        return candidates

    def extract_keywords(self):
        words = self.query.lower().split()

        kewords = [
            w
            for w in words
            if len(w) > 2 and w not in self.stopwords
        ]
        
        return kewords

    def keyword_score(self, text:str, keywords: list):
        expanded = self.expand_keywords(keywords)
        score = 0
        for k in expanded:
            if k in text:
                score += 1
        
        return score

    def expand_keywords(self, words):

        SYNONYMS = {
            "tax-free": ["exclusive", "exempt", "no tax"],
            "before": ["exclusive", "prior"],
            "vat": ["vat", "tax"],
            "price": ["price", "cost", "fee"],
            "under 18": ["minor", "underage", "youth"],
            "over 18": ["adult", "overage", "mature"],
            "discount": ["discount", "reduction", "offer"],
            "minor": ["minor", "underage", "under age 18"],
        }

        expanded = set()

        for w in words:
            expanded.add(w)

            if w in SYNONYMS:
                expanded.update(SYNONYMS[w])
        print("Expanded keywords:", expanded)
        return expanded