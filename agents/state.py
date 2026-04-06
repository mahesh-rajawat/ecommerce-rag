class AgentState:
    def __init__(self, question: str):
        self.question = question
        self.state = []
        self.final_answer = None

    def add_step(self, thought, action, action_input, observation):
        self.state.append({
            "thought": thought,
            "action": action,
            "input": action_input,
            "observation": observation
        })

    def set_final_answer(self, answer):
        self.final_answer = answer
        