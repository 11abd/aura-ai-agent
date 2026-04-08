import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Settings:
    """
    Central configuration class
    All environment variables should be accessed from here
    """

    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/aura_db"
    )

    # App Config
    APP_NAME: str = "AURA AI Agent"
    DEBUG: bool = True


# Create a global settings object
settings = Settings()