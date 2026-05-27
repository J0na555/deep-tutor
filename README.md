# Deep Tutor

Deep Tutor is a **local developer intelligence layer**: orchestration, prompts, and lightweight memory that shape **how** you learn in the terminal. It is **not** a standalone chat app, a replacement IDE, or a code-generation product. It integrates with tools you already use—primarily **[OpenCode](https://opencode.ai)** in the terminal and **local models via Ollama** (e.g. Qwen / DeepSeek-class weights)—so the workflow stays **terminal-native** and **under your control**.

**One-line framing:** *A system designed to improve how developers think.*

---

## Read next

| Doc | What it covers |
|-----|----------------|
| [Philosophy](philosophy.md) | Learning over convenience; thinking over autocomplete; anti-goals |
| [System design](docs/system-design.md) | Canonical blueprint: two environments, stack, orchestrator, memory, MVP |
| [Usage model](docs/USAGE_MODEL.md) | Concrete workflows with OpenCode + leveling layout |

---

## Two environments (critical)

1. **Deep Tutor project** — **This repository.** Prompt packs, orchestrator logic, **lightweight memory** (`memory/`), domain configs, scripts, experiments about pedagogy. It is primarily a **context and learning orchestration system**, not a backend monolith.

2. **Leveling environment** — **Separate workspace** (e.g. sibling repo `leveling-arc/`): `domains/`, `projects/`, `notes/`, `reflections/`, `devlogs/`, `experiments/`. That is where **skill progression and reflection** live. Deep Tutor **operates inside** that layout via folder context and conventions—not inside a bespoke Deep Tutor UI.

Details and diagrams: [System design §3](docs/system-design.md#3-two-environments).

---

## Intended stack

```text
Leveling environment → Deep Tutor context layer → OpenCode CLI → Local LLM (Ollama)
```

See [System design §2](docs/system-design.md#2-system-flow).

---

## Repo intent (target layout)

```text
deep-tutor/
├── prompts/
├── agents/           # Teaching behavior / prompt-mode specs—not autonomous “swarm” agents
├── orchestrator/
├── memory/
├── domains/
├── configs/
├── scripts/
├── experiments/
├── docs/
├── devlogs/
├── philosophy.md
└── README.md
```

Today this repo is mostly **documentation** plus a **minimal orchestrator and memory skeleton**. **Routing v1** classifies utterances into teach modes (`mentor` / `debug` / `concept`) and logs decisions to `memory/data/routing.jsonl`; tighter OpenCode hook integration remains **target** behavior in the system design.

```bash
./scripts/route -m "IndexError on line 5 when I access nums[i]"
./scripts/preamble -m "What is a deadlock?" --cwd ../leveling-arc/domains/backend
```

**DSA pilot (Workflow A):** sibling `leveling-arc/domains/dsa/` with `CONTEXT.md` — run `./scripts/pilot-dsa` to verify binding and preamble assembly; see [experiments/pilot-dsa](experiments/pilot-dsa/README.md).

---

## Culture

Engineering narrative belongs in [devlogs/](devlogs/) and structured tries in [experiments/](experiments/). Honest devlogs beat polished hype—the same posture the tool teaches.
