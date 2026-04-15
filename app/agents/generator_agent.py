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

    def generate_resume(
        self,
        job_context: str,
        critic_feedback: str = "",
        retry_count: int = 0
    ) -> str:
        """
        Generate tailored resume using job context and prior judge feedback.
        """

        feedback = critic_feedback.strip() if critic_feedback else "No previous judge feedback."
        formatted_prompt = self.prompt.format(
            resume=self.resume,
            context=job_context,
            feedback=feedback,
            attempt=retry_count + 1
        )

        response = self.llm.invoke(formatted_prompt)

        return response.content
