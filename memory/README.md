# Memory

Boring, inspectable learning state per [system design §11](../docs/system-design.md#11-memory-system).

Default store: `memory/data/learning.sqlite` (gitignored). Override with `memory_db` in [configs/default.json](../configs/default.json) or `DEEP_TUTOR_MEMORY_DB`.

## What it tracks

| Table | Purpose |
|-------|---------|
| `weak_concepts` | Concepts to revisit |

**Routing log (v1):** teach-mode decisions append to `memory/data/routing.jsonl` (gitignored). Disable via `routing_log_enabled: false` in `configs/default.json` or `DEEP_TUTOR_ROUTING_LOG=0`.
| `mistake_fingerprints` | Repeated errors (simple text keys, incrementing count) |
| `solved_topics` | Topics not to over-drill |
| `frustration_cues` | Session-level struggle signals |

Rows are scoped by **domain** (required) and optional **project** key from orchestrator binding.

## CLI

```bash
# Show slice for current cwd binding
./scripts/memory show

# Record learning signals
./scripts/memory mistake "off-by-one loop boundary" --domain dsa
./scripts/memory weak "binary search invariant" --domain dsa --notes "lose left bound"
./scripts/memory solved "two-pointer basics" --domain dsa
./scripts/memory frustration "many turns same bug" --domain dsa
```

The orchestrator injects a formatted slice into [scripts/preamble](../scripts/preamble) output when records exist.
