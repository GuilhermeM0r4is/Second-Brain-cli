# Second Brain CLI
> A modular, privacy-focused terminal-based personal knowledge management and study assistant built with Python.

Second Brain CLI (SBRAIN) is a personal knowledge-management tool designed to help students organize notes, manage study material, and eventually use AI to summarize and transform their knowledge into useful study resources.
The project is being developed progressively as a personal software-engineering project, with a focus on clean architecture, modularity, persistence, CLI design, and AI integration.

---

## Features

### Core Features
* Create notes
* List notes
* Search notes by ID or title
* Update existing notes
* Delete notes
* Manage tags
* Search notes by tags
* Manage favorite notes
* View note statistics
* Persistent local JSON storage
* Rich terminal interface
* Command-based CLI

### AI Features
SBRAIN is being extended with a provider-independent AI layer supporting:

* Local AI models through Ollama
* Cloud AI providers through API keys
* AI-generated note summaries
* AI-generated titles
* Flashcard generation
* Question generation

The AI layer is designed so that the core application does not depend on a specific AI provider.

---

## Privacy
Privacy is an important design goal of SBRAIN.

The application is designed to support **local AI processing**, allowing users to run models directly on their own machine through Ollama. When using a cloud provider, the user explicitly configures their own API credentials. The project does not require a central SBRAIN server or account.
> Local models are recommended when working with sensitive or private study material.

---

## Requirements
* Python 3.10+
* Git
* Ollama (optional, only required for local AI functionality)

Python dependencies:
```text
rich
openai
anthropic
google-genai
ollama
```

These dependencies are listed in `requirements.txt`.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/GuilhermeM0r4is/Second-Brain-cli.git
```

Enter the project directory:
```bash
cd Second-Brain-cli
```

### 2. Create a virtual environment
Windows:
```bash
python -m venv venv
```

Activate it:
```bash
venv\Scripts\activate
```

Linux/macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Running SBRAIN
From the root directory:

```bash
python run.py
```

The application will start directly in the terminal.
Example:
```text
SB > h
```

The help command displays the available commands.

---

## Command Overview
The exact command set may evolve as development continues. Typical commands include:

```text
c   Create a note
l   Lists content
f   Find a note
u   Update a note
d   Delete a note
s   Show statistics
a   AI functionalities
h   Show help
0   Exit
```

Example to create a note with <title> <content> <tag>:
```text
SB > c | Algorithms | QuickSort | algorithms
```

Find a note by ID (can also be by title):
```text
SB > f 1
```

List notes:
```text
SB > l -n
```

---

# AI Configuration
SBRAIN's AI layer is designed to support multiple providers.

Currently supported/planned providers include:
* Ollama
* OpenAI
* Anthropic
* Google Gemini

### Local AI with Ollama
Ollama allows models to run locally on the user's computer.
After installing Ollama and downloading a model, SBRAIN can communicate with the local Ollama service.
For example:

```bash
ollama pull llama3.2
```

The SBRAIN configuration can then be set to use:
```text
Provider: Ollama
Model: llama3.2
API_key: NONE
Data_sharing: LOCAL
```

No external API key is required for local Ollama models.

### Cloud Providers
Users may alternatively configure an API provider using their own API credentials.
Examples include:

```text
OpenAI
Anthropic
Google Gemini
Ollama Cloud
```

<<<< API keys should **never be committed to Git**. >>>>

---

# Data Storage
The current version uses JSON for persistence.
Local application data is stored inside:

```text
Storage/
└── data.json
```

The JSON database is intentionally excluded from Git through `.gitignore`. This means every user has their own local database.
Future versions will migrate the persistence layer to SQLite.

---

# Project Structure
```text
Second-Brain-cli/
│
├── run.py
│
├── AI_Layer/
│   ├── __init__.py
│   ├── ai.py
│   ├── ai_config.py
│   └── model.py
│
├── Core_Features/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── notes.py
│   ├── storage.py
│   ├── ui.py
│   └── config.py
│
├── Storage/
│   └── data.json
│
├── requirements.txt
├── .gitignore
└── README.md
```

The architecture is separated into layers so that functionality can be developed independently.

### `Core_Features`
Contains the main application logic, note management, persistence, configuration and terminal interface.

### `AI_Layer`
Contains AI-related functionality and provider configuration.

### `Storage`
Contains local persistent application data.

### `run.py`
Acts as the application entry point.

---

# Development Philosophy
SBRAIN is intentionally being developed incrementally.
Each version introduces new functionality while attempting to improve the architecture of the previous version. The project focuses on learning and applying:

* Python
* Object-oriented programming
* Modular architecture
* File persistence
* JSON
* SQLite
* API integration
* AI integration
* CLI development
* Git and version control
* Software engineering practices

---

# Roadmap

## B1 — Core System
* [x] Note creation
* [x] Note listing
* [x] Note searching
* [x] Note updating
* [x] Note deletion
* [x] Tags
* [x] Favorites
* [x] Statistics
* [x] Rich CLI interface
* [x] Modular architecture

## B2 — AI Integration
* [x] AI configuration system
* [x] Provider configuration
* [x] Ollama integration
* [X] OpenAI integration
* [X] Anthropic integration
* [X] Google Gemini integration
* [X] AI note summaries
* [X] AI-generated titles
* [X] Flashcard generation
* [X] Quiz generation

## B3 — Knowledge & Documents
* [ ] PDF import     <-- work in progress
* [ ] PowerPoint import
* [ ] Document text extraction
* [ ] Automatic document-to-note conversion
* [ ] Chunking
* [ ] Embeddings
* [ ] Local vector database
* [ ] RAG-based knowledge retrieval

## B4 — Study System
* [ ] Flashcard system
* [ ] Quiz system
* [ ] Spaced repetition
* [ ] Study sessions
* [ ] Progress tracking

## Future
Possible future features include:

* SQLite migration
* Markdown rendering
* Cloud synchronization
* Encryption
* Custom AI prompts
* Self-hosted AI models
* Fine-tuned models
* Advanced knowledge retrieval

---

# Project Status

**Current version: B2 — AI Integration**
SBRAIN is an active personal project and is continuously evolving.

The primary goal is not only to build a useful application, but also to use the project as a practical environment for learning software engineering and developing a portfolio project from the ground up.

---

## License
This project is currently developed as a personal open-source project.
See the repository for the current licensing information.
