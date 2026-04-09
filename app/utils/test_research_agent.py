from app.agents.research_agent import ResearchAgent
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_research():
    agent = ResearchAgent()

    query = "Machine learning jobs in Chennai with Python and AWS"

    logger.info(f"Query: {query}")

    result = agent.research(query)

    print("\n--- SUMMARY ---\n")
    print(result["summary"])

    print("\n--- CONTEXT (RAW DATA) ---\n")
    print(result["context"][:500])


if __name__ == "__main__":
    test_research()