from config.settings import DISTANCE_THRESHOLD
import numpy as np
from logger.logger import get_logger
from utils.math import cosine

class ConfidenceScorer:
    def __init__(self):
        self.logger = get_logger("confidence.scorer")

    def score(self, candidates:list, query_vector, keywords:list) -> float:
        if not candidates:
            return 0.0
        
        similarities = []
        keywords_matches = []
        for c in candidates:
            similarity = cosine(query_vector, c["embedding"])
            similarities.append(similarity)

            keyword = self.keyword_overlap(keywords, c["text"])
            keywords_matches.append(keyword)
        
        
        # 1. Average of similarities
        semantic = np.mean(similarities)
        self.logger.debug(f"Average of similarities:{semantic}")
        
        keyword_score = min(np.mean(keywords_matches), 1.0)

        self.logger.debug(f"keyword_score:{keyword_score}")

        # find the string similarity
        strong = [s for s in similarities if s > 0.7]

        self.logger.debug(f"strong similarity:{strong}")

        coverage = min(len(strong) / 5, 1.0)

        self.logger.debug(f"coverage: {coverage}")

        # std measures: How much do the similarity scores differ from each other?
        # low = retrieval is consitent
        # high = retrieval is noisy
        std = np.std(similarities)
        self.logger.debug(f"std: {std}")
        # Concentration to check, is all retrieved chunks clustered in quality
        concentration = 1 - min(std / 0.3, 1.0)
        
        # Find: How many strong documents agree with each other?
        supporting = len(strong)
        consistency = min(supporting / 3, 1.0)
        self.logger.debug(f"semantic: {semantic}, keyword_score: {keyword_score}, coverage: {coverage}, concentration: {concentration}, consistency: {consistency}")
        confidence = self.compute_confidence(
            semantic,
            keyword_score,
            coverage,
            concentration,
            consistency
        )
        self.logger.debug(f"confidence: {confidence}")

        return round(min(confidence, 1.0), 2)

        # distances = [
        #     c['distance']
        #     for c in candidates
        # ]
        # k_scores = [
        #     c['k_score']
        #     for c in candidates
        # ]
        
        # avg_distance = sum(distances) / len(distances)
        # avg_k = sum(k_scores) / len(k_scores)

        # # normalize distance (lower = better)
        # distance_score = self._distance_to_score(avg_distance)

        # #normalize keyword score
        # keyword_score = min(avg_k / max(keywords_count, 1), 1.0)

        # #coverage
        # coverage_score = min(len(candidates) / 10, 1.0)

        # strong = [c for c in candidates if c["distance"] < DISTANCE_THRESHOLD]
        # coverage_score = min(len(strong) / 5, 1.0)

        # confidence = (
        #     0.5 * distance_score +
        #     0.3 * keyword_score +
        #     0.2 * coverage_score
        # )
        # return round(confidence, 2)

    # def _distance_to_score(self, d: float, max_d: float = 500) -> float:
    #     """
    #     Normalize FAISS L2 distance to 0–1
    #     """
    #     score = 1 - (d / max_d)
    #     return max(0.0, min(score, 1.0))

    def keyword_overlap(self, keywords, text):
        t = text.lower()
        hits = sum(1 for k in keywords if k in t)
        return hits / max(len(keywords), 1)
    

    def compute_confidence(
        self,
        semantic,
        keyword,
        coverage,
        concentration,
        consistency
    ):
        # Hard fail
        if semantic < 0.5:
            return 0.05

        # Base score
        base = (
            0.35 * semantic +
            0.25 * coverage +
            0.20 * consistency +
            0.10 * keyword +
            0.10 * concentration
        )

        # Evidence penalty
        penalty = 1.0

        if coverage == 0:
            penalty *= 0.5

        if consistency == 0:
            penalty *= 0.5

        if semantic < 0.5:
            penalty *= 0.6
        
        self.logger.debug(f"Base confidence: {base}, Penalty: {penalty}")

        return round(base * penalty, 3)

