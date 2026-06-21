import json
from ui import console
from models import Note
from dataclasses import asdict

def load_notes() -> list:
    ''' loads a JSON file and its content, if not found, creates one '''

    # it will try to open the file and load its content
    try:
        with open('data.json', 'r') as file:
            data = json.load(file)  # Load as dicts
            return [Note(**note_dict) for note_dict in data]  # Convert to Note objects

    # if there's no file, we'll need to create it -> returns []        
    except FileNotFoundError:
        with open("data.json", "w") as file:
            json.dump([], file)
        return []
    
    # if there's corrupted data in the .json file
    except json.JSONDecodeError:
        console.print("[red]JSON Error: Corrupted data.json file[/red]")
        return []
    
    
def save_notes(notes: list) -> None:
    ''' takes the notes list and saves it into the json file '''

    # Convert Note → dict using auxiliar function
    notes_dict = [asdict(note) for note in notes]

    # using the write function will guarantee the existance of the file
    # or create it itself if it doesn't yet exist
    with open("data.json", "w") as file:
        json.dump(notes_dict, file)