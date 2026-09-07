---
name: record-progress
description: >
  Must use when a task step is finished. Requires review skill first or specific information from the user.
---

**Core principle**: Unrecorded progress is lost work and creates confusion for the next session.

## Rules
1. NEVER commit without a task ID. Every commit message references a backlog task: `feat(TASK-<XX>): add feature Y`. No untracked commits.
2. ALWAYS record what was NOT done. Progress must include blockers, deferred decisions, and partial progress; not just what shipped.

## Workflow

1. Read the plan. Confirm every Definition of Done checkbox is checked. If anything is incomplete, report the user and route back to implement-task skill. Do not record partial work as done.
2. Mark the completed task as closed. If the task revealed new tasks during implementation, add them to backlog with proper IDs, dependencies, and to-do status.
3. Write a handoff note to `docs/handoff.md` for the next session using the template [handoff-template](./references/handoff-template.md)
4. Update `memory.md`. Record:
  - New decisions made during this session
  - Patterns discovered
  - Lessons learned
  - Cross-links to related entries
5. Stage all changes (Never commit secrets, keys, or `.env` files). Commit with message format: "<type>(<TASK-ID>): <short description>". Examples:
  - `feat(TASK-007): add app shell navigation`
  - `fix(TASK-003): patch invite-code email leak`
  - `docs(TASK-006): record design system decisions`
6  Update the user concisely. Name the task, the commit, and the gate results. Point to `docs/handoff.md` and the updated `project-backlog.json` instead of restating their contents. Next session loads orient → continues with the suggested task.
