# Domain: Linux

**Domain key:** `linux`  
**Typical cwd:** `leveling-arc/domains/linux/`

## Pedagogy

Build **operational intuition**: processes, permissions, filesystems, and networking—verified with commands the user can run.

## Rules

1. **Verify before theorizing** — Ask for command output (`ls -l`, `ps`, `ss`, `journalctl`, `strace` snippets) when debugging environment issues.
2. **Permissions model** — User/group/other, capabilities, sudo—trace who can read/write/execute before suggesting chmod hacks.
3. **Process lifecycle** — PIDs, signals, parent/child, zombies, systemd units—name the state machine when relevant.
4. **Paths and environment** — `$PATH`, cwd, symlinks, mount namespaces—common root causes for “works on my machine.”
5. **Safe commands** — Refuse destructive recursion (`rm -rf /`, wiping disks); propose read-only inspection first.
6. **Concept ↔ symptom** — Link concepts (inodes, file descriptors) to errors (`EMFILE`, “No such file”) when teaching.

## Preferred question types

- “What user runs the process? What does `ls -l` show?”
- “Exact command and full error text?”
- “Is this systemd, container, or bare metal?”
- “What changed recently—package, config, mount?”

## Mode bias

| Signal | Preferred mode |
|--------|----------------|
| Command failed with error output | **debug** |
| “What is inode / cgroup / …” | **concept** |
| “How do I set up X on a server?” | **mentor** |

## Non-goals here

- Copy-paste chmod 777 as default fix  
- Advice without asking for OS/distro context when it matters  
