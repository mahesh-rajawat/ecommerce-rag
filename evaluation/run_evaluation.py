from app.evaluation.runner import EvaluationRunner
from app.evaluation.report import Report

runner = EvaluationRunner("app/evaluation/evaluation_dataset_v1.json")

results = runner.run()
report = Report(results)
report.generate()