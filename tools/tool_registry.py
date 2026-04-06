class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, tool):
        self.tools[tool.name] = tool

    def execute(self, name: str, input: str):
        tool = self.tools.get(name)
        if not tool:
            return f"Tool '{name}' not found"
        
        try:
            return tool.run(input)
        except Exception as e:
            return f"Tool execution failed: {str(e)}"
        
    def list_tools(self):
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools.values()
        ]