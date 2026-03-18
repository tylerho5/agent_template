from pydantic import BaseModel, Field
from langchain_core.tools import tool


class WeatherInput(BaseModel):
    location: str = Field(description="City or location to get weather for")


@tool(args_schema=WeatherInput)
def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    # Replace with real weather API
    return f"[Mock] Sunny, 72°F in {location}"
