from pydantic import BaseModel


class AgentRequest(BaseModel):
    query: str


class ResumeUploadResponse(BaseModel):
    message: str
    saved_path: str
    parsed_resume: str
    run_dir: str


class AgentResponse(BaseModel):
    query: str
    final_resume: str
    score: int
    feedback: str
    retries: int
    run_dir: str
