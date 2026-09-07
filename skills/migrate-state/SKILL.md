---
name: migrate-state
description: >-
  Must use when a project still uses project-backlog.yaml (old layout). Converts it to the new
  layout: project-backlog.json plus docs/handoff.md and docs/plans/TASK-XX.md.
---

**Core principle**: The old backlog mixes state, plan, and handoff in one yaml file. Split them into the new layout without losing a single field.

## Detect

Old layout: `project-backlog.yaml` present and `project-backlog.json` missing. The plan and handoff live inside the yaml.
New layout: `project-backlog.json` present. Nothing to migrate.

## Rules

1. NEVER convert blind. Read the yaml first. Every task, plan field, and handoff field maps to the new layout. Nothing is dropped.
2. NEVER delete `project-backlog.yaml` until `project-backlog.json` parses and the `docs/` files are written. Keep the yaml as backup until verified.
3. NEVER invent content. If a field is missing, leave it out or note it. Do not fabricate a plan or handoff that was not there.
4. NEVER change task statuses or dependencies during migration. Preserve them exactly.

## Workflow

1. Confirm the old layout: `project-backlog.yaml` exists, `project-backlog.json` does not.
2. Read `project-backlog.yaml` in full. Separate the content into:
   - project meta (name, description)
   - tasks list (id, title, status, dependencies, notes)
   - the embedded plan (belongs to the in-progress task)
   - the embedded handoff (the last recorded session)
3. Create `project-backlog.json` from the project meta and tasks. Use the schema from initialize-project. Exclude the plan and handoff; they move to `docs/`.
4. Create `docs/` if missing. Write the handoff to `docs/handoff.md` using the handoff-template. If the project has no handoff, write an empty placeholder.
5. For each plan found, write `docs/plans/TASK-XX.md` using the plan-template. Name the file after the task's ID. In the old layout there is one plan for the current task.
6. Validate: `project-backlog.json` parses as JSON; every plan and the handoff read as markdown with no yaml remnants.
7. Update references: any line in `AGENTS.md` or `memory.md` pointing at `project-backlog.yaml` now points at `project-backlog.json` and `docs/`.
8. Delete `project-backlog.yaml` only after validation passes.
9. Commit: `chore(migrate): split backlog, plans, handoff into new layout`.
10. Route to `orient`.