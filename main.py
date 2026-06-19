from storage import load_notes
from notes import find_note, delete_note
from commands import cmd_c, cmd_u, cmd_l, cmd_h

# set up the header for later usage
header = ("\n\033[1;36m[use '|' as a separator for topics]"
         "\n\033[1;32m>\033[0m Create note: \033[1;34mc title content [tags] [fvr]"
         "\n\033[1;32m>\033[0m List notes: \033[1;34ml"
         "\n\033[1;32m>\033[0m Find note: \033[1;34mf note_id/title"
         "\n\033[1;32m>\033[0m Update note: \033[1;34mu title content [tags] [fvr]"
         "\n\033[1;32m>\033[0m Delete note: \033[1;34md note_id/title"
         "\n\033[1;32m>\033[0m Help: \033[1;34mh [-@]"
         "\n\033[1;31m0.\033[0m Exit")

print("\033[1;36m-- Welcome to SECOND-BRAIN-CLI --"
      "\n\033[1;34mversion: B1.3\n", header)

while True:
      ''' infinite cycle that allows the user to do all the different tasks '''

      # formats the choice input for the user to use it
      inpt = input("\n\033[1;34m> \033[0m")
      if len(inpt) == 0: continue
      
      # gets the cmd option and the action itself to work with
      cmd = inpt[0]
      actn = inpt[2:].split(" | ")
      siz_action = len(actn)

      notes = load_notes()      # loads all the notes

      d_optn = {"c": lambda: cmd_c(actn, siz_action, notes),    # create a note command
                "u": lambda: cmd_u(actn, siz_action, notes),    # updates an already existing note
                "l": lambda: cmd_l(notes),    # lists all the different notes
                "f": lambda: find_note(actn[0], notes),     # gets the note which id matches the one in the input
                "d": lambda: delete_note(actn[0], notes),   # deletes the note which id matches the one in the input
                "h": lambda: cmd_h(header, actn)    # reprints all the different choices - help command
                  }

      if cmd in d_optn: d_optn[cmd]()     # chooses the option from the dict
      
      elif cmd == "0": break
      else: print("\033[1;36msecond_brain_cli: Invalid Choice\033[0m")