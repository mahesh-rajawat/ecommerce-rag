from app.config.settings import DISTANCE_THRESHOLD
import numpy as np
from app.logger.logger import get_logger
from app.utils.math import cosine
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
            0.40 * semantic +
            0.15 * agreement +
            0.15 * keyword +
            0.10 * concentration +
            0.20 * evidence
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
        query_lower = query.lower()
        words = query_lower.split()
        
        # Use our CONCEPT_GROUPS to expand the facts
        expanded = self.expand_keywords(words)
        
        numbers = re.findall(r'\d+', query)
        # Currency is a HARD fact. If query has € and doc has €, evidence should spike.
        currency = re.findall(r'€|euro|eur|\$|dollar', query_lower)
        
        # Filter out stopwords but keep expanded concepts
        significant_words = {w for w in words if w not in stopwords and len(w) > 2}
        
        return significant_words.union(expanded).union(set(numbers)).union(set(currency))
    
    def evidence_coverage(self, facts:dict, candidates):
        
        text = " ".join(c["text"].lower() for c in candidates)
        hits = 0
        for f in facts:
            if f in text:
                hits += 1
        
        return hits / max(len(facts), 1)
    
    def expand_keywords(self, words):
        # Concept Buckets: Group everything that means the same thing
        CONCEPT_GROUPS = {
            "shipping": ["shipping", "delivery", "postage", "freight", "transport", "shipment"],
            "costs": ["price", "cost", "fee", "charge", "amount", "euro", "€", "handling"],
            "returns": ["return", "refund", "exchange", "cancel", "restitution"],
            "condition": ["opened", "package", "original", "used", "new", "seal"]
        }

        expanded = set()
        for w in words:
            w_lower = w.lower()
            expanded.add(w_lower)
            
            # If the word belongs to a concept, add the whole bucket
            for concept, bucket in CONCEPT_GROUPS.items():
                if w_lower in bucket or w_lower == concept:
                    expanded.update(bucket)
        
        return expanded

        