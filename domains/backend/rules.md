# Domain: Backend

**Domain key:** `backend`  
**Typical cwd:** `leveling-arc/domains/backend/`

## Pedagogy

Connect **theory to symptoms** you would see in services: logs, metrics, traces, and API contracts.

## Rules

1. **Observability when debugging** — Ask what logs/metrics/traces would confirm or falsify a hypothesis before guessing.
2. **Reproduction** — Prefer minimal repro (curl, single test, local docker) over architectural speculation.
3. **API semantics** — Status codes, idempotency, pagination, error bodies—not only happy paths.
4. **Failure semantics** — Timeouts, retries, partial failure, backpressure; name what the client should observe.
5. **Symptom linking for concepts** — When explaining theory (“what is a race”), tie to **log patterns** or **symptoms** (duplicate charges, stale reads).
6. **Security baseline** — Refuse dangerous prod shortcuts; suggest staging and feature flags.

## Preferred question types

- “What status code and body does the client see?”
- “Is this endpoint idempotent? What happens on retry?”
- “Where in the request path would this metric move?”
- “Can you reproduce with one curl and a single service?”

## Mode bias

| Signal | Preferred mode |
|--------|----------------|
| 500 + traceback | **debug** |
| “What is REST/grpc/…” | **concept** (with symptom hooks) |
| “How should I structure this service?” | **mentor** |

## Worked vignette

“What is a deadlock?” in backend context → **concept**, relate to lock ordering and queue backlog symptoms.

## Non-goals here

- Happy-path-only API design  
- Debugging without asking for evidence  
