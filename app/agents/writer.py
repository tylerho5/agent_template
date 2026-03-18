from app.agents._base import AgentConfig

config = AgentConfig(
    name="writer",
    description="Write or edit content such as emails, summaries, reports, or documentation",
    prompt_file="writer",
    tools=[],
)
