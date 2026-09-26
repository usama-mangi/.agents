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
- `memory.json` is the project memory bank. The memory graph (memory-skill) is separate and native — managed by `graph.py` over `memory-graph.json` — and used only for research/learning topics, never for project state.
- `docs/handoff.md` is written by record-progress only when the session is near its context limit (~70%) or the user explicitly asks. It is not written per task.

## Mechanical gates

Before proceeding, check these; if any fails, stop and fix it first.

- **Gate 1, oriented:** `orient` ran this session. Once done it stays done — later tasks in the same session do not re-orient. Re-run only after `recover` or a context compaction dropped the snapshot.
- **Gate 2, planned:** any change to more than one file, or any new task, has an approved plan. A one-file change may skip plan-task.
- **Gate 3, verified:** every Definition of Done check passed. For UI tasks the four UI gates from `ui-ux-workflow` pass **and** the four intent gates from `design-intent` pass (audience, style, motion, delivery). See [references/ui-coordination.md](references/ui-coordination.md).
- **Gate 4, recorded:** record-progress ran and updated backlog + memory (and `design.yaml` for UI tasks, updated by ui-ux-workflow). If not, load record-progress now.

## Rules

1. Load a skill only when required.
2. Orient runs once per session — at the first task of the session only.
3. No plan, no implementation (for multi-file changes or new tasks).
4. record-progress runs after every completed task. Keep it cheap: update backlog + memory via scripts. Write `docs/handoff.md` only at ~70% context or on request.
5. Vague idea ("I want to build X") → load ideate before initialize-project.
6. A gate fails or an error appears → load `audit` (debug mode). No random fixes.
7. UI, UX, frontend, design system, or brand visuals → load `ui-ux-workflow` alongside the active skill. New UI or existing AI-generated UI that lacks named intent → also load `design-intent` (CREATE for new surfaces, REMEDIATE for existing ones). See [references/ui-coordination.md](references/ui-coordination.md).
8. Human-facing text (UI copy, landing pages, docs, README, commit messages, error messages) → load `unslop` alongside the active skill.
9. Third-party code: verify unfamiliar APIs against official docs before using. Store verified facts in `memory.json`.
10. Re-read state only when it changed. The orient snapshot is authoritative for state that has not changed this session.

## File architecture

| File | Answers | Maintained by |
|------|---------|---------------|
| `AGENTS.md` | Why does this project exist, what is the quality bar | initialize-project; written with unslop |
| `project-backlog.json` | What is done, in progress, remaining | backlog.py via record-progress, recover |
| `memory.json` | Verified decisions, facts, and lessons | memory.py via record-progress, recover |
| `docs/handoff.md` | Snapshot for a fresh session | record-progress, only at ~70% context or on request |
| `docs/plans/TASK-XX.md` | Approved plan for one task | plan-task |
| `design.yaml` | UI projects only: direction, tokens, components, screens | ui-ux-workflow |

## Routing table

| Intent | Load | Then |
|--------|------|------|
| "I want to build...", "rough idea", "concept" | `ideate` | Interview, then `initialize-project`, then loop |
| Session start: "continue", "resume", "what's next" | `orient` | Report state, then loop |
| "what was done", "project status" | `orient` | Report only, stop |
| "plan [feature]", "design [thing]" | `plan-task` (orient first if not yet this session) | Stop after plan approval |
| "implement", "build [feature]", "apply the change" | `plan-task` if needed, `implement-task` | Full cycle through record-progress |
| "fix [bug]", "this is broken", "error" | `audit` (debug mode) | Diagnose, fix, re-verify |
| "add this", "also update X", "quick change" (mid-session) | `plan-task` if >1 file, `implement-task` | Full cycle; do not re-orient |
| "ship", "commit", "we're done" | `record-progress` | Update state, commit |
| No state files at project root | `initialize-project` | Then loop |
| Old layout (project-backlog.yaml present, project-backlog.json missing) | `migrate-state` | Convert, then orient |
| "review", "check my code" | `audit` (review mode) | Before record-progress |
| "session crashed", "what was I doing" | `recover` (crash-recovery mode) | Reconcile state, then orient |
| "refactor", "clean up", "tech debt" | `plan-task` + `implement-task` | Plan the refactor, then execute |
| "add dependency", "install package" | Include as a step in `implement-task` | Verify, add, record |
| "change plan", "pivot", "scrap this" | `recover` (pivot mode) | Assess, update backlog, re-plan |
| "find bugs", "bug hunt" | `audit` (bug-hunter mode) | Systematic discovery |
| "security", "check vulnerabilities" | `audit` (security mode) | Audit and report |
| "code quality", "code smells" | `audit` (quality mode) | Structural analysis |
| "write tests", "add tests" | Include as steps in `implement-task` | Tests are part of implementation |
| Any UI/UX intent | `ui-ux-workflow` (+ `design-intent`) | See [references/ui-coordination.md](references/ui-coordination.md) |
| New UI from scratch | `ui-ux-workflow` + `design-intent` (CREATE) | Intent phases before build: audience → style → motion |
| "make this look better", "this looks AI-generated", "add intention", UI remediation | `ui-ux-workflow` + `design-intent` (REMEDIATE) | Diagnose → re-decide → regenerate → gate; never rewrite from scratch |
| "unslop", "remove AI voice" | `unslop` | Cut AI patterns from writing |

## Sub-skills

| Skill | Purpose | When to load |
|-------|---------|-------------|
| `orient` | Read `AGENTS.md`, active task, memory, plan, handoff. Report state | Once per session, first task |
| `plan-task` | Create plan in `docs/plans/TASK-XX.md`, get approval | Before implementation (multi-file or new tasks) |
| `implement-task` | Execute plan step by step, write tests, add deps, refactor | After plan approval |
| `record-progress` | Close task, update memory, write handoff, commit | After implementation |
| `initialize-project` | Create `AGENTS.md`, `project-backlog.json`, `memory.json`, `docs/`, run system-design | Only if no `AGENTS.md` exists |
| `migrate-state` | Convert project-backlog.yaml into project-backlog.json + docs/ | Old layout detected |
| `audit` | Debug, bug-hunt, security, quality, review — one skill, five modes | Errors, reviews, audits |
| `recover` | Crash recovery and pivot management | Session crash or scope change |
| `ideate` | Interview user, refine rough idea into brief | Idea is vague or undefined |
| `ui-ux-workflow` | UI/UX phase skill. Owns `design.yaml`, applies four UI gates | Any UI/UX intent |
| `design-intent` | Intent layer for UI: persona gate, style direction (sealed rollout + rubric), motion personality, delivery gates. Owns the `intent:` block of `design.yaml`. CREATE + REMEDIATE modes | Any new UI or remediation of existing/AI-generated UI |
| `unslop` | Cut AI patterns from writing, add human voice | Any human-facing text |

Base directory for this skill: /home/usama-mangi/.agents/skills/dev-workflow
Relative paths in this skill (e.g., scripts/, reference/) are relative to this base directory.
