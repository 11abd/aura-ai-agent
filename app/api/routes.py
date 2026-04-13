from fastapi import APIRouter
from app.api.schemas import AgentRequest, AgentResponse
from app.api.service import AgentService

router = APIRouter()

agent_service = AgentService()


@router.post("/run-agent", response_model=AgentResponse)
def run_agent(request: AgentRequest):
    """
    Run full agent workflow
    """

    result = agent_service.run(request.query)

    return result