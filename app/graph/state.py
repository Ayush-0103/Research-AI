from typing import TypedDict, List


class ResearchState(TypedDict):

    topic: str

    sections: List[str]

    research_data: List[dict]

    verified_research: List[dict]