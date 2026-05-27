# Prompts

Prompts encode **teaching posture**, **hint ceilings**, and **refusal patterns**. They align with **prompt modes** (mentor / debug / concept) chosen by the orchestrator—not with user-facing “pick a bot.”

## Artifacts in this repo

| Location | Contents |
|----------|----------|
| [prompts/](../prompts/) | Base posture, mode packs, assembly index |
| [agents/](../agents/) | Mode specs, routing signals, handoffs |
| [domains/](../domains/) | Per-domain rule bundles |
| [Hint policy](hint-policy.md) | Levels 1–5, escalation, frustration floor |

## Canonical sections (system design)

- [Prompting and guardrails](system-design.md#13-prompting-and-guardrails)
- [Hint escalation](system-design.md#10-hint-escalation)
- [Teaching behaviors and prompt modes](system-design.md#9-teaching-behaviors-and-prompt-modes)

**Canonical blueprint:** [System design](system-design.md)
