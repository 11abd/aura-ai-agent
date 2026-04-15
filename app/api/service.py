from app.graph.builder import build_graph
from app.utils.run_logger import RunLogger

class AgentService:
    """
    Handles execution of the full agent workflow
    """

    def __init__(self):
        self.graph = build_graph()

    def run(self, query: str):
        """
        Execute agent system
        """
        logger = RunLogger()

        input_state = {
            "query": query,
            "plan": [],
            "context": None,
            "generated_resume": None,
            "score": None,
            "feedback": None,
            "retries": 0,
            "logger" :logger
        }

        result = self.graph.invoke(input_state)

        logger.save()

        return {
            "query": query,
            "final_resume": result["generated_resume"],
            "score": result["score"],
            "retries": result["retries"]
        }