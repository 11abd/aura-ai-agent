from app.rag.rag_service import RAGService
from app.tools.web_search import WebSearchTool
from app.tools.tool_registry import ToolRegistry
from app.agents.tool_selector import ToolSelectorAgent




class ResearchAgent:

    def __init__(self):

        self.tool_registry = ToolRegistry()
        self.tool_selector = ToolSelectorAgent()

    def is_retrieval_good(self, docs, query: str) -> bool:
        """
        Check if retrieved documents are useful
        """

        # Condition 1: No docs
        if not docs or len(docs) == 0:
            return False

        # Condition 2: Very small content
        total_length = sum(len(doc.page_content) for doc in docs)
        if total_length < 100:
            return False

        # LLM validation (will add later)

        return True

    def research(self, query: str) -> dict:

        # 🔥 Step 1: Choose tool
        selection = self.tool_selector.select_tool(query)

        tool = self.tool_registry.get_tool(selection.tool_name)

        # 🔥 Step 2: Execute tool
        context = tool.run(query)

        return {
            "query": query,
            "tool_used": selection.tool_name,
            "reason": selection.reason,
            "context": context
        }