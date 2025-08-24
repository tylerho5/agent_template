# AI Agent Boilerplate

Python boilerplate for LangGraph-based AI agent with OpenRouter integration.

## Features
- LangGraph workflow with OpenRouter (via OpenAI API)
- Tool separation using `langchain-core`
- Prompt management in `prompts/`
- FastAPI endpoints (`/health`, `/query`)
- Modular tool system for easy extension
- Configurable prompts and model settings

## Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenRouter API key and model preference

# Run the server
uvicorn main:app --reload
```

## Project Structure
- `main.py`: Core FastAPI app and LangGraph workflow
- `tools.py`: Custom tools (weather, web search)
- `utils.py`: Utility functions (prompt loading)
- `prompts/`: System and user prompt templates
- `.env`: Environment variables (API keys, model settings)

## Adding Custom Tools
1. Define new tool functions in `tools.py` using `@tool` decorator
2. Import tools in `main.py` and add to the `tools` list
3. Agent will automatically use available tools when needed

## Customization
- Modify prompts in `prompts/` directory
- Change model settings in `.env` file
- Extend workflow in `main.py` for complex behaviors

## Example Usage
```bash
# Health check
curl http://localhost:8000/health

# Query endpoint
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the weather in New York?"}'
```

## Development
- Type checking: `source venv/bin/activate && python -m mypy main.py`
- Linting: `source venv/bin/activate && python -m pylint main.py`