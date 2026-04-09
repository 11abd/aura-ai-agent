from app.rag.rag_service import RAGService


class ResearchAgent:

    def __init__(self):
        self.rag_service = RAGService()

    def research(self, query: str) -> dict:

        docs, answer = self.rag_service.run(query)

        context = "\n\n".join([doc.page_content for doc in docs])

        return {
            "query": query,
            "num_results": len(docs),
            "context": context,
            "summary": answer
        }