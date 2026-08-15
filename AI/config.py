from AI.model import (Model, get_flashcard_prompt, get_quiz_prompt, get_sumchunk_prompt, get_synthesis_prompt,
                      format_card_print, format_quiz_print)
from AI.parsing import parse_chunk_summary, parse_synthesis, parse_flashcards, parse_quiz
from AI.safe_guarding import ensure_model, ask_parsed_with_retry
from AI.storage import save_generated
from Material.material import get_note, create_note
from Material.storage import load_notes
from Material.model import Note, CONSOLE
from Storage.storage import save_storage
from dataclasses import asdict
import re

MATH_DENSITY_THRESHOLD = 0.02
SUMMARY_LIMIT = 12000
MAX_CHARS = 5000


# ------------------------ CONFIG BASED FUNCTIONS ------------------------
def change_config(siz_action: int, model: Model, actn: list) -> str | Model:
    ''' function that changes the configuration of the AI model '''

    if siz_action == 1: return CONSOLE.print(f"[green]ai_tools: {model}[/green]")
    if siz_action < 2: return CONSOLE.print(f"[red]ai_tools: Invalid action[/red]")

    for num in range(1, siz_action):

        # if the action is not in the correct format, we skip it
        if ":" not in actn[num]: return CONSOLE.print(f"[red]ai_tools: Invalid action format: {actn[num]}[/red]")

        key, value = actn[num].split(":", 1)     # splits the action into key and value
        key = key.strip()
        value = value.strip()

        if key not in ["provider", "model", "api_key"]: return CONSOLE.print(f"[red]ai_tools: Invalid key: {key}[/red]")

        if key == "api_key" and value != "":
            CONSOLE.print(f"\n[yellow]ai_tools: Warning: You are using a non-local model, keep in mind that your data may be shared![/yellow]")
            setattr(model, "data_sharing", "CLOUD")  # sets the data sharing to ON if the api_key is not empty

        # updates the model with the new key-value pair
        setattr(model, key, value)      # sets the attribute of the model to the new value

    CONSOLE.print(f"[green]ai_tools: Updated AI info to: provider: {model.provider} | model: {model.model} | data_sharing: {model.data_sharing}[/green]")
    return save_storage("ai", asdict(model))  # saves the new configuration to the json file


def reset_config() -> None:
    ''' resets the configuration of the AI model to default values '''
    
    model = Model(provider = "ollama", model = "NONE", api_key = "NONE", data_sharing = "LOCAL")
    CONSOLE.print(f"[green]ai_tools: provider: {model.provider} | model: {model.model} | " 
                  f"api_key: {model.api_key} | data_sharing: {model.data_sharing}[/green]")
    
    return save_storage("ai", asdict(model))  # saves the current configuration to the json file


def note_find(actn: list, notes: list[Note], model: Model) -> Note | None:
    ''' auxiliar function finds a note, and ensures validations '''

    result = get_note(actn[1], notes)
    if result == None: return CONSOLE.print("[red]ai_tools: Note not found[/red]")
    
    # ensures that the model is valid and ready to use
    if ensure_model(model) == False: 
        return CONSOLE.print("[red]ai_tools: Invalid model configuration. Please set the provider and model before using AI features.[/red]")

    return result


# ------------------------ SUMMARIZING BASED FUNCTIONS ------------------------
def split_note(content: str) -> list[str]:
    ''' splits a note into smaller notes '''

    paragraphs = content.split("\n\n")
    chunks = []; current = ""

    for paragraph in paragraphs:
        if len(current) + len(paragraph) > MAX_CHARS:

            if current: chunks.append(current.strip())
            current = paragraph

        else: current += "\n\n" + paragraph

    if current.strip(): chunks.append(current.strip())
    return chunks


# config.py
import re

MATH_SYMBOL_PATTERN = re.compile(
    r'[∂∇∫∑√±≤≥≠∈⊂⊆∀∃⇒⇔→↦×÷·∞]|\\frac|\\partial|\\nabla|\\int|\\sum|\\lim|\\sqrt|\\mathbf|\\begin\{')

# common leftover patterns from OCR'd math: "R2", "R3", "Rn", digit-glued-to-letter like "y2", "x2"
MATH_STRUCTURAL_PATTERN = re.compile(
    r'\bR\d\b|\bR[nm]\b|\b[a-zA-Z]\d\b|\b\d[a-zA-Z]\b|f\([a-zA-Z],\s*[a-zA-Z]\)|D[a-zA-Z]?f\(|∀|∃')

MATH_KEYWORDS = [
    "derivative", "differential", "gradient", "jacobian", "matrix", "vector",   # English
    "theorem", "equation", "integral", "differentiable", "partial derivative",
    "derivada", "diferencial", "gradiente", "jacobiana", "matriz", "vetor",     # Portuguese (just to try out)
    "teorema", "equação", "integral", "diferenciável", "derivada parcial"]


