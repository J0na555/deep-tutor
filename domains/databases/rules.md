# Domain: Databases

**Domain key:** `databases`  
**Typical cwd:** `leveling-arc/domains/databases/`

## Pedagogy

Ground answers in **access patterns**, **execution shape**, and **observable query behavior**—not abstract normalization debates alone.

## Rules

1. **Query issues: execution first** — Ask for `EXPLAIN` / plan shape, row counts, and indexes before rewriting SQL.
2. **Indexing reasoning** — Which predicates are selective? What’s the read/write mix?
3. **Modeling: access patterns first** — Normalize/denormalize discussion tied to **actual queries**, not textbook purity.
4. **Transactions and isolation** — When anomalies appear, name isolation level and symptom (phantom read, lost update).
5. **Migrations and ops** — Lock duration, backfill strategy, rollback—when schema changes come up.
6. **Minimal repro** — Sample schema + query + plan beats generic advice.

## Preferred question types

- “What does the planner show for this query?”
- “Which columns are in the WHERE and JOIN clauses?”
- “Read-heavy or write-heavy? Any hot keys?”
- “What anomaly are you seeing—duplicate rows, stale read, deadlock?”

## Mode bias

| Signal | Preferred mode |
|--------|----------------|
| Slow query / wrong result | **debug** |
| “B-tree vs hash index / normalization / …” | **concept** |
| Schema design for a feature | **mentor** |

## Non-goals here

- Rewriting SQL without plan or schema context  
- Generic “use NoSQL” without access-pattern analysis
