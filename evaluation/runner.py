import json
from app.pipeline.searching import SearchingPipeline

class EvaluationRunner:
    def __init__(self, dataset_path):
        self.dataset = self.load_dataset(dataset_path)

    def load_dataset(self, dataset_path):
        with open(dataset_path, 'r') as f:
            dataset = json.load(f)
        return dataset
    
    def run(self):
        results = []

        for item in self.dataset:
            print(f"Running: {item['id']}")
            searching = SearchingPipeline(
                item['question'],
                item['company']
            )
            response = searching.run()

            results.append({
                "id": item["id"],
                "question": item["question"],
                "answer": response["answer"],
                "confidence": response["confidence"],
                "sources": response["sources"],
                "expected": item
            })
        
        return results

