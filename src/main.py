from storage import load_notes
from notes import create_note, note_update, list_notes, find_note, delete_note, notes_stats, help
from ui import print_info, console
from config import SEPARATOR

def main():
    ''' main function that keeps the program running all the time '''

    while True:
        ''' infinite cycle that allows the user to do all the different tasks '''

        print()
        notes = load_notes()      # loads all the notes

        # formats the choice input for the user to use it
        inpt = console.input("[blue]SB > [/blue]")
        if len(inpt) == 0: continue
      
        # gets the cmd option and the action itself to work with
        cmd = inpt[0]
        actn = inpt[2:].split(SEPARATOR)
        siz_action = len(actn)

        d_optn = {"c": lambda: create_note(actn, siz_action, notes),
                "u": lambda: note_update(actn, siz_action, notes),
                "l": lambda: list_notes(notes),
                "f": lambda: find_note(actn[0], notes),
                "d": lambda: delete_note(actn[0], notes),
                "s": lambda: notes_stats(notes),
                "h": lambda: help(actn)
                  }

        if cmd in d_optn: d_optn[cmd]()     # chooses the option from the dict
      
        elif cmd == "0": break
        else: console.print("[blue]SB: [red]Invalid choice, use 'h' for help[/red]")

print_info()  # prints the information in the beginning
main()		  # runs the program itself