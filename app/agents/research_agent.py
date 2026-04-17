import re

from app.rag.langchain_loader import load_job_documents
from app.agents.tool_selector import ToolSelectorAgent
from app.tools.tool_registry import ToolRegistry


class ResearchAgent:
    GENERIC_QUERY_TOKENS = {
        "a",
        "an",
        "and",
        "apply",
        "application",
        "career",
        "developer",
        "developers",
        "engineer",
        "engineers",
        "find",
        "for",
        "freshers",
        "in",
        "job",
        "jobs",
        "looking",
        "match",
        "me",
        "my",
        "of",
        "on",
        "openings",
        "opportunities",
        "opportunity",
        "position",
        "positions",
        "resume",
        "role",
        "roles",
        "search",
        "show",
        "software",
        "tailor",
        "the",
        "to",
        "with",
        "work",
    }

    def __init__(self):
        self.tool_registry = ToolRegistry()
        self.tool_selector = ToolSelectorAgent()

    def _tokenize(self, text: str) -> set[str]:
        return set(re.findall(r"[a-z0-9\+\#\.]+", text.lower()))

    def _extract_signal_tokens(self, query: str) -> set[str]:
        tokens = self._tokenize(query)
        return {
            token for token in tokens
            if len(token) > 2 and token not in self.GENERIC_QUERY_TOKENS
        }

    def _load_local_job_tokens(self) -> set[str]:
        documents = load_job_documents("data/raw/jobs.txt")
        local_tokens = set()

        for doc in documents:
            local_tokens.update(self._tokenize(doc.page_content))
            local_tokens.update(self._tokenize(doc.metadata.get("title", "")))
            local_tokens.update(self._tokenize(doc.metadata.get("location", "")))
            local_tokens.update(self._tokenize(" ".join(doc.metadata.get("skills", []))))

        return local_tokens

    def should_force_web_search(self, query: str) -> bool:
        """
        Detect when the requested role is poorly covered by the local job corpus.
        """
        signal_tokens = self._extract_signal_tokens(query)
        if not signal_tokens:
            return False

        local_job_tokens = self._load_local_job_tokens()
        coverage = len(signal_tokens & local_job_tokens) / len(signal_tokens)

        # If the important role or skill tokens are mostly absent locally,
        # using RAG will likely return unrelated jobs.
        return coverage < 0.6

    def is_retrieval_good(self, docs, query: str) -> bool:
        """
        Check if retrieved documents are useful.
        """
        if not docs:
            return False

        total_length = sum(len(doc.page_content) for doc in docs)
        if total_length < 100:
            return False

        query_tokens = self._tokenize(query)
        signal_tokens = self._extract_signal_tokens(query)
        matched_tokens = set()

        for doc in docs:
            matched_tokens.update(self._tokenize(doc.page_content))
            matched_tokens.update(self._tokenize(doc.metadata.get("title", "")))
            matched_tokens.update(self._tokenize(doc.metadata.get("location", "")))
            for skill in doc.metadata.get("skills", []):
                matched_tokens.update(self._tokenize(skill))

        if query_tokens and len(query_tokens & matched_tokens) / len(query_tokens) < 0.3:
            return False

        if signal_tokens and len(signal_tokens & matched_tokens) / len(signal_tokens) < 0.6:
            return False

        return True

    def research(self, query: str) -> dict:
        if self.should_force_web_search(query):
            selected_tool_name = "web_search"
            reason = (
                "The requested role or skill set is not well covered by the local job dataset, "
                "so web search was used to avoid irrelevant RAG matches."
            )
        else:
            selection = self.tool_selector.select_tool(query)
            selected_tool_name = selection.tool_name
            reason = selection.reason

        tool = self.tool_registry.get_tool(selected_tool_name)

        if selected_tool_name == "rag":
            docs = tool.retrieve(query)
            if self.is_retrieval_good(docs, query):
                context = tool.format_documents(docs)
            else:
                selected_tool_name = "web_search"
                reason = (
                    f"{reason} RAG fallback triggered because local matches were weak or off-domain."
                )
                context = self.tool_registry.get_tool(selected_tool_name).run(query)
        else:
            context = tool.run(query)

        return {
            "query": query,
            "tool_used": selected_tool_name,
            "reason": reason,
            "context": context,
        }
