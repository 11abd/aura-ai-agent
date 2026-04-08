from langchain_openai import ChatOpenAI
from app.config.settings import settings

def get_llm():
    """
    Returns a configured OpenAI LLM instance
    """
    return ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0.3,
        max_tokens=1000,
        api_key=settings.OPENAI_API_KEY
    )