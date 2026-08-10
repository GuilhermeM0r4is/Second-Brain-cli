from rich.console import Console
from rich.panel import Panel
from rich.align import Align

CONSOLE = Console()

banner = """[bold cyan]

 ███████╗██████╗ ██████╗  █████╗ ██╗███╗   ██╗
 ██╔════╝██╔══██╗██╔══██╗██╔══██╗██║████╗  ██║
 ███████╗██████╔╝██████╔╝███████║██║██╔██╗ ██║
 ╚════██║██╔══██╗██╔══██╗██╔══██║██║██║╚██╗██║
 ███████║██████╔╝██║  ██║██║  ██║██║██║ ╚████║
 ╚══════╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝
[/bold cyan]
              SBRAIN-CLI • B2.1
"""

# set up the header for later usage
header = """
[blue][<tags> and <fvr> are optional, but recommended for better organization,
use "|" as separator between arguments, and "-" for flags][/blue]

[green]> [/green]Create note: [blue]c title | content | tags | fvr[/blue]
[green]> [/green]List notes: [blue]l -@[/blue]
[green]> [/green]Find note: [blue]f note_id or title or -tag[/blue]
[green]> [/green]Update note: [blue]u title | content | tags | fvr[/blue]
[green]> [/green]Delete note: [blue]d note_id or title[/blue]
[green]> [/green]Stats: [blue]s[/blue]
[green]> [/green]AI functions: [blue]a sum | note_id or title[/blue]
[green]> [/green]Help: [blue]h -@[/blue]
[red]0. [/red]Exit
"""

def print_header() -> None:
    ''' prints the header - that's all it does '''
    print()     # prints a blank line for better formatting
    CONSOLE.print(Panel(header, border_style="cyan", title="COMMANDS"))


def print_info() -> None:
    ''' print fucntion for the intro messages '''
    CONSOLE.print(Align.center(banner))     # prints the banner in center
    print_header()
    