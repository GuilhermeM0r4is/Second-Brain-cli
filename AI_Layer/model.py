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


def format_sum_print(summary: str, title: str) -> str:
    """ formats the print output to give the summarized info """

    CONSOLE.print(      # displays the summary in a panel
        Panel(
            f"[cyan]{summary}[/cyan]",
            border_style="cyan", 
            title = title["title"],
        )
    )


def format_card_print(front: str, back: str, title: str) -> str:
    """ formats the print output to give the flashcards info """

    CONSOLE.print(      # displays the summary in a panel
        Panel(
            f"[cyan]{front}[/cyan]\n\n\n",
            f"[cyan]{back}[/cyan]",
            border_style="cyan", 
            title = f"{title}",
        )
    )


def format_quiz_print(question: str, opt: str, c_answer: str, explanation: str, title: str) -> str:
    """ formats the print output to give the quizzes info """

    CONSOLE.print(      # displays the summary in a panel
        Panel(
            f"[cyan]{question}[/cyan]\n",
            f"[cyan]{opt}[/cyan]\n\n\n\n",
            f"[cyan]{c_answer}[/cyan]\n",
            f"[cyan]{explanation}[/cyan]",
            border_style="cyan", 
            title = f"{title}",
        )
    )


SUMMARIZE_TEMPLATE = """       
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
        {
            {
                "title": "Generated title",
                "summary": "Generated summary"
            }
        }
        - Do not use Markdown.
        - Do not wrap the JSON in ```json.
        - Do not include any text outside the JSON.
        NOTE TITLE: {title} 
        NOTE CONTENT: {content} """


FLASHCARDS_TEMPLATE = """       
        You are the flashcard generation engine of Second Brain CLI, a personal knowledge-management and study tool.
        Read the ENTIRE note before generating the flashcards.
        Your task is to create useful study flashcards based ONLY on the information contained in the note. 
        Requirements:
        1. Identify the most important concepts, facts, definitions, relationships, processes, and examples.
        2. Create clear questions or prompts for the front of each card.
        3. Provide accurate answers or explanations for the back of each card.
        4. Make each card test one specific concept whenever possible.
        5. Avoid trivial questions or cards containing unnecessary information.
        6. Do not invent, assume, or add information that is not present in the note.
        7. Avoid creating duplicate or nearly identical cards.
        8. Make the cards useful for active recall by requiring the student to remember the answer rather than simply recognize it.
        9. Use the terminology and concepts from the original note.
        10. Generate as many cards as necessary to cover the important information, while avoiding unnecessary repetition.

        Return ONLY valid JSON using exactly this structure:
        {
            "cards": 
            [
                {
                    "title": "Title of the flashcard"
                    "front": "Question or prompt",
                    "back": "Answer or explanation"
                },  
                {
                    "title": "Another flashcard title"
                    "front": "Another question",
                    "back": "Another answer"
                }
            ]
        }
        - Do not use Markdown.
        - Do not wrap the JSON in ```json.
        - Do not include any text outside the JSON.
        NOTE TITLE: {title}
        NOTE CONTENT: {content} """


QUIZZ_TEMPLATE = """
        You are the quiz generation engine of Second Brain CLI, a personal knowledge-management and study tool.
        Read the ENTIRE note before generating the quiz. Your task is to create multiple-choice questions that
        test the student's understanding of the important information contained in the note.
        Requirements:
        1. Identify the most important concepts, facts, definitions, relationships, processes, and examples in the note.
        2. Create clear and unambiguous multiple-choice questions.
        3. Each question must have exactly 4 possible options.
        4. Each question must have exactly ONE correct answer.
        5. Make incorrect options plausible and related to the topic, but clearly incorrect according to the note.
        6. Randomize the position of the correct answer between A, B, C, and D.
        7. Provide the correct answer as the exact text of the corresponding option.
        8. Provide a concise explanation explaining why the correct answer is correct.
        9. Questions should test understanding and recall rather than trivial details whenever possible.
        10. Do not create duplicate or nearly identical questions.
        11. Do not invent, assume, or add information that is not present in the note.
        12. Use the terminology and concepts from the original note.
        13. Generate enough questions to cover the important information while avoiding unnecessary repetition.

        Return ONLY valid JSON using exactly this structure:
        {
            "questions": 
            [
                {
                "title": "Title of the quizz with number of the question"
                "question": "What is the main idea of the note?",
                "options": 
                    [
                    "Option A",
                    "Option B",
                    "Option C",
                    "Option D"
                    ],
                "correct_answer": "Option C",
                "explanation": "Because ..."
                }
            ]
        }
        Do not use Markdown.
        Do not wrap the JSON in ```json.
        Do not include any text outside the JSON.
        NOTE TITLE: {title}
        NOTE CONTENT: {content} """


def get_summary_prompt(title: str, content: str) -> str:
    return SUMMARIZE_TEMPLATE.format(title = title, content = content)


def get_flashcard_prompt(title: str, content: str) -> str:
    return FLASHCARDS_TEMPLATE.format(title = title, content = content)


def get_quizz_prompt(title: str, content: str) -> str:
    return QUIZZ_TEMPLATE.format(title = title, content = content)