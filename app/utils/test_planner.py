from app.agents.planner_agent import PlannerAgent
from app.utils.logger import setup_logger, get_logger

setup_logger()
logger = get_logger(__name__)


def test_planner():
    agent = PlannerAgent()

    goal = "Find machine learning jobs and generate a tailored resume"

    logger.info(f"Goal: {goal}")

    plan = agent.create_plan(goal)

    print("\n--- GENERATED PLAN ---\n")

    for i, step in enumerate(plan):
        print(f"{i+1}. {step}")


if __name__ == "__main__":
    test_planner()