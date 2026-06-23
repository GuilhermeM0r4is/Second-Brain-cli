import json
from AI_Layer.model import Model, CONSOLE
from dataclasses import asdict
from pathlib import Path

# Define config file path once
CONFIG_FILE = Path(__file__).parent.parent / "Storage" / "ai_config.json"

def load_config() -> Model | None:
    ''' gets the local or API key of the AI model to use '''

    # it will try to open the file and load its content
    try:
        with open(CONFIG_FILE, 'r') as file:
            data = json.load(file)  # Load as dicts
            return Model(**data)

    # if there's no file, we'll need to create it -> returns empty        
    except FileNotFoundError:
        with open(CONFIG_FILE, "w") as file:
            json.dump({}, file)
        return None
    
    # if there's corrupted data in the .json file
    except json.JSONDecodeError:
        CONSOLE.print("[red]JSON Error: Corrupted ai_config.json file[/red]")
        return None
    
    
def save_config(config: Model) -> None:
    ''' takes the config dict and saves it into the json file '''

    # Convert Model → dict using auxiliar function
    config_dict = asdict(config)

    # using the write function will guarantee the existance of the file
    # or create it itself if it doesn't yet exist
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_dict, file, indent=4)