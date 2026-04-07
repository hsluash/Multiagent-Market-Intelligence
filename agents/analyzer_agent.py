from google.adk import Agent
from config import MODEL

analyzer_agent = Agent(
    name="analyzer_agent",
    model=MODEL,
    instruction="""
Analyze the provided market data and extract insights.

Return ONLY valid JSON in this exact format:

{
  "trends": ["..."],
  "opportunities": ["..."],
  "risks": ["..."]
}

Rules:
- Do NOT add any extra text
- Do NOT explain anything
- Output must be valid JSON only
"""
)