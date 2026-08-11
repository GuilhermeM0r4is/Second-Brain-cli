from Core_Features.config import SEPARATOR
from Core_Features.ui import CONSOLE
from Core_Features.material import (create_note, note_update, list_info, find_info, 
                                 delete_info, notes_stats, help)
from Core_Features.storage import load_notes
from AI_Layer.ai import ai_tools

def main():
    ''' main function that keeps the program running all the time '''

    while True:
        ''' infinite cycle that allows the user to do all the different tasks '''

        # formats the choice input for the user to use it
        inpt = CONSOLE.input("\n[blue]SBRAIN > [/blue]")
        if not inpt: continue
      
        # gets the cmd option and the action itself to work with
        cmd = inpt[0]
        actn = [part.strip() for part in inpt[2:].split(SEPARATOR)]

        d_optn = {"c": lambda: create_note(actn, len(actn)),
                "l": lambda: list_info(actn[0]),
                "f": lambda: find_info(actn),
                "d": lambda: delete_info(actn),
                "u": lambda: note_update(actn, len(actn)),
                "s": lambda: notes_stats(),
                "a": lambda: ai_tools(actn, len(actn)),
                "h": lambda: help(actn)
                }

        if cmd in d_optn: 
            try: d_optn[cmd]()     # chooses the option from the dict
            except Exception as e: CONSOLE.print(f"[red]SBRAIN: {e}[/red]")
      
        elif cmd == "0": break
        else: CONSOLE.print("[blue]SBRAIN: [red]Invalid choice, use 'h' for help[/red]")