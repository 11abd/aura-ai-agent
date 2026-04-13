from app.config.llm import get_llm
from app.rag.loader import load_resume
from app.agents.prompts import get_generator_prompt


class GeneratorAgent:
    """
    Agent responsible for generating tailored resume
    """

    def __init__(self):
        self.llm = get_llm()
        self.prompt = get_generator_prompt()

        # Load resume once (efficient)
        self.resume = load_resume("data/raw/resume.txt")

    def generate_resume(self, job_context: str) -> str:
        """
        Generate tailored resume using job context
        """

        formatted_prompt = self.prompt.format(
            resume=self.resume,
            context=job_context
        )

        response = self.llm.invoke(formatted_prompt)

        return response.content