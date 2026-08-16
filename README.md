# Second Brain CLI

> A modular, privacy-focused terminal-based personal knowledge management and study assistant built with Python.

Second Brain CLI (SBRAIN) is a personal knowledge-management tool designed to help students organize notes, manage study material, and use AI to summarize and transform their knowledge into useful study resources.

The project is developed progressively as a personal software-engineering project, focusing on clean architecture, modularity, persistence, CLI design, document processing, and AI integration.

---

## Features

### Core Features
- Create, list, search, update, and delete notes
- Manage tags and favorite notes
- Search notes by tags
- View note statistics
- Persistent local JSON storage
- Rich terminal interface
- Command-based CLI

### AI Features
- Local AI models through Ollama
- Cloud AI providers through API keys
- AI-generated note summaries
- AI-generated titles
- Flashcard generation
- Quiz/question generation
- AI document chunk processing
- Automatic document-to-note conversion

### Document Features
- PDF import
- PowerPoint (`.pptx`) import
- Document text extraction
- OCR for scanned/image-based documents
- Automatic document-to-note conversion
- Document chunking

---

## Privacy

Privacy is an important design goal of SBRAIN.

The application supports **local AI processing** through Ollama. Cloud providers can also be configured using the user's own API credentials.

SBRAIN does not require a central server or account.

> Local models are recommended when working with sensitive or private study material.

---

## Requirements

- Python 3.10+
- Git
- Ollama *(optional, required only for local AI)*
- Tesseract OCR *(required for OCR functionality)*

Python dependencies are listed in `requirements.txt` and include the libraries required for:

- Terminal UI
- AI provider communication
- Ollama
- PDF processing
- PowerPoint processing
- OCR
- Document/text extraction

Install all Python dependencies with:

```bash
pip install -r requirements.txt
```

---

## Tesseract OCR

SBRAIN uses Tesseract OCR for scanned and image-based documents.

Tesseract is a system dependency and must be installed separately from the Python packages.

### Windows

Install Tesseract OCR and ensure the executable is available to SBRAIN.

A typical installation path is:

```
C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Linux

```bash
sudo apt install tesseract-ocr
```

### macOS

```bash
brew install tesseract
```

Verify the installation with:

```bash
tesseract --version
```

Tesseract is only required when OCR functionality is used.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/GuilhermeM0r4is/Second-Brain-cli.git
cd Second-Brain-cli
```

### 2. Create a virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Tesseract

Follow the Tesseract OCR instructions above if OCR functionality is required.

---

## Running SBRAIN

From the project root:

```bash
python run.py
```

Example:

```
SB > h
```

Use `h` to display the available commands.

---

## Command Overview

The command set may evolve as development continues.

| Command | Description |
|---------|-------------|
| `c` | Create a note |
| `l` | List content |
| `f` | Find a note |
| `u` | Update a note |
| `d` | Delete a note |
| `s` | Show statistics |
| `a` | AI functionalities |
| `h` | Show help |
| `0` | Exit |

Create a note:

```
SB > c | Algorithms | QuickSort | algorithms
```

Find a note by ID or title:

```
SB > f 1
```

List notes:

```
SB > l -n
```

---

## AI Configuration

SBRAIN's AI layer is provider-independent.

### Supported Providers
- Ollama
- OpenAI
- Anthropic
- Google Gemini
- Ollama Cloud

### Local AI with Ollama

Install Ollama and download a model:

```bash
ollama pull llama3.2
```

Example SBRAIN configuration:

```
Provider: Ollama
Model: llama3.2
API_key: NONE
Data_sharing: LOCAL
```

No external API key is required for local Ollama models.

### Cloud Providers

Users can configure supported cloud providers using their own API credentials.

> API keys should never be committed to Git.

---

## Data Storage

The current application data is stored locally:

```
Storage/
├── data.json
└── storage.py
```

`data.json` is included locally but excluded from Git through `.gitignore`.

Each user therefore has their own independent local database.

The project is currently migrating the persistence layer from JSON toward SQLite.

---

## Document Processing

SBRAIN contains a dedicated document-processing layer for importing and converting study material.

Current pipeline:

```
Document
   ↓
Import
   ↓
Text Extraction / OCR
   ↓
Chunking
   ↓
AI Processing
   ↓
Automatic Note Creation
```

