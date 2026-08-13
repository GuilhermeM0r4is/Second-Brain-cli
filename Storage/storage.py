import json
from Material.ui import CONSOLE
from pathlib import Path

# Get the path to data.json in the Storage folder
data_file = Path(__file__).parent.parent / "Storage" / "storage.json"

DEFAULT_STORAGE = {
    "ai": {
        "provider": "ollama",
        "model": "NONE",
        "api_key": "NONE",
        "data_sharing": "LOCAL"
    },
    "import": {
        "dpi": 300,
        "language": "eng"
    }
}

def load_storage(kind: str | None = None) -> dict:
    ''' loads a JSON file and its content, if not found, creates one '''
    
    try:    # it will try to open the file and load its content
        with open(data_file, 'r') as file:
            data = json.load(file)  # Load as dicts

        if kind is None: return data
        return data.get(kind, {})

    # if there's no file, we'll need to create it -> returns []        
    except FileNotFoundError:
        with open(data_file, "w") as file:
            json.dump(DEFAULT_STORAGE, file, indent = 4, ensure_ascii = False)

        if kind is None: return DEFAULT_STORAGE
        return DEFAULT_STORAGE.get(kind, {})
    
    # if there's corrupted data in the .json file
    except json.JSONDecodeError:
        CONSOLE.print("[red]storage: Corrupted storage.json file[/red]")
        return {}
    
    
def save_storage(kind: str, info: dict) -> None:
    ''' takes the notes list and saves it into the json file '''
    
    data = load_storage() 
    data[kind] = info

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent = 4, ensure_ascii = False)