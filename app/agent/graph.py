from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pydantic import SecretStr

from app.agent import load_prompt
from app.config import get_settings
from app.tools import get_tools
from app.agent.memory import get_checkpointer, get_store


def build_supervisor():
    """Build and return the compiled supervisor agent."""
    settings = get_settings()

    llm = ChatOpenAI(
        api_key=SecretStr(settings.openrouter_api_key),
        base_url=settings.openrouter_base_url,
        model=settings.openrouter_model,
    )

    # Collect direct tools + dispatch tool
    tools = get_tools()

    try:
        from app.agent.dispatch import get_dispatch_tool
    except ImportError:
        pass
    else:
        dispatch = get_dispatch_tool()
        if dispatch is not None:
            tools = [*tools, dispatch]

    agent = create_agent(
        llm,
        tools=tools,
        system_prompt=load_prompt("supervisor"),
        checkpointer=get_checkpointer(),
        store=get_store(),
    )
    return agent
