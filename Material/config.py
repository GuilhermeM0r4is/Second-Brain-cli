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
                        "\n[blue]example_usage: [/blue]c <title> | <content> | <tags> | <fvr>"),

                "-l": ("\n[green]list_info: lists all the info and their respective contents.[/green]\n"
                        "[cyan]notes: [/cyan]lists all notes;\n"
                        "[cyan]cards: [/cyan]lists all flashcards generated;\n"
                        "[cyan]quiz: [/cyan]lists all generated quizes.\n"
                        "\n[blue]example_usage: [/blue]l sum"),

                "-f": ("\n[green]find_info: finds in the JSON file the info looked for/green]\n"
                        "[cyan]notes | note_id or title: [/cyan]note id or title to look after;\n"
                        "[cyan]notes | -tag: [/cyan]searches for a specific tag for notes;\n"
                        "[cyan]sum | title: [/cyan]searches for a title in summarized notes;\n"
                        "[cyan]cards | title: [/cyan]searches for a title in flashcard notes;\n"
                        "[cyan]quiz | title: [/cyan]searches for a title in all quiz notes.\n"
                        "\n[blue]example_usage: [/blue]f <note_id/title>\n"
                        "[blue]example_usage: [/blue]f notes | -tag <tag>\n"
                        "[blue]example_usage: [/blue]f quiz | <title>\n"),

                "-d": ("\n[green]delete_info: deletes the informatiin in JSON file using its ID or title[/green]\n"
                        "[cyan]notes | note_id or title: [/cyan]id or title to look after;\n"
                        "[cyan]sum | title: [/cyan]deletes for a title in summarized notes;\n"
                        "[cyan]cards | title: [/cyan]deletes for a title in flashcard notes;\n"
                        "[cyan]quiz | title: [/cyan]deletes for a title in all quiz notes.\n"
                        "\n[blue]example_usage: [/blue]d notes | <note_id/title>\n"
                        "[blue]example_usage: [/blue]d cards | <title>\n"),
                              
                "-u": ("\n[green]update_note: updates an existing note in JSON file using the given info[/green]\n"
                        "[cyan]title: [/cyan]title of the note to look after;\n"
                        "[cyan]content: [/cyan]could be an updated text or no changes;\n"
                        "[cyan]tags: [/cyan]letters, names, or anything that might make it easier for you to keep track of;\n"
                        "[cyan]fvr: [/cyan]if the note should be considered favorite or not - 0: false, 1: true.\n"
                        "\n[blue]update_note [/blue]can also work with files, use: [blue]u file_name.txt | <tags> | <fvr>[/blue]\n"
                        "[blue]update_note [/blue]can also update titles with: [blue]u note_title | -new_title[/blue]"),

                "-s": ("\n[green]notes_stats: shows some funny stats about your notes such as total, favorite's amount and favorite tag.[/green]"),

                "-i": ("\n[green]import_document: imports pdf, pptx and md into notes[/green]\n"
                        "[cyan]document_type: [/cyan]a file that has to match the given types;\n"
                        "[cyan]tags: [/cyan]tags to give to the note;\n"
                        "[cyan]fvr: [/cyan]if the note is favorite (0 or 1);\n"
                        "[cyan]-config: [/cyan]shows current terrasect config;\n"
                        "[cyan]-dpi | int: [/cyan]configures terrasect dpi value;\n"
                        "[cyan]-lang: [/cyan]configures terrasect language.\n"
                        "\n[blue]example_usage: [/blue]i document.pdf | cool_tag | 1\n"
                        "[blue]example_usage: [/blue]i -lang | eng+port\n"),

                "-a": ("\n[green]ai_tools: uses AI to help you with your notes[/green]\n"
                        "[cyan]-c: [/cyan]shows the current AI configuration;\n"
                        "[cyan]-c | provider:<provider> | model:<model> | api_key:<api_key> [/cyan]changes the AI configuration;\n"
                        "[cyan]-r: [/cyan]resets the AI configuration;\n"
                        "[cyan]sum | title or note_id: [/cyan]summarizes a note given its ID or title;\n"
                        "[cyan]cards | title or note_id: [/cyan]generates flashcards for a note given its ID or title;\n"
                        "[cyan]quiz | title or note_id: [/cyan]generates a quiz for a note given its ID or title;\n"
                        "[cyan]all | title or note_id: [/cyan]does all the three (sum, cards, quiz) at once.\n"
                        "\n[blue]example_usage: [/blue]a -c | provider:openai | api_key:your_api_key\n"
                        "[blue]example_usage: [/blue]a sum | really_cool_title\n"
                        "[blue]example_usage: [/blue]a all | 2\n")
                        }