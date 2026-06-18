import json

from dotenv import load_dotenv

from app.agents.fact_check_agent import FactCheckAgent

load_dotenv()

with open(
    "research_data.json",
    "r",
    encoding="utf-8"
) as f:

    research_data = json.load(f)

fact_checker = FactCheckAgent()

verified_data = fact_checker.verify_research(
    research_data
)

with open(
    "verified_research.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        verified_data,
        f,
        indent=4,
        ensure_ascii=False
    )

print("Verified research saved successfully.")