# OpenCode integration

Deep Tutor injects its assembled preamble into OpenCode sessions automatically via a project plugin. Manual paste (`scripts/preamble`) still works when the plugin is not installed.

**Canonical design:** [System design §5](../docs/system-design.md#5-terminal-stack-opencode-and-ollama), [§15 Integration](../docs/system-design.md#15-mvp-vs-future-scope)

## Quick install (leveling workspace)

From the `deep-tutor` repo:

```bash
./scripts/opencode-install --target ../leveling-arc
```

Then start OpenCode from any directory under the leveling workspace (e.g. `domains/dsa/`). The plugin loads from `.opencode/plugins/deep-tutor.js` and calls `scripts/opencode-hook` before each model turn.

## What gets injected

On each LLM call, OpenCode runs the orchestrator for the session cwd:

1. **Context binding** — domain/project from path or flags  
2. **Routing v1** (when a user message is available) — mentor / debug / concept  
3. **Preamble assembly** — base + mode + domain rules + hint level + memory slice  

The result is appended to OpenCode’s system prompt (same text as `scripts/preamble`).

## Configuration

| Variable | Purpose |
|----------|---------|
| `DEEP_TUTOR_ROOT` | Force path to this repo when auto-detect fails |
| `DEEP_TUTOR_OPENCODE=0` | Disable injection for one session |
| `DEEP_TUTOR_LEVELING_ROOT` | Leveling workspace (also in `configs/default.json`) |
| `DEEP_TUTOR_MESSAGE` | Used by `opencode-hook` when invoked from the plugin |

## Manual / debugging

```bash
# Same JSON the plugin consumes
./scripts/opencode-hook --cwd ../leveling-arc/domains/dsa -m "What is two-pointer?"

# Human-readable preamble (unchanged)
./scripts/preamble --cwd ../leveling-arc/domains/dsa -m "IndexError on nums[i]"
```

## Global install

```bash
./scripts/opencode-install --global
```

Installs the plugin to `~/.config/opencode/plugins/deep-tutor.js`. Set `DEEP_TUTOR_ROOT` in your shell profile so every OpenCode session can find this repo.

## Disable

- Per session: `DEEP_TUTOR_OPENCODE=0 opencode`
- Per workspace: remove `.opencode/plugins/deep-tutor.js`
