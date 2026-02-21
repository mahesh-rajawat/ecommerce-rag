from config.settings import DISTANCE_THRESHOLD
from logger.logger import get_logger

class Reranker:
    stopwords = {"the", "is", "in", "and", "to", "of", "a", "that", "it", "with", "as", "for", "was", "on", "are", "by", "this", "be", "or"}

    def __init__(self, query):
        self.query = query
        self.logger = get_logger("search.rerank")

    def re_rank(self, distance, indexes, documents):
        self.logger.info("Reranking candidates")
        keywords = self.extract_keywords()
        candidates = []
        for dis, idx in zip(distance[0], indexes[0]):
        # index saftey, else index not found error
            if idx < 0 or idx >= len(documents):
                continue
        
            doc = documents[idx]
            k_score = self.keyword_score(doc['text'], keywords)

            if dis < DISTANCE_THRESHOLD or k_score > 0:
                candidates.append({
                    'idx': int(idx),
                    "distance": float(dis),
                    "k_score": int(k_score)
                })

        #Rank results
        candidates.sort(
            key=lambda x: (x['distance'], -x['k_score'])
        )

        for c in candidates:
            self.logger.debug(
                "Candidate idx=%s distance=%.2f keyword_score=%d",
                c["idx"], c["distance"], c["k_score"]
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
            "price": ["price", "cost", "fee"]
        }

        expanded = set()

        for w in words:
            expanded.add(w)

            if w in SYNONYMS:
                expanded.update(SYNONYMS[w])

        return expanded