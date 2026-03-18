from enum import Enum

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pydantic import SecretStr

from app.agent import load_prompt
from app.agents import REGISTRY
from app.config import get_settings


def get_dispatch_tool():
    """Build and return the task dispatch tool, or None if no subagents registered."""
    if not REGISTRY:
        return None

    AgentName = Enum("AgentName", {name.upper(): name for name in REGISTRY})

    agent_descriptions = "\n".join(
        f"- {cfg.name}: {cfg.description}" for cfg in REGISTRY.values()
    )

    tool_description = (
        "Delegate a task to a specialized subagent.\n\n"
        f"Available agents:\n{agent_descriptions}\n\n"
        "Args:\n"
        "    agent_name: Which agent to delegate to.\n"
        "    description: Detailed description of the task for the subagent."
    )

    @tool(description=tool_description)
    def task(agent_name: AgentName, description: str) -> str:
        """Delegate a task to a specialized subagent."""
        config = REGISTRY[agent_name.value]
        settings = get_settings()

        model_name = config.model or settings.openrouter_model
        llm = ChatOpenAI(
            api_key=SecretStr(settings.openrouter_api_key),
            base_url=settings.openrouter_base_url,
            model=model_name,
        )

        subagent = create_agent(
            llm,
            tools=config.tools,
            system_prompt=load_prompt(config.prompt_file),
        )

        result = subagent.invoke(
            {"messages": [{"role": "user", "content": description}]}
        )
        return result["messages"][-1].content

    return task
