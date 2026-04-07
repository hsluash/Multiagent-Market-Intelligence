from google.adk import Agent
from config import MODEL

report_agent = Agent(
    name="report_agent",
    model=MODEL,
    instruction="""
You will receive structured JSON with:
- trends
- opportunities
- risks

Convert it into a professional business report.

Format:
- Title
- Key Trends
- Opportunities
- Risks
- Summary

Be concise and clear.
"""
)