---
name: dev-workflow
description: >
  Must load this skill when working with code, config, docs, or project state. Only skip it for pure reading, research, or answering questions with no file changes.
---

# Skill: dev-workflow

**Core principle**: This is a loop. This skill decides what to do next.

## The loop

1. At session start, run `orient` once. Its snapshot stays in context.
2. For each task, route from the table below, run the phase skill, then return here.
3. Phase skills never chain: always pass back through the router.
4. Every completed task ends at `record-progress` (a cheap state write — see below).

`dev-workflow` loads once per session. Keep the routing table and gates in context; do not re-read this file each loop.

## State, read and written cheap

State lives in two JSON stores in the project root, driven by scripts in this skill:
`python3 ~/.agents/skills/dev-workflow/scripts/<script>`.

| Store | Script | Covers |
|-------|--------|--------|
| `project-backlog.json` | `backlog.py` — `get --active` fetches only the in-progress task, `list` shows one line per task, `add`/`update`/`remove` write state | task state |
| `memory.json` | `memory.py` — `get --keyword K` fetches only matching entries, `add`/`update`/`remove` write state | decisions, verified docs, patterns, lessons |

- Fetch by keyword / active task only. Never dump a whole store into context.
- `memory.json` is the project memory bank. The memory graph (memory-skill) is separate and used only for research/learning topics, never for project state.
- `docs/handoff.md` is written by record-progress only when the session is near its context limit (~70%) or the user explicitly asks. It is not written per task.

## Mechanical gates

Before proceeding, check these; if any fails, stop and fix it first.

- **Gate 1, oriented:** `orient` ran this session. Once done it stays done — later tasks in the same session do not re-orient. Re-run only after `recover` or a context compaction dropped the snapshot.
- **Gate 2, planned:** any change to more than one file, or any new task, has an approved plan. A one-file change may skip plan-task.
- **Gate 3, verified:** every Definition of Done check passed. For UI tasks the four UI gates from `ui-ux-workflow` pass too. See [references/ui-coordination.md](references/ui-coordination.md).
- **Gate 4, recorded:** record-progress ran and updated backlog + memory (and `design.yaml` for UI tasks, updated by ui-ux-workflow). If not, load record-progress now.

## Rules

1. Load a skill only when required.
2. Orient runs once per session — at the first task of the session only.
3. No plan, no implementation (for multi-file changes or new tasks).
4. record-progress runs after every completed task. Keep it cheap: update backlog + memory via scripts. Write `docs/handoff.md` only at ~70% context or on request.
5. Vague idea ("I want to build X") → load ideate before initialize-project.
6. Third-party code → load latest-doc alongside the active skill.
7. A gate fails or an error appears → load debug. No random fixes.
8. UI, UX, frontend, design system, or brand visuals → load ui-ux-workflow alongside the active skill. See [references/ui-coordination.md](references/ui-coordination.md).
9. Human-facing text (UI copy, landing pages, docs, README, commit messages, error messages, emails, or copy embedded in generated UI) → load unslop alongside the active skill.
10. Re-read state only when it changed. The orient snapshot is authoritative for state that has not changed this session.

## File architecture

| File | Answers | Maintained by |
|------|---------|---------------|
| `AGENTS.md` | Why does this project exist, what is the quality bar | initialize-project; written with unslop |
| `project-backlog.json` | What is done, in progress, remaining | backlog.py via record-progress, pivot |
| `memory.json` | Verified decisions, facts, and lessons | memory.py via record-progress, latest-doc, pivot |
| `docs/handoff.md` | Snapshot for a fresh session | record-progress, only at ~70% context or on request |
| `docs/plans/TASK-XX.md` | Approved plan for one task | plan-task |
| `design.yaml` | UI projects only: direction, tokens, components, screens | ui-ux-workflow |

## Routing table

| Intent | Load | Then |
|--------|------|------|
| "I want to build...", "rough idea", "concept" | `ideate` | Interview, then `initialize-project`, then loop |
| Session start: "continue", "resume", "what's next", "pick up" | `orient` | Report state, then loop |
| "what was done", "project status" | `orient` | Report only, stop |
| "plan [feature]", "design [thing]" | `plan-task` (orient first if not yet this session) | Stop after plan approval |
| "implement", "build [feature]", "apply the change" | `plan-task` if needed, `implement-task` | Full cycle through record-progress |
| "fix [bug]", "this is broken" | Full cycle | Bugs are unblocked tasks |
| "add this", "also update X", "quick change" (mid-session) | `plan-task` if >1 file, `implement-task` | Full cycle; do not re-orient |
| "ship", "commit", "we're done" | `record-progress` | Update state, commit |
| No state files at project root | `initialize-project` | Then loop |
| Old layout (project-backlog.yaml present, project-backlog.json missing) | `migrate-state` | Convert, then orient |
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
| Any UI/UX intent (build UI, polish, audit, fix layout/typography/colour/motion/a11y/copy/onboarding, design system, tokens, components, rebrand) | `ui-ux-workflow` | See [references/ui-coordination.md](references/ui-coordination.md) |
| "unslop", "remove AI voice" | `unslop` | Cut AI patterns from writing |

## Sub-skills

| Skill | Purpose | When to load |
|-------|---------|-------------|
| `ideate` | Interview the user, refine a rough idea into a brief saved in `AGENTS.md` | Idea is vague or undefined |
| `orient` | Read `AGENTS.md`, active task via `backlog.py get --active`, relevant `memory.json` entries, current plan, and `docs/handoff.md` if present. Report state | Once per session, at the first task |
| `plan-task` | Create plan in `docs/plans/TASK-XX.md`, get approval | Before implementation (multi-file or new tasks) |
| `implement-task` | Execute the plan step by step, verify gates | After plan approval |
| `record-progress` | Close the task and update `memory.json` via scripts; write `docs/handoff.md` and commit only on handoff triggers; update `project-backlog.json` | After implementation |
| `initialize-project` | Create `AGENTS.md`, `project-backlog.json`, `memory.json`, and `docs/` from scratch | Only if no `AGENTS.md` exists |
| `migrate-state` | Convert project-backlog.yaml into project-backlog.json + docs/ | Old layout detected, or user requests migration |
| `ui-ux-workflow` | UI/UX phase skill. Owns `design.yaml`, applies the four UI gates | Any UI/UX intent. See [references/ui-coordination.md](references/ui-coordination.md) |
| `latest-doc` | Verify library docs before use; record facts in `memory.json` via memory.py | Alongside skills touching third-party code |
| `debug` | Reproduce, isolate, fix, verify | Gates fail or errors occur |
| `write-tests` | Guided test writing, red-green | Plan includes test steps |
| `review` | Self-review | Last gate before record-progress |
| `recover` | Repair state after a crash | Session crashed or state inconsistent |
| `refactor` | Incremental refactoring with a test safety net | Cleanup, tech debt |
| `add-dependency` | Verify and add packages safely | Installing a library |
| `pivot` | Handle scope changes | Abandoning or redirecting work |
| `bug-hunter` | Proactive bug discovery | Before releases, audits |
| `security-audit` | Vulnerability scanning | Security-relevant work or explicit request |
| `code-quality` | Smells, complexity, duplication | Quality passes |
| `system-design` | Architecture decisions | New projects or features |
| `unslop` | Cut AI patterns from writing, add human voice | Any human-facing text: docs, copy, UI strings, commits, READMEs |

Base directory for this skill: /home/usama-mangi/.agents/skills/dev-workflow
Relative paths in this skill (e.g., scripts/, reference/) are relative to this base directory.