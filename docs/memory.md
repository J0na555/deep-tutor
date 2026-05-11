# Memory System

## Goal

Track user learning progress over time.

---

# Memory Types

## Short-Term Memory

Current conversation context.

Stores:
- recent messages
- current problem
- current hints

---

## Long-Term Memory

Persistent learning profile.

Stores:
- weak topics
- repeated mistakes
- solved concepts
- learning trends

---

## Project Memory

Stores:
- codebase patterns
- architecture decisions
- recurring project mistakes

---

# Example Memory Record

{
  "topic": "recursion",
  "status": "weak",
  "mistakes": [
    "missing base case"
  ],
  "attempts": 4
}

---

# Initial Database

SQLite

Tables:
- users
- sessions
- concepts
- mistakes
- projects

---

# Future Improvements

- vector search
- semantic memory
- spaced repetition
- adaptive learning paths
