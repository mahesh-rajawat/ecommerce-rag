from config.settings import DISTANCE_THRESHOLD

class ConfidenceScorer:
    def score(self, candidates:list, keywords_count:int) -> float:
        if not candidates:
            return 0.0
        
        distances = [
            c['distance']
            for c in candidates
        ]
        k_scores = [
            c['k_score']
            for c in candidates
        ]
        
        avg_distance = sum(distances) / len(distances)
        avg_k = sum(k_scores) / len(k_scores)

        # normalize distance (lower = better)
        distance_score = self._distance_to_score(avg_distance)

        #normalize keyword score
        keyword_score = min(avg_k / max(keywords_count, 1), 1.0)

        #coverage
        coverage_score = min(len(candidates) / 10, 1.0)

        strong = [c for c in candidates if c["distance"] < DISTANCE_THRESHOLD]
        coverage_score = min(len(strong) / 5, 1.0)

        confidence = (
            0.5 * distance_score +
            0.3 * keyword_score +
            0.2 * coverage_score
        )
        return round(confidence, 2)

    def _distance_to_score(self, d: float, max_d: float = 500) -> float:
        """
        Normalize FAISS L2 distance to 0–1
        """
        score = 1 - (d / max_d)
        return max(0.0, min(score, 1.0))

