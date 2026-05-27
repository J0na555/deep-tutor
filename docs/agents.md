# Agents

In Deep Tutor, **“agents” are not autonomous AI systems**—especially in the MVP. They are **prompt modes**: packaged **teaching behaviors** and **reasoning stances** (mentor, debugging, concept explanation, …) that the orchestrator selects. You interact through **OpenCode**; you do not “call Agent B.”

## Artifacts in this repo

| Mode | Spec | Prompt pack |
|------|------|-------------|
| Mentor | [agents/mentor.md](../agents/mentor.md) | [prompts/modes/mentor.md](../prompts/modes/mentor.md) |
| Debug | [agents/debug.md](../agents/debug.md) | [prompts/modes/debug.md](../prompts/modes/debug.md) |
| Concept | [agents/concept.md](../agents/concept.md) | [prompts/modes/concept.md](../prompts/modes/concept.md) |

Index: [agents/README.md](../agents/README.md)

## Canonical sections (system design)

- [Teaching behaviors and prompt modes](system-design.md#9-teaching-behaviors-and-prompt-modes)
- [Orchestrator](system-design.md#8-orchestrator)
- [Hint escalation](system-design.md#10-hint-escalation)

**Hint policy:** [hint-policy.md](hint-policy.md)  
**Philosophy:** [Philosophy](../philosophy.md)
