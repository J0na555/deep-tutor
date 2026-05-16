# Philosophy

Deep Tutor is a **serious engineering experiment** in **learning systems**, not a consumer AI product pitch. It exists to answer one question with discipline: **does this setup make you a clearer thinker over months?**

**Core statement:** Deep Tutor is **a system designed to improve how developers think.**

---

## What we optimize for

- **Learning** over convenience  
- **Thinking** over autocomplete  
- **Debugging** over dependency on the model  
- **Guidance** over solution dumping  
- **Growth** over speed  

The terminal integration (OpenCode + local models) is there so the loop stays **close to real work**—not so you can maximize tokens per hour.

---

## What Deep Tutor must resist becoming

The design intentionally pushes back against:

- **Passive autocomplete** — answers appearing without diagnosis  
- **Answer machines** — completing homework or interviews without understanding  
- **Shortcut tools** — replacing cognition when a smaller step would teach more  

If you routinely fight the constraints and demand full solutions, the architecture stops helping: **the pedagogy lives in the constraint surface**, not in raw model horsepower.

---

## Non-negotiables

1. **Learning over convenience** — If the fastest path is “paste this,” the system should resist until the case for disclosure is clear.  
2. **Thinking over generation** — Code may appear at higher hint levels or when withholding collapses learning; the default is not wholesale solutions.  
3. **Debugging over dependency** — Traces and errors are curriculum: hypothesize, narrow, reproduce, instrument.  
4. **Reflection over memorization** — Mistakes and themes are recorded so patterns emerge across sessions.  
5. **Growth over speed** — Prefer fewer repeated mistakes and calmer debugging over throughput theater.  

---

## Honesty about limits

- A **local LLM** can be wrong, overconfident, or shallow on niche topics. **You** remain responsible for verification.  
- **Memory and routing** are approximate; they need iteration and honest evaluation—not faith.  
- Docs may describe **target behavior** ahead of code in this repo; see [System design](docs/system-design.md).  

---

## Two places, one habit

- **Deep Tutor project** — Intelligence layer: orchestrator, prompts, memory, configs (this repository).  
- **Leveling environment** — my **developer growth workspace**: domains of study, application projects, notes, reflections, devlogs.  

**Domains** organize **what i learn**. **Projects** organize **where i ship**. Keeping that split preserves sane mental models when the same keyword (e.g. “caching”) appears in theory drills and in production code.

---

## Growth documentation (Git, devlogs, experiments)

The culture around the tool is part of the system:

- **Commits** — Explain *why*; avoid churn for graphs.  
- **Devlogs** — What you tried, what failed, what you learned—without performance theater.  
- **Reflections** — Short synthesis after hard sessions.  
- **Experiments** — Bounded hypotheses; abandoning a bad idea is a successful outcome.  

The goal is a **truthful record of reasoning over time**, not a personal brand kit.

---

## Summary

Deep Tutor is for developers who want a **mentor-shaped layer** in the terminal: **OpenCode** (or equivalent) for execution, **Ollama** for local inference, and **Deep Tutor** for **teaching posture**, **memory**, and **domain-aware rules**. The stance is reflective, systems-oriented, and grounded—closer to a careful experiment than to “AGI tutor” marketing.
