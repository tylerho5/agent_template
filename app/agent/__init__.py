from pathlib import Path


def load_prompt(name: str) -> str:
    """Load a prompt template by name (without extension) from app/prompts/."""
    path = Path(__file__).resolve().parent.parent / "prompts" / f"{name}.txt"
    return path.read_text().strip()
