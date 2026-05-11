# Deep Tutor Architecture

## Goal

Build a local learning operating system that teaches through guidance, not shortcuts. A personal mentor layer between you and everything you try to learn.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Core Principles

- Prioritize learning over speed
- Encourage debugging and thinking
- Avoid giving full solutions immediately
- Track learning progress and weaknesses
- Run locally on the user's machine

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# High Level Architecture

## Both MVP and Post-MVP (Same Pattern)

The interface is always the ORCHESTRATOR. You never pick an agent directly.

```
User (terminal)
   ↓
Deep Tutor Orchestrator (single entry point)
   ↓
Selected Agent (thinking style)
   ↓
LLM (Qwen via Ollama)
   ↓
Response
   ↓
Memory updated
```

MVP has only Mentor Agent available. Post-MVP adds Debug + Concept agents.

But the orchestrator is the ONLY interface in both cases.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Main Components

## Orchestrator (The Brain)

This is the SINGLE interface. Users never see agents directly.

Responsible for:
- routing requests to appropriate agent
- managing memory (per user + folder context)
- selecting agents based on request type
- deciding hint levels
- folder-based context detection
- building final LLM prompts
- enforcing teaching constraints

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Agents (Thinking Styles, Not User-Facing)

Agents are NOT independent systems. They are "thinking styles" the orchestrator selects.

### Mentor Agent
Default teacher. Guides thinking without direct solutions.

### Debug Agent
Triggered by errors. Teaches debugging habits, not fixes.

### Concept Agent
Triggered by theory questions. Explains "why", not "how to code it".

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Memory System

Stores:
- weak concepts
- repeated mistakes
- solved topics
- learning history

SQLite initially.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

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

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Future Features

- project awareness
- spaced repetition
- adaptive difficulty
- codebase analysis
- voice interaction


# Request Lifecycle

## Example Flow

User Input:
"Why does my recursion never stop?"

↓

Orchestrator receives request

↓

Memory lookup:
- user previously struggled with recursion
- common issue: missing base cases

↓

Request classification:
- category: debugging + concept explanation
- difficulty: beginner/intermediate

↓

Agent Selection:
Primary Agent:
- Debug Agent

Supporting Agent:
- Concept Agent

↓

Hint Level Decision:
- user attempted problem 2 times
- no direct solution yet
- use Hint Level 2

↓

LLM Prompt Construction:
Includes:
- mentor rules
- user history
- current code snippet
- selected hint level

↓

Response Generated:
"What condition causes the recursion to stop?"

↓

Memory Update:
Store:
- topic = recursion
- issue = missing termination condition
- hint_level_used = 2
- solved = false


# Orchestrator Decision Logic

## Agent Routing Rules

IF request contains:
- stack trace
- runtime error
- unexpected output

→ Route to Debug Agent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IF request contains:
- "what is"
- "how does"
- theory-related questions

→ Route to Concept Agent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

IF request contains:
- coding attempt
- unfinished solution
- logic confusion

→ Route to Mentor Agent

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Hint Level Logic

Hint Level 1:
- first attempt
- low frustrationw

Hint Level 2:
- repeated confusion
- partial understanding shown

Hint Level 3:
- user stuck after multiple attempts

Hint Level 4:
- repeated failures
- frustration threshold exceeded
- explicit request for deeper help

Hint Level 5:
- full explanation with walkthrough
- used when educational value of withholding is low