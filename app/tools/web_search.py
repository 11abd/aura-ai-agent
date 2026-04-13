import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()


class WebSearchTool:

    def __init__(self):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

    def search(self, query: str) -> str:
        """
        Perform real web search using Tavily
        """

        response = self.client.search(query=query, max_results=3)

        results = []

        for r in response.get("results", []):
            results.append(f"{r['title']}\n{r['content']}")

        return "\n\n".join(results)
    
    def run(self, query: str) -> str:
        return self.search(query)