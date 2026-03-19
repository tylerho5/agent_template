import importlib
import pkgutil

from app.subagents._base import AgentConfig

REGISTRY: dict[str, AgentConfig] = {}


def _discover_agents() -> None:
    """Scan all modules in app/subagents/ and collect AgentConfig instances."""
    package = importlib.import_module("app.subagents")
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        if module_name.startswith("_"):
            continue
        module = importlib.import_module(f"app.subagents.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, AgentConfig):
                REGISTRY[attr.name] = attr


_discover_agents()
