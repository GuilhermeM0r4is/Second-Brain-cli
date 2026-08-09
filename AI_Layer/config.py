import json
from rich.panel import Panel

from AI_Layer.communication import ask_ai
from AI_Layer.model import CONSOLE, Model
from AI_Layer.storage import save_config
from AI_Layer.safe_guarding import ensure_model, safe_json
from Core_Features.notes import get_note
from Core_Features.models import Note


def change_config(siz_action: int, model: Model, actn: list) -> str | Model:
    ''' function that changes the configuration of the AI model '''

    if siz_action < 2: return CONSOLE.print(f"[red]ai_tools: Invalid action[/red]")

    for num in range(1, siz_action):

        # if the action is not in the correct format, we skip it
        if ":" not in actn[num]: return CONSOLE.print(f"[red]ai_tools: Invalid action format: {actn[num]}[/red]")

        key, value = actn[num].split(":")     # splits the action into key and value
        key = key.strip()
        value = value.strip()

        if key not in ["provider", "model", "api_key"]: return CONSOLE.print(f"[red]ai_tools: Invalid key: {key}[/red]")

        if key == "api_key" and value != "":
            CONSOLE.print(f"\n[yellow]ai_tools: Warning: You are using a non-local model, keep in mind that your data may be shared![/yellow]")
            setattr(model, "data_sharing", "CLOUD")  # sets the data sharing to ON if the api_key is not empty

        # updates the model with the new key-value pair
        setattr(model, key, value)      # sets the attribute of the model to the new value

    CONSOLE.print(f"[green]ai_tools: Updated AI info to: provider: {model.provider} | model: {model.model} | data_sharing: {model.data_sharing}[/green]")
    return save_config(model)  # saves the new configuration to the json file


def reset_config() -> Model:
    ''' resets the configuration of the AI model to default values '''
    
    model = Model(provider = "ollama", model = "NONE", api_key = "NONE", data_sharing = "LOCAL")
        
    CONSOLE.print(f"[green]ai_tools: provider: {model.provider} | model: {model.model} | " 
                  f"api_key: {model.api_key} | data_sharing: {model.data_sharing}[/green]")
    
    return save_config(model)  # saves the current configuration to the json file


def sum_note(actn: list, notes: list[Note], model: Model) -> str:
    ''' summarizes a note using the AI model in json file '''
    try:
        result = get_note(actn[1], notes)
        if result == None: return CONSOLE.print("[red]ai_tools: Note not found[/red]")

        # ensures that the model is valid and ready to use
        if ensure_model(model) == False: 
            return CONSOLE.print("[red]ai_tools: Invalid model configuration. Please set the provider and model before using AI features.[/red]")

        prompt = f"""       
        You are the summarization engine of Second Brain CLI, a personal knowledge-management tool.
        Read the ENTIRE note before generating your response.
        Your task is to:
        1. Create a concise and descriptive title for the note.
        2. Write a clear summary of its complete content.
        3. Preserve the important concepts, facts, definitions, relationships, examples, and conclusions.
        4. Do not invent information that is not present in the note.
        5. Remove unnecessary repetition and irrelevant details.
        6. Write the summary so that a university student can understand it without needing to reread the original note.
        7. Keep the summary reasonably concise while retaining the important information.

        Return ONLY valid JSON using exactly this structure:
        {{
            "title": "Generated title",
            "summary": "Generated summary"
        }}
        NOTE TITLE: {result.title}
        NOTE CONTENT: {result.content} """

        # send the prompt to the AI model and get the response
        raw = ask_ai(prompt, model)
        answer = safe_json(raw)  # safely parse the JSON response

        if answer == {} or "title" not in answer or "summary" not in answer: 
            return CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")

        CONSOLE.print(      # displays the summary in a panel
            Panel(
                answer["summary"],
                title = answer["title"],
                expand = False
            )
        )
    except ValueError as e: return CONSOLE.print(f"[red]ai_tools: {e}[/red]")