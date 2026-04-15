from app.rag.rag_service import RAGService


class RAGTool:
    """
    Tool wrapper for RAG system
    """

    def __init__(self):
        self.rag = RAGService()

    def retrieve(self, query: str):
        """
        Retrieve documents without generating an answer.
        """
        return self.rag.retrieve_documents(query)

    def format_documents(self, docs) -> str:
        """
        Convert retrieved documents into a single context string.
        """
        return "\n\n".join([doc.page_content for doc in docs])

    def run(self, query: str) -> str:
        """
        Execute RAG retrieval + generation
        """

        docs = self.retrieve(query)
        return self.format_documents(docs)
