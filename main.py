from models import generate_note_id, create_note
from notes import add_note, load_note_by_id
from storage import load_notes

print("\033[1;36m-- Welcome to SECOND-BRAIN-CLI --\033[0m"
      "\n\033[1;33mversion: b1.0\033[0m")

print("\n\033[1;32m>\033[0m Create note: \033[1;33mc title, content, tags\033[0m"
      "\n\033[1;32m>\033[0m List notes: \033[1;33ml\033[0m"
      "\n\033[1;32m>\033[0m Find note: \033[1;33mf note_id\033[0m"
      "\n\033[1;32m>\033[0m Help: \033[1;33mh\033[0m"
      "\n\033[1;31m0.\033[0m Exit")

while True:
      ''' infinite cycle that allows the user to do all the different tasks '''

      # formats the choice input for the user to use it
      choice = input("\n\033[1;34m> \033[0m").split()

      if len(choice) == 0: continue

      # create a note command
      elif choice[0] == "c" and len(choice) == 4:
            
            notes = load_notes()      # loads all the notes

            # gets the id from the generated notes and creates a new note
            id = generate_note_id(notes)
            note = create_note(id, choice[1], choice[2], choice[3])

            # adds and saves the note into the database
            add_note(note)


      # lists all the different notes
      elif choice[0] == "l" and len(choice) == 1:

            print()
            # prints the notes from the database
            for note in load_notes(): print(note)


      # gets the note which id matches the one in the input
      elif choice[0] == "f" and len(choice) == 2:
            print(load_note_by_id(choice[1]))


      # reprints all the different choices - help command
      elif choice[0] == "h":
            print("\n\033[1;32m>\033[0m Create note: \033[1;33mc title, content, tags\033[0m"
                  "\n\033[1;32m>\033[0m List notes: \033[1;33ml\033[0m"
                  "\n\033[1;32m>\033[0m Find note: \033[1;33mf note_id\033[0m"
                  "\n\033[1;32m>\033[0m Help: \033[1;33mh\033[0m"
                  "\n\033[1;31m0.\033[0m Exit")
      
      elif choice[0] == "0": break
      else: print("\033[1;36msecond_brain_cli: Invalid Choice\033[0m")