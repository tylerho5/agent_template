from dataclasses import dataclass, field

from langchain_core.tools import BaseTool


@dataclass
class AgentConfig:
    """Configuration for a subagent."""

    name: str
    description: str
    prompt_file: str  # stem only, e.g. "researcher" → app/prompts/researcher.txt
    tools: list[BaseTool] = field(default_factory=list)
    model: str | None = None  # None = inherit supervisor's model
