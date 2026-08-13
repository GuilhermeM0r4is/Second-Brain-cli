from AI.model import CONSOLE, Model, get_flashcard_prompt, get_summary_prompt, get_quizz_prompt
from AI.model import format_card_print, format_quiz_print
from AI.storage import save_generated
from AI.safe_guarding import ensure_model, safe_json, ask_with_retry
from Material.material import get_note, create_note
from Material.storage import load_notes
from Material.model import Note
from Storage.storage import save_storage
from dataclasses import asdict


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


def sum_note(actn: list, model: Model) -> str:
    ''' summarizes a note using the AI model in json file '''
    try:
        result = note_find(actn, load_notes(), model)
        prompt = get_summary_prompt(result.title, result.content)

        # send the prompt to the AI model and get the response
        answer = safe_json(ask_with_retry(prompt, model))

        if answer == {} or "title" not in answer or "summary" not in answer: 
            return CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")

        print()
        create_note([answer["title"], answer["summary"]], 2)
        return CONSOLE.print(f"\n[green]ai_tools: Note summarized and added to database[/green]")

    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")


def flashcards(actn: list, model: Model) -> str:
    ''' generates flashcards for a note using the AI model '''
    try:
        result = note_find(actn, load_notes(), model)
        prompt = get_flashcard_prompt(result.title, result.content)

        # send the prompt to the AI model and get the response
        answer = safe_json(ask_with_retry(prompt, model))

        if answer == {} or "cards" not in answer or not isinstance(answer["cards"], list) or len(answer["cards"]) == 0: 
            return CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")

        for card in answer["cards"]:

            if "front" not in card or "back" not in card or "title" not in card: 
                return CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")

            format_card_print(card["front"], card["back"], card["title"])
            save_generated(card, "cards")

        return CONSOLE.print(f"\n[green]ai_tools: {len(answer["cards"])}x Flashcards generated.[/green]")

    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")


def quiz(actn: list, model: Model) -> str:
    ''' generates a quiz for a note using the AI model '''
    try:
        result = note_find(actn, load_notes(), model)
        prompt = get_quizz_prompt(result.title, result.content)

        # send the prompt to the AI model and get the response
        answer = safe_json(ask_with_retry(prompt, model))

        if answer == {} or "questions" not in answer or not isinstance(answer["questions"], list) or len(answer["questions"]) == 0: 
            return CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")

        for quest in answer["questions"]:

            if "question" not in quest or "options" not in quest or "correct_answer" not in quest: 
                return CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")
            if "explanation" not in quest or "title" not in quest:
                return CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")

            format_quiz_print(quest["question"], quest["options"], quest["correct_answer"],
                               quest["explanation"], quest["title"])
            save_generated(quest, "quiz")

        return CONSOLE.print(f"\n[green]ai_tools: {len(answer["questions"])}x Quiz generated.[/green]")

    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")


def all(actn: list, model: Model) -> str:
    ''' does all the three generations at once '''
    try:
        sum_note(actn, model)
        flashcards(actn, model)
        quiz(actn, model)
    
    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")
