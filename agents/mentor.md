# Agent spec: Mentor

**Mode id:** `mentor`  
**Prompt pack:** [prompts/modes/mentor.md](../prompts/modes/mentor.md)

## Summary

Guided problem solving for **approach choice**, **partial implementations**, and **reasoning gaps** without a crisp runtime error. Default when classification is ambiguous.

## Routing signals (select mentor)

| Signal | Examples |
|--------|----------|
| `partial_code` | Snippet with no traceback; “is this the right approach?” |
| `approach_question` | “How should I structure this?” / “Which data structure?” |
| `stuck_no_error` | “I’m stuck” without stack trace or failing test output |
| `design_in_progress` | Algorithm or module sketch without execution failure |

## Do not select when

| Stronger signal | Route to |
|-----------------|----------|
| Stack trace, assertion failure, wrong output under run | **debug** |
| Pure definition/comparison, no code failure | **concept** |

## Default hint range

- **Start:** 1–2  
- **Raise floor** when frustration cues or repeated similar mistakes (see [hint policy](../docs/hint-policy.md))  
- **Ceiling:** orchestrator sets per turn; mentor rarely needs level 5 unless explicit relief  

## Worked vignette

**Wrong loop boundary, no traceback:** Mentor; hint 1–2; ask for loop invariant or termination argument before suggesting a fix.

## Orchestrator outputs

- `mode: mentor`
- `prompt_slice: prompts/modes/mentor.md`
- `hint_level: 1–5`
- Optional `secondary: concept` when a thin definition would unblock (keep brief)
