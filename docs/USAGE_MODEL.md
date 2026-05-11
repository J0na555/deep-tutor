# Deep Tutor Usage Model

How to use Deep Tutor in practice. This is the actual workflow and interaction pattern.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Terminal-Based Interface (Open Code Integration)

Deep Tutor is a **terminal-first system** using the Open Code interface.

## Basic Usage

```bash
deep-tutor ~/projects/leetcode
```

This spawns an interactive mentor session in the terminal within that folder context.

## How It Works

When you start a session in a folder:

1. **Folder detection**: System reads the folder path
2. **Project type inference**: Determines if it's LeetCode, Django, Flask, raw scripts, etc.
3. **Memory loading**: Loads both global + folder-scoped memory
4. **Session init**: Sets up the orchestrator for this context
5. **Interactive loop**: You can ask questions; orchestrator responds

## Example Interaction

```
$ deep-tutor ~/projects/leetcode
Welcome to Deep Tutor (LeetCode context)
Your global skill level: Intermediate
Topics in this folder: recursion (weak), dynamic_programming (improving), arrays (strong)

> Why is my recursion timing out?

Orchestrator analysis:
- Request type: debugging + performance
- Memory: You struggled with recursion base cases 3 days ago
- Folder context: Pattern recognition problems common here
- Agent: Debug Agent
- Hint level: 2 (based on 4 previous attempts on recursion)

Debug Agent response:
"Have you verified that every recursive call is actually progressing toward the base case?
Let me ask: what's the value of N when your recursion times out?"

> I think N is still 100 because...

Orchestrator:
- Tracks this interaction
- Updates recursion mastery in LeetCode folder
- Logs mistake pattern
- Adjusts hint level for next interaction
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Folder-Based Context Detection

The system infers project type from folder structure.

## How Detection Works

```
~/projects/leetcode/
  └── solution.py
  └── .leetcode_meta
  └── notes.md

→ Detected as: LeetCode DSA practice
→ Agent focus: DSA Agent (once available)
→ Teaching style: strict hinting, pattern recognition
→ Memory scoping: DSA-specific topics
```

## Supported Project Types (MVP + Later)

### LeetCode (DSA Practice)
```
~/projects/leetcode/
Triggers: DSA Agent (post-MVP)
Focus: pattern recognition, optimization
Memory: problem types, algorithm mastery, performance benchmarks
```

### Django / Flask (Backend Web)
```
~/projects/django-app/
Triggers: Concept + Debug agents
Focus: architecture, ORM, request handling
Memory: framework patterns, common errors, API design
```

### React / Next.js (Frontend)
```
~/projects/react-app/
Triggers: Mentor + Concept agents
Focus: component patterns, state management, hooks
Memory: React-specific patterns, performance issues
```

### Raw Scripts / Experiments
```
~/projects/scripts/
Triggers: Mentor Agent (default)
Focus: general problem-solving
Memory: script-specific topics
```

### Generic / Unrecognized
```
~/projects/my-app/
Triggers: Mentor Agent (default)
Focus: general guidance
Memory: generic topic tracking
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Request Flow with Folder Context

Here's what happens when you ask a question:

```
1. USER INPUT (in ~/projects/django-app/)
   "Why does my query return an empty list?"

2. ORCHESTRATOR READS CONTEXT
   - Folder: ~/projects/django-app/
   - Project type: Django
   - Folder memory: "You made a similar mistake with querysets 2 weeks ago"
   - Global memory: "Your Django skills: intermediate"

3. REQUEST CLASSIFICATION
   - Type: debugging + database query
   - Context: backend/ORM
   - Is it a common mistake? YES (querysets returning empty lists)

4. AGENT SELECTION
   - Primary: Debug Agent (runtime behavior)
   - Secondary: Concept Agent (if ORM clarification needed)

5. HINT LEVEL DECISION
   - You've asked 3 questions on querysets this session
   - Hint level 1 used 2x, didn't help
   - → Hint level 2

6. PROMPT CONSTRUCTION
   Includes:
   - Debug Agent rules
   - Django-specific patterns
   - Your folder-scoped memory (querysets)
   - Your global memory (ORM understanding)
   - Hint level 2 constraints

7. LLM CALL
   Local model (Qwen via Ollama) generates response

8. RESPONSE
   "Have you printed the query before `.all()`? 
    What does `print(MyModel.objects.filter(...).query)` show?"

9. MEMORY UPDATE
   - Session: logged querysets question
   - Folder memory: querysets + 1 attempt
   - If solved: mastery_score increases
   - If not: frustration_score tracked
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Memory Scoping Behavior

## How Memory Works Across Folders

### Scenario 1: Same Topic, Different Folders

```
Monday:
$ deep-tutor ~/projects/leetcode
> How do I optimize a recursive solution?
[Mastery recorded in leetcode folder: recursion = 40]
[Global mastery: recursion = 40]

Wednesday:
$ deep-tutor ~/projects/django-app
> How does recursion work in this ORM context?

Orchestrator sees:
- Global recursion mastery: 40 (you struggled with it)
- Folder recursion mastery: NEW (this is first time in Django context)
- Recommendation: adjust hints based on global knowledge, 
  but also explore Django-specific recursion (different context!)
```

### Scenario 2: Same Mistake Pattern, Different Projects

```
LeetCode folder:
"off-by-one error in array loop" (recorded 3 times)

Django folder:
"off-by-one error in pagination logic" (recorded 2 times)

Global memory sees:
- You're repeatedly making off-by-one errors (6 total)
- Pattern: boundary conditions are your weakness

Hint level escalation applies globally.
```

### Scenario 3: Session Within Same Folder

```
$ deep-tutor ~/projects/leetcode
[Session starts, hint level 1]

