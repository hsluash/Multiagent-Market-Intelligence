from google.adk import Agent
from tools.market_tools import get_market_trends
from config import MODEL

data_agent = Agent(
    name="data_agent",
    description="Generates initial market context and raw observations.",
    tools=[get_market_trends],
    instruction="""
You are responsible for generating initial market context.

Given a topic:
- Describe general market trends
- Mention demand patterns
- Keep it concise
"""
)