from rich.console import Console

NOTE_ID_PREFIX = "N"
SEPARATOR = "|"
FAVORITE_TRUE = "1"
FAVORITE_FALSE = "0"
CONSOLE = Console()

HELP_COMMAND = {"-c": ("\n[green]create_note: creates a new note to be later on stored in JSON file using the given info[/green]\n"
                        "[cyan]title: [/cyan]title of the note to create refering to its content;\n"
                        "[cyan]content: [/cyan]could be a text, or pasted text to be included inside the note;\n"
                        "[cyan]tags: [/cyan]letters, names, or anything that might make it easier for you to keep track of;\n"
                        "[cyan]fvr: [/cyan]if the note should be considered favorite or not - 0: false, 1: true.\n"
                        "\n[blue]create_note [/blue]can also work with files, use: [blue]c file_name.txt | <tags> | <fvr>[/blue]\n"
                        "[blue]example_usage: [/blue]c <title> | <content> | <tags> | <fvr>"),

                "-l": ("\n[green]list_notes: lists all the notes and their respective contents.[/green]\n"
                        "[cyan]-n: [/cyan]lists all notes.\n"
                        "[cyan]-sum: [/cyan]lists all summarized notes.\n"
                        "[cyan]-cards: [/cyan]lists all flashcards generated.\n"
                        "[cyan]-quiz: [/cyan]lists all generated quizes.\n"
                        "\n[blue]example_usage: [/blue]l -sum"),

                "-f": ("\n[green]find_note: finds a note in the JSON file using their ID or Title[/green]\n"
                        "[cyan]note_id | title: [/cyan]id or title to look after.\n"
                        "[cyan]-tag: [/cyan]searches for a specific tag.\n"
                        "[blue]example_usage: [/blue]f <note_id/title>\n"
                        "[blue]example_usage: [/blue]f -tag <tag>"),
                              
                "-u": ("\n[green]update_note: updates an existing note in JSON file using the given info[/green]\n"
                        "[cyan]title: [/cyan]title of the note to look after;\n"
                        "[cyan]content: [/cyan]could be an updated text or no changes;\n"
                        "[cyan]tags: [/cyan]letters, names, or anything that might make it easier for you to keep track of;\n"
                        "[cyan]fvr: [/cyan]if the note should be considered favorite or not - 0: false, 1: true.\n"
                        "\n[blue]update_note [/blue]can also work with files, use: [blue]u file_name.txt | <tags> | <fvr>[/blue]\n"
                        "[blue]update_note [/blue]can also update titles with: [blue]u note_title | -new_title[/blue]"),

                "-d": ("\n[green]delete_note: deletes a note in the JSON file using their ID or Title[/green]\n"
                        "[cyan]note_id | title: [/cyan]id or title to look after.\n"
                        "\n[blue]example_usage: [/blue]d <note_id/title>"),

                "-s": ("\n[green]notes_stats: shows some funny stats about your notes such as total, favorite's amount and favorite tag.[/green]"),

                "-a": ("\n[green]ai_tools: uses AI to help you with your notes[/green]\n"
                        "[cyan]-c: [/cyan]shows the current AI configuration.\n"
                        "[cyan]-c | provider:<provider> | model:<model> | api_key:<api_key> [/cyan]changes the AI configuration.\n"
                        "[cyan]-r: [/cyan]resets the AI configuration.\n"
                        "[cyan]sum | title or note_id: [/cyan]summarizes a note given its ID or title.\n"
                        "[cyan]cards | title or note_id: [/cyan]generates flashcards for a note given its ID or title.\n"
                        "[cyan]quiz | title or note_id: [/cyan]generates a quiz for a note given its ID or title.\n"
                        "\n[blue]example_usage: [/blue]a -c | provider:openai | api_key:your_api_key\n"
                        "[blue]example_usage: [/blue]a sum | really_cool_title\n"
                        "[blue]example_usage: [/blue]a quiz | 2\n")
                        }