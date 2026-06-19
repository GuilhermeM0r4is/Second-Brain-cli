from models import generate_note_id, create_note, note_info, txt_to_note
from notes import add_note, update_note
from storage import save_notes

def cmd_c(actn, siz_action, notes):
    ''' create a note command to add notes to JSON file '''

    # gets the id from the generated notes and creates a new note
    id = generate_note_id(notes)

    # using a .txt file as note creation
    if actn[0].endswith('.txt'): 
          title, content = txt_to_note(actn[0])

    else:     # it's a direct input in cmd
        title = actn[0]; content = actn[1]
    
    tags, fvr = note_info(actn, siz_action)
                  
    note = create_note(id, title, content, tags, fvr)

    # adds and saves the note into the database
    add_note(note)
    print(note)


def cmd_u(actn, siz_action, notes):
    ''' updates an already existing note '''

    # updates the title of the note only
    if siz_action == 2 and "-" in actn[1]:
                  
        for note in notes:      # checks all the notes for title
            if note['title'] == actn[0]: note['title'] = actn[1][1:]; break
                        
        save_notes(notes)
        print("\033[1;32mupdate_note: Title Updated\033[0m")

    else:
        # using a .txt file as note creation
        if actn[0].endswith('.txt'): title, content = txt_to_note(actn[0])

        else:     # it's a direct input in cmd
            title = actn[0]; content = actn[1]
        
        tags, fvr = note_info(actn, siz_action)

        # gets the id from the generated notes and creates a new note
        note = create_note(0, title, content, tags, fvr)

        # updates the note from the notes list
        update_note(note, notes)


def cmd_l(notes):
    ''' list all the notes in the JSON file '''

    # prints the notes from the database
    if len(notes) != 0: 
        for note in notes: print(note)
        print("\033[1;32m> Total Notes: ", len(notes))

    else: print("\033[1;36mlist_notes: No Notes\033[0m")


def cmd_h(header, actn):
    ''' gives all the information on help command '''

    # create a dictionary with all the outcomes to just look through afterwards
    d_options = {"": header,
                "-c": ("\n\033[1;32mcreate_note: creates a new note to be later on stored in JSON file using the given info\n"
                        "\033[1;36mtitle: title of the note to create refering to its content;\n"
                        "content: could be a text, or pasted text to be included inside the note;\n"
                        "tags: letters, names, or anything that might make it easier for you to keep track of;\n"
                        "fvr: if the note should be considered favorite or not - 0: false, 1: true.\033[0m"
                        "\n\ncreate_note can also work with files, just use: \033[1;34mc file_name.txt [tags] [fvr]"),

                "-l": ("\n\033[1;32mlist_notes: lists all the notes and their respective meanings."),

                "-f": ("\n\033[1;32mfind_note: finds a note in the JSON file using their ID or Title\n"
                        "\033[1;36mnote_id/title: id or title to look after."),
                              
                "-u": ("\n\033[1;32mupdate_note: updates an existing note in JSON file using the given info\n"
                        "\033[1;36mtitle: title of the note to look after;\n"
                        "content: could be an updated text or no changes;\n"
                        "tags: letters, names, or anything that might make it easier for you to keep track of;\n"
                        "fvr: if the note should be considered favorite or not - 0: false, 1: true.\033[0m"
                        "\n\nupdate_note can also work with files, just use: \033[1;34mu file_name.txt [tags] [fvr]\033[0m"
                        "\nupdate_note can also update titles with: \033[1;34mu title -new_title"),

                "-d": ("\n\033[1;32mdelete_note: deletes a note in the JSON file using their ID or Title\n"
                        "\033[1;36mnote_id/title: id or title to look after.")
                        }
            
    if actn[0] in d_options: print(d_options[actn[0]])
    else: print("\033[1;36mhelp: Invalid Choice\033[0m")