import json
import re

from AI.communication import ask_ai
from AI.model import Model, CONSOLE

def ask_with_retry(prompt: str, model: Model, retries = 3) -> str | None:
    """ Sends a prompt to the AI model and retries if it fails."""

    for attempt in range(1, retries + 1):
        try: 
            return ask_ai(prompt, model)
        except Exception as e:
            if attempt == retries:
                CONSOLE.print(f"[red]ai_tools: AI request failed after {retries} attempts: {e}[/red]")
                return None

            CONSOLE.print(f"[yellow]ai_tools: Retry {attempt}/{retries}...[/yellow]")

    return None


def ensure_model(model: Model) -> bool:
    ''' ensures that the model is valid and ready to use '''

    if model is None or not isinstance(model, Model) or model.model == "NONE":
        CONSOLE.print("[red]ai_tools: No model configuration found. Please set the provider and model before using AI features.[/red]")
        return False

    if model.provider not in ["ollama", "openai", "anthropic", "gemini"]:
        CONSOLE.print("[red]ai_tools: Invalid model configuration. Please set the provider and model before using AI features.[/red]")
        return False

    if model.provider in ["openai", "anthropic", "gemini"] and (model.api_key is None or model.api_key == "NONE"):
        CONSOLE.print("[red]ai_tools: No API key found for the selected provider. Please set the API key before using AI features.[/red]")
        return False

    return True


def clean_json_string(text: str) -> str:
    ''' cleans the JSON string to ensure it's valid '''

    if text is None or not isinstance(text, str): return ""

    # Remove any characters before the first '{' and after the last '}'
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match: return match.group(0)
    else: return ""


def safe_json(text: str) -> dict:
    ''' safely parses a JSON string into a dictionary '''

    if isinstance(text, dict): return text  # if it's already a dict, return it
    if not isinstance(text, str) or text == "": return {}

    cleaned_text = clean_json_string(text)
    if not cleaned_text: return {}

    try:
        return json.loads(cleaned_text)
    
    except json.JSONDecodeError:
        CONSOLE.print("[red]ai_tools: AI returned invalid JSON[/red]")
        return {}