from app.tools.rag_tool import RAGTool
from app.tools.web_search import WebSearchTool


class ToolRegistry:
    """
    Central place to manage all tools
    """

    def __init__(self):
        self.tools = {
            "rag": RAGTool(),
            "web_search": WebSearchTool()
        }

    def get_tool(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())