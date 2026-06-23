from dataclasses import dataclass
from rich.console import Console

CONSOLE = Console()

@dataclass
class Model:
    provider: str
    model: str | None
    api_key: str | None