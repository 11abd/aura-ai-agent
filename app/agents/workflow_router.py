from app.agents.prompts import get_workflow_router_prompt
from app.agents.schemas import WorkflowRoute
from app.config.llm import get_llm


class WorkflowRouterAgent:
    """
    LLM router that decides whether to run the resume pipeline.
    """

    def __init__(self):
        self.llm = get_llm()
        self.prompt = get_workflow_router_prompt()

    def decide(self, query: str) -> WorkflowRoute:
        """
        Return a workflow routing decision for the query.
        """
        formatted_prompt = self.prompt.format(query=query)
        structured_llm = self.llm.with_structured_output(WorkflowRoute)
        response = structured_llm.invoke(formatted_prompt)
        return response
