from google.adk import Agent
import os

model_name = os.getenv("MODEL")

data_agent = Agent(
    name="report_agent",
    model=model_name,
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