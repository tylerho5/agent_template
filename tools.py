from langchain_core.tools import tool
import inspect
import sys

# Example of how to add a new tool:
# To add a new tool, simply define it with the @tool decorator
# The get_tools() function will automatically detect and include it
# @tool
# def calculator(expression: str) -> str:
#     """Evaluate a mathematical expression"""
#     try:
#         result = eval(expression)
#         return str(result)
#     except Exception as e:
#         return f"Error: {str(e)}"

@tool
def get_weather(location: str) -> str:
    """Get current weather for a location"""
    return f"Sunny, 72°F in {location}"

@tool
def search_web(query: str) -> str:
    """Search the web for information"""
    return f"Results for: {query}"

def get_tools():
    """Dynamically collect all tool functions from this module and return them as a list."""
    current_module = sys.modules[__name__]
    tools = []
    for name, obj in inspect.getmembers(current_module):
        if hasattr(obj, 'name') and hasattr(obj, 'invoke'):
            # This is a tool function (has tool decorator attributes)
            tools.append(obj)
    return tools