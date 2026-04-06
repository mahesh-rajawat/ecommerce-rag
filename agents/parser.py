
class AgentParser:
    def parse(self, text:str):
        result = {
            "thought": None,
            "action": None,
            "input": None,
            "final_answer": None
        }

        if "Final Answer:" in text:
            result["final_answer"] = text.split("Final Answer:")[1].strip()
            return result
        if "Thought:" in text:
            result["thought"] = text.split("Thought:")[1].split("\n")[0].strip()

        if "Action:" in text:
            result["action"] = text.split("Action:")[1].split("\n")[0].strip()

        if "Action Input:" in text:
            result["input"] = text.split("Action Input:")[1].split("\n")[0].strip()

        return result
    