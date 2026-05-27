# Prompt modes (agents)

In Deep Tutor, **“agents” are prompt modes**—packaged teaching behaviors the orchestrator selects. They are **not** autonomous bots or separate chat endpoints.

**Canonical design:** [System design §9](../docs/system-design.md#9-teaching-behaviors-and-prompt-modes)

| Mode | Spec | Prompt pack |
|------|------|-------------|
| **Mentor** | [mentor.md](mentor.md) | [prompts/modes/mentor.md](../prompts/modes/mentor.md) |
| **Debug** | [debug.md](debug.md) | [prompts/modes/debug.md](../prompts/modes/debug.md) |
| **Concept** | [concept.md](concept.md) | [prompts/modes/concept.md](../prompts/modes/concept.md) |

## Routing priority (default)

When signals conflict, apply in order ([§8.2](../docs/system-design.md#82-default-routing-priorities)):

1. **Safety / scope** — narrow or refuse unsafe instructions  
2. **Hard debug signals** — trace, fatal error, crash language → **debug**  
3. **Theory-first** — definitions/comparisons without failing run → **concept**  
4. **Guided work** — stuck on approach, no clear runtime failure → **mentor**  
5. **Tie-break** — theory + failure together → **debug** first; add concept only if clearly prerequisite  

## Handoffs

| From | To | When |
|------|-----|------|
| Debug | Concept | Error is symptom of primitive misunderstanding |
| Concept | Mentor | Moving from “what is it” to “how in my repo” |
| Mentor | Debug | Runtime evidence appears; speculation stops |

## Non-goals (MVP)

- Separate chatbots per mode  
- User-facing “call the Debug agent”  
- Tool policies disconnected from OpenCode’s own guardrails  

The orchestrator picks **prompt structure**, **memory**, **domain rules**, and **hint ceiling**—the user stays in OpenCode.
