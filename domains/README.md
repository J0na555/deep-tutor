# Domain rule bundles

Default **domain rule packs** checked into Deep Tutor. The orchestrator loads `domains/<key>/rules.md` when cwd resolves under `leveling-arc/domains/<key>/` (or via explicit `--domain` flag).

**Canonical examples:** [System design §8.3](../docs/system-design.md#83-domain-rule-examples-realistic)

| Domain key | Path | Focus |
|------------|------|-------|
| `dsa` | [dsa/rules.md](dsa/rules.md) | Algorithms, complexity, reasoning first |
| `system-design` | [system-design/rules.md](system-design/rules.md) | Tradeoffs, failure modes, comparisons |
| `backend` | [backend/rules.md](backend/rules.md) | Services, APIs, observability |
| `databases` | [databases/rules.md](databases/rules.md) | Queries, indexing, modeling |
| `linux` | [linux/rules.md](linux/rules.md) | Shell, permissions, processes |
| `ai-engineering` | [ai-engineering/rules.md](ai-engineering/rules.md) | Pipelines, eval, local models |
| *(fallback)* | [generic/rules.md](generic/rules.md) | Ambiguous cwd or unrelated repos |

## Overrides in leveling

You may copy or extend a bundle in your leveling workspace (e.g. `leveling-arc/domains/dsa/RULES.md`). **Target behavior:** orchestrator prefers leveling overrides when present; these files are portable defaults.

## Hint policy

Domain rules set **emphasis**, not disclosure ceiling. Always respect [hint policy](../docs/hint-policy.md).
