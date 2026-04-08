from google.adk import Agent
from config import MODEL

report_agent = Agent(
    name="report_agent",
    model=MODEL,
    description="Generates a final business report.",
    instruction="""
Convert the structured JSON into a professional market intelligence report.

Include:
- Executive Summary
- Key Trends
- Opportunities
- Risks
- Conclusion

Keep it concise and business-friendly.
"""
)