# Prompt packs

Prompt packs are **inspectable instruction blocks** the orchestrator assembles for OpenCode. They encode teaching posture, hint ceilings, and refusal patterns—not a separate chat UI.

**Canonical design:** [System design §9–10, §13](../docs/system-design.md)

| File | Role |
|------|------|
| [base.md](base.md) | Shared posture and guardrails for every mode |
| [hint-levels.md](hint-levels.md) | Injectable ceiling blocks for levels 1–5 |
| [modes/mentor.md](modes/mentor.md) | Guided problem solving; questions before answers |
| [modes/debug.md](modes/debug.md) | Hypotheses, reproduction, evidence-first debugging |
| [modes/concept.md](modes/concept.md) | Layered intuition → precision → minimal example |

**Hint levels:** [Hint policy](../docs/hint-policy.md) — levels 1–5 apply across all modes.

**Mode selection:** [agents/](../agents/) — routing signals, handoffs, and which pack to load.

**Domain overlays:** [domains/](../domains/) — per-domain rules merged after mode selection.

## Assembly order (target)

1. `base.md`
2. Selected mode pack (`modes/<mode>.md`)
3. Domain rule bundle (`domains/<key>/rules.md`)
4. Hint ceiling block ([hint-levels.md](hint-levels.md) for the current level)
5. Optional memory snippets (orchestrator; not in this directory yet)

Paste or include the concatenated result in your OpenCode agent configuration, or use a preamble script when available.
