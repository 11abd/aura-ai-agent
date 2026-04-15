import re

from app.agents.tool_selector import ToolSelectorAgent
from app.tools.tool_registry import ToolRegistry


class ResearchAgent:
    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.tool_selector = ToolSelectorAgent()

    def is_retrieval_good(self, docs, query: str) -> bool:
        """
        Check if retrieved documents are useful.
        """
        if not docs:
            return False

        total_length = sum(len(doc.page_content) for doc in docs)
        if total_length < 100:
            return False

        query_tokens = set(re.findall(r"[a-z0-9\+\#\.]+", query.lower()))
        matched_tokens = set()

        for doc in docs:
            matched_tokens.update(re.findall(r"[a-z0-9\+\#\.]+", doc.page_content.lower()))
            matched_tokens.update(re.findall(r"[a-z0-9\+\#\.]+", doc.metadata.get("title", "").lower()))
            matched_tokens.update(re.findall(r"[a-z0-9\+\#\.]+", doc.metadata.get("location", "").lower()))
            for skill in doc.metadata.get("skills", []):
                matched_tokens.update(re.findall(r"[a-z0-9\+\#\.]+", skill.lower()))

        if query_tokens and len(query_tokens & matched_tokens) / len(query_tokens) < 0.3:
            return False

        return True

    def research(self, query: str) -> dict:
        selection = self.tool_selector.select_tool(query)
        selected_tool_name = selection.tool_name
        tool = self.tool_registry.get_tool(selected_tool_name)

        if selected_tool_name == "rag":
            docs = tool.retrieve(query)
            if self.is_retrieval_good(docs, query):
                context = tool.format_documents(docs)
            else:
                selected_tool_name = "web_search"
                selection.reason = (
                    f"{selection.reason} RAG fallback triggered because local matches were weak."
                )
                context = self.tool_registry.get_tool(selected_tool_name).run(query)
        else:
            context = tool.run(query)

        return {
            "query": query,
            "tool_used": selected_tool_name,
            "reason": selection.reason,
            "context": context,
        }
