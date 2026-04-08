from google.adk import Agent
from config import MODEL

analyzer_agent = Agent(
    name="analyzer_agent",
    model=MODEL,
    description="Extracts structured insights from market data.",
    instruction="""
Analyze the provided market data and extract:

1. Key Trends (3-5)
2. Opportunities (2-4)
3. Risks (2-4)

Return ONLY valid JSON in this format:
{
  "trends": [],
  "opportunities": [],
  "risks": []
}

Be concise and non-redundant.
"""
)
