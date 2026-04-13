from app.config.llm import get_llm
from app.agents.prompts import get_tool_selection_prompt
from app.agents.schemas import ToolSelection


class ToolSelectorAgent:
    """
    Agent to decide which tool to use
    """

    def __init__(self):
        self.llm = get_llm()
        self.prompt = get_tool_selection_prompt()

    def select_tool(self, query: str) -> ToolSelection:
        """
        Returns structured tool selection
        """

        formatted_prompt = self.prompt.format(query=query)

        structured_llm = self.llm.with_structured_output(ToolSelection)

        response = structured_llm.invoke(formatted_prompt)

        return response