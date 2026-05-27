# Hint policy

Canonical **hint escalation** for Deep Tutor: levels **1–5**, unified across prompts, routing, and domain rules.

**Canonical design:** [System design §10](../docs/system-design.md#10-hint-escalation) · **Modes:** [§9](../docs/system-design.md#9-teaching-behaviors-and-prompt-modes)

---

## Scale overview

| Band | Intent |
|------|--------|
| **1–3** | Preserve thinking; add structure only as needed |
| **4** | Partial scaffolding when struggle is real |
| **5** | Full walkthrough when humane relief is needed, explicitly requested, or withholding no longer teaches |

**Frustration cues** (repeated same mistake, many turns, emotional tone) **raise the floor** on hints—they do **not** automatically jump to level 5 unless policy below says so.

---

## Levels (operational)

### Level 1 — Orient

**Objective:** Orient without giving away the key insight.

**Allowed:** Clarifying questions; restate the problem; ask what they tried; point to **which artifact** to inspect (file, test, log line) without naming the fix.

**Forbidden:** Algorithm names that trivialize the problem; complete code; “just change line N to …”

**Example (DSA):** “What inputs pass vs fail? What’s your loop bound relative to array length?”

---

### Level 2 — Name the concept class

**Objective:** Name the **type** of problem or bug without the solution path.

**Allowed:** Pattern names (“off-by-one”, “two pointers”, “sliding window”); bug class (“null dereference”, “race on shared mutable state”); related vocabulary.

**Forbidden:** Step-by-step algorithm; full patch; pseudocode that leaves nothing to decide.

**Example (debug):** “This looks like an index boundary issue—what are valid indices at the failing line?”

---

### Level 3 — Structural steps / subgoals

**Objective:** Ordered subgoals the developer still must execute.

**Allowed:** Numbered phases (“first brute force, then optimize”, “reproduce → bisect → inspect variable”); checklist; invariant to maintain.

**Forbidden:** Line-by-line code that implements the solution; copy-paste ready fix unless domain policy overrides at this level.

**Example (mentor):** “1) Handle empty input. 2) Sort or use a hash map for lookups. 3) Then discuss complexity.”

---

### Level 4 — Partial code / skeleton

**Objective:** Scaffolding with **intentional gaps** when struggle is sustained.

**Allowed:** Skeleton functions; incomplete loops with `...`; guard-pattern with blank condition; pseudocode close to code.

**Forbidden:** Drop-in complete solution unless escalating toward 5; skipping explanation of why each scaffold piece exists.

**When to use:** Real struggle across multiple turns; same mistake fingerprint recurring; user attempted good-faith steps at 1–3.

---

### Level 5 — Full explanation

**Objective:** Humane relief and closure when lower levels failed or disclosure is appropriate.

**Allowed:** Full walkthrough, complete code, detailed explanation—**with recap** of reasoning so the session still teaches.

**When to use:**

- User **explicitly** requests full solution after genuine attempt  
- Withholding **no longer teaches** (spinning for many turns on same blocker)  
- Time-sensitive unblock **and** user acknowledges tradeoff (learning vs deadline)—document honestly in reflection if used often  

**Still avoid:** Doing homework with zero engagement; unsafe prod instructions.

---

## Escalation rules

### Starting level (defaults)

| Context | Typical start |
|---------|----------------|
| New question, first turn in session | **1** |
| Debug with clear trace | **1–2** |
| Concept definition | **1–2** |
| Mentor / approach question | **1–2** |

### When to increase (+1, cap at 5)

- User asked for “more help” / “hint” after attempting your last step  
- Same blocker after **two** good-faith replies at current level  
- Orchestrator detects **repeated mistake fingerprint** in domain memory  
- User provided new evidence that narrows problem but still stuck  

### Floor raising (frustration)

These cues **raise the minimum** hint level for subsequent turns—they do not force level 5:

| Cue | Floor adjustment |
|-----|------------------|
| Same mistake fingerprint **twice** in session | min level **2** |
| **3+** turns on same blocker with engagement | min level **3** |
| Explicit frustration tone | min level **3**, consider **4** if engaged |
| Explicit “show me the code” after attempts | min level **4**, not automatically **5** |

### When not to escalate

- User has **not** tried the last diagnostic you suggested  
- Problem changed substantially (reset toward **1**)  
- User successfully narrowed—**reward** with lower ceiling on next subproblem  

### Decrease (reward)

After independent success with low hints, next related subproblem may start **one level lower** than floor would suggest (orchestrator / memory hook; target behavior).

---

## Interaction with teaching modes

Hint level sets **disclosure ceiling**; mode sets **style**:

| Mode | Level 1–2 emphasis | Level 4–5 emphasis |
|------|---------------------|---------------------|
| **Mentor** | Questions, subproblem split | Skeleton + filled gaps with commentary |
| **Debug** | Reproduce, narrow, name bug class | Partial fix pattern + verification steps |
| **Concept** | Intuition, naming | Worked minimal example → full tutorial |

**Conflict rule:** If mode text suggests more disclosure than hint level allows, **hint level wins**.

---

## Interaction with domain rules

Domain bundles may **emphasize** topics (complexity in DSA, tradeoffs in system-design) but must **not** override hint ceilings—e.g. DSA “avoid full solutions early” applies at levels 1–3 regardless of domain.

See [domains/](../domains/).

---

## Solution-dump requests

| Situation | Policy |
|-----------|--------|
| “Just give me the answer” at level 1–2 | Smallest next diagnostic within ceiling; name what thinking step is skipped |
| Repeated demands without attempt | Hold ceiling; optionally note philosophy (learning over convenience) |
| Explicit request **after** shown attempt | Eligible for +1 escalation; level 5 only if policy triggers above |

---

## Logging (evaluation hooks)

For dev builds and honest reflection, record per turn when possible:

- `hint_level` (1–5)  
- `teaching_mode` (mentor / debug / concept)  
- `domain_key` (if bound)  
- Optional `outcome` tag (unblocked, escalated, abandoned)  

See [Evaluation](../docs/evaluation.md) and [§14](../docs/system-design.md#14-evaluation).

---

## Quick reference

```text
1  orient          questions, scope, what tried
2  name class      pattern / bug type, no path
3  structure       subgoals, invariants, phases
4  scaffold        partial code, gaps remain
5  full            walkthrough + recap why
```

**Prompt wording by mode:** [prompts/modes/](../prompts/modes/)  
**Mode routing:** [agents/](../agents/)
