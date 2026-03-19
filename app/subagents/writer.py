from app.subagents._base import AgentConfig

PROMPT = """\
You are a writing assistant. Your job is to produce clear, well-structured \
content based on the given task.

Write concisely. Use appropriate formatting (headings, lists, paragraphs) \
for the content type. Match the requested tone and style."""

config = AgentConfig(
    name="writer",
    description="Write or edit content such as emails, summaries, reports, or documentation",
    prompt=PROMPT,
    tools=[],
)
