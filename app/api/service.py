from app.agents.workflow_router import WorkflowRouterAgent
from app.graph.builder import build_graph
from app.utils.run_logger import RunLogger


class AgentService:
    """
    Handles execution of the full agent workflow
    """

    def __init__(self):
        self.graph = build_graph()
        self.workflow_router = WorkflowRouterAgent()

    def run(self, query: str):
        """
        Execute agent system
        """
        logger = RunLogger()

        route = self.workflow_router.decide(query)
        logger.log(
            "workflow_router",
            {
                "query": query,
                "use_resume_workflow": route.use_resume_workflow,
            }
        )

        if not route.use_resume_workflow:
            logger.log(
                "direct_response",
                {
                    "response_preview": route.direct_response[:300],
                }
            )
            logger.save_artifact("direct_response", route.direct_response, "md")
            logger.save()

            return {
                "query": query,
                "final_resume": route.direct_response,
                "score": 0,
                "feedback": "",
                "retries": 0,
                "run_dir": logger.run_dir,
            }

        input_state = {
            "query": query,
            "plan": [],
            "context": None,
            "generated_resume": None,
            "score": None,
            "feedback": None,
            "retries": 0,
            "logger": logger
        }

        result = self.graph.invoke(input_state)

        logger.log("final", {
            "query": query,
            "score": result["score"],
            "feedback": result["feedback"],
            "retries": result["retries"],
            "final_resume": result["generated_resume"]
        })
        logger.save_artifact("final_resume", result["generated_resume"], "md")
        logger.save_artifact("final_feedback", result["feedback"], "md")
        logger.save()

        return {
            "query": query,
            "final_resume": result["generated_resume"],
            "score": result["score"],
            "feedback": result["feedback"],
            "retries": result["retries"],
            "run_dir": logger.run_dir
        }
