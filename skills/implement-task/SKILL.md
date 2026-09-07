---
name: implement-task
description: >
  Must run after plan-task. Require an approved plan before implementation. Next step is review skill.
---

**Core principle**: Each line of code must be written with a purpose. Repeatable functionalities go in functions. Prefer generic functions and extend with specific functions if required. Use official skill of the language, library, or framework in implementation if available.

## Rules

1. NEVER implement without an approved plan. If no plan exists for the task, STOP and load plan-task. No exceptions.
2. NEVER skip steps in the plan. Implement each step in order. If you think a step is unnecessary, ask the user. Do not skip silently.
3. NEVER add steps not in the plan. If you discover the plan is incomplete, STOP. Update the plan, get re-approval, then continue.
4. NEVER declare done without running review and security-audit skills.
5. NEVER re-read the plan file. The approved plan is already in context from plan-task.

## Workflow

1. Use the approved plan already in context from plan-task; do not re-read the file. Work the first implementation step. Do exactly what it says. Run only the checks that step needs. If a check fails for the step, STOP and fix before moving to the next step.
2. Move to next step ONLY after current step's requirements are met.
3. After the last step, run the full gate suite once (tests, lint, typecheck, build). Do not re-run the whole suite per step; verify each step with its own checks only.
4. Route to `review`.
