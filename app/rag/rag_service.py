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

    def retrieve_documents(self, query: str):
        """
        Retrieve documents once (optimized)
        """
        return self.retriever.invoke(query)

    def generate_answer_from_docs(self, query: str, docs):
        """
        Generate answer using already retrieved docs
        """

        context = "\n\n".join([doc.page_content for doc in docs])

        formatted_prompt = self.prompt.format(
            context=context,
            question=query
        )

        response = self.llm.invoke(formatted_prompt)

        return response.content

    def run(self, query: str):
        """
        Full pipeline (optimized)
        """

        docs = self.retrieve_documents(query)

        answer = self.generate_answer_from_docs(query, docs)

        return docs, answer