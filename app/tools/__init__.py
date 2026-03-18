import importlib
import pkgutil
from langchain_core.tools import BaseTool

_all_tools: list[BaseTool] | None = None


def get_tools() -> list[BaseTool]:
    """Auto-discover all @tool-decorated functions in app/tools/ modules."""
    global _all_tools
    if _all_tools is not None:
        return _all_tools

    _all_tools = []
    package = importlib.import_module("app.tools")
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f"app.tools.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, BaseTool):
                _all_tools.append(attr)
    return _all_tools
