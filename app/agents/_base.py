from dataclasses import dataclass, field

from langchain_core.tools import BaseTool


@dataclass
class AgentConfig:
    """Configuration for a subagent."""

    name: str
    description: str
    prompt: str
    tools: list[BaseTool] = field(default_factory=list)
    model: str | None = None  # None = inherit supervisor's model
