from app.evaluation.matrics import Matrics

class Report:
    def __init__(self, results):
        self.results = results
        self.matrics = Matrics()

    def generate(self):
        total = len(self.results)

        retrieval = 0
        answer = 0
        confidence = 0

        for r in self.results:
            retrieval += self.matrics.retrieval_hit(r)
            answer += self.matrics.answer_match(r)
            confidence += self.matrics.confidence_ok(r)

        print("\n=======Evaluation Report===========")
        
        print("Total Queries:", total)
        
        print("Retrieval Accurecy:",
             round(retrieval / total, 2))
        
        print("Answer Accurecy:",
              round(answer / total, 2))
        
        print("Confidence Accuracy:",
              round(confidence / total, 2))