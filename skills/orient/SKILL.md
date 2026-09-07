---
name: orient
description: >
  Must use as the first step when continuing work, assessing progress, or looking for next step. Always runs before plan-task, implement-task, or record-progress. This is the FIRST step of every dev-workflow session.
---

**Core principle**: The project must contain `AGENTS.md` and `project-backlog.json` files (and `memory.md` optionally). Handoff lives in `docs/handoff.md`, plans in `docs/plans/`. If `project-backlog.yaml` is present instead of `project-backlog.json`, the project is on the old layout: report it and route to `migrate-state`, do not read the yaml as current state. If no state files are present then route to initialize-project.

## Critical Rules

1. NEVER leave a blind spot. On the first orient, read all state files. On later loops, read only the files that changed; unchanged files are already in context.
2. NEVER modify files during orient. This skill READS only. If files are ambiguous, report. Do not silently fix it.

## Workflow

1. Find the nearest ancestor directory containing `AGENTS.md` and `project-backlog.json` files. On the first orient, read all state: the backlog, `docs/handoff.md`, the current task's plan in `docs/plans/`, and `memory.md` if present. On later loops in the same session, re-read only the files changed since the last orient; the rest is already in context.
2. Summarize to the user in this format:
```
## Orientation: [Project Name]

**Purpose:** [from AGENTS.md, one line]
**Phase:** [from project-backlog.json]
**Active task:** [from project-backlog.json. "none" if no task active]

**Last done:** [from project-backlog.json, docs/handoff.md and memory.md, what was delivered]
**Gates:** [test counts, lint, build status from project-backlog.json]

**Next:** [from project-backlog.json: specific task ID + title]
**Blockers:** [project-backlog.json or "none"]

Should I proceed with [TASK-ID: title] or do you have something else in mind?
```

Do NOT proceed to planning or implementation until the user responds.
