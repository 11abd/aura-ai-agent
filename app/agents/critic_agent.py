from app.config.llm import get_llm
from app.agents.prompts import get_critic_prompt
from app.agents.schemas import CriticOutput


class CriticAgent:
    """
    Agent responsible for LLM-as-judge evaluation of generated resumes.
    """

    def __init__(self):
        self.llm = get_llm()
        self.prompt = get_critic_prompt()

    def evaluate(self, context: str, resume: str) -> CriticOutput:
        """
        Evaluate resume and return structured LLM-as-judge output.
        """

        formatted_prompt = self.prompt.format(
            context=context,
            resume=resume
        )

        structured_llm = self.llm.with_structured_output(CriticOutput)
        response = structured_llm.invoke(formatted_prompt)

        return response
