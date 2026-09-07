---
name: dev-workflow
description: >
  Must load this skill when working with code, config, docs, or project state. Only skip it for
  pure reading, research, or answering questions with no file changes.
---

**Core principle**: This is a loop. This skill decides what to do next. Refer to this throughout the session and not just at the beginning.

## The loop

Run this cycle for every task, every time:
1. Match the user's intent to the routing table below. Load the first phase skill.
2. The phase skill runs to completion.
3. When the phase skill finishes, route again from this skill, already in context. Do not re-read it. Do not chain phases by memory. Do not start a new phase without passing back through the router.
4. Until the task is done and record-progress has run.

`dev-workflow` loads once per session. Keep the routing table, gates, and rules in context; route from that copy instead of re-reading this file each loop.

## Mechanical gates

Check these before proceeding; if any check fails, stop and fix it before moving on.
  - Gate 1, oriented: `AGENTS.md` has been read this loop. If the project has a `design.yaml`, orient reads it too. If not, load orient first. No code work on an unoriented session.
  - Gate 2, planned: for any change touching more than one file, or any new task, a plan exists and is approved. If not, load plan-task.
  - Gate 3, verified: all gates in the plan's Definition of Done passed. For UI tasks, the four UI gates from `ui-ux-workflow` (knowledge-grounded, slop-checked, a11y-checked, system-checked) must pass too. See [references/ui-coordination.md](references/ui-coordination.md) for what counts as a UI task. If not, debug or fix before declaring done.
  - Gate 4, recorded: record-progress ran for the completed task and state files were updated. For UI tasks, `design.yaml` is updated by `ui-ux-workflow` per its per-task workflow before record-progress runs. If not, load record-progress now.

## Rules
1. Load a skill only when required. Do not load before the skill is to be used.
2. Orient runs before any code work in every loop. It is not optional.
3. No plan, no implementation. A change touching one file is ok; anything larger needs plan-task first.
4. record-progress runs after every completed task. Unrecorded work is lost work.
5. If the user's idea is vague ("I want to build X" with no problem, users, or scope), load ideate before initialize-project.
6. When working with a third-party library, load latest-doc alongside the active skill. Verify APIs against real docs; do not assume you know the docs.
7. When a gate fails or an error appears, load debug alongside the active skill. No random fixes.
8. When the task touches UI, UX, frontend, design system, or brand visuals, load `ui-ux-workflow` alongside the active skill. See [references/ui-coordination.md](references/ui-coordination.md) for what counts.
9. Load unslop alongside the active skill whenever output includes human-facing text: UI copy, landing pages, marketing text, docs, READMEs, commit messages, error messages, or emails. Write all such text following unslop before it ships. Generated content counts too: a landing page's headings, buttons, and body copy all follow unslop, not just standalone prose.
10. Re-read state only when it changed. `orient` reads all state on the first loop and the delta on later loops. Read plans and the handoff from context, not from disk, when you already have them.

## File architecture

Every project on this workflow keeps these files:

| File | Answers |
|------|---------|
| `AGENTS.md` | Why does this project exist and what is the quality bar? Must be written with `unslop` skill |
| `project-backlog.json` | What task is done, in progress, and remaining. State only; no plan, no handoff. |
| `docs/handoff.md` | What was delivered, how it was verified, and what comes next. Written by record-progress. |
| `docs/plans/TASK-XX.md` | The plan for task TASK-XX. One plan per task, written by plan-task. |
| `design.yaml` | (UI projects only) Design direction, tokens, components, screens, slop and a11y status, current design task. Read by orient whenever present. |

## Routing table

