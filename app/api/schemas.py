from pydantic import BaseModel


class AgentRequest(BaseModel):
    query: str


class AgentResponse(BaseModel):
    query: str
    final_resume: str
    score: int
    retries: int