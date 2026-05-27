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

## Manual session (Workflow A)

```bash
cd ../leveling-arc/domains/dsa
/path/to/deep-tutor/scripts/preamble --binding-only   # expect domain: dsa, curated_context: yes
/path/to/deep-tutor/scripts/preamble                  # paste into OpenCode
# start OpenCode in this cwd, ask a problem; composed instructions bias toward DSA pedagogy
```

## Success signal

More turns on **invariants and complexity** than on copying a final program ([USAGE_MODEL](../../docs/USAGE_MODEL.md)).

## What this pilot does not cover

- OpenCode agent hook automation (paste preamble manually for MVP)
- Routing v1 / teach-mode auto-selection (Phase 2)
