from dotenv import load_dotenv
from app.agents.planner_agent import PlannerAgent

load_dotenv()

topic = input("Enter research topic: ")

planner = PlannerAgent()

plan = planner.create_plan(topic)

print("\nResearch Plan:\n")
print(plan)