from app.rag.rag_service import RAGService
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_rag_llm():
    rag = RAGService()

    query = "Find machine learning jobs in Chennai with Python"

    logger.info(f"Query: {query}")

    answer = rag.generate_answer(query)

    print("\n--- FINAL ANSWER ---\n")
    print(answer)


if __name__ == "__main__":
    test_rag_llm()