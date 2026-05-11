from storage import load_notes, save_notes

def add_note(note):
    ''' adds a note given and saves it into the json database '''

    notes = load_notes()
    notes.append(note)
    save_notes(notes)

def load_note_by_id(note_id):
    ''' searches for a note in the json file, 
    gets an int but searches for the string '''

    # gets the current string ID
    note_id = f"N{note_id:04d}"

    notes = load_notes()
    for note in notes:
        if note["id"] == note_id: return note

    # found no note with that specific ID
    raise ValueError("Note ID not found")