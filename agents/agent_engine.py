from app.agents.parser import AgentParser
from app.agents.state import AgentState

class AgentEngine:
    def __init__(self, llm, tool_registery):
        self.llm = llm
        self.tool_registery = tool_registery
        self.parser = AgentParser()

    def run(self, question: str):
        state = AgentState(question)

        for step in range(5):
            prompt = self.build_prompt()
            response = self.llm(prompt)

            parsed = self.parser.parse(response)

            #Final answer
            if parsed['final_answer']:
                state.set_final_answer(parsed['final_answer'])
                return state
            
            #Tool execution
            action = parsed['action']
            action_input = parsed['action_input']

            if not action:
                return state
            
            observation = self.tool_registery.execute(action, action_input)

            state.add_step(parsed['thought'], action, action_input, observation)

            return state

    
    def build_prompt(self, state):
        history = ""

        for step in state.steps:
            history += f"""
Thought: {step['thought']}
Action: {step['action']}
Action Input: {step['input']}
Observation: {step['observation']}
"""
        return f"""
You are an AI commerce assistant.

Available tools:
- search_knowledge
- search_products

Rules:
- Use tools when needed
- Do NOT guess
- Think step by step

Format:
Thought:
Action:
Action Input:

When done:
Final Answer:

Question: {state.question}

{history}
"""
        

            