Question 1: hint level 1
Question 2: hint level 1 (still working well)
Question 3: hint level 2 (showing frustration)
Question 4: hint level 2 (adjusted based on session context)

[Session ends]
[All memory updated: folder + global]
[Next session in same folder uses learned level as baseline]
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Typical Workflows

## Workflow 1: LeetCode DSA Practice (MVP Focus)

```bash
$ deep-tutor ~/projects/leetcode

You: I can't figure out the optimal way to solve this

Mentor: Let's think about this step by step.
        What's the time complexity of your current approach?

You: O(n^2), I think?

Mentor: That's right. For this problem, can you achieve better?
        What information does the problem give you that you're not using?

[You think, experiment, solve]

Mentor: Good! You solved it with O(n log n).
        Now, why does this approach work?
```

Folder memory updated:
- "pattern: sorting + binary search" mastered
- "time complexity analysis: improving"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Workflow 2: Django Project (Post-MVP Multi-Agent)

```bash
$ deep-tutor ~/projects/django-api

You: My API endpoint is returning 500 errors

Mentor (detects error): Let's debug this.
                        What does your error log say?

You: AttributeError: NoneType has no attribute 'id'

Debug Agent (routes to debug): Let me help you trace this.
                               Which line is the error on?

You: Line 42: return User.objects.get(username=name).id

Debug Agent: Ah, what could make `.get()` return None?
             How does your code handle that case?

Concept Agent (if needed): By the way, `.get()` vs `.filter()` 
                           differ in how they handle missing objects.
```

Folder memory updated:
- "Django ORM error handling: weak"
- "NoneType errors: pattern recognized"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Workflow 3: Concept Questions (Concept Agent)

```bash
$ deep-tutor ~/projects/django-api

You: What's the difference between a class and an instance?

Concept Agent (routes to concept): Great question.
                                   Think of a class as a blueprint.

Mentor (guides to application): In your Django models, 
                                what's the class? What's an instance?

You: The class is the User model?

Concept Agent: Right! And what's an instance?

You: A specific user in the database?

Concept Agent: Exactly. Each row in your users table 
               is a different instance of the User class.
```

Folder memory updated:
- "OOP concepts: improving"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Open Code Integration

Deep Tutor integrates with Open Code for **terminal interactivity**.

## Why Terminal-First?

1. **Context-aware**: Can read folder structure automatically
2. **Lightweight**: No web UI overhead
3. **Fast iteration**: Type questions, get answers immediately
4. **Memory integration**: Can read your code files if needed (later)
5. **Integrated workflow**: Mentor stays in your terminal

## Open Code Features Used

- **stdin/stdout**: Interactive question/answer loop
- **File reading**: Access to code context (if enabled)
- **Environment**: Detects project folder, Python version, etc.
- **Process management**: Session lifecycle

Example terminal session:

```bash
$ deep-tutor ~/projects/leetcode

Deep Tutor (LeetCode Context)
Loaded folder memory: 23 sessions, 5 weak topics

> What's wrong with my binary search?

[Orchestrator processes]
[Debug Agent generates response]

Mentor: What does your algorithm do when the target
        is not in the array?

> It returns -1

Mentor: Good! Is that what your code actually does?

> [user checks code]
> Actually, I think it might return None

Mentor: Ah! Could that be causing issues with your
        test assertions?

> Oh! Yes! That's the bug!

[Session ends]
[Memory saved: binary_search topic, bug_type: type_mismatch]

$ 
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Advanced Features (Post-MVP)

## Code Reading Integration

Once available, Deep Tutor can:

```bash
$ deep-tutor ~/projects/django-api

> Fix my serializer bug

Orchestrator can:
1. Read your serializer code
2. Identify the issue
3. Guide you to the fix (not give it directly)
4. Reference specific lines
```

## Project Structure Analysis

```bash
$ deep-tutor ~/projects/leetcode

Orchestrator auto-detects:
- Problem difficulty patterns
- Your success rate per problem type
- Time spent per category
- Common stumbling points
```

## Spaced Repetition Integration

```bash
$ deep-tutor ~/projects/leetcode

> [user solves a problem]

Orchestrator:
"You solved this 5 days ago. Let's revisit it.
 Can you solve it again without looking at your solution?"
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Rules & Constraints

## For Users

1. **No easy outs**: System is designed to resist shortcut requests
   - Asking "just tell me the answer" → guided to think instead
   
2. **Embrace hints**: Hints are deliberate; trust the process
   - Hint level 1 = think independently
   - Hint level 5 = system believes learning value is low

3. **Folder = context**: Switch folders = switch learning context
   - LeetCode folder for DSA practice
   - Django folder for framework learning
   - Different memory, different teaching style

## For the System

1. **Never give full solutions** (unless hint level 5 + multiple failures)
2. **Always reference memory** when making decisions
3. **Adapt to folder context** in agent selection + teaching style
4. **Track all interactions** for long-term learning patterns
5. **Escalate carefully**: frustration is a signal, not a reason to give up

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# Mental Model: Why This Works

Deep Tutor works because:

1. **Folder = contract** → You go to LeetCode folder to practice, not for shortcuts
2. **Memory = accountability** → System sees your patterns, adapts accordingly
3. **Terminal = friction** → No easy "copy-paste" workflow; forces engagement
4. **Orchestrator = fairness** → One consistent decision-maker, not agent-picking
5. **Hints = learning** → Designed to make you think, not feel stuck

The workflow feels natural because it mirrors how a real mentor works:

> You go to your mentor with a problem.
> They don't solve it for you.
> They ask questions, reference what you've struggled with before.
> They adjust their explanations based on your understanding.
> They remember your weaknesses and push you on them.
