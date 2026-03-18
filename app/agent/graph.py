from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pydantic import SecretStr

from app.config import get_settings
from app.tools import get_tools
from app.agent.memory import get_checkpointer, get_store


def _load_prompt(name: str) -> str:
    path = Path(__file__).resolve().parent.parent / "prompts" / f"{name}.txt"
    return path.read_text().strip()


def build_supervisor():
    """Build and return the compiled supervisor agent."""
    settings = get_settings()

    llm = ChatOpenAI(
        api_key=SecretStr(settings.openrouter_api_key),
        base_url=settings.openrouter_base_url,
        model=settings.openrouter_model,
    )

    # Collect direct tools + dispatch tool (added in Plan 4)
    tools = get_tools()

    try:
        from app.agent.dispatch import get_dispatch_tool

        dispatch = get_dispatch_tool()
        if dispatch is not None:
            tools = [*tools, dispatch]
    except ImportError:
        pass

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=_load_prompt("supervisor"),
        checkpointer=get_checkpointer(),
        store=get_store(),
    )
    return agent
