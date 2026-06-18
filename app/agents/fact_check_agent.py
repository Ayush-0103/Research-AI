import json
import re

from langchain_google_genai import ChatGoogleGenerativeAI


class FactCheckAgent:

    def __init__(self):

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.1
        )

    def verify_research(self, research_data):

        prompt = f"""
You are a senior research analyst.

Research Data:

{json.dumps(research_data, indent=2)}

Tasks:

1. Review all sections.
2. Remove weak claims.
3. Summarize each section.
4. Extract important statistics.
5. Assign confidence level.

Return ONLY valid JSON.

Format:

[
  {{
    "section": "...",
    "summary": "...",
    "key_statistics": [
      "...",
      "..."
    ],
    "confidence": "High"
  }}
]
"""

        response = self.llm.invoke(prompt)

        cleaned = re.sub(
            r"```json|```",
            "",
            response.content
        ).strip()

        return json.loads(cleaned)