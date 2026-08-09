from dataclasses import dataclass
from rich.console import Console

CONSOLE = Console()

@dataclass
class Model:
    provider: str | None = "ollama"
    model: str | None = "NONE"
    api_key: str | None = "NONE"
    data_sharing: str | None = "LOCAL"  # default value for data sharing