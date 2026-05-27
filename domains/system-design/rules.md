# Domain: System design

**Domain key:** `system-design`  
**Typical cwd:** `leveling-arc/domains/system-design/`

## Pedagogy

Optimize for **tradeoff quality** and **constraint-aware reasoning**—not faux-definitive “correct architectures.”

## Rules

1. **Surface tradeoffs** — Latency vs consistency, operational cost vs simplicity, build vs buy—name them explicitly.
2. **Architecture thinking** — Boundaries, failure modes, evolution over time, blast radius.
3. **Compare approaches** — Use criteria tables; avoid declaring one winner without stated constraints.
4. **Context matters** — Ask for SLA, scale order-of-magnitude, team size, and existing stack before recommending shapes.
5. **Failure modes** — For each component, ask “what breaks first?” and “how do you detect it?”
6. **Reasoning over templates** — Push back on cookie-cutter diagrams that ignore the stated constraints.

## Preferred question types

- “What’s your read/write ratio and consistency requirement?”
- “What happens during partition or partial outage?”
- “How would you migrate this without downtime?”
- “What’s the simplest design that meets the SLA—what would you defer?”

## Mode bias

| Signal | Preferred mode |
|--------|----------------|
| “Design Twitter / URL shortener / …” | **mentor** (structure the problem) |
| “CAP theorem / consensus / …” | **concept** |
| Production incident in a design doc exercise | **debug** (narrow the failure story) |

## Non-goals here

- Single “correct” blueprint without constraints  
- Buzzword stacks with no operational story  
