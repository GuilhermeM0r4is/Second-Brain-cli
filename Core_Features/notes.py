from Core_Features.config import NOTE_ID_PREFIX, HELP_COMMAND, FAVORITE_TRUE
from Core_Features.models import (Note, generate_note_id, note_info, txt_to_note, note_format_print)
from Core_Features.storage import save_notes, load_notes
from Core_Features.ui import print_header, CONSOLE
from collections import Counter

def add_note(note: Note) -> None:
    ''' adds a note given and saves it into the json database '''

    notes = load_notes()
    notes.append(note)
    save_notes(notes)


def get_note(info: str, notes: list) -> Note | list[Note] | None:
    """ Find a note by ID or title """

    if info.isdigit():  # returns the note by ID
        note_id = f"{NOTE_ID_PREFIX}{int(info):04d}"

        return next((note for note in notes if note.id == note_id), None)
    
    elif "-" in info:   # returns a list of notes with all the tags
        return [note for note in notes if info[1:] in note.tags.split(",")]

    # returns the note by the respective title
    return next((note for note in notes if note.title == info), None)


def update_note(note_updated: Note, notes: list[Note]) -> None:
    ''' updates an existing note given the new information '''
    
    # gets the note with the same title
    note = get_note(note_updated.title, notes)

    if isinstance(note, Note): 
        note_updated.id = note.id

        # takes the id from the note based on the title and updates it
        id = note.id[-1]
        notes[int(id) - 1] = note_updated

        save_notes(notes)
        return CONSOLE.print("[green]update_note: Note updated[/green]")
        
    CONSOLE.print("[red]delete_note: Note ID not found[/red]")
    

#################################### MAIN FUNCTIONS FOR COMMANDS ####################################

def create_note(actn: list, siz_action: int, notes: list[Note]) -> None:
    ''' create a note command to add notes to JSON file '''

    if siz_action < 2: return CONSOLE.print("[red]create_note: Missing required arguments[/red]")

    # gets the id from the generated notes and creates a new note
    id = generate_note_id(notes)

    # using a .txt file as note creation
    if actn[0].endswith('.txt'): 
        document_result = txt_to_note(actn[0])

        # makes sure there were no errors and gets info
        if document_result is None: return
        title, content = document_result
          
        actn.insert(1, "-")   # allows note_info function to work
        siz_action += 1

    else: title = actn[0]; content = actn[1]     # it's a direct input in cmd
    
    # uses the note_info to get the list of values
    note_information = note_info(actn, siz_action)
        
    # assures the information was not a failed error
    if note_information is None: CONSOLE.print("[red]create_note: Use 0 or 1 for favorite option[/red]"); return
    tags, fvr = note_information
    
    note = Note(id = id, title = title, content = content,
                tags = tags, favorite = fvr)

    # adds and saves the note into the database
    add_note(note)
    note_format_print(note)     # prints the note stylized
    

def note_update(actn: list, siz_action: int, notes: list[Note]) -> None:
    ''' updates an already existing note '''

    # updates the title of the note only
    if siz_action == 2 and "-" in actn[1]:
                  
        note = get_note(actn[0], notes)
        if isinstance(note, Note): note.title = actn[1][1:]
                        
        save_notes(notes)
        CONSOLE.print("[green]update_note: Title updated [/green]", actn[0])

    else:
        # using a .txt file as note creation
        if actn[0].endswith('.txt'): 
            document_result = txt_to_note(actn[0])
        
            # makes sure there were no errors and gets info
            if document_result is None: return
            title, content = document_result

        else:     # it's a direct input in cmd
            title = actn[0]; content = actn[1]
        
        # uses the note_info to get the list of values
        note_information = note_info(actn, siz_action)
        
        # assures the information was not a failed error
        if note_information is None: CONSOLE.print("[red]note_update: Use 0 or 1 for favorite option[/red]"); return
        tags, fvr = note_information

        # gets the id from the generated notes and creates a new note
        note = Note(id = "", title = title, content = content,
                tags = tags, favorite = fvr)

        # updates the note from the notes list
        update_note(note, notes)


def list_notes(notes: list[Note]) -> None:
    ''' list all the notes in the JSON file '''

    # prints the notes from the database
    if len(notes) != 0: 
        for note in notes: note_format_print(note)

    else: CONSOLE.print("[red]list_notes: No notes[/red]")


def find_note(info: str, notes: list[Note]) -> None:
    ''' searches for a note, gets an ID or title and goes after it '''

    try:
        # searches for a note that matches the requirements
        result = get_note(info, notes)

        if isinstance(result, list):    # assures the print of all the tags
            for note in result: note_format_print(note)
            return

        # insures the note is currently a note itself and not None
        elif result is not None: return note_format_print(result)

        # found no note with that specific ID
        CONSOLE.print("[red]find_note: Note ID not found[/red]")
    
    except ValueError: CONSOLE.print("[red]find_note: Invalid note ID[/red]")


def delete_note(info: str, notes: list[Note]) -> None:
    ''' deletes a note in the json file by its id value '''

    note = get_note(info, notes)

    if isinstance(note, Note):
        notes.remove(note)
        save_notes(notes)
        return CONSOLE.print("[green]delete_note: Note deleted[/green]")
                
    CONSOLE.print("[red]delete_note: Note ID not found[/red]")


def notes_stats(notes: list[Note]) -> None:
    ''' prints all funny and different stats from notes '''

    CONSOLE.print(f"[green]> Total Notes: {len(notes)}[/green]")

    # gets the amount of favorite notes user has in total
    fav_amount = sum(1 for note in notes if note.favorite == FAVORITE_TRUE)
    CONSOLE.print(f"[green]> Total Favorites: {fav_amount}[/green]")

    # shows the most used tag
    all_tags = []
    for note in notes:
        if note.tags:   # if it has a tag
            tags = [tag.strip() for tag in note.tags.split(",")]
            all_tags.extend(tags)   # extends the list with another list

    if len(all_tags) == 0:
        CONSOLE.print(f"[green]> Most Used Tag: None[/green]")

    else:
        tag_counts = Counter(all_tags)
        fav_tag = tag_counts.most_common(1)[0][0]
        CONSOLE.print(f"[green]> Favorite Tag: {fav_tag}[/green]")


def help(actn: list) -> None:
    ''' gives all the information on help command '''

    if actn[0] == "": print_header(); return

    # create a dictionary with all the outcomes to just look through afterwards    
    if actn[0] in HELP_COMMAND: CONSOLE.print(HELP_COMMAND[actn[0]])
    else: CONSOLE.print("[red]help: Invalid choice[/red]")