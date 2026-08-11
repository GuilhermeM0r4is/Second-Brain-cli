from Core_Features.config import NOTE_ID_PREFIX, HELP_COMMAND, FAVORITE_TRUE
from Core_Features.models import (Note, generate_note_id, note_info, txt_to_note, note_format_print)
from Core_Features.storage import save_notes, load_notes
from Core_Features.ui import print_header, CONSOLE
from AI_Layer.storage import load_generated, save_generated
from AI_Layer.model import format_quiz_print, format_card_print, format_sum_print
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


def info_restriction(items: dict, info: str) -> bool:
    ''' assures the generated item is working '''

    if info not in ["sum", "cards", "quiz"] or info is None:
        CONSOLE.print("[red]list_info: Invalid usage[/red]")
        return False

    if not items or len(items) == 0:
        label = {"sum": "summarized notes",
                "cards": "flashcards",
                "quiz": "quizzes"
                }.get(info, "generated items")
    
        CONSOLE.print(f"[red]list_info: No {label}[/red]")
        return False
    
    return True


#################################### NORMALIZE STUDY MATERIAL ####################################

def norm_note_for_material(note: Note) -> dict:
    """ returns the dict material from a note """
    return {
        "type": "note",
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "tags": note.tags,
        "favorite": note.favorite,
        "created_at": note.created_at}


def norm_generated_for_material(item: dict, kind: str) -> dict:
    """ gets the item kind to return the correct study material """

    if kind == "sum":
        return {
            "type": "sum",
            "title": item.get("title", ""),
            "content": item.get("summary", "")}

    elif kind == "cards":
        return {
            "type": "card",
            "title": item.get("title", ""),
            "front": item.get("front", ""),
            "back": item.get("back", ""),
            "content": item.get("front", "") + " | " + item.get("back", "")}

    elif kind == "quiz":
        return {
            "type": "quiz",
            "title": item.get("title", ""),
            "question": item.get("question", ""),
            "options": item.get("options", []),
            "correct_option": item.get("correct_option", ""),
            "explanation": item.get("explanation", "")}

    return {
        "type": kind,
        "id": item.get("id", ""),
        "title": item.get("title", "Untitled"),
        "content": item}
    

#################################### MAIN FUNCTIONS FOR COMMANDS ####################################

def create_note(actn: list, siz_action: int) -> None:
    ''' create a note command to add notes to JSON file '''

    if siz_action < 2: return CONSOLE.print("[red]create_note: Missing required arguments[/red]")

    # gets the id from the generated notes and creates a new note
    notes = load_notes()      # loads all the notes
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
    
    note_information = note_info(actn, siz_action)      # uses the note_info to get the list of values
        
    # assures the information was not a failed error
    if note_information is None: CONSOLE.print("[red]create_note: Use 0 or 1 for favorite option[/red]"); return
    tags, fvr = note_information
    
    note = Note(id = id, title = title, content = content, tags = tags, favorite = fvr)

    # adds and saves the note into the database
    add_note(note)
    note_format_print(note)     # prints the note stylized


def list_info(info: str) -> None:
    """ list notes or AI-generated materials by type."""

    if info == "notes":
        notes = load_notes()      # loads all the notes
        if len(notes) == 0: return CONSOLE.print("[red]list_info: No notes[/red]")

        for note in notes:
            material = norm_note_for_material(note)
            note_format_print(note)  # keep note formatter
        return

    items = load_generated(info)
    if info_restriction(items, info) == False: return

    for item in items:
        material = norm_generated_for_material(item, info)

        if info == "sum": format_sum_print(material["summary"], material["title"])

        elif info == "cards": 
            format_card_print(material["front"], material["back"], material["title"])

        elif info == "quiz":
            format_quiz_print(material["question"], material["options"],
                              material["correct_option"], material["explanation"], material["title"])


def find_info(info: str) -> None:
    ''' searches for a note, or AI-generated content '''

    if len(info) < 2: return CONSOLE.print("[red]find_info: Missing material type or title[/red]")
    kind = info[0]
    query = info[1]

    if kind == "notes":    # searches for a note that matches the requirements
        notes = load_notes()
        result = get_note(query, notes)

        if isinstance(result, list):    # assures the print of all the tags
            for note in result: note_format_print(note)
            return

        # insures the note is currently a note itself and not None
        elif result is not None: return note_format_print(result)
        return CONSOLE.print("[red]find_note: Note ID not found[/red]")

    items = load_generated(kind)
    if info_restriction(items, kind) == False: return

    material = next((item for item in items[kind] if item.get("title") == query), None)
    if material is None: return CONSOLE.print(f"[red]find_info: No {kind} found with title '{query}'[/red]")

    if kind == "sum": 
        format_sum_print(material["summary"], material["title"])

    elif kind == "cards": 
        format_card_print(material["front"], material["back"], material["title"])

    elif kind == "quiz": 
        format_quiz_print(material["question"], material["options"], material["correct_option"],
                          material["explanation"], material["title"])


def delete_info(info: str) -> None:
    ''' deletes a note in the json file by its id value '''

    if len(info) < 2: return CONSOLE.print("[red]find_info: Missing material type or title[/red]")
    kind = info[0]
    query = info[1]

    if kind == "notes":      # working with deleting a note
        notes = load_notes()
        note = get_note(query, notes)

        if isinstance(note, Note):
            notes.remove(note)
            save_notes(notes)
            return CONSOLE.print("[green]delete_note: Note deleted[/green]")
                    
        CONSOLE.print("[red]delete_note: Note ID not found[/red]")

    items = load_generated(kind)
    if info_restriction(items, kind) == False: return
    
    material = next((item for item in items[kind] if item.get("title") == query), None)
    if material is None: return CONSOLE.print(f"[red]find_info: No {kind} found with title '{query}'[/red]")

    items[kind].remove(material)
    save_generated(items, kind)
    
    if kind == "sum": 
        format_sum_print(material["summary"], material["title"])
    
    elif kind == "cards": 
        format_card_print(material["front"], material["back"], material["title"])
    
    elif kind == "quiz": 
        format_quiz_print(material["question"], material["options"], material["correct_option"],
                              material["explanation"], material["title"])


def note_update(actn: list, siz_action: int) -> None:
    ''' updates an already existing note '''

    if siz_action < 2: return CONSOLE.print("[red]update_note: Missing required arguments[/red]")

    # updates the title of the note only
    if siz_action == 2 and "-" in actn[1]:

        notes = load_notes()
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
        update_note(note, load_notes())


def notes_stats() -> None:
    ''' prints all funny and different stats from notes '''

    notes = load_notes()
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

    if len(all_tags) == 0: CONSOLE.print(f"[green]> Most Used Tag: None[/green]")

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