# UI coordination

Read this only when a UI task is in scope. Otherwise ignore.

## When this applies

A task touches UI, UX, frontend, design system, or brand visuals when any of these match: build a new UI, design a page or feature, polish or improve an existing UI, audit a frontend for slop or a11y, fix layout / typography / colour / motion / a11y / copy / onboarding, set up a design system, build tokens, create a component library, rebrand or change brand direction, add a component, change a token, change a colour, font, or spacing value.

If none match, this file does not apply. Pure backend, infra, or data work stays on dev-workflow alone.

## What changes for UI tasks

- `AGENTS.md` and `design.yaml` are both read on orient.
- The `ui-ux-workflow` skill is loaded alongside the active skill for the duration of the task.
- The four UI gates from `ui-ux-workflow` (knowledge-grounded, slop-checked, a11y-checked, system-checked) must pass before dev-workflow's gate 3 (verified) can pass.
- `ui-ux-workflow` updates `design.yaml` during its per-task workflow (step 5). dev-workflow does not write to `design.yaml`.