---
name: initialize-project
description: >
  Must use when current project does not contain AGENTS.md and project-backlog.json files. Require ideate skill first.
---

**Core principle** A project without `AGENTS.md` and `project-backlog.json` files is not acceptable.

## Rules

1. NEVER skip the codebase audit. If the project already has code, examine it before creating files. The first tasks should reflect what actually needs doing, not generic defaults.
2. NEVER create project-backlog.json with fewer than 3 tasks. A backlog with one task is not a roadmap it's a note. Identify at least 3 concrete tasks from the brief, or audit.

## Workflow

1. If the project has existing code:
  - List the directory structure
  - Identify main entry points
  - Note patterns (error handling, naming, testing)
  - Note tech stack (confirm what the user said)
  - Identify gaps or debt

2. Create `AGENTS.md` file by filling the template [mission-template]('./references/mission-template.md'). AGENTS.md must be specific enough that a new agent could understand the project's purpose, quality bar, and constraints from this file alone. Must use `unslop` skill when writing `AGENTS.md`.

3. Create the `docs/` structure: `docs/handoff.md` (empty placeholder) and `docs/plans/` folder.
4. Create `project-backlog.json` as valid JSON. Seed with tasks from the interview and audit. Schema:
```json
{
  "project": { "name": "<name>", "description": "<one line>" },
  "tasks": [
    {
      "id": "TASK-01",
      "title": "<concrete title>",
      "status": "to-do",
      "dependencies": [],
      "notes": "<optional context>"
    }
  ],
  "log": { "last_updated": "<ISO date>", "recent_changes": [] }
}
```
  Each task needs:
  - A TASK-XX ID (sequential, starting at TASK-01)
  - A concrete title (not vague — "Add user authentication" not "Auth stuff")
  - Dependencies (empty array, or specific TASK-XX IDs)
  - A valid status. `to-do` -> `active` -> `testing` -> `blocked`/`closed`
  Include at least:
  - Foundational/scaffolding tasks (if new project)
  - The first feature the user wants to build
  - A quality/testing task

5. Summarize what was created:
  - Files created (list them)
  - backlog tasks (list IDs and titles)
  - Suggested first task
  Then ask: "Should I start with [TASK-001: title]?"
