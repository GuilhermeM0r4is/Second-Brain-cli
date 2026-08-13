from Storage.storage import load_storage
from AI.config import change_config, reset_config, sum_note, flashcards, quiz
from AI.model import Model, CONSOLE


def ai_tools(actn: list, siz_action: int) -> str | Model:
    ''' function that uses and executes all ai related commands '''

    model = Model(**load_storage("ai"))
    
    # shows the current model working / config
    if siz_action == 1 and isinstance(model, Model) and actn[0] == "-c":
        return CONSOLE.print(f"[green]ai_tools: provider: {model.provider} | model: {model.model} | " 
                             f"api_key: {model.api_key} | data_sharing: {model.data_sharing}[/green]")

    # available options for the ai_tools command
    ai_options = {"-c": lambda: change_config(siz_action, model, actn),
                 "-r": lambda: reset_config(), 
                 "sum": lambda: sum_note(actn, model),
                 "cards": lambda: flashcards(actn, model),
                 "quiz": lambda: quiz(actn, model),
                 "all": lambda: all(actn, model)} 

    if actn[0] in ai_options: return ai_options[actn[0]]()     # chooses the option from the dict
    return CONSOLE.print(f"[red]ai_tools: wrong command usage[/red]")