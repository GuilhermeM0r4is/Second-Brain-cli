from models import generate_note_id, create_note
from notes import add_note, load_note_by_id, delete_note_by_id, update_note
from storage import load_notes

# set up the header for later usage
header = ("\n\033[1;36m[use '|' as a separator for topics]"
         "\n\033[1;32m>\033[0m Create note: \033[1;33mc title content tags fvr"
         "\n\033[1;32m>\033[0m List notes: \033[1;33ml"
         "\n\033[1;32m>\033[0m Find note: \033[1;33mf note_id/title"
         "\n\033[1;32m>\033[0m Update note: \033[1;33mu title content tags fvr"
         "\n\033[1;32m>\033[0m Delete note: \033[1;33md note_id/title"
         "\n\033[1;32m>\033[0m Help: \033[1;33mh\033[1;34m [or use h -@ to get help with a command]"
         "\n\033[1;31m0.\033[0m Exit")

print("\033[1;36m-- Welcome to SECOND-BRAIN-CLI --"
      "\n\033[1;33mversion: b1.0\n", header)

while True:
      ''' infinite cycle that allows the user to do all the different tasks '''

      # formats the choice input for the user to use it
      inpt = input("\n\033[1;34m> \033[0m")
      if len(inpt) == 0: continue
      
      # gets the cmd option and the action itself to work with
      cmd = inpt[0]
      actn = inpt[2:].split(" | ")

      notes = load_notes()      # loads all the notes

      # create a note command
      if cmd == "c" and len(actn) != 0:
            
            if len(actn) == 4: tags = actn[2]; fvr = actn[3]
            elif len(actn) == 3: tags = actn[2]; fvr = ""
            else: tags = ""; fvr = ""

            # gets the id from the generated notes and creates a new note
            id = generate_note_id(notes)
            note = create_note(id, actn[0], actn[1], tags, fvr)

            # adds and saves the note into the database
            add_note(note)
            print(note)

      
      # updates an already existing note
      elif cmd == "u" and len(actn) >= 2:

            if len(actn) == 4: tags = actn[2]; fvr = actn[3]
            elif len(actn) == 3: tags = actn[2]; fvr = 0
            else: tags = ""; fvr = 0

            # gets the id from the generated notes and creates a new note
            note = create_note(0, actn[0], actn[1], tags, fvr)

            # updates the note from the notes list
            print(update_note(note, notes))


      # lists all the different notes
      elif cmd == "l":
            print()
            # prints the notes from the database
            if len(notes) != 0: 
                  for note in load_notes(): print(note)
            else: print("\033[1;36mlist_notes: No Notes\033[0m")


      # gets the note which id matches the one in the input
      elif cmd == "f":
            print(load_note_by_id(actn[0]))


      # deletes the note which id matches the one in the input
      elif cmd == "d":
            print(delete_note_by_id(actn[0]))

      # reprints all the different choices - help command
      elif cmd == "h":

            # create a dictionary with all the outcomes to just look through afterwards
            d_options = {"": header,
                        "-c": ("\n\033[1;32mcreate_note: creates a new note to be later on stored in JSON file using the given info\n"
                            "\033[1;36mtitle: title of the note to create refering to its content;\n"
                            "content: could be a text, or pasted text to be included inside the note;\n"
                            "tags: letters, names, or anything that might make it easier for you to keep track of;\n"
                            "fvr: if the note should be considered favorite or not - 0: false, 1: true.\033[0m"
                            "\n\ncreate_note can also work with files, just use: \033[1;33mc file_name.txt"),

                        "-l": ("\033[1;32mlist_notes: lists all the notes and their respective meanings."),

                        "-f": ("\n\033[1;32mfind_note: finds a note in the JSON file using their ID or Title\n"
                              "\033[1;36mnote_id/title: id or title to look after."),
                              
                        "-u": ("\n\033[1;32mupdate_note: updates an existing note in JSON file using the given info\n"
                            "\033[1;36mtitle: title of the note to look after;\n"
                            "content: could be an updated text or no changes;\n"
                            "tags: letters, names, or anything that might make it easier for you to keep track of;\n"
                            "fvr: if the note should be considered favorite or not - 0: false, 1: true.\033[0m"
                            "\n\nupdate_note can also work with files, just use: \033[1;33mu file_name.txt"),

                        "-d": ("\n\033[1;32mdelete_note: deletes a note in the JSON file using their ID or Title\n"
                              "\033[1;36mnote_id/title: id or title to look after.")
                        }
            
            if actn[0] in d_options: print(d_options[actn[0]])
            else: print("\033[1;36mhelp: Invalid Choice\033[0m")

      elif cmd == "0": break
      else: print("\033[1;36msecond_brain_cli: Invalid Choice\033[0m")