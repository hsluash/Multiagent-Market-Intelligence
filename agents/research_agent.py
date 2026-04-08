from google.adk import Agent
from google.adk.tools import google_search
from config import MODEL
 
research_agent = Agent(
    name="research_agent",
    model=MODEL,
    description="Adds deeper insights to the market context using live web research.",
    tools=[google_search],
    instruction="""
You are a market research agent.
 
Use the google_search tool to gather the latest real-world insights about the given topic.
 
STRICT RULES:
- Stay ONLY within the topic
- Do NOT include unrelated industries
- Focus on recent developments, demand signals
- Mention key companies
- Mention investments
- Mention policies
 
Output a concise research summary.
"""
)