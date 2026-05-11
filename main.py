from models import generate_note_id, create_note
from notes import add_note, load_note_by_id
from storage import load_notes, save_notes

print("\033[1;36m-- Welcome to SECOND-BRAIN-CLI --\033[0m"
      "\n\033[1;33mversion: b1.0\033[0m")

print("\n\033[1;32m1.\033[0m Create note"
      "\n\033[1;32m2.\033[0m List notes"
      "\n\033[1;32m3.\033[0m Find note"
      "\n\033[1;31m0.\033[0m Exit")

choice = input("\n\033[1;34m> \033[0m")
if choice == 0: exit