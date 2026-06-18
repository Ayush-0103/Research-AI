import json
from langchain_google_genai import ChatGoogleGenerativeAI
import re


class PlannerAgent:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2
        )

    def create_plan(self, topic: str):

        prompt = f"""
You are a senior industry research consultant.

Topic:
{topic}

Create a research plan specifically for this topic.

The section names must include the topic context.

Return ONLY valid JSON.

Example:

{{
    "topic": "Electric Vehicle Market in India",
    "sections": [
        "Current Electric Vehicle Market Size in India",
        "Major EV Manufacturers in India",
        "Government EV Policies and Incentives",
        "Charging Infrastructure and Battery Ecosystem",
        "Future Outlook of EV Industry in India"
    ]
}}
"""

        response = self.llm.invoke(prompt)

        cleaned = re.sub(r"```json|```", "", response.content).strip()

        return json.loads(cleaned)