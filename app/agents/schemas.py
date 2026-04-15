from pydantic import BaseModel, Field


class CriticOutput(BaseModel):
    """
    Structured output for LLM-as-judge resume evaluation.
    """

    score: int = Field(description="Overall score from 0 to 10")
    verdict: str = Field(description="Short overall judgment of resume readiness")
    role_fit: int = Field(description="Role-fit score from 0 to 10")
    truthfulness: int = Field(description="Truthfulness score from 0 to 10")
    keyword_alignment: int = Field(description="Keyword alignment score from 0 to 10")
    clarity: int = Field(description="Clarity and structure score from 0 to 10")
    strategic_emphasis: int = Field(description="Strategic emphasis score from 0 to 10")
    strengths: str = Field(description="Top strengths observed in the resume")
    risks: str = Field(description="Biggest risks, gaps, or credibility issues")
    improvements: str = Field(description="Highest-impact improvements to make next")
    feedback: str = Field(description="Concise overall feedback summary")


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
