# AGENTS.md

## Build/Run Commands
- Run (local): `uvicorn app.main:app --reload`
- Run (docker): `docker compose up --build`
- Type Check: `python -m mypy app/`
- Lint: `python -m ruff check app/`
- Format: `python -m ruff format app/`

## Code Style Guidelines
- **Imports**: Group stdlib > third-party > local; sort alphabetically
- **Formatting**: Ruff (default settings)
- **Types**: Use type hints on function signatures
- **Naming**: snake_case (functions/vars), PascalCase (classes)
- **Errors**: Log with context via structured logger

## Architecture
- Agent framework: LangGraph with `create_agent`
- LLM provider: OpenRouter (any model)
- Tools: Auto-discovered from `app/tools/`
- Subagents: Auto-discovered from `app/agents/`
- Memory: Configurable checkpointer (in-memory / Redis)
