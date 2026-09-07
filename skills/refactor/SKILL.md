---
name: refactor
description: >
  Must use when refactoring existing code. Use to clean up code, reduce technical debt, fix code smells, or restructure existing code. This skill requires existing tests as a safety net.
---

**The core principle:** Refactoring changes HOW code works, not WHAT it does. If the tests pass before and after, the behavior is preserved. If tests fail, revert that step.

## Rules
1. NEVER refactor without existing tests passing first. No tests -> use tests first. (use write-tests), verify, THEN refactor.
2. NEVER refactor and add features in the same change. These are two separate tasks with two separate backlog entries.
3. NEVER make a large refactor in one step. Break into small steps, each independently committable. If step 3 breaks things, revert it.
4. ALWAYS run tests after each step. Green → commit → next step. Red → revert that step → re-diagnose.

## Workflow

1. Run the full test suite. Record:
  - Tests: X passing, Y failing (before refactor, Y should be 0)
  - Build: pass/fail
  - Lint: pass/fail
  If tests are failing, fix them first. Do not refactor on a broken baseline.
2. Name the specific issue. Be precise:
  - "This function is 200 lines and does 5 things" (long function)
  - "These two classes are identical except for one field" (duplication)
  - "This variable name doesn't describe its contents" (unclear naming)
  - "These two modules depend on each other" (circular dependency)
  Do not refactor vaguely ("this code is bad"). Name the problem.
3. Plan the refactor. Describe:
  - **Current state:** what the code looks like now
  - **Target state:** what it should look like after
  - **Steps:** small, ordered changes (each should be independently committable)
  - **Risk:** which steps might break things (run tests extra carefully after those)
4. For each step:
  - Make the change
  - Run the relevant tests
  - If green → commit with descriptive message
  - If red → revert that step, re-diagnose, try a different approach
  Do NOT proceed to step 2 until step 1 is committed and green.
5. After all steps:
  - Full test suite passes (same count as baseline)
  - Build passes
  - Lint passes
  - No new warnings
  If anything regressed, investigate before recording done.
6. Update project-backlog.json with:
  - What was refactored and why
  - What the code looked like before vs after
  - Any decisions made during refactoring
  - That all tests pass
