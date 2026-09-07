---
name: recover
description: >
  Must use when recovery is required after a session crash or mid-implementation termination.
---

**Core principle**: Git log > project-backlog.json. If both don't match, git wins.

## Rules
1. NEVER assume what was done. Verify with `git log` and `git diff`. What was committed is truth. What backlog file says is interpretation.
2. NEVER overwrite state backlog without reading it first. Read current state, read git history, then reconcile. Blind overwriting loses information.
3. NEVER mark partial work as done. If 3 of 5 steps were completed, record exactly that. Do not mark the task done.
4. ALWAYS check for uncommitted work. `git status` and `git diff` reveal staged-but-not-committed or unstaged changes that may be valuable.

## Workflow

1. If `docs/handoff.md` exists, it is the last recorded snapshot. Note:
  - What task was being worked on
  - What steps were planned
  - What was supposed to happen next
  Handoff may be absent (it is written only on handoff triggers). Fall back to git log and `python3 ~/.agents/skills/dev-workflow/scripts/backlog.py get --active` for the task state, and `python3 ~/.agents/skills/dev-workflow/scripts/memory.py get --keyword <active-task-id>` for the last decisions.
2. Run git log --oneline -10. This shows what was ACTUALLY committed. Compare with handoff:
  - Were commits made that handoff doesn't mention?
  - Were commits NOT made that handoff says were done?
3. Run git status. Limit `git diff --stat` and `git diff --cached --stat` to the paths touched by the pending task; do not diff the whole tree when the crash is localized. Look for:
  - Uncommitted changes (working directory)
  - Staged but not committed changes
  - Untracked new files
  If uncommitted work exists, ask the user whether to commit, stash, or discard it.
4. Report to user. Summarize:
  - What git log shows (actual commits)
  - What state files said vs what was real (discrepancies found)
  - Current state after reconciliation
  - Suggested next step
