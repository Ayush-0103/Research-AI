import json

from dotenv import load_dotenv

from app.agents.report_writer_agent import ReportWriterAgent

load_dotenv()

with open(
    "verified_research.json",
    "r",
    encoding="utf-8"
) as f:

    verified_research = json.load(f)

writer = ReportWriterAgent()

report = writer.generate_report(
    "Electric Vehicle Market in India",
    verified_research
)

with open(
    "report.md",
    "w",
    encoding="utf-8"
) as f:

    f.write(report)

print("Report saved successfully.")