from google.adk import Agent
from tools.market_tools import get_market_trends
import os

model_name = os.getenv("MODEL")

data_agent = Agent(
    name="data_agent",
    model=model_name,
    instruction="""
Retrieve market trends using the available tool.
Return only relevant data.
""",
    tools=[get_market_trends],
)