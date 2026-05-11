# Deep Tutor Architecture

## Goal

Build a local AI programming mentor that teaches through guidance instead of giving direct answers.

---

# Core Principles

- Prioritize learning over speed
- Encourage debugging and thinking
- Avoid giving full solutions immediately
- Track learning progress and weaknesses
- Run locally on the user's machine

---

# High Level Architecture

User
↓
Orchestrator
↓
Selected Agent
↓
LLM (Qwen3 via Ollama)
↓
Response

---

# Main Components

## Orchestrator
Responsible for:
- routing requests
- managing memory
- selecting agents
- handling modes

---

## Agents

### Mentor Agent
General coding mentor.

### Debug Agent
Helps debug errors step-by-step.

### Concept Agent
Explains programming concepts deeply.

---

## Memory System

Stores:
- weak concepts
- repeated mistakes
- solved topics
- learning history

SQLite initially.

---

# Tech Stack

Backend:
- Python
- FastAPI

LLM:
- Ollama
- Qwen3 8B

Database:
- SQLite

Future:
- ChromaDB
- FAISS

---

# Future Features

- project awareness
- spaced repetition
- adaptive difficulty
- codebase analysis
- voice interaction
