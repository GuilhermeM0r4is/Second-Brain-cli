NOTE_ID_PREFIX = "N"
SEPARATOR = " | "
FAVORITE_TRUE = "1"
FAVORITE_FALSE = "0"

HELP_COMMAND = {"-c": ("\n[green]create_note: creates a new note to be later on stored in JSON file using the given info[/green]\n"
                        "[cyan]title: [/cyan]title of the note to create refering to its content;\n"
                        "[cyan]content: [/cyan]could be a text, or pasted text to be included inside the note;\n"
                        "[cyan]tags: [/cyan]letters, names, or anything that might make it easier for you to keep track of;\n"
                        "[cyan]fvr: [/cyan]if the note should be considered favorite or not - 0: false, 1: true.\n"
                        "\n[blue]create_note [/blue]can also work with files, just use: [blue]c file_name.txt [tags] [fvr][/blue]"),

                "-l": ("\n[green]list_notes: lists all the notes and their respective contents.[/green]"),

                "-f": ("\n[green]find_note: finds a note in the JSON file using their ID or Title[/green]\n"
                        "[cyan]note_id | title: [/cyan]id or title to look after.\n"
                        "[cyan]-tag: [/cyan]searches for a specific tag."),
                              
                "-u": ("\n[green]update_note: updates an existing note in JSON file using the given info[/green]\n"
                        "[cyan]title: [/cyan]title of the note to look after;\n"
                        "[cyan]content: [/cyan]could be an updated text or no changes;\n"
                        "[cyan]tags: [/cyan]letters, names, or anything that might make it easier for you to keep track of;\n"
                        "[cyan]fvr: [/cyan]if the note should be considered favorite or not - 0: false, 1: true.\n"
                        "\n[blue]update_note [/blue]can also work with files, just use: [blue]u file_name.txt [tags] [fvr][/blue]\n"
                        "[blue]update_note [/blue]can also update titles with: [blue]u title -new_title[/blue]"),

                "-d": ("\n[green]delete_note: deletes a note in the JSON file using their ID or Title[/green]\n"
                        "[cyan]note_id | title: [/cyan]id or title to look after."),

                "-s": ("\n[green]notes_stats: shows some funny stats about your notes such as total, favorite's amount and favorite tag.[/green]")
                        }