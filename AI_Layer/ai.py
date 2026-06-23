from Core_Features.models import Note
from AI_Layer.ai_config import load_config, save_config
from AI_Layer.model import Model, CONSOLE

def ai_tools(actn: list, siz_action: int, notes: list[Note]) -> None:
    ''' function that uses and executes all ai related commands '''

    model = load_config()

    # change the configuration
    if actn[0] == "config":

        # shows the current model working / config
        if siz_action == 1 and model is Model:
            # makes sure it prints either the model or the api_key after the provider
            CONSOLE.print(f"[green]ai_tools: {model.provider} : {model.model}{model.api_key}[/green]")