| Intent | Load | Then |
|--------|------|------|
| "I want to build...", "rough idea", "concept" | `ideate` | Interview, then `initialize-project`, then loop |
| "continue", "resume", "what's next", "pick up" | `orient` | Report state, then loop |
| "what was done", "project status" | `orient` | Report only, stop |
| "plan [feature]", "design [thing]" | `orient`, then `plan-task` | Stop after plan approval |
| "implement", "build [feature]", "apply the change" | `orient`, `plan-task` if needed, `implement-task` | Full cycle through record-progress |
| "fix [bug]", "this is broken" | Full cycle | Bugs are unblocked tasks |
| "add this", "also update X", "quick change" (mid-session) | Full cycle | Re-run gates 1 and 2 even for small changes |
| "ship", "commit", "we're done" | `record-progress` | Update state, commit |
| No state files at project root | `initialize-project` | Then loop |
| Old layout (project-backlog.yaml present, project-backlog.json missing) | `migrate-state` | Convert to new layout, then orient |
| "test failed", "error", "debug" | `debug` | Diagnose, fix, re-verify |
| "write tests", "add tests" | `write-tests` | Tests for the current task |
| "review", "check my code" | `review` | Before record-progress |
| "session crashed", "what was I doing" | `recover` | Reconcile state, then orient |
| "refactor", "clean up", "tech debt" | `refactor` | Baseline, incremental, verify |
| "add dependency", "install package" | `add-dependency` | Verify, add, record |
| "change plan", "pivot", "scrap this" | `pivot` | Assess, update project-backlog.json, re-plan |
| "find bugs", "bug hunt" | `bug-hunter` | Systematic discovery |
| "security", "check vulnerabilities" | `security-audit` | Audit and report |
| "code quality", "code smells" | `code-quality` | Structural analysis |
| "system design", "architecture" | `system-design` | Decisions and trade-offs |
| Any UI/UX intent (build UI, polish, audit, fix layout/typography/colour/motion/a11y/copy/onboarding, set up design system, build tokens, create component library, rebrand) | `ui-ux-workflow` | See [references/ui-coordination.md](references/ui-coordination.md) |
| "unslop", "remove AI voice" | `unslop` | Cut AI patterns from writing |
| Any human-facing text in scope (UI copy, landing pages, docs, README, commits) | `unslop` alongside the active skill | Write that text following unslop |

## Sub-skills

| Skill | Purpose | When to load |
|-------|---------|-------------|
| `ideate` | Interview the user, refine a rough idea into a project brief. Save in `AGENTS.md` | Idea is vague or undefined |
| `orient` | Read `AGENTS.md`, `project-backlog.json`, `docs/handoff.md`, `docs/plans/<current task>`, and `memory.md`. If `design.yaml` exists, read it too. Report orientation, verify consistency | First in every loop |
| `plan-task` | Create plan for current task in `docs/plans/TASK-XX.md`, get approval | Before implementation |
| `implement-task` | Execute the plan step by step, verify gates | After plan approval |
| `record-progress` | Write `docs/handoff.md`, update `project-backlog.json` (and `memory.md` if needed). Commit. | After implementation |
| `initialize-project` | Create `AGENTS.md`, `project-backlog.json`, and `docs/` from scratch | Only if no `AGENTS.md` exists |
| `migrate-state` | Convert an old project-backlog.yaml into project-backlog.json + docs/ | Old layout detected, or user requests migration |
| `ui-ux-workflow` | UI/UX phase skill. Owns `design.yaml`, applies four UI gates, provides `initialize-design-system` and `brand-direction` sub-flows | Any UI/UX intent. See [references/ui-coordination.md](references/ui-coordination.md) |
| `latest-doc` | Verify library docs before use | Alongside skills touching third-party code |
| `debug` | Reproduce, isolate, fix, verify | Gates fail or errors occur |
| `write-tests` | Guided test writing, red-green | Plan includes test steps |
| `review` | Self-review | Last gate before record-progress |
| `recover` | Repair state after a crash | Session crashed or state inconsistent |
| `refactor` | Incremental refactoring with a test safety net | Cleanup, tech debt |
| `add-dependency` | Verify and add packages safely | Installing a library |
| `pivot` | Handle scope changes | Abandoning or redirecting work |
| `bug-hunter` | Proactive bug discovery | Before releases, audits |
| `security-audit` | Vulnerability scanning | Before deployment, after auth work |
| `code-quality` | Smells, complexity, duplication | Quality passes |
| `system-design` | Architecture decisions | New projects or features |
| `unslop` | Cut AI patterns from writing, add human voice | Any human-facing text: docs, copy, UI strings, commits, READMEs |
