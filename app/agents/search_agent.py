from app.tools.search_tool import SearchTool


class SearchAgent:

    def __init__(self):
        self.search_tool = SearchTool()

    def research_section(self, section: str):

        results = self.search_tool.search(section)

        return {
            "section": section,
            "results": results
        }