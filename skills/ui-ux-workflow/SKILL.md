---
name: ui-ux-workflow
description: >
  Must load when the task touches UI, UX, frontend, design system, or brand visuals. Requires
  dev-workflow to be loaded first.
---

**Core principle**: Apply the four UI gates (knowledge-grounded, slop-checked, a11y-checked, system-checked) to every screen and component. Own the `design.yaml` file at the project root.

## Rules

1. NEVER ship a screen or component without running all four UI gates.
2. NEVER ship a colour, type, or spacing value that is not in the token set. Add the token first.
3. NEVER add a font from the slop defaults (Inter as the only family, Geist, Space Grotesk, Instrument Serif) unless the brand brief explicitly demands it.
4. NEVER ship text below WCAG AA contrast in any mode. NEVER ship a tap target under 44 by 44 px. NEVER encode meaning in colour alone or in icon alone.
5. NEVER add a new component unless three real requests exist for it.
6. NEVER name a token "purple-500" or "gradient-start". Tokens are semantic.
7. NEVER ship name-swappable copy. Run the name-swap test.
8. Load `unslop` alongside this skill whenever output includes human-facing text.
9. Read [references/hci-foundations.md](./references/hci-foundations.md) before designing or evaluating a surface.
10. Read [references/design-process.md](./references/design-process.md) before running a design project, evaluating a screen, or breaking a creative block.
11. Read [references/design-system.md](./references/design-system.md) before initializing or auditing a design system.
12. New UI, or remediation of existing (especially AI-generated) UI → load `design-intent` alongside this skill. Nothing is generated before its intent phases are green: audience block (A1), named style direction from a sealed rollout (A2), motion personality (A3). This skill's four gates check the *output*; `design-intent` forces the *decisions* that make the output non-default.
13. `design-intent` owns the `intent:` block of `design.yaml` (audience, style, motion, delivery). This skill owns the rest. Read the intent block on orient; never write it.
14. Mechanical support lives in `design-intent/scripts/intent.py`: `scan` (slop tells + intent coverage), `gates` (exit 1 on any intent-gate fail), `merge` (deep-merge decisions into `intent:`).

## Gates

- **Knowledge-grounded.** For surface work, the [HCI foundations](./references/hci-foundations.md) are applied. For design process work, [design-process.md](./references/design-process.md) is applied. For design-system work, [design-system.md](./references/design-system.md) is applied. No rule here is invented; every rule traces back to one of those three files.
- **Intent-checked.** For new UI or UI remediation, the four intent gates from `design-intent` (audience, style, motion, delivery) pass before this skill's four output gates run — `python3 ~/.agents/skills/design-intent/scripts/intent.py gates` exits 0. A screen can pass slop/a11y/system checks and still be generic: the intent gates are what prevent that.
- **Slop-checked.** Every screen and component passes the [slop checklist](./references/slop-checklist.md). Any match is a violation. Fix before ship.
- **A11y-checked.** Every screen and component passes the [a11y checklist](./references/a11y-checklist.md). Any violation fails the gate.
- **System-checked.** Tokens, components, and the eight good-vs-bad factors pass via the design-system phases in [design-system.md](./references/design-system.md). No raw colour values, no 3px nudges, no component that consumes a primitive token directly.

## Workflow

### Sub-flow: initialize-design-system

Run when `design.yaml` does not exist at the project root, or when a full rebuild is requested.

1. Read the brief from `AGENTS.md`.
2. Read [references/hci-foundations.md](./references/hci-foundations.md), [references/design-process.md](./references/design-process.md), [references/design-system.md](./references/design-system.md).
3. Audit the existing surface if any (read-only).
4. Run the `brand-direction` sub-flow to seed the `brand` block.
5. Build `design.yaml` per the [schema](references/design-yaml-schema.md). Tokens first, then components, then screens.
6. Run the [slop checklist](references/slop-checklist.md) and [a11y checklist](references/a11y-checklist.md) on the initial tokens. Fix before declaring init done.
7. Commit `design.yaml`. Mark the init task closed: `python3 ~/.agents/skills/dev-workflow/scripts/backlog.py update --id <TASK-XX> --status closed`.

### Sub-flow: brand-direction

Run when `design.yaml.brand.differentiators` is empty or stale, or as step 4 of `initialize-design-system`.

1. Read `AGENTS.md` for product context.
2. Write 2 to 3 reference lines that sound exactly like the brand.
3. List 10 to 20 deliberate choices that distinguish this product from the training-data mean.
4. Run the name-swap test on every headline. If the sentence still fits after replacing the brand name with a competitor, rewrite.
5. Write the `brand` block of `design.yaml`.

### Per-task workflow

1. Read `design.yaml` and the relevant reference file.
2. Run the four gates on the change. Block on any failure.
3. Implement.
4. Re-run the four gates on the result.
5. Update `design.yaml` (tokens, components, screens, current_task).
6. Hand off to dev-workflow for review and record-progress.
