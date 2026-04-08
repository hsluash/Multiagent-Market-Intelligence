from google.adk import Agent
from config import MODEL

research_agent = Agent(
    name="research_agent",
    model=MODEL,
    tools=[{"google_search": {}}],
    generation_config={"temperature": 0.2},
    instruction="""
You are a market research agent.

Use real-world knowledge to gather the latest insights about the given topic.

STRICT RULES:
- Stay ONLY within the topic
- Do NOT include unrelated industries
- Focus on current trends, companies, and developments
- Mention key companies
- Mention investments
- Mention policies

Output a concise research summary.
"""
)