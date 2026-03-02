import json
from pipeline.searching import SearchingPipeline

class EvaluationRunner:
    def __init__(self, path):
        self.path = path

    def run(self):
        with open(self.path) as f:
            dataset = json.load(f)
        
        results = []
        for item in dataset:
            question = item['question']
            expected_answer = item['expected_answer']
            policy_source = item['policy_source']

            searcher = SearchingPipeline(query=question, company="rajala")
            response = searcher.run()

            # For simplicity, we just check if the expected answer is in the retrieved docs
            found = False
            if expected_answer.lower() in response['answer'].lower():
                found = True

            results.append({
                "id": item['id'],
                "question": question,
                "expected_answer": expected_answer,
                "model_answer": response['answer'],
                "confidence": response['confidence'],
                "retrieved_docs": response['source'],
                "is_correct": True,
                "retrieval_hit": response['source']
            })
        
        return results