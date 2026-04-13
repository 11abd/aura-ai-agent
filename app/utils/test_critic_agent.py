from app.agents.research_agent import ResearchAgent
from app.agents.generator_agent import GeneratorAgent
from app.agents.critic_agent import CriticAgent
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_full_pipeline():
    research_agent = ResearchAgent()
    generator_agent = GeneratorAgent()
    critic_agent = CriticAgent()

    query = "Machine learning jobs in Chennai with Python and AWS"

    logger.info("Step 1: Research...")
    research_result = research_agent.research(query)

    context = research_result["context"]

    logger.info("Step 2: Generate resume...")
    resume = generator_agent.generate_resume(context)

    logger.info("Step 3: Evaluate resume...")
    evaluation = critic_agent.evaluate(context, resume)

    print("\n--- GENERATED RESUME ---\n")
    print(resume[:500])

    print("\n--- EVALUATION ---\n")
    print(f"Score: {evaluation.score}/10")
    print(f"Feedback: {evaluation.feedback}")


if __name__ == "__main__":
    test_full_pipeline()