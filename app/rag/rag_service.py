from app.rag.pipeline import build_or_load_vector_db
from app.rag.retriever import get_retriever
from app.config.llm import get_llm
from app.rag.prompt import get_rag_prompt


class RAGService:
    """
    Handles full RAG pipeline:
    Retriever + LLM + Prompt
    """

    def __init__(self):
        self.vector_store = build_or_load_vector_db()
        self.retriever = get_retriever(self.vector_store)
        self.llm = get_llm()
        self.prompt = get_rag_prompt()

    def retrieve_context(self, query: str) -> str:
        """
        Retrieve relevant documents using semantic search
        """

        docs = self.retriever.invoke(query)  

        context = "\n\n".join([doc.page_content for doc in docs])

        return context

    def generate_answer(self, query: str) -> str:
        """
        Full RAG execution
        """

        context = self.retrieve_context(query)

        formatted_prompt = self.prompt.format(
            context=context,
            question=query
        )

        response = self.llm.invoke(formatted_prompt)

        return response.content