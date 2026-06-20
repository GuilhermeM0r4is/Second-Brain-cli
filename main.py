from storage import load_notes
from notes import find_note, delete_note
from notes import cmd_c, cmd_u, cmd_l, cmd_h
from ui import print_info, console

def main():
    while True:
        ''' infinite cycle that allows the user to do all the different tasks '''

        print()

        # formats the choice input for the user to use it
        inpt = console.input("[blue]SB > [/blue]")
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
                "h": lambda: cmd_h(actn)    # reprints all the different choices - help command
                  }

        if cmd in d_optn: d_optn[cmd]()     # chooses the option from the dict
      
        elif cmd == "0": break
        else: console.print("[blue]SB: [red]Invalid choice, use 'h' for help[/red]")

print_info()  # prints the information in the beginning
main()		  # runs the program itself