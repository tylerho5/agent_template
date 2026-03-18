from app.agents._base import AgentConfig
from app.tools.web_search import web_search

config = AgentConfig(
    name="researcher",
    description="Research a topic using web search and return a summary of findings",
    prompt_file="researcher",
    tools=[web_search],
)
