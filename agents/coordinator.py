from google.adk.agents import SequentialAgent
from agents.data_agent import data_agent
from agents.analyzer_agent import analyzer_agent
from agents.report_agent import report_agent
from agents.research_agent import research_agent

coordinator_agent = SequentialAgent(
    name="market_intelligence_coordinator",
    description="Coordinates agents to generate market reports",
    sub_agents=[
        data_agent,
        research_agent,
        analyzer_agent,
        report_agent
    ]
)

root_agent = coordinator_agent