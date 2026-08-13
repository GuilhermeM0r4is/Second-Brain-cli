import json
from AI.model import CONSOLE
from pathlib import Path

# Define config file path once
GENERATED_FILE = Path(__file__).parent.parent / "Storage" / "generated.json"


def load_generated(kind: str | None = None) -> dict | list | None:
    ''' loads generated data from generated.json, optionally filtered by kind '''
    try:
        with open(GENERATED_FILE, 'r') as file:
            data = json.load(file)

        # if there's no kind, just gives everything
        if kind is None: return data

        return data.get(kind, [])

    except FileNotFoundError:
        with open(GENERATED_FILE, "w") as file:
            json.dump({}, file)
        return {}

    except json.JSONDecodeError:
        return CONSOLE.print("[red]JSON Error: Corrupted generated.json file[/red]")


def save_generated(data: dict, kind: str) -> None:
    ''' takes the generated data and saves it into the json file '''

    try:    # looks into the existing data, to get an idea of wehre to store the kinds
        with open(GENERATED_FILE, "r") as file:
            existing = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError): existing = {}

    key = kind if kind in ("cards", "quiz") else "other"
    existing.setdefault(key, [])   # ensure it's a list
    existing[key].append(data)

    # stores the data into the existing ones
    with open(GENERATED_FILE, "w") as file:
        json.dump(existing, file, indent = 4)


def overwrite_generated(items: list, kind: str) -> None:
    ''' overwrites the full list of generated items for a given kind '''
    try:
        with open(GENERATED_FILE, "r") as file:
            existing = json.load(file)

    except (FileNotFoundError, json.JSONDecodeError): existing = {}
    existing[kind] = items
    
    with open(GENERATED_FILE, "w") as file:
        json.dump(existing, file, indent = 4)