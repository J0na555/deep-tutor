# Memory System

## Goal

Track user learning progress over time, scoped by folder context and global profile.

Memory serves two purposes:
1. **Global memory**: tracks learning across all projects
2. **Folder memory**: tracks learning specific to each project/folder

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Memory Types

## Global Memory

Tracks progress across all projects and folders.

Stores:
- overall skill level
- global weak topics
- repeated mistakes (across all projects)
- learning trends over time

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Folder-Scoped Memory

Tracks progress within a specific project folder.

Stores:
- topic mastery in this folder
- mistakes specific to this project
- learning history in this context
- codebase patterns learned

When you run `deep-tutor ~/projects/leetcode`, it uses LeetCode-scoped memory.
When you run `deep-tutor ~/projects/django-app`, it uses Django-scoped memory.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Short-Term Memory

Current conversation context.

Stores:
- recent messages
- current problem
- current hints

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Long-Term Memory

Persistent learning profile.

Stores:
- weak topics
- repeated mistakes
- solved concepts
- learning trends

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Project Memory

Stores:
- codebase patterns
- architecture decisions
- recurring project mistakes

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Example Memory Record

{
  "topic": "recursion",
  "status": "weak",
  "mistakes": [
    "missing base case"
  ],
  "attempts": 4
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Initial Database

SQLite with folder-scoped tables.

Tables:
- users (global profile)
- folders (folder contexts)
- global_concepts (skills across all projects)
- folder_concepts (skills in specific folder)
- global_mistakes (repeated mistakes overall)
- folder_mistakes (mistakes in specific folder)
- sessions (per-session metadata)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Future Improvements

- vector search
- semantic memory
- spaced repetition
- adaptive learning paths

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Memory Schema

## User Table

Global user profile.

Fields:
- user_id (PK)
- skill_level (global)
- preferred_learning_style
- frustration_score (current session)
- last_active
- total_sessions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Folder Table

Tracks folder contexts.

Fields:
- folder_id (PK)
- user_id (FK -> users.user_id)
- folder_path
- project_type (detected: leetcode, django, flask, etc.)
- first_visited
- last_visited
- session_count

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Session Table

Per-session metadata.

Fields:
- session_id (PK)
- user_id (FK -> users.user_id)
- folder_id (FK -> folders.folder_id)
- topic
- agent_used
- hints_used
- solved
- duration
- timestamp

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Global Concept Progress Table

Tracks mastery across all projects.

Fields:
- concept_id (PK)
- user_id (FK -> users.user_id)
- concept_name (recursion, loops, etc.)
- mastery_score (0-100)
- attempts (across all folders)
- successful_solves
- last_reviewed

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Folder Concept Progress Table

Tracks mastery within a specific folder.

Fields:
- folder_concept_id (PK)
- folder_id (FK -> folders.folder_id)
- concept_name
- mastery_score (0-100, folder-specific)
- attempts_in_folder
- successful_solves_in_folder
- last_reviewed_in_folder

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Global Mistake Table

Repeated mistakes across all projects.

Fields:
- mistake_id (PK)
- user_id (FK -> users.user_id)
- concept
- mistake_type
- frequency (across all folders)
- last_seen
- resolved

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Folder Mistake Table

Mistakes specific to a folder.

Fields:
- folder_mistake_id (PK)
- folder_id (FK -> folders.folder_id)
- concept
- mistake_type
- frequency_in_folder
- last_seen_in_folder
- resolved

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Memory Update Triggers

- frustration_score increases when repeated failures happen in a session
- mastery_score increases after independent or low-hint successful solves
- mistake frequency increments when the same error pattern reappears
- session records are written at session end and summarized into long-term memory