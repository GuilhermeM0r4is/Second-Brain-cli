from storage import load_notes, save_notes

def add_note(note):
    ''' adds a note given and saves it into the json database '''

    notes = load_notes()
    notes.append(note)
    save_notes(notes)


def find_note(info, notes):
    ''' searches for a note in the json file, 
    gets an ID or title and goes after it '''

    if info.isdigit():    # if we're looking for an ID

        # gets the current string ID
        note_id = f"N{int(info):04d}"

        for note in notes:
            if note["id"] == note_id: return print(f"\033[1;32m{note}\033[0m")

    else:   # we are instead looking for a title
        for note in notes: 
            if note["title"] == info: return print(f"\033[1;32m{note}\033[0m")

    # found no note with that specific ID
    print("\033[1;31mload_note_by_id: Note ID not found\033[0m")


def update_note(note_updated, notes):
    ''' updates an existing note given the new information '''
    
    for note in notes:
        if note["title"] == note_updated["title"]:

            note_updated["id"] = note["id"]

            # takes the id from the note based on the title and updates it
            id = note["id"][-1]
            notes[int(id) - 1] = note_updated

            save_notes(notes)
            return print("\033[1;32mupdate_note: Note Updated\033[0m")
        
    print("\033[1;31mdelete_note_id: Note ID not found\033[0m")


def delete_note(info, notes):
    ''' deletes a note in the json file by its id value '''

    if info.isdigit():    # if we're looking for an ID

        # gets the current string ID
        note_id = f"N{int(info):04d}"

        for note in notes:
            if note["id"] == note_id:
                notes.remove(note)
                save_notes(notes)
                return print("\033[1;32mdelete_note_id: Note Deleted\033[0m")

    else:   # we are instead looking for a title
        for note in notes:
            if note["title"] == info: 
                notes.remove(note)
                save_notes(notes)
                return print("\033[1;32mdelete_note_id: Note Deleted\033[0m")
                
    print("\033[1;31mdelete_note_id: Note ID not found\033[0m")