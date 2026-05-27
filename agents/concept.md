# Agent spec: Concept

**Mode id:** `concept`  
**Prompt pack:** [prompts/modes/concept.md](../prompts/modes/concept.md)

## Summary

Layered explanations for **mental models**, **definitions**, and **comparisons** when there is no primary failing run.

## Routing signals (select concept)

| Signal | Examples |
|--------|----------|
| `theory_question` | “What is a deadlock?” / “Explain CAP” |
| `comparison` | “Redis vs Memcached?” / “B-tree vs hash index?” |
| `definition` | “What does idempotent mean?” |
| `mental_model` | “How does git rebase work conceptually?” |

## Do not select when

| Condition | Route to |
|-----------|----------|
| Stack trace or failing test dominates message | **debug** (concept only as secondary) |
| “How do I implement X in my code” with partial code | **mentor** |

## Default hint range

- **Start:** 1–3 for new topics (intuition → structure)  
- Level 4–5 when user explicitly asks for worked example or lower levels failed  

## Worked vignette

**“What is a deadlock?” while cwd is `domains/backend`:** Concept; relate to locks and queues from prior context per memory; hint 2–3.

## Handoff to mentor

When user shifts to **application in their repo** (“how do I use this here?”), switch to **mentor**—do not re-deliver the full concept unless a gap blocks progress.

## Orchestrator outputs

- `mode: concept`
- `prompt_slice: prompts/modes/concept.md`
- `hint_level: 1–5`
- Optional domain overlay for symptom linking (backend, databases)
