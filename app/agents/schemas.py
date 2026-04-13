from pydantic import BaseModel, Field


class CriticOutput(BaseModel):
    """
    Structured output for evaluation
    """

    score: int = Field(description="Score from 0 to 10")
    feedback: str = Field(description="Detailed improvement feedback")