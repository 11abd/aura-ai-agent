from pydantic import BaseModel, Field


class CriticOutput(BaseModel):
    """
    Structured output for evaluation
    """

    score: int = Field(description="Score from 0 to 10")
    feedback: str = Field(description="Detailed improvement feedback")


class ToolSelection(BaseModel):
    """
    Output for selecting tool
    """

    tool_name: str = Field(
        description="Tool to use: rag or web_search"
    )

    reason: str = Field(
        description="Why this tool was chosen"
    )