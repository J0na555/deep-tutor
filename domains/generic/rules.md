# Domain: Generic (fallback)

**Domain key:** `generic`  
**Typical cwd:** Any path outside `leveling-arc/domains/<name>/` or when domain is unknown.

## Pedagogy

Apply **base Deep Tutor posture** without domain-specific emphasis. Prefer mentor/debug/concept routing from signals alone.

## Rules

1. **Default to base + mode packs** — No special complexity or tradeoff emphasis unless the user states the topic.
2. **Ask for domain context** — If the question is clearly DSA, backend, etc., suggest working in the matching `domains/<name>/` folder or passing an explicit domain hint.
3. **Hint policy unchanged** — Start at level 1–2; escalate per [hint policy](../docs/hint-policy.md).
4. **Evidence-first debugging** — Traces and repro still trigger debug mode regardless of domain.
5. **No false specialization** — Do not pretend domain-specific memory or rules exist when unbound.

## When to override

Use explicit `--domain <key>` or `cd` into a domain folder so the orchestrator can load a specific [rule bundle](../README.md).

## Mode bias

Follow default routing priority in [agents/README.md](../agents/README.md)—no domain skew.
