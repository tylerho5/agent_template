import importlib
import pkgutil

from app.agents._base import AgentConfig

REGISTRY: dict[str, AgentConfig] = {}


def _discover_agents() -> None:
    """Scan all modules in app/agents/ and collect AgentConfig instances."""
    package = importlib.import_module("app.agents")
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        if module_name.startswith("_"):
            continue
        module = importlib.import_module(f"app.agents.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, AgentConfig):
                REGISTRY[attr.name] = attr


_discover_agents()
