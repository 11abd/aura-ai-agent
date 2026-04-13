from typing import TypedDict, List, Optional


class AgentState(TypedDict):
    """
    Shared state across all nodes
    """

    query: str
    plan: List[str]

    context: Optional[str]
    generated_resume: Optional[str]

    score: Optional[int]
    feedback: Optional[str]

    retries: int