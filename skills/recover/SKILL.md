---
name: recover
description: >
  Use when session crashed, state is inconsistent, or user wants to change direction (pivot). Replaces pivot and recover skills.
---

**Core principle:** Git log is ground truth. If git and state files disagree, git wins.

## Rules

1. NEVER assume what was done. Verify with `git log` and `git diff`.
2. NEVER overwrite state without reading it first.
3. NEVER mark partial work as done. Record exactly what was completed.
4. ALWAYS check for uncommitted work (`git status`, `git diff`).
5. NEVER pivot without recording reasoning. Unrecorded pivots create ghost work.
6. NEVER abandon tasks without marking them blocked with a reason.

## Mode: crash-recovery

Triggered by: "session crashed", "what was I doing"

1. If `docs/handoff.md` exists, note: active task, planned steps, next action.
2. Run `git log --oneline -10`. Compare with handoff state.
3. Run `git status`. Check for uncommitted, staged-but-not-committed, untracked changes.
4. If uncommitted work exists, ask user: commit, stash, or discard?
5. Report: what git shows, what state files said, discrepancies, current state, suggested next step.

## Mode: pivot

Triggered by: "change plan", "pivot", "scrap this"

1. Ask user: what to do differently? why is current approach not working? what does new direction look like?
2. Review backlog: `python3 ~/.agents/skills/dev-workflow/scripts/backlog.py list`
   - Which tasks affected? Abandoned? Modified? New?
3. Update backlog via scripts:
   - Abandoned: `backlog.py update --id TASK-XX --status blocked --notes "Blocked: <reason>"`
   - Modified: `backlog.py update --id TASK-XX --title "<new direction>"`
   - New: `backlog.py add --id TASK-XX --title "<title>" --deps ...`
4. Record pivot in memory:
   `python3 ~/.agents/skills/dev-workflow/scripts/memory.py add --key pivot-<date> --text "<reason, abandoned, added, carried over>" --cat decisions`
5. Create or update plan for new direction.
6. Summarize: what was abandoned, what is new, what still applies, next step.
