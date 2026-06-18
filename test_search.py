from dotenv import load_dotenv
import json

from app.agents.planner_agent import PlannerAgent
from app.agents.search_agent import SearchAgent

load_dotenv()

planner = PlannerAgent()
search_agent = SearchAgent()

topic = "Analyze Electric Vehicle Market in India"

plan = planner.create_plan(topic)

print("\nResearch Sections:\n")

research_data = []

for section in plan["sections"]:

    data = search_agent.research_section(
        plan["topic"],
        section
    )

    research_data.append(data)

    print("\n" + "=" * 80)
    print(f"SECTION: {section}")
    print("=" * 80)

    for result in data["results"]:

        print(f"\nTitle: {result['title']}")
        print(f"URL: {result['url']}")

with open(
    "research_data.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        research_data,
        f,
        indent=4,
        ensure_ascii=False
    )

print("\nResearch data saved to research_data.json")