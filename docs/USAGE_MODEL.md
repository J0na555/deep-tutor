# Usage model

Deep Tutor’s **usage model** is **terminal-native**: you keep working in **OpenCode** with **local models (Ollama)**. Deep Tutor supplies **policies, prompts, and memory**—not a second chat application.

**Canonical details:** [System design](system-design.md) · **Folder context:** [§12 Folder and domain context](system-design.md#12-folder-and-domain-context) · **Lifecycle:** [§7 Request lifecycle](system-design.md#7-request-lifecycle)

---

## Daily mental model

1. Open a terminal session in the **place that matches intent** (domain drill vs application project).  
2. Start **OpenCode** from that directory (or attach the workspace you use in practice).  
3. Let **path context** imply **domain rules** (see system design)—or pass an explicit domain hint when ambiguous.  
4. Treat Deep Tutor artifacts as **inspectable inputs** to the session: preamble text, included rule files, memory snippets—not magic background state you cannot see.

---

## Workflow A — Study inside a domain folder

**Goal:** Algorithms practice with **DSA-style** pedagogy (reasoning first, complexity discussion, no instant full solutions).

**Setup:**

- Work inside `leveling-arc/domains/dsa/` (or your equivalent).  
- Keep a short `README.md` or `CONTEXT.md` listing current focus and conventions—something the orchestrator can prefer over raw scratch files (**target**).  

**Session:**

1. `cd ~/work/leveling-arc/domains/dsa`  
2. Launch OpenCode from this cwd.  
3. (**Target**) Run or paste Deep Tutor’s **domain preamble** for `dsa`—rules such as: brute-force baseline encouraged before polish; ask for complexity; avoid dumping full solutions at low hint levels.  
4. Ask your question as you naturally would in OpenCode; the **composed instructions** bias the model toward mentor/debug/concept behaviors per orchestrator policy—not a separate UI.

**Success signal:** you spend more turns on **invariants and complexity** than on copying a final program.

---

## Workflow B — System design study

**Goal:** Discuss tradeoffs and comparisons without false certainty.

**Setup:**

- Work in `leveling-arc/domains/system-design/`.  
- Optionally maintain notes that link problems you’ve already explored (“rate limiting variants,” “cache coherence vs latency”).  

**Session:**

1. cwd under `domains/system-design/`.  
2. (**Target**) Inject Deep Tutor rules emphasizing **tradeoffs**, **failure modes**, and **comparison** rather than single “correct” architectures.  
3. Use OpenCode to sketch diagrams in markdown or to critique your own bullets—the agent loop stays OpenCode; the **stance** comes from Deep Tutor prompts.

**Success signal:** answers routinely expose **constraints** (“under high partition risk…” / “if your SLA is …”) instead of cookie-cutter blueprints.

---

## Workflow C — Application project (shipping context)

**Goal:** Debug and implement under **real** constraints; still avoid turning the model into a blind codegen oracle.

**Setup:**

- cwd in `leveling-arc/projects/<app>/` or a standalone repo you treat as application work.  
- (**Target**) Separate **project memory** (recurring defects, flaky test themes) from **domain memory** (theoretical gaps).

**Session:**

1. Reproduce the bug or failed test **before** leaning on hints—matches Debug-oriented teaching behavior.  
2. Paste traceback + minimal snippet through OpenCode as you already would.  
3. (**Target**) Orchestrator selects **debug-heavy** prompt structure; memory surfaces prior related mistakes (“third `NoneType` this month”) without preempting your hypothesis.

**Success signal:** faster **narrowing** (what variable at crash?) rather than faster **paste of a patch you don’t understand**.

---

## Workflow D — Explicit domain override

**Goal:** Stay flexible when cwd is ambiguous (symlinks, monorepos, jumping between trees).

**Practice:**

- (**Target**) Support flags or env vars understood by your orchestrator script: e.g. “treat as `dsa` even though cwd is `notes/`.”  
- Document your personal convention in **`leveling-arc/README.md`** so future-you does not rely on memory.

---

## Memory hygiene (MVP-friendly)

- Append **one-line mistake fingerprints** after sour sessions—structured enough to grep, light enough to maintain.  
- Periodically mark topics **solved** so prompts do not re-litigate basics without cause.  
- Prefer **curated** notes over dumping entire directories into context—noise degrades local models fast.

Full framing: [Memory system](system-design.md#11-memory-system).

---

## What not to do

- Don’t maintain a parallel “Deep Tutor chat” as the source of truth—**OpenCode stays the interface**.  
- Don’t expand memory into **vector+RAG** because it sounds impressive; grow storage **when simple files stop working**.  
- Don’t pretend teaching behaviors are **autonomous coworkers**; they are **prompt modes** selected by policy ([§9](system-design.md#9-teaching-behaviors-and-prompt-modes)).

---

## Philosophy

[Philosophy](../philosophy.md)