def math_density(content: str) -> float:
    """ estimates how math-heavy a note is, combining symbol/structural markers and topic keywords """

    if not content: return 0.0
    words = content.split()
    word_count = max(len(words), 1)

    symbol_hits = len(MATH_SYMBOL_PATTERN.findall(content))
    structural_hits = len(MATH_STRUCTURAL_PATTERN.findall(content))

    lowered = content.lower()
    keyword_hits = sum(lowered.count(kw) for kw in MATH_KEYWORDS)

    total_hits = symbol_hits + structural_hits + (keyword_hits * 2)  # weight keywords a bit heavier
    return total_hits / word_count


def is_math_heavy(content: str) -> bool:
    return math_density(content) > MATH_DENSITY_THRESHOLD


def summarize_chunk(title: str, content: str, model: Model, math_heavy: bool) -> dict:
    ''' summarizes a small note chunck and returns the response '''

    prompt = get_sumchunk_prompt(title, content, math_heavy)
    return ask_parsed_with_retry(prompt, model, parse_chunk_summary, max_tokens = 1500) or {}


def synthesize_summaries(title: str, summaries: list[dict], model: Model) -> dict:
    ''' synthesizes all note chuncks and returns the finel answer '''

    prompt = get_synthesis_prompt(title, summaries)
    return ask_parsed_with_retry(prompt, model, parse_synthesis, max_tokens = 3000) or {}


def summarize_large_note(title: str, content: str, model: Model, math_heavy: bool) -> dict:
    """ summarizes a large note splitting it into chunks """

    chunks = split_note(content)
    summaries = []

    for number, chunk in enumerate(chunks, start=1):
        CONSOLE.print(f"[blue]ai_tools: Analyzing section {number}/{len(chunks)}...[/blue]")

        summary = summarize_chunk(title, chunk, model, math_heavy)
        if summary: summaries.append(summary)

    if not summaries: return {}
    CONSOLE.print("[blue]ai_tools: Starting to synthesize the summaries[/blue]\n")
    return synthesize_summaries(title, summaries, model)


def sum_note(actn: list, model: Model) -> str:
    ''' summarizes a note using the AI model '''
    try:
        result = note_find(actn, load_notes(), model)
        if not result: return CONSOLE.print("[red]ai_tools: Note not found[/red]")

        heavy = is_math_heavy(result.content)
        if heavy:
            CONSOLE.print("[yellow]ai_tools: This note is math-heavy — results may be "
                          "less precise for equations. Formulas will be described "
                          "rather than reproduced exactly where needed.[/yellow]")

        answer = summarize_large_note(result.title, result.content, model, math_heavy = heavy)

        if not answer:
            return CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")

        if "title" not in answer or "summary" not in answer:
            return CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")

        # carry over the original note's tags, appending "sum" to mark it as a generated summary
        existing_tags = [t.strip() for t in result.tags.split(",") if t.strip()] if result.tags else []
        if "sum" not in existing_tags: existing_tags.append("sum")
        tags = ",".join(existing_tags)

        create_note([answer["title"], answer["summary"], tags, result.favorite], 4)
        return CONSOLE.print("\n[green]ai_tools: Note summarized and added to database[/green]")

    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")


# ------------------------ FLASHCARD + QUIZ BASED FUNCTIONS ------------------------
def flashcards(actn: list, model: Model) -> str:
    ''' creates flashcards from a given note (should use summarized notes) '''

    try:
        result = note_find(actn, load_notes(), model)

        heavy = is_math_heavy(result.content)
        if heavy:
            CONSOLE.print("[yellow]ai_tools: This note is math-heavy — results may be "
                          "less precise for equations. Formulas will be described "
                          "rather than reproduced exactly where needed.[/yellow]")

        prompt = get_flashcard_prompt(result.title, result.content, heavy)
        cards = ask_parsed_with_retry(prompt, model, parse_flashcards)
        if not cards:
            return CONSOLE.print("[red]ai_tools: AI returned no usable flashcards[/red]")

        for card in cards:
            format_card_print(card["front"], card["back"], card["title"])
            save_generated(card, "cards")

        return CONSOLE.print(f"\n[green]ai_tools: {len(cards)}x Flashcards generated.[/green]")

    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")


def quiz(actn: list, model: Model) -> str:
    ''' creates flashcards from a given note (should use summarized notes) '''

    try:
        result = note_find(actn, load_notes(), model)

        heavy = is_math_heavy(result.content)
        if heavy:
            CONSOLE.print("[yellow]ai_tools: This note is math-heavy — results may be "
                          "less precise for equations. Formulas will be described "
                          "rather than reproduced exactly where needed.[/yellow]")

        prompt = get_quiz_prompt(result.title, result.content, heavy)
        questions = ask_parsed_with_retry(prompt, model, parse_quiz)

        if not questions:
            return CONSOLE.print("[red]ai_tools: AI returned no usable quiz questions[/red]")

        for quest in questions:
            format_quiz_print(quest["question"], quest["options"], quest["correct_answer"],
                               quest["explanation"], quest["title"])
            save_generated(quest, "quiz")

        return CONSOLE.print(f"\n[green]ai_tools: {len(questions)}x Quiz generated.[/green]")

    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")


def all_at_once(actn: list, model: Model) -> str:
    ''' does all the three generations at once '''
    try:
        sum_note(actn, model)
        flashcards(actn, model)
        quiz(actn, model)
    
    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")
