from app.graph.builder import build_graph
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_graph():
    app = build_graph()

    input_state = {
        "query": "Machine learning jobs in Chennai with Python and AWS",
        "plan": [],
        "context": None,
        "generated_resume": None,
        "score": None,
        "feedback": None,
        "retries": 0
    }

    logger.info("Running full agent system...")

    result = app.invoke(input_state)

    print("\n--- FINAL RESULT ---\n")
    print(f"Score: {result['score']}")
    print(f"Retries: {result['retries']}")
    print("\n--- FINAL RESUME ---\n")
    print(result["generated_resume"][:500])


if __name__ == "__main__":
    test_graph()