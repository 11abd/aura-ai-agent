import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables

load_dotenv()

def get_llm():
    """
    Returns a configured OpenAI LLM instance
    This will be reused across agents
    """
    return ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
    temperature=0.3,  # lower = more deterministic
    max_tokens=1000
    )
