from app.rag.pipeline import build_vector_db
from app.rag.retriever import get_retriever
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_rag():
    logger.info("Building vector DB...")

    vector_store = build_vector_db()

    retriever = get_retriever(vector_store)

    query = "Machine Learning jobs in Chennai with Python"

    logger.info(f"Query: {query}")

    results = retriever.invoke(query)

    print("\n--- RETRIEVED RESULTS ---\n")

    for i, doc in enumerate(results):
        print(f"\nResult {i+1}:\n")
        print(doc.page_content[:300])


if __name__ == "__main__":
    test_rag()