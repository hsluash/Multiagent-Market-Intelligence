from google.adk import Agent
from tools.market_tools import get_market_trends
from config import MODEL

data_agent = Agent(
    name="data_agent",
    model=MODEL,
    instruction="""
Retrieve market trends using the available tool.
Return only relevant data.
""",
    tools=[get_market_trends],
)