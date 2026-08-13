from pathlib import Path
from Material.config import FAVORITE_FALSE, FAVORITE_TRUE, CONSOLE
from Material.material import create_note
from Documents.text import import_text
from Documents.pdf import import_pdf
from Documents.pptx import import_pptx
from Documents.ocr import is_available, check_ocr_languages
from Storage.storage import load_storage, save_storage


IMPORTERS = {
    ".pdf": import_pdf,
    ".pptx": import_pptx,
    ".md": import_text,
    ".txt": import_text
}

def get_info(action: list, siz_action: int) -> tuple[str, str] | None:
    ''' finds the favorite and tags from a note '''

    tags = ""; fvr = FAVORITE_FALSE
    # checks the len of action to see if we have tags and fvr set up
    if siz_action >= 2: tags = action[1]
    
    if siz_action == 3:
        if action[2] in (FAVORITE_FALSE, FAVORITE_TRUE): fvr = action[2]
        # makes it so only 0 or 1 can be used to favorite
        else: CONSOLE.print(f"[yellow]import_document: {action[2]} Invalid (not 0 nor 1), setting favorite as False[/yellow]")

    return tags, fvr


def config_dpi(value: int) -> None:
    ''' configures the dpi value to tesseract '''

    if not 76 <= value <= 600: 
        return CONSOLE.print(f"[red]import_config: Invalid dpi value, keep between 76-600.[/red]")

    storage = load_storage("import")
    storage["dpi"] = value

    CONSOLE.print(f"[green]import_config: Storage updated, dpi -> {value}[/green]")
    return save_storage("import", storage)


def config_lang(language: str) -> None:
    ''' configures the language values to tesseract '''

    if not is_available():
        return CONSOLE.print(f"[red]import_config: Tesserac not installed[/red]")

    if not check_ocr_languages(language):
        return CONSOLE.print(f"[red]import_config: Language(s) not installed in tesseract[/red]")

    storage = load_storage("import")
    storage["language"] = language

    CONSOLE.print(f"[green]import_config: Storage updated new {language}[/green]")
    return save_storage("import", storage)



def import_documents(actn: list, siz_action: int) -> str:
    ''' imports all type of documents into functions '''

    if siz_action > 3 or not actn:
        return CONSOLE.print(f"[red]import_documents: Invalid usage[/red]")

    path = Path(actn[0])

    if not path.is_file():
        return CONSOLE.print(f"[red]import_documents: File not found: {path}[/red]")

    extension = path.suffix.lower()

    if extension not in IMPORTERS:
        return CONSOLE.print(f"[red]import_documents: Unsupported file type: {extension}[/red]")

    data = load_storage("import")
    dpi = data["dpi"]; language = data["language"]

    document = IMPORTERS[extension](path, dpi, language)
    if document is None: return CONSOLE.print(f"[red]import_documents: Document Invalid[/red]")

    tags, fvr = get_info(actn, siz_action)
    print()
    create_note([document.title, document.text, tags, fvr], 4)
    return CONSOLE.print(f"\n[green]import_documents: Note imported successfully[/green]")


def importing(actn: list, siz_action: int) -> None:
    ''' checks the import function, configuration of OCR and importing '''

    if not actn:
        return CONSOLE.print(f"[red]import_documents: Invalid usage[/red]")

    if actn[0] == "-config":
        if siz_action != 1: return CONSOLE.print(f"[red]import_config: Usage: i -config[/red]")

        data = load_storage("import")
        return CONSOLE.print(f"[green]import_config: {data}[/green]")

    elif actn[0] == "-dpi":
        if siz_action != 2: 
            return CONSOLE.print(f"[red]import_config: Usage: i -dpi | <dpi>[/red]")

        try: dpi = int(actn[1])
        except ValueError: 
            return CONSOLE.print(f"[red]import_config: DPI must be a number[/red]")
        return config_dpi(dpi)

    elif actn[0] == "-lang":
        if siz_action != 2: 
            return CONSOLE.print(f"[red]import_config: Usage: i -lang | <language>[/red]")
        return config_lang(actn[1])

    import_documents(actn, siz_action)