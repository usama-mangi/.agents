---
name: pivot
description: >
  Must use when scope changes, direction turns, or plan is abandoned. Useful when user asks for a change of plans.
---

**Core principle**: Do not pivot without providing rationale, updating plan, and recording the decision. Unrecorded pivots create ghost work that confuses future sessions.

## Rules
1. NEVER pivot without updating plan. Abandoned tasks MUST be marked blocked with a reason. New tasks MUST be added with dependencies. Unrecorded pivots create phantom work.
2. NEVER abandon work without recording what was done. If 2 of 5 steps were completed, record that. The next agent needs to know what exists.
3. NEVER start a new direction without orienting first. Read the current state before pivoting. You need to know what exists to know what to keep.
4. ALWAYS record the reasoning. WHY are we pivoting? The reason is as important as the change. Future sessions need to understand the decision.

## Workflow
1. Ask the user:
  - What do you want to do differently?
  - Why is the current approach not working?
  - What does the new direction look like?
  Get a clear answer. "I don't like it" is not enough; understand the root cause.

2. Review the current project-backlog.json:
  - Which tasks are affected?
  - Which tasks should be abandoned?
  - Which tasks should be modified?
  - What new tasks are needed?
  - Do any existing tasks' dependencies change?

3. For each affected task:
  - **Abandoned tasks:** Mark as `blocked` with reason: "Blocked: [reason]"
  - **Modified tasks:** Update title/description to reflect new direction
  - **New tasks:** Add with proper IDs and dependencies

4. Add a pivot note to project-backlog.json:
  - Pivot: <date> - <short description>
  - **Reason:** <why we pivoted>
  - **Abandoned:** <task IDs>
  - **Added:** <task IDs>
  - **Carried over:** <task IDs that still apply>

5. Create plan for the new task:
  - If continuing existing work with modified approach → update `docs/plans/TASK-XX.md`
  - If starting fresh → create a new plan in `docs/plans/` via plan-task
  - If abandoning entirely → mark the plan as abandoned in `docs/plans/TASK-XX.md`

6. memory.md:
  - Record the decision and reasoning
  - This is valuable institutional knowledge

7. Communicate to user. Summarize:
  - What was abandoned and why
  - What is new
  - What still applies from the old direction
  - What the next step is
