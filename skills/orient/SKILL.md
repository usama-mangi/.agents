---
name: orient
description: >
  Must use as the first step of a new dev-workflow session when continuing work, assessing progress, or picking the next task. Runs once per session at the first task. Not for mid-session tasks: gate 1 in dev-workflow tracks that orient already ran.
---

# Orient

**Core principle**: Orient produces a session snapshot once, cheaply. Fetch only what answers "where do we stand": the active task, its plan, and relevant memory — never the whole backlog or memory store.

## Rules

1. Runs once per session. If `AGENTS.md` is already read and the active task is already in context from a prior orient this session, do not re-run — go straight to the router.
2. NEVER modifies files. This skill reads only. Ambiguous state is reported, not silently fixed.
3. NEVER dump whole files. Fetch the active task and keyword-matched memory only.
4. Re-run only after `recover` (crash) or a context compaction dropped the snapshot.

## What to read

Find the nearest ancestor directory with `AGENTS.md` and `project-backlog.json`. If `project-backlog.yaml` is present instead, report it and route to `migrate-state`. If no state files exist, route to `initialize-project`. Then read, in order:

1. `AGENTS.md` — purpose and quality bar.
2. `python3 ~/.agents/skills/dev-workflow/scripts/backlog.py get --active` — project meta + the in-progress task + last closed task.
3. The current plan `docs/plans/<active-task-id>.md` if it exists.
4. `python3 ~/.agents/skills/dev-workflow/scripts/memory.py get --keyword <active-task-id>` — the keywords of the active task, plus any other keywords the task hints at. Read only the returned entries.
5. `docs/handoff.md` — only if present. It is written on handoff triggers, not after every task, so it may not exist.
6. `design.yaml` — only if present (UI projects).

## Report

Summarize in this compact form:

```
## Orientation: <name>
Active: <TASK-XX> — <title>
Last: <one line from the last-closed task or handoff>
Next: <suggested task or question>
```

Then route: if the user asked to continue, propose the active task and wait; if the user asked for status only, stop after the report. Plan nothing and implement nothing until the user responds.