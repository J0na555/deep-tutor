# 🧠 Deep Tutor — What You're Actually Building

At its core, this is NOT "an AI app".

It's a **local learning operating layer for you as a developer**.

Think of it like:

> A personal coding mentor that sits between you and everything you try to learn.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🧩 The Big Picture (Simple Mental Model)

Your system has 3 main layers:

```text
USER (you)
   ↓
Deep Tutor Orchestrator (The Brain)
   ↓
Specialized Agents (Thinking Styles)
   ↓
Local LLM (Qwen / DeepSeek via Ollama)
```

But the key idea is:

> You don't talk to agents directly. You talk to ONE system.

The orchestrator handles everything.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🧠 1. The Orchestrator (The Brain)

This is the most important part.

It acts like:

> "A senior developer deciding how to teach you this problem."

## What it does:

When you ask something, it:

### 1. Understands the request

* Is this debugging?
* Is this theory?
* Is this practice?
* Is this confusion?

### 2. Checks your memory

It looks at:

* what you already know
* what you struggle with
* past mistakes
* similar topics you failed before

### 3. Chooses the right agent

It routes your question:

```text
error → Debug Agent
concept → Concept Agent
confused code → Mentor Agent
```

### 4. Decides HOW to respond

It chooses:

* hint level (1–5)
* difficulty adjustment
* whether to push or guide

### 5. Builds the final prompt

It combines:

* your question
* memory context
* agent rules
* hint level constraints

Then sends it to the local LLM.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 👥 2. Agents (Thinking Styles, Not Independent Systems)

Agents are NOT independent AI systems.

They are just **different "thinking styles" inside the same system**.

The orchestrator selects which style to apply.

### 🧑‍🏫 Mentor Agent (Default Teacher)

This is your main learning mode.

**Job:**
* guide thinking
* ask questions
* avoid full solutions
* force reasoning

**Behavior:**
> "A strict senior dev sitting next to you"

### 🐛 Debug Agent (Problem Hunter)

Triggered when things break.

**Job:**
* analyze errors
* interpret stack traces
* isolate problems
* guide debugging steps

**Behavior:**
> doesn't fix your code — makes you find the bug

### 🧠 Concept Agent (Explainer)

Triggered for theory.

**Job:**
* explain concepts clearly
* give mental models
* connect ideas together

**Behavior:**
> teaches "why it works", not "how to code it"

### (Later) Other Agents

You don't start with these, but you *will* add them:

* **DSA Agent** → problem solving patterns
* **Code Review Agent** → architecture feedback
* **Reflection Agent** → learning review after solving

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🔁 3. How a Request Actually Flows

This is the real system behavior:

```text
You (via terminal):
"Why is my loop skipping elements?"

↓

Orchestrator:
- detects: logic issue + possible debugging
- reads folder context: ~/projects/leetcode
- checks memory: you struggled with loops before

↓

Routes request to:
Debug Agent (thinking style)

↓

Debug Agent applies rules:
- asks guiding questions
- avoids direct fixes

↓

Orchestrator applies:
- hint level (based on past attempts)
- difficulty adjustment

↓

Final response:
hint + question + direction

↓

Memory updated:
- folder: leetcode
- topic: loops
- mistake: boundary error
- hint level used: 2
- context: array indexing
```

That's the full loop.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🧠 4. Memory System (Your Learning Brain)

This is what makes it personal.

It stores your evolution over time.

### What it remembers:

**📌 Concept mastery (per folder context)**
* recursion: weak
* loops: improving
* APIs: new

**📌 Mistakes you repeat**
* off-by-one errors
* forgetting base cases
* bad variable naming

**📌 Learning behavior**
* how often you ask for help
* how long you struggle per topic
* what confuses you most

### Why this matters:

The system can say things like:

> "You made this same mistake in recursion 3 days ago, and in this project too."

That's where it becomes powerful.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 📂 5. Folder-Based Context (VERY IMPORTANT)

This is a key idea — and it's core to the system.

You don't use it like a chat app.

You use it like:

```bash
deep-tutor ~/projects/leetcode
deep-tutor ~/projects/springboot-app
deep-tutor ~/projects/django-api
```

### What happens:

The system:

* detects the folder context
* reads project type (LeetCode, Django, Flask, etc.)
* adjusts teaching style
* adapts agent selection
* scopes memory to that project

### Example:

**In LeetCode folder:**
* DSA Agent more active
* strict hinting
* pattern recognition focus

**In Django project:**
* Concept + Debug agents
* architecture focus
* backend patterns

**In random scripts:**
* Mentor agent dominates
* general guidance

So yes — same system, different learning context per folder.

That's powerful.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🎯 6. The Real Purpose

This system is NOT:

* a chatbot
* a code generator
* an assistant

It is:

> a learning loop that forces you to think like a developer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🔥 What Makes This Actually Good

Most AI tools:

* give answers → reduce thinking → create dependency

Your system:

* delays answers
* increases thinking
* builds independence
* tracks weakness
* adapts difficulty
* remembers context

That's the difference.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# ⚠️ One Reality Check (Important)

This system only works if:

> YOU enforce the "no easy answer" rule.

If you break that rule and let it become a shortcut tool, it stops working.

The power is in the constraints, not the features.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🧭 Final Mental Model

If you want the cleanest understanding:

```text
Deep Tutor = Learning Operating System

Orchestrator = decision maker
Agents = teaching styles (not user-facing)
Memory = your brain history (scoped per folder)
LLM = execution engine (Qwen via Ollama)
Terminal CLI = interface (open code integration)
Folders = context environment
```

The system doesn't feel like "using AI".

It feels like "having a good mentor in your terminal".
