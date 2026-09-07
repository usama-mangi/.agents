---
name: record-progress
description: >
  Must use when a task is finished, before ending a session response. Requires review skill first or specific information from the user.
---

# Record progress

**Core principle**: Unrecorded progress is lost work. Every finished task closes its backlog task and writes its decisions to memory — cheaply, via scripts. The heavy handoff snapshot is reserved for when a fresh session is about to need it.

## Rules

1. NEVER commit without a task ID. Commit message references the backlog task: `feat(TASK-<XX>): add feature Y`. No untracked commits.
2. ALWAYS record what was NOT done: blockers, deferred decisions, partial progress — not just what shipped.
3. Handoff (`docs/handoff.md`) is written ONLY when the session is near its context limit (~70%), when a context compaction is imminent, or when the user explicitly asks. Do not write it after ordinary tasks.
4. Staging a commit: never commit secrets, keys, or `.env` files.

## Workflow

1. Confirm the plan's Definition of Done (from context) passed. If anything is incomplete, report and route back to implement-task. Do not record partial work as done.
2. Close the task: `python3 ~/.agents/skills/dev-workflow/scripts/backlog.py update --id <TASK-XX> --status closed`.
3. Add any tasks discovered during implementation: `backlog.py add --id TASK-XX --title ... --deps ...`.
4. Write decisions to memory: `python3 ~/.agents/skills/dev-workflow/scripts/memory.py add --key <short-key> --text <fact> --cat <category>`. Record only new, durable knowledge: decisions, patterns, verified facts, lessons. Skip anything already in AGENTS.md or the plan. Use `update --append` to extend an existing entry.
5. Handoff — only on the triggers from rule 3. Write `docs/handoff.md` using [handoff-template](./references/handoff-template.md). Keep it a snapshot: what was delivered, how it was verified, what comes next.
6. Commit (if the project is a git repo): stage the state files and the day's work. Message: `<type>(<TASK-ID>): <short description>`, e.g. `feat(TASK-007): add app shell navigation`.
7. Update the user in one or two lines: the task, the commit, and gate results. Point to state files instead of restating them.

The next fresh session starts with orient, which reads the active task and memory directly — no handoff needed for day-to-day continuity.