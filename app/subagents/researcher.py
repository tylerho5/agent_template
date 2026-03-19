from app.subagents._base import AgentConfig
from app.tools.web_search import web_search

PROMPT = """\
You are a research assistant. Your job is to find accurate, relevant \
information on the given topic.

Use your search tools to gather information. Synthesize findings into a \
clear, well-organized summary. Cite sources when possible."""

config = AgentConfig(
    name="researcher",
    description="Research a topic using web search and return a summary of findings",
    prompt=PROMPT,
    tools=[web_search],
)
