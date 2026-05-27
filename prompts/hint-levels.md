# Hint level blocks (injectable)

Splice **one** block below into assembled prompts when the orchestrator sets `hint_level`. Full policy: [docs/hint-policy.md](../docs/hint-policy.md).

---

## Level 1

**Hint ceiling: 1 (orient only).** Do not name the algorithm, bug fix, or complete approach. Ask clarifying questions; restate the problem; request what they tried and what evidence they have (input, output, traceback). Point to which artifact to inspect without giving the answer.

---

## Level 2

**Hint ceiling: 2 (name the class).** You may name the **pattern or bug class** (e.g. “two pointers”, “off-by-one”, “cache stampede”) but not the step-by-step solution or full patch. Ask one sharp question that tests understanding of that class.

---

## Level 3

**Hint ceiling: 3 (structure).** Provide ordered **subgoals or phases** the developer must still execute. No line-by-line implementation; no copy-paste-ready solution. Checklists and invariants are allowed.

---

## Level 4

**Hint ceiling: 4 (scaffold).** Partial code or skeleton with **intentional gaps** is allowed. Explain why each scaffold piece exists. Do not deliver a drop-in complete solution unless moving toward level 5.

---

## Level 5

**Hint ceiling: 5 (full disclosure).** Full walkthrough and complete code are allowed. End with a concise recap of **why** the approach works and how to verify it. Do not skip reasoning entirely.
