# Pilot: DSA domain (Workflow A)

End-to-end check that Deep Tutor binds `leveling-arc/domains/dsa`, loads **CONTEXT.md**, and assembles a mentor preamble with **DSA domain rules**.

Canonical workflow: [docs/USAGE_MODEL.md § Workflow A](../../docs/USAGE_MODEL.md#workflow-a--study-inside-a-domain-folder).

## Prerequisites

- Sibling workspace `leveling-arc/` with `domains/` and `projects/` (see `leveling-arc/README.md` next to this repo)
- `leveling-arc/domains/dsa/CONTEXT.md` — curated focus for the pilot

## Smoke test

From `deep-tutor`:

```bash
./scripts/pilot-dsa
```

Exit 0 means binding, curated context, and preamble assembly all match the pilot contract.

## OpenCode integration (recommended)

Install the plugin once, then start OpenCode from this cwd — preamble injection is automatic:

```bash
/path/to/deep-tutor/scripts/opencode-install --target /path/to/leveling-arc
cd /path/to/leveling-arc/domains/dsa
opencode
```

See [integration/opencode](../../integration/opencode/README.md).

## Manual session (fallback)

```bash
cd ../leveling-arc/domains/dsa
/path/to/deep-tutor/scripts/preamble --binding-only   # expect domain: dsa, curated_context: yes
/path/to/deep-tutor/scripts/preamble                  # inspect or paste if plugin not installed
```

## Success signal

More turns on **invariants and complexity** than on copying a final program ([USAGE_MODEL](../../docs/USAGE_MODEL.md)).

## Routing v1 (optional)

Pass the user message so teach mode is selected automatically:

```bash
/path/to/deep-tutor/scripts/preamble -m "IndexError when i goes past len(a)-1"
```

Decisions append to `memory/data/routing.jsonl` for offline review ([system design §11.4](../../docs/system-design.md#114-update-triggers-examples)).

## What this pilot does not cover

- Per-turn hint escalation from session state (hint level is config/default for now)
- Post-turn memory writes from OpenCode session events
