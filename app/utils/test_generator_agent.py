from app.agents.generator_agent import GeneratorAgent
from app.agents.research_agent import ResearchAgent
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_generator():
    research_agent = ResearchAgent()
    generator_agent = GeneratorAgent()

    query = "Machine learning jobs in Chennai with Python and AWS"

    logger.info("Fetching job context...")

    research_result = research_agent.research(query)

    context = research_result["context"]

    logger.info("Generating tailored resume...")

    resume = generator_agent.generate_resume(context)

    print("\n--- GENERATED RESUME ---\n")
    print(resume)


if __name__ == "__main__":
    test_generator()