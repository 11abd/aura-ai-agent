from app.agents.research_agent import ResearchAgent
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_tool_selection():
    agent = ResearchAgent()

    queries = [
        "Machine learning jobs in Chennai",
        "Latest AI trends in 2026",
        "Python developer jobs with AWS"
    ]

    for q in queries:
        print("\n========================")
        print(f"Query: {q}")

        result = agent.research(q)

        print(f"Tool Used: {result['tool_used']}")
        print(f"Reason: {result['reason']}")
        print(f"Context Preview:\n{result['context'][:300]}")


if __name__ == "__main__":
    test_tool_selection()