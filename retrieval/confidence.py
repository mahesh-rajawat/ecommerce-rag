from config.settings import DISTANCE_THRESHOLD
import numpy as np
from logger.logger import get_logger
from utils.math import cosine
import re

stopwords = {"the", "is", "in", "and", "to", "of", "a", "that", "it", "with", "as", "for", "was", "on", "are", "by", "this", "be", "or"}

class ConfidenceScorer:
    def __init__(self):
        self.logger = get_logger("confidence.scorer")

    def score(self, candidates:list, query:str, query_vector, keywords:list) -> float:
        if not candidates:
            return 0.0
        
        similarities = []
        keywords_matches = []
        for c in candidates:
            similarity = 1 - (c['distance'] / 2)
            similarities.append(similarity)
            # Keyword overlap: How many of the query keywords appear in the retrieved chunk?
            keyword = self.keyword_overlap(keywords, c["text"])
            keywords_matches.append(keyword)
        
        facts = self.extract_facts(query)
        print(f"Facts: {facts}")
        evidence = self.evidence_coverage(facts, candidates)

        self.logger.debug(f"evidence: {evidence}")
        
        # 1. Average of similarities - gives a sense of overall relevance
        top_n = min(3, len(similarities))
        semantic = np.mean(sorted(similarities, reverse=True)[:top_n])

        self.logger.debug(f"Average of similarities:{semantic}")
        # 2. Keyword match score - how well do the retrieved chunks match the query keywords?
        keyword_score = min(np.mean(keywords_matches), 1.0)

        self.logger.debug(f"keyword_score:{keyword_score}")

        # 
        top = max(similarities)

        strong = [
            s for s in similarities
            if s >= top * 0.9
        ]

        self.logger.debug(f"strong similarity:{strong}")

        # 3. Coverage: Do we have multiple strong matches, or just one? Multiple strong matches suggest a more reliable retrieval.
        agreement = min(len(strong) / 3, 1.0)

        self.logger.debug(f"agreement: {agreement}")

        # std measures: How much do the similarity scores differ from each other?
        # low = retrieval is consitent
        # high = retrieval is noisy
        # STD: If all candidates have similar scores, it suggests a consistent retrieval. A high std might indicate that only one chunk is relevant while others are noise.
        std = np.std(similarities)
        self.logger.debug(f"std: {std}")
        # Concentration to check, is all retrieved chunks clustered in quality
        # If std is low, it means the scores are concentrated, which is a good sign. If std is high, it means the scores are spread out, which could indicate noise.
        # Concentration: If the scores are tightly clustered (low std), it suggests a more reliable retrieval. A high std might indicate that only one chunk is relevant while others are noise.
        concentration = 1 - min(std / 0.3, 1.0)
        
        # Find: How many strong documents agree with each other?
        # Consistency: If multiple retrieved chunks have high similarity scores, it suggests that they are consistently relevant to the query. If only one chunk has a high score and the rest are low, it might indicate a less reliable retrieval.

        self.logger.debug(f"semantic: {semantic}, keyword_score: {keyword_score}, agreement: {agreement}, concentration: {concentration}")
        confidence = self.compute_confidence(
            semantic,
            keyword_score,
            agreement,
            concentration,
            evidence
        )
        self.logger.debug(f"confidence: {confidence}")

        return round(min(confidence, 1.0), 2)


    def keyword_overlap(self, keywords, text):
        t = text.lower()
        hits = sum(1 for k in keywords if k in t)
        return hits / max(len(keywords), 1)
    

    def compute_confidence(
        self,
        semantic,
        keyword,
        agreement,
        concentration,
        evidence
    ):
        semantic_factor = max((semantic - 0.4) / 0.6, 0)
        
        # Base score
        base = (
            0.35 * semantic +
            0.25 * agreement +
            0.15 * keyword +
            0.15 * concentration +
            0.10 * evidence
        )

        # Evidence penalty
        penalty = 1.0

        if concentration < 0.5:
            penalty *= 0.7

        if agreement == 0:
            penalty *= 0.5

        if semantic < 0.5:
            penalty *= 0.6

        if evidence < 0.4:
            penalty *= 0.5

        if evidence < 0.2:
            penalty *= 0.3
        
        self.logger.debug(f"Base confidence: {base}, Penalty: {penalty}, Semantic factor: {semantic_factor}")

        return round(base * penalty, 3)
    
    # Evidence score

    def extract_facts(self, query):
        words = query.lower().split()
        numbers = re.findall(r'\d+', query)
        dates = re.findall(r'\b\d{4}-\d{2}-\d{2}\b', query)
        keywords = [
            w
            for w in words
            if len(w) > 2 and w not in stopwords
        ]
        return set(keywords + numbers + dates)
    
    def evidence_coverage(self, facts:dict, candidates):
        
        text = " ".join(c["text"].lower() for c in candidates)
        hits = 0
        for f in facts:
            if f in text:
                hits += 1
        
        return hits / max(len(facts), 1)

        