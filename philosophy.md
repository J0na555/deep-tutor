# Philosophy

Deep Tutor is a serious engineering experiment: **improve how you think**, not how fast you can paste code. The system behaves like a patient senior developer, mentor, and debugging coach—not like autocomplete, a bulk code generator, or an instant-answer chatbot.

## What we optimize for

- **Reasoning** over output volume  
- **Debugging ability** over “works on my machine” luck  
- **Conceptual models** over syntax memorization  
- **Independent problem solving** over dependency on the model  
- **Long-term growth** over session-by-session throughput  

Teaching is **guided**. The orchestrator and prompts are biased toward questions, constraints, and escalating hints—not toward replacing your cognition.

## Non-negotiables (for builders and users)

1. **Learning over convenience** — If the fastest path is “copy this,” the system should resist until the learning case for disclosure is clear.  
2. **Thinking over generation** — Code may appear at high hint levels or when pedagogy would otherwise collapse; the default is not full solutions.  
3. **Debugging over dependency** — Errors and traces are treated as curriculum: hypothesize, narrow, reproduce, instrument.  
4. **Reflection over memorization** — Mistakes and themes are recorded so you see patterns, not isolated incidents.  
5. **Growth over speed** — Metrics focus on fewer repeated mistakes and calmer debugging—not on maximizing tokens per hour.  

## Anti-goals

The system should **not** slide into:

- A shortcut machine for homework or interviews without understanding  
- Passive autocomplete for daily coding  
- An authoritative oracle for production changes without human review  
- A performance theater (“look how productive I am”) disconnected from real understanding  

If you routinely override constraints and demand full solutions, the design stops working: **the power is in the constraint surface**, not in raw model capability.

## Honesty about limits

- A local LLM is not magic; it can be wrong, overconfident, or narrow.  
- Memory and routing are approximations; they need evaluation and iteration.  
- **Target behavior** in docs may run ahead of what is implemented in this repo; the system design calls that out where relevant.  

## Two places, one habit

- **Deep Tutor project (engine)** — software: orchestrator, memory, prompts, integrations.  
- **Leveling environment** — your personal growth workspace: domains, notes, application projects, reflections, devlogs.  

Domains organize **what you are learning**. Projects are **where you apply it**. Keeping that distinction clear prevents “study” and “shipping” from collapsing into one undifferentiated pile.

## Growth documentation (Git, devlogs, experiments)

The culture around the tool matters:

- **Commits** — small, meaningful units that explain *why* a change exists.  
- **Devlogs** — honest narrative: what you tried, what failed, what you learned.  
- **Reflections** — short, regular synthesis; not performative essays.  
- **Experiments** — bounded hypotheses, recorded outcomes, intentional abandonment when disproven.  

The goal is a truthful record of reasoning over time—not a polished personal brand.

## Summary

Deep Tutor is built for developers who want a **mentor-shaped** local layer: one entrypoint, explicit teaching posture, memory that accumulates, and a workspace that respects the difference between **learning** and **application**. If that sounds restrictive, it is: the restrictions are the pedagogy.
