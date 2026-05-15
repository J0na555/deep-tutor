# Deep Tutor

Deep Tutor is a **local developer growth system**: an orchestrated teaching layer that prioritizes reasoning, debugging, and long-term learning over instant answers. It is designed to run as software you control (local LLM, local memory), with a strict separation between the **engine** (this repository) and your **leveling workspace** (where domains, notes, and application projects live).

- **[Philosophy](philosophy.md)** — non-negotiables, anti-goals, and how the system is meant to be used.
- **[System design](docs/system-design.md)** — canonical blueprint: two environments, orchestration, agents, memory, lifecycle, guardrails, evaluation, MVP vs future.

**Engine vs leveling:** This repo is the **Deep Tutor project** (orchestrator, agent modes, prompts, memory implementation, APIs). The **leveling environment** is a separate workspace (e.g. sibling directory `leveling-arc/`) where you structure learning domains, reflections, devlogs, and experiments. The orchestrator is intended to consume context from that workspace; details are in the system design document.

For day-to-day usage patterns (terminal session, folder context), see [Usage model](docs/USAGE_MODEL.md) (stub → [System design §15](docs/system-design.md#15-usage-and-session-model)).

Development narratives belong in [devlogs/](devlogs/) and structured tries in [experiments/](experiments/).
