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
    note_id = f"N{int(note_id):04d}"

    notes = load_notes()
    for note in notes:
        if note["id"] == note_id: return note

    # found no note with that specific ID
    return "\033[1;31mload_note_by_id: Note ID not found\033[0m"


def update_note(note_updated, notes):
    ''' updates an existing note given the new information '''
    
    for note in notes:
        if note["title"] == note_updated["title"]:

            note_updated["id"] = note["id"]

            # takes the id from the note based on the title and updates it
            id = note["id"][-1]
            notes[int(id) - 1] = note_updated

            save_notes(notes)
            return "\033[1;32mupdate_note: Note Updated\033[0m"
        
    return "\033[1;31mdelete_note_id: Note ID not found\033[0m"


def delete_note_by_id(note_id):
    ''' deletes a note in the json file by its id value '''

    # gets the current string ID
    note_id = f"N{int(note_id):04d}"

    notes = load_notes()

    for note in notes:
        if note["id"] == note_id:
            notes.remove(note)
            save_notes(notes)
            return "\033[1;32mdelete_note_id: Note Deleted\033[0m"
    
    return "\033[1;31mdelete_note_id: Note ID not found\033[0m"