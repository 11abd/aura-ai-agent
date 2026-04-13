from app.rag.rag_service import RAGService


class RAGTool:
    """
    Tool wrapper for RAG system
    """

    def __init__(self):
        self.rag = RAGService()

    def run(self, query: str) -> str:
        """
        Execute RAG retrieval + generation
        """

        docs, answer = self.rag.run(query)

        context = "\n\n".join([doc.page_content for doc in docs])

        return context