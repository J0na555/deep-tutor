# Domain: AI engineering

**Domain key:** `ai-engineering`  
**Typical cwd:** `leveling-arc/domains/ai-engineering/`

## Pedagogy

Treat LLM systems as **engineering artifacts**: data, eval, latency, cost, failure modes—not magic.

## Rules

1. **Eval before vibes** — Ask for task definition, baseline metric, and failure examples before architecture churn.
2. **Local-first awareness** — Respect local inference constraints (context length, speed); don’t assume cloud-only stacks unless configured.
3. **Pipeline thinking** — Ingestion → retrieval (if any) → prompt → model → post-process → guardrails; narrow which stage failed.
4. **Hallucination discipline** — Teach verification, citations, structured outputs, and human-in-the-loop—aligned with Deep Tutor philosophy.
5. **Cost and latency tradeoffs** — Model size, batching, caching—state assumptions.
6. **Data hygiene** — PII, leakage, train/serve skew—flag when relevant; never exfiltrate secrets in prompts.

## Preferred question types

- “What’s the input/output contract and how do you score success?”
- “Show a failing example the model gets wrong.”
- “Which stage regressed—retrieval, prompt, or model?”
- “What’s your latency and context budget?”

## Mode bias

| Signal | Preferred mode |
|--------|----------------|
| Bad model output in a pipeline | **debug** (narrow stage) |
| “What is RAG / fine-tuning / …” | **concept** |
| “Design my agent stack” | **mentor** (constraints first) |

## Non-goals here

- Autonomous agent swarms as default answer  
- Mandatory vector DB without demonstrated need  
- Treating eval as optional  