Currently implemented:

- PDF import
- PowerPoint import
- Text extraction
- OCR
- Document extraction
- Chunking
- Automatic document-to-note conversion

The next stage is SQLite migration, followed by embeddings, vector storage, and RAG.

---

## Project Structure

```
Second-Brain-cli/
│
├── run.py
│
├── AI/
│   ├── __init__.py
│   ├── ai.py
│   ├── communication.py
│   ├── config.py
│   ├── model.py
│   ├── parsing.py
│   ├── safe_guarding.py
│   └── storage.py
│
├── Material/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── material.py
│   ├── storage.py
│   ├── ui.py
│   └── config.py
│
├── Storage/
│   ├── data.json
│   └── storage.py
│
├── Documents/
│   ├── __init__.py
│   ├── documents.py
│   ├── model.py
│   ├── ocr.py
│   ├── pdf.py
│   ├── pptx.py
│   └── text.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

### `AI/`
Handles AI providers, model configuration, communication, response parsing, safety checks, and AI-related storage.

### `Material/`
Contains the main knowledge-management functionality, including notes/material, tags, favorites, statistics, CLI functionality, and material management.

### `Storage/`
Contains persistent application data and the storage layer.

`data.json` is ignored by Git so every installation has its own local data.

### `Documents/`
Handles document importing and processing, including:

- PDF
- PowerPoint
- OCR
- Text extraction
- Document models
- Document management

### `run.py`
Application entry point.

---

## Development Philosophy

SBRAIN is intentionally developed incrementally, with each stage expanding both functionality and architecture.

The project focuses on:

- Python
- Object-oriented programming
- Modular architecture
- JSON
- SQLite
- File persistence
- API integration
- AI integration
- Document processing
- OCR
- CLI development
- Git and version control
- Software engineering
- Knowledge retrieval

---

## Roadmap

### B1 — Core System
- [x] Note creation
- [x] Note listing
- [x] Note searching
- [x] Note updating
- [x] Note deletion
- [x] Tags
- [x] Favorites
- [x] Statistics
- [x] Rich CLI interface
- [x] Modular architecture

### B2 — AI Integration
- [x] AI configuration system
- [x] Provider configuration
- [x] Ollama integration
- [x] OpenAI integration
- [x] Anthropic integration
- [x] Google Gemini integration
- [x] AI note summaries
- [x] AI-generated titles
- [x] Flashcard generation
- [x] Quiz generation
- [x] AI chunk processing
- [x] Structured AI responses

### B3 — Knowledge & Documents
- [x] PDF import
- [x] PowerPoint import
- [x] Document text extraction
- [x] OCR
- [x] Automatic document-to-note conversion
- [x] Chunking
- [ ] SQLite migration — work in progress
- [ ] Embeddings
- [ ] Local vector database
- [ ] RAG-based knowledge retrieval

### B4 — Study System
- [ ] Flashcard system
- [ ] Quiz system
- [ ] Spaced repetition
- [ ] Study sessions
- [ ] Progress tracking

### Future
- [ ] Markdown rendering
- [ ] Cloud synchronization
- [ ] Encryption
- [ ] Custom AI prompts
- [ ] Self-hosted AI models
- [ ] Fine-tuned models
- [ ] Advanced knowledge retrieval
- [ ] Semantic search
- [ ] Vector-based knowledge retrieval

---

## Project Status

**Current version:** B3 — Knowledge & Documents

Document processing is now implemented, including PDF and PowerPoint importing, text extraction, OCR, chunking, and automatic document-to-note conversion.

The current development focus is:

- SQLite migration

The planned knowledge pipeline is:

```
Documents
    ↓
Extraction / OCR
    ↓
Chunking
    ↓
AI Processing
    ↓
Automatic Notes
    ↓
SQLite
    ↓
Embeddings
    ↓
Vector Database
    ↓
RAG
    ↓
Advanced Knowledge Retrieval
```

SBRAIN is an active personal project and is continuously evolving.

The primary goal is to build a useful application while using the project as a practical environment for learning software engineering and developing a portfolio project from the ground up.

---

## License

This project is currently developed as a personal open-source project.

See the repository for the current licensing information.
