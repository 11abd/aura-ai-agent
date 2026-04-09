from langchain_core.prompts import PromptTemplate


def get_planner_prompt():
    """
    Prompt for planning steps based on user goal
    """

    template = """
You are an AI planning agent.

Break the user's goal into clear, step-by-step actions.

Rules:
- Be logical and structured
- Keep steps concise
- Maximum 5 steps
- Each step should be actionable

User Goal:
{goal}

Output format:
1. Step one
2. Step two
3. Step three
"""

    return PromptTemplate(
        input_variables=["goal"],
        template=template
    )