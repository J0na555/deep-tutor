# Agent spec: Debug

**Mode id:** `debug`  
**Prompt pack:** [prompts/modes/debug.md](../prompts/modes/debug.md)

## Summary

Hypothesis-driven debugging for **stack traces**, **failed tests**, **wrong outputs**, and **crash language** under execution evidence.

## Routing signals (select debug)

| Signal | Examples |
|--------|----------|
| `has_stack_trace` | Python/Java/JS traceback pasted |
| `test_failure` | pytest/jest/cargo test output |
| `wrong_output` | “Expected X got Y” with runnable context |
| `crash_language` | “segfault”, “IndexError”, “500 with trace”, “null pointer” |
| `reproduction_attempt` | User describes steps that reliably fail |

## Do not select when

| Condition | Route to |
|-----------|----------|
| No execution evidence; pure “what is X?” | **concept** |
| Approach question only, no failure | **mentor** |

## Default hint range

- **Start:** 1–2 for new failures (orient, name bug class)  
- **Micro-example (system design):** `IndexError` + two lines → hint **2**: name index/range issue, ask for valid range before patch  
- Raise with repeated same mistake fingerprint in domain memory  

## Worked vignettes

| Situation | Mode | Hint | Action |
|-----------|------|------|--------|
| `IndexError` + snippet | debug | 2 | Ask for index ranges before failing line |
| Service 500 + traceback | debug | 2–3 | Reproduce, narrow layer; optional thin concept if ORM unfamiliar |
| Flaky test, intermittent | debug | 2 | Ask for timing/shared-state hypothesis |

## Handoff to concept

When trace exposes **unfamiliar primitive** (e.g. async ordering, ORM session lifecycle), add a **short concept clause**—then return to narrowing.

## Orchestrator outputs

- `mode: debug`
- `prompt_slice: prompts/modes/debug.md`
- `hint_level: 1–5`
- Optional `secondary: concept` (thin)
