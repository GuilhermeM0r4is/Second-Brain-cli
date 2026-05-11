from datetime import datetime   # imports the datetime module to work with date and time

def generate_note_id(notes):
    ''' generates a new note_id from the notes array '''

    if len(notes) == 0: return "N0001"

    # gets the last note from the array -> and its number ID "N0001"
    last_id = notes[-1]["id"]

    # gets the int value from the string and sums + 1 
    value = int(last_id[1:]) + 1 

    # returns the f-string value
    return f"N{value:04d}"

def create_note(note_id, title, content, tags):
    ''' creates a new note to be later on stored in JSON file '''

    return {"id": note_id, 
            "title": title, 
            "content": content, 
            "tags": tags, 
            # represents as 2026-05-09T15:30:00
            "created_at": datetime.now().isoformat(),
            "favorite": False }