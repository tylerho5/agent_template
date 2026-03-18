# AI Agent Template

A complete Python template for building AI agents with LangGraph and OpenRouter.

## Features

- **LangGraph supervisor agent** with tool calling via OpenRouter
- **Subagent system** — single-dispatch pattern with auto-discovered agents
- **Streaming** — SSE endpoint for real-time token streaming
- **Conversation memory** — in-memory default, Redis opt-in
- **Long-term memory** — opt-in persistent memory store
- **Auto-discovery** — drop in tools or agents, they're registered automatically
- **Docker ready** — `docker compose up` and go

## Quick Start

### Local

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your OpenRouter API key
uvicorn app.main:app --reload
```

### Docker

```bash
cp .env.example .env  # add your OpenRouter API key
docker compose up --build
```

## Project Structure

```
app/
├── main.py              # FastAPI entrypoint
├── config.py            # Settings (pydantic-settings)
├── api/
│   ├── routes.py        # /query, /query/stream, /health
│   └── middleware.py     # Error handling + request logging
├── agent/
│   ├── graph.py         # Supervisor agent (create_agent)
│   ├── memory.py        # Checkpointer factory (memory/redis)
│   └── dispatch.py      # Single-dispatch subagent tool
├── agents/
│   ├── _base.py         # AgentConfig dataclass
│   ├── researcher.py    # Example: research subagent
│   └── writer.py        # Example: writing subagent
├── tools/
│   ├── web_search.py    # Example tool
│   └── weather.py       # Example tool
└── prompts/
    └── agent.md         # Main agent system prompt
```

## Usage

### Query (sync)

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the weather in Tokyo?"}'
```

### Query (streaming)

```bash
curl -X POST http://localhost:8000/query/stream \
  -H "Content-Type: application/json" \
  -d '{"text": "Research the latest AI trends"}'
```

### Conversation threads

Pass `thread_id` to maintain context across requests:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"text": "My name is Alice", "thread_id": "abc123"}'

curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"text": "What is my name?", "thread_id": "abc123"}'
```

## Adding a Tool

Create a file in `app/tools/`:

```python
from pydantic import BaseModel, Field
from langchain_core.tools import tool

class MyToolInput(BaseModel):
    query: str = Field(description="...")

@tool(args_schema=MyToolInput)
def my_tool(query: str) -> str:
    """Description of what this tool does."""
    return "result"
```

It's auto-discovered. No imports needed elsewhere.

## Adding a Subagent

Create a config in `app/agents/my_agent.py`:

```python
from app.agents._base import AgentConfig
from app.tools.my_tool import my_tool

PROMPT = """\
You are a specialist assistant. Your job is to ...

Use your tools to accomplish the task. Be concise."""

config = AgentConfig(
    name="my_agent",
    description="What this agent does (the supervisor reads this)",
    prompt=PROMPT,
    tools=[my_tool],
)
```

It's auto-discovered and available via the `task` dispatch tool.

## Configuration

See `.env.example` for all options. Key settings:

| Variable | Default | Description |
|---|---|---|
| `OPENROUTER_API_KEY` | (required) | Your OpenRouter API key |
| `OPENROUTER_MODEL` | `openai/gpt-4o-mini` | Model for the supervisor agent |
| `MEMORY_BACKEND` | `memory` | `memory` or `redis` |
| `LONG_TERM_MEMORY` | `false` | Enable persistent memory store |
| `CORS_ORIGINS` | `*` | Allowed CORS origins |

## License

MIT
