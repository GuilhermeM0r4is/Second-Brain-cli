from datetime import datetime   # imports the datetime module to work with date and time
from ui import console, Panel

def generate_note_id(notes: list) -> str:
    ''' generates a new note_id from the notes array '''

    if len(notes) == 0: return "N0001"

    # gets the last note from the array -> and its number ID "N0001"
    last_id = notes[-1]["id"]

    # gets the int value from the string and sums + 1 
    value = int(last_id[1:]) + 1 

    # returns the f-string value
    return f"N{value:04d}"


def create_note(note_id: str, title: str, content: str, tags: str, fvr: str) -> dict:
    ''' creates a new note to be later on stored in JSON file '''

    return {"id": note_id, 
            "title": title, 
            "content": content, 
            "tags": tags, 
            # represents as 2026-05-09T15:30:00
            "created_at": datetime.now().isoformat(),
            "favorite": fvr }


def txt_to_note(txt: str) -> tuple[str, str] | None:
    ''' creates a new note from a .txt file given '''
    try:
        # opens the file and uses it to get the components to create the note
        with open(txt, "r", encoding='utf-8', errors='replace') as file:

            title = file.readline().strip()
            # the content comes as a whole string all together
            content = ' '.join(line.strip() for line in file.readlines())

        return title, content
    
    except FileNotFoundError: console.print(f"[red]File Error: Not found[/red]")
    except Exception as e: console.print(f"[red]File Error: Failed reading file[/red]")


def note_info(action: list, siz_action: int) -> tuple[str, str]:
    ''' takes the action and turns it into the tags and fvr info '''

    tags = ""; fvr = ""

    # checks the len of action to see if we have tags and fvr set up
    if siz_action >= 3: 
        tags = action[2]
    
    if siz_action == 4: 
        fvr = action[3]

    return tags, fvr


def note_format_print(note: dict) -> None:
    ''' prints the note in the determined format '''

    console.print(Panel(
        f"[cyan]Title:[/cyan] {note['title']}\n"
        f"[cyan]Content:[/cyan] {note['content']}\n"
        f"[cyan]Tags:[/cyan] {note['tags']}\n"
        f"[cyan]Created At:[/cyan] {note['created_at']}\n"
        f"[cyan]Favorite:[/cyan] {note['favorite']}", 
        border_style="cyan", title=note["id"]))