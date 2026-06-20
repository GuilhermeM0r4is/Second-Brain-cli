from models import generate_note_id, create_note, note_info, txt_to_note, note_format_print
from storage import save_notes, load_notes
from ui import print_header, console

def add_note(note: dict) -> None:
    ''' adds a note given and saves it into the json database '''

    notes = load_notes()
    notes.append(note)
    save_notes(notes)


def find_note(info: str, notes: list) -> None:
    ''' searches for a note, gets an ID or title and goes after it '''

    try:
        if info.isdigit():    # if we're looking for an ID

            # gets the current string ID
            note_id = f"N{int(info):04d}"

            for note in notes:
                if note["id"] == note_id: return note_format_print(note)

        else:   # we are instead looking for a title
            for note in notes: 
                if note["title"] == info: return note_format_print(note)

        # found no note with that specific ID
        console.print("[red]find_note: Note ID not found[/red]")
    
    except ValueError: console.print("[red]find_note: Invalid note ID[/red]")


def update_note(note_updated: dict, notes: list) -> None:
    ''' updates an existing note given the new information '''
    
    for note in notes:
        if note["title"] == note_updated["title"]:

            note_updated["id"] = note["id"]

            # takes the id from the note based on the title and updates it
            id = note["id"][-1]
            notes[int(id) - 1] = note_updated

            save_notes(notes)
            return console.print("[green]update_note: Note updated[/green]")
        
    console.print("[red]delete_note_id: Note ID not found[/red]")


def delete_note(info: str, notes: list) -> None:
    ''' deletes a note in the json file by its id value '''

    if info.isdigit():    # if we're looking for an ID

        # gets the current string ID
        note_id = f"N{int(info):04d}"

        for note in notes:
            if note["id"] == note_id:
                notes.remove(note)
                save_notes(notes)
                return console.print("[green]delete_note_id: Note deleted[/green]")

    else:   # we are instead looking for a title
        for note in notes:
            if note["title"] == info: 
                notes.remove(note)
                save_notes(notes)
                return console.print("[green]delete_note_id: Note deleted[/green]")
                
    console.print("[red]delete_note_id: Note ID not found[/red]")
    

def cmd_c(actn: list, siz_action: int, notes: list) -> None:
    ''' create a note command to add notes to JSON file '''

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

    else:     # it's a direct input in cmd
        title = actn[0]; content = actn[1]
        console.print(actn)
    
    tags, fvr = note_info(actn, siz_action)
    note = create_note(id, title, content, tags, fvr)

    # adds and saves the note into the database
    add_note(note)
    note_format_print(note)     # prints the note stylized
    


def cmd_u(actn: list, siz_action: int, notes: list) -> None:
    ''' updates an already existing note '''

    # updates the title of the note only
    if siz_action == 2 and "-" in actn[1]:
                  
        for note in notes:      # checks all the notes for title
            if note['title'] == actn[0]: note['title'] = actn[1][1:]; break
                        
        save_notes(notes)
        console.print("[green]update_note: Title updated [/green]", actn[0])

    else:
        # using a .txt file as note creation
        if actn[0].endswith('.txt'): 
            document_result = txt_to_note(actn[0])
        
            # makes sure there were no errors and gets info
            if document_result is None: return
            title, content = document_result

        else:     # it's a direct input in cmd
            title = actn[0]; content = actn[1]
        
        tags, fvr = note_info(actn, siz_action)

        # gets the id from the generated notes and creates a new note
        note = create_note("", title, content, tags, fvr)

        # updates the note from the notes list
        update_note(note, notes)


def cmd_l(notes: list) -> None:
    ''' list all the notes in the JSON file '''

    # prints the notes from the database
    if len(notes) != 0: 
        for note in notes: note_format_print(note)
        console.print("[green]> Total Notes: [/green]", len(notes))

    else: console.print("[red]list_notes: No notes[/red]")


def cmd_h(actn: list) -> None:
    ''' gives all the information on help command '''

    if actn[0] == "": print_header(); return

    # create a dictionary with all the outcomes to just look through afterwards
    d_options = {"-c": ("\n[green]create_note: creates a new note to be later on stored in JSON file using the given info[/green]\n"
                        "[cyan]title: [/cyan]title of the note to create refering to its content;\n"
                        "[cyan]content: [/cyan]could be a text, or pasted text to be included inside the note;\n"
                        "[cyan]tags: [/cyan]letters, names, or anything that might make it easier for you to keep track of;\n"
                        "[cyan]fvr: [/cyan]if the note should be considered favorite or not - 0: false, 1: true.\n"
                        "\n[blue]create_note [/blue]can also work with files, just use: [blue]c file_name.txt [tags] [fvr][/blue]"),

                "-l": ("\n[green]list_notes: lists all the notes and their respective meanings.[/green]"),

                "-f": ("\n[green]find_note: finds a note in the JSON file using their ID or Title[/green]\n"
                        "[cyan]note_id/title: [/cyan]id or title to look after."),
                              
                "-u": ("\n[green]update_note: updates an existing note in JSON file using the given info[/green]\n"
                        "[cyan]title: [/cyan]title of the note to look after;\n"
                        "[cyan]content: [/cyan]could be an updated text or no changes;\n"
                        "[cyan]tags: [/cyan]letters, names, or anything that might make it easier for you to keep track of;\n"
                        "[cyan]fvr: [/cyan]if the note should be considered favorite or not - 0: false, 1: true.\n"
                        "\n[blue]update_note [/blue]can also work with files, just use: [blue]u file_name.txt [tags] [fvr][/blue]\n"
                        "[blue]update_note [/blue]can also update titles with: [blue]u title -new_title[/blue]"),

                "-d": ("\n[green]delete_note: deletes a note in the JSON file using their ID or Title[/green]\n"
                        "[cyan]note_id/title: [/cyan]id or title to look after.")
                        }
            
    if actn[0] in d_options: console.print(d_options[actn[0]])
    else: console.print("[red]Help: Invalid choice[/red]")