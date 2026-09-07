---
name: plan-task
description: >
  Must use before implementation step. Session is oriented by then (orient runs once per session as gate 1). Always require this skill before implement-task
---

**Core principle**: Implementation without a plan is random work. Plan without orientation is also random work.

## Rules

1. NEVER create a plan that is a file list. A plan specifies WHAT changes, WHY, and HOW: layout, behavior, states, error handling. "Modify these 5 files" is not a plan.
2. NEVER skip the approval gate. Show the plan to the user. Do NOT implement until explicitly approved.
3. NEVER re-read or re-present an approved plan. Show it once for approval; it stays in context for implement-task.
4. NEVER ignore dependencies. Verify all prerequisite tasks are `closed` in project-backlog.json before planning the dependent task.

## Workflow

1. The task to plan comes from the orient snapshot or the user. If you need its details, fetch only it: `python3 ~/.agents/skills/dev-workflow/scripts/backlog.py get --task <TASK-XX>`. Verify:
  - The task exists in project-backlog.json with a TASK-XX ID
  - All dependencies are closed
  - No other task is currently in progress (if there is, flag it)

2. Read relevant context:
  - AGENTS.md to understand the context
  - Related existing code: patterns, conventions, error handling
  - Any task the new task depends on (to understand integration points)

3. Create the plan in `docs/plans/TASK-XX.md` using the template [plan-template](./references/plan-template.md)

4. Mark the task as in progress, present the plan once, and await approval. Show the full plan to the user. Ask: "Is this plan approved, or should I revise it?" Do NOT proceed to implement-task until the user explicitly approves. The approved plan stays in context; implement-task does not re-read the file.
