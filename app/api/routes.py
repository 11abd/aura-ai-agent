from fastapi import APIRouter, File, HTTPException, UploadFile

from app.api.schemas import AgentRequest, AgentResponse, ResumeUploadResponse
from app.api.service import AgentService
from app.rag.knowledge_base import update_resume_and_refresh_index

router = APIRouter()

agent_service = AgentService()


@router.post("/run-agent", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    """
    Run full agent workflow
    """

    result = agent_service.run(request.query)

    return result


@router.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume source file and refresh the vector DB.
    """
    suffix = ""
    if file.filename:
        suffix = file.filename.rsplit(".", 1)[-1].lower()

    if suffix not in {"txt", "md", "pdf"}:
        raise HTTPException(status_code=400, detail="Upload a txt, md, or pdf resume.")

    content = await file.read()
    return update_resume_and_refresh_index(file.filename, content)
