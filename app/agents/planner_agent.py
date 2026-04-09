from app.config.llm import get_llm
from app.agents.prompts import get_planner_prompt


class PlannerAgent:
    """
    Agent responsible for breaking down user goals into steps
    """

    def __init__(self):
        self.llm = get_llm()
        self.prompt = get_planner_prompt()

    def create_plan(self, goal: str) -> list:
        """
        Generate plan from user goal
        """

        formatted_prompt = self.prompt.format(goal=goal)

        response = self.llm.invoke(formatted_prompt)

        plan_text = response.content

        return self._parse_plan(plan_text)

    def _parse_plan(self, plan_text: str) -> list:
        """
        Convert numbered text into list of steps
        """

        steps = []

        for line in plan_text.split("\n"):
            line = line.strip()

            if line and line[0].isdigit():
                # Remove "1. ", "2. " etc.
                step = line.split(".", 1)[-1].strip()
                steps.append(step)

        return steps