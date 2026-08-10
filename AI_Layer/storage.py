import json
from AI_Layer.model import Model, CONSOLE
from dataclasses import asdict
from pathlib import Path

# Define config file path once
CONFIG_FILE = Path(__file__).parent.parent / "Storage" / "ai_config.json"
GENERATED_FILE = Path(__file__).parent.parent / "Storage" / "generated.json"

def load_config() -> Model | None:
    ''' gets the local or API key of the AI model to use '''

    # it will try to open the file and load its content
    try:
        with open(CONFIG_FILE, 'r') as file:
            data = json.load(file)  # Load as dicts
            return Model(**data)  # Convert dicts to Model instance

    # if there's no file, we'll need to create it -> returns empty        
    except FileNotFoundError:
        with open(CONFIG_FILE, "w") as file:
            json.dump({"provider": "ollama", "model": "NONE", "api_key": "NONE", "data_sharing": "LOCAL"}, file)
        return None
    
    # if there's corrupted data in the .json file
    except json.JSONDecodeError:
        return CONSOLE.print("[red]JSON Error: Corrupted ai_config.json file[/red]")


def save_config(config: Model) -> None:
    ''' takes the config dict and saves it into the json file '''

    # Convert Model → dict using auxiliar function
    config_dict = asdict(config)

    # using the write function will guarantee the existance of the file
    # or create it itself if it doesn't yet exist
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_dict, file, indent = 4)


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

    if kind == "sum": existing["sum"] = data
    elif kind == "cards": existing["cards"] = data
    elif kind == "quizz": existing["quizz"] = data
    else: existing["other"] = data

    # stores the data into the existing ones
    with open(GENERATED_FILE, "w") as file:
        json.dump(existing, file, indent = 4)