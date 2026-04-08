from app.config.llm import get_llm
from app.utils.logger import setup_logger, get_logger

# Setup logging
setup_logger()
logger = get_logger(__name__)

def test_llm():
    logger.info("Initializing LLM...")

    llm = get_llm()

    logger.info("Sending test prompt...")
    response = llm.invoke("Say hello like a professional AI system.")

    logger.info("LLM response received")
    print(response.content)

if __name__ == "__main__":
    test_llm()