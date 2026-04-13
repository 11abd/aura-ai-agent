from app.rag.rag_service import RAGService
from app.tools.web_search import WebSearchTool




class ResearchAgent:

    def __init__(self):
        self.rag_service = RAGService()
        self.web_search = WebSearchTool()

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

        docs, answer = self.rag_service.run(query)

        context = "\n\n".join([doc.page_content for doc in docs])

        #Smart condition
        if not self.is_retrieval_good(docs, query):
            web_result = self.web_search.search(query)

            context += "\n\n[WEB SEARCH RESULTS]\n" + web_result

        return {
            "query": query,
            "num_results": len(docs),
            "context": context,
            "summary": answer
        }