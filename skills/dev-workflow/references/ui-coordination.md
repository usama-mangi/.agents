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

## The intent layer (design-intent)

Load `design-intent` in addition to `ui-ux-workflow` when:

- Building **new** UI (pages, screens, components, landing pages) — CREATE mode.
- Improving existing UI, especially AI-generated UI that "lacks intention" or "doesn't feel human" — REMEDIATE mode (diagnose → re-decide → regenerate under constraints; never rewrite from scratch).

The intent layer adds the decisions the output gates cannot force: a written persona before any copy, a named style direction chosen from a sealed rollout with recorded rubric scores, a motion personality before any animation, and a delivery matrix (all states, real content, launch assets) so the run does not stop at "the demo works."

- `design-intent` owns the `intent:` block of `design.yaml`; `ui-ux-workflow` owns the rest. Neither writes the other's block.
- Mechanical support: `python3 ~/.agents/skills/design-intent/scripts/intent.py scan|gates|merge` — scan reports slop tells + intent coverage, gates exits 1 on any intent-gate fail, merge deep-merges decisions into the `intent:` block.
- Gate order for UI tasks: intent gates (design-intent A4) → output gates (ui-ux-workflow) → dev-workflow gate 3. A generation step must not start before the intent gates are green; an exception must cite a criterion + compensating control, never a fear.