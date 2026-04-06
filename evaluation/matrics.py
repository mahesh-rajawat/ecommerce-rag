class Matrics:
    def retrieval_hit(self, result):
        expected = result["expected"]["expected_chunk"]
        sources = result["sources"]

        for e in expected:
            if e in str(sources):
                return 1
            
        return 0
    
    def answer_match(self, result):
        expected_phrases = result["expected"]["expected_answer_contains"]
        answer = result['answer'].lower()
        hits = 0
        for p in expected_phrases:
            if p.lower() in answer:
                hits += 1
        
        return hits / len(expected_phrases)
    
    def confidence_ok(self, result):
        return 1 if result['confidence'] >= 0.4 else 0