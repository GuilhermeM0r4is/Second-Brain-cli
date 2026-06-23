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
                SBRAIN • B1.5
"""

# set up the header for later usage
header = """[blue]
[use '|' as a separator for topics][/blue]
[green]> [/green]Create note: [blue]c title content [tags] [fvr][/blue]
[green]> [/green]List notes: [blue]l[/blue]
[green]> [/green]Find note: [blue]f note_id | title | -tag[/blue]
[green]> [/green]Update note: [blue]u title content [tags] [fvr][/blue]
[green]> [/green]Delete note: [blue]d note_id | title[/blue]
[green]> [/green]Stats: [blue]s[/blue]
[green]> [/green]Help: [blue]h [-@][/blue]
[red]0. [/red]Exit
"""

def print_header() -> None:
    ''' prints the header - that's all it does '''

    print()
    # prints the header information as intended
    CONSOLE.print(Panel(header, border_style="cyan", title="COMMANDS"))


def print_info() -> None:
    ''' print fucntion for the intro messages '''

    # prints the banner in center
    CONSOLE.print(Align.center(banner))
    print_header()
    