class BaseDomain:
    name = "base"

    def get_prompt(self, context, question: str) -> str:
        raise NotImplementedError
    
    def get_threshold(self) -> float:
        return 0.5
    
    def get_min_confidence(self) -> float:
        return 0.35