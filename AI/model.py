from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel

CONSOLE = Console()

@dataclass
class Model:
    provider: str | None = "ollama"
    model: str | None = "NONE"
    api_key: str | None = "NONE"
    data_sharing: str | None = "LOCAL"  # default value for data sharing


def format_card_print(front: str, back: str, title: str) -> str:
    """ formats the print output to give the flashcards info """

    print()
    CONSOLE.print(      # displays the summary in a panel
        Panel(
            f"[cyan]Front: [/cyan]{front}\n\n"
            f"[cyan]Back: [/cyan]{back}",
            border_style = "cyan", 
            title = f"{title}",
        )
    )


def format_quiz_print(question: str, opt: list, c_answer: str, explanation: str, title: str) -> str:
    """ formats the print output to give the quizzes info """


    opt_text = "\n".join(f"{i+1}. {o}" for i, o in enumerate(opt))
    print()
    CONSOLE.print(      # displays the summary in a panel
        Panel(
            f"[cyan]Q: [/cyan]{question}\n"
            f"{opt_text}\n\n\n\n"
            f"[cyan]A: [/cyan]{c_answer}\n"
            f"[cyan]Exp: [/cyan]{explanation}",
            border_style = "cyan", 
            title = f"{title}",
        )
    )


def get_summary_prompt(title: str, content: str) -> str:

    return f"""
        You are the summarization engine of Second Brain CLI, a personal knowledge-management tool.
        Read the ENTIRE note before generating your response.

        Your task is to:
        1. Create a concise and descriptive title for the note.
        2. Write a clear summary of its complete content.
        3. Preserve important concepts, facts, definitions, relationships, examples,
           equations, numerical values, and conclusions.
        4. Do not invent information that is not present in the note.
        5. Remove unnecessary repetition and irrelevant details.
        6. Write the summary so that a university student can understand it without
           needing to reread the original note.
        7. Keep the summary reasonably concise while retaining important information.

        Return ONLY valid JSON using exactly this structure:

        {{
            "title": "Generated title",
            "summary": "Generated summary"
        }}

        - Do not use Markdown.
        - Do not wrap the JSON in ```json.
        - Do not include any text outside the JSON.

        NOTE TITLE: {title}
        NOTE CONTENT: {content}
    """


def get_flashcard_prompt(title: str, content: str) -> str:

    return f"""
        You are the flashcard generation engine of Second Brain CLI,
        a personal knowledge-management and study tool.

        Read the ENTIRE note before generating the flashcards.

        Your task is to create useful study flashcards based ONLY on the
        information contained in the note.

        Requirements:
        1. Identify the most important concepts, facts, definitions, relationships,
           processes, equations, and examples.
        2. Create clear questions or prompts for the front of each card.
        3. Provide accurate answers or explanations for the back of each card.
        4. Make each card test one specific concept whenever possible.
        5. Avoid trivial questions or cards containing unnecessary information.
        6. Do not invent, assume, or add information that is not present in the note.
        7. Avoid creating duplicate or nearly identical cards.
        8. Make the cards useful for active recall.
        9. Use the terminology and concepts from the original note.
        10. Generate as many cards as necessary to cover the important information,
            while avoiding unnecessary repetition.

        Return ONLY valid JSON using exactly this structure:

        {{
            "cards": [
                {{
                    "title": "Title of the flashcard",
                    "front": "Question or prompt",
                    "back": "Answer or explanation"
                }},
                {{
                    "title": "Another flashcard title",
                    "front": "Another question",
                    "back": "Another answer"
                }}
            ]
        }}

        - Do not use Markdown.
        - Do not wrap the JSON in ```json.
        - Do not include any text outside the JSON.

        NOTE TITLE: {title}
        NOTE CONTENT: {content}
    """

def get_quiz_prompt(title: str, content: str) -> str:

    return f"""
        You are the quiz generation engine of Second Brain CLI,
        a personal knowledge-management and study tool.

        Read the ENTIRE note before generating the quiz.

        Your task is to create multiple-choice questions that test the student's
        understanding of the important information contained in the note.

        Requirements:
        1. Identify the most important concepts, facts, definitions, relationships,
           processes, equations, and examples in the note.
        2. Create clear and unambiguous multiple-choice questions.
        3. Each question must have exactly 4 possible options.
        4. Each question must have exactly ONE correct answer.
        5. Make incorrect options plausible and related to the topic, but clearly
           incorrect according to the note.
        6. Vary which position (1st, 2nd, 3rd, 4th) holds the correct answer across questions.
        7. Provide the correct answer as the exact text of the corresponding option.
        8. Provide a concise explanation explaining why the correct answer is correct.
        9. Questions should test understanding and recall rather than trivial details
           whenever possible.
        10. Do not create duplicate or nearly identical questions.
        11. Do not invent, assume, or add information that is not present in the note.
        12. Use the terminology and concepts from the original note.
        13. Generate enough questions to cover the important information while
            avoiding unnecessary repetition.
        14. The "title" field must be a short descriptive label based on the question's 
            topic (e.g. "Mitochondria and ATP Production"), never a literal placeholder 
            or a generic "Question N" pattern.

        Example of a correctly filled question (for a note about the solar system):

        {{
            "title": "Largest Planet",
            "question": "Which planet is the largest in the solar system?",
            "options": ["Earth", "Jupiter", "Saturn", "Mars"],
            "correct_answer": "Jupiter",
            "explanation": "Jupiter is the largest planet by both mass and volume."
        }}        
        
        Return ONLY valid JSON using exactly this structure:

        {{
            "questions": [
                {{
                    "title": "...",
                    "question": "...",
                    "options": ["...", "...", "...", "..."],
                    "correct_answer": "...",
                    "explanation": "..."
                }}
            ]
        }}

        - Do not use Markdown.
        - Do not wrap the JSON in ```json.
        - Do not include any text outside the JSON.

        NOTE TITLE: {title}
        NOTE CONTENT: {content}
    """