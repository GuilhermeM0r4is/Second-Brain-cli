from datetime import datetime   # imports the datetime module to work with date and time
from Core_Features.config import CONSOLE
from Core_Features.config import NOTE_ID_PREFIX, FAVORITE_FALSE, FAVORITE_TRUE
from dataclasses import dataclass
from rich.panel import Panel

@dataclass      # Uses the note dataclass to
class Note:     # make it more readable
    id: str
    title: str
    content: str
    tags: str
    favorite: str
    created_at: str | None = None  # represents as 2026-05-09T15:30:00
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()    

def generate_note_id(notes: list[Note]) -> str:
    ''' generates a new note_id from the notes array '''

    if len(notes) == 0: return NOTE_ID_PREFIX + "0001"

    # gets the last note from the array -> and its number ID "N0001"
    last_id = notes[-1].id

    # gets the int value from the string and sums + 1 
    value = int(last_id[1:]) + 1 

    # returns the f-string value
    return f"{NOTE_ID_PREFIX}{value:04d}"


def txt_to_note(txt: str) -> tuple[str, str] | None:
    ''' creates a new note from a .txt file given '''
    try:
        # opens the file and uses it to get the components to create the note
        with open(txt, "r", encoding='utf-8', errors='replace') as file:

            title = file.readline().strip()
            # the content comes as a whole string all together
            content = ' '.join(line.strip() for line in file.readlines())

        return title, content
    
    except FileNotFoundError: CONSOLE.print(f"[red]File Error: Not found[/red]")
    except Exception as e: CONSOLE.print(f"[red]File Error: Failed reading file[/red]")


def note_info(action: list, siz_action: int) -> tuple[str, str] | None:
    ''' takes the action and turns it into the tags and fvr info '''

    tags = ""; fvr = FAVORITE_FALSE

    # checks the len of action to see if we have tags and fvr set up
    if siz_action >= 3: 
        tags = action[2]
    
    if siz_action == 4:
        if action[3] in (FAVORITE_FALSE, FAVORITE_TRUE):
            fvr = action[3]

        else: return None   # makes it so only 0 or 1 can be used to favorite

    return tags, fvr


def note_format_print(note: Note) -> None:
    ''' prints the note in the determined format '''

    CONSOLE.print(Panel(
        f"[cyan]Title:[/cyan] {note.title}\n"
        f"[cyan]Content:[/cyan] {note.content}\n"
        f"[cyan]Tags:[/cyan] {note.tags}\n"
        f"[cyan]Created At:[/cyan] {note.created_at}\n"
        f"[cyan]Favorite:[/cyan] {note.favorite}", 
        border_style="cyan", title=note.id))