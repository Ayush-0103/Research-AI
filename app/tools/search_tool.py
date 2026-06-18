import os
from tavily import TavilyClient


class SearchTool:

    def __init__(self):
        self.client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )

    def search(self, query: str):
        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        cleaned_results = []

        for item in response.get("results", []):
            cleaned_results.append(
                {
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "content": item.get("content"),
                }
            )

        return cleaned_results