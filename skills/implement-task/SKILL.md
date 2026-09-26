---
name: implement-task
description: >
  Must run after plan-task. Require an approved plan before implementation. Next step is audit (review mode).
---

**Core principle**: Each line of code must be written with a purpose. Repeatable functionalities go in functions. Prefer generic functions and extend with specific functions if required.

## Rules

1. NEVER implement without an approved plan. If no plan exists, STOP and load plan-task.
2. NEVER skip steps in the plan. Implement each step in order. If a step seems unnecessary, ask the user.
3. NEVER add steps not in the plan. If the plan is incomplete, STOP. Update the plan, get re-approval.
4. NEVER declare done without running audit in review mode.
5. NEVER re-read the plan file. The approved plan is already in context from plan-task.

## Workflow

1. Work the first implementation step exactly as specified. Run only the checks that step needs. If a check fails, STOP and fix before moving on.
2. Move to next step ONLY after current step's requirements are met.
3. After the last step, run the full gate suite once (tests, lint, typecheck, build).
4. Route to `audit` (review mode).

## Testing Rules (when plan includes test steps)

1. NEVER write tests after implementation without seeing them fail first. Write test → run → confirm fails (red) → implement → pass (green).
2. NEVER test implementation details. Test what the code DOES, not how it does it.
3. NEVER write assertion-free tests. Every test must assert a specific outcome.
4. ALWAYS test the error path. For every happy-path test, consider bad input, missing data, network failure.
5. Read 2–3 existing test files to match project patterns (framework, assertions, naming). Follow existing patterns exactly.
6. One behavior per test. Arrange → Act → Assert. Test name describes behavior.
7. Anti-patterns to avoid: snapshot-only tests, mock-testing (asserting mock was called), assertion-free tests, testing framework internals.

## Dependency Rules (when plan includes adding a package)

1. NEVER add unmaintained package. Check: last publish < 6 months, weekly downloads > 10K, open issues < 100.
2. NEVER add without checking license. GPL in proprietary = legal liability.
3. NEVER add for one utility function. Write it yourself.
4. Search codebase first: does similar functionality exist? Check transitive dependencies.
5. Verify build, tests, lint pass after installation. Revert if anything fails.

## Refactoring Rules (when plan includes refactoring)

1. NEVER refactor without existing tests passing first. No tests → write tests first, verify, then refactor.
2. NEVER refactor and add features in the same change. These are two separate tasks.
3. NEVER make a large refactor in one step. Break into small steps, each independently committable.
4. Run tests after each step. Green → commit → next. Red → revert that step → re-diagnose.
5. After all steps: full test suite passes (same count as baseline), build passes, lint passes, no new warnings.
