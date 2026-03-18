from pydantic import BaseModel, Field
from langchain_core.tools import tool


class WebSearchInput(BaseModel):
    query: str = Field(description="The search query to look up")
    num_results: int = Field(default=5, description="Number of results to return")


@tool(args_schema=WebSearchInput)
def web_search(query: str, num_results: int = 5) -> str:
    """Search the web for information on a given query."""
    # Replace with real search API (e.g., Tavily, SerpAPI, Brave)
    return f"[Mock] Top {num_results} results for: {query}"
