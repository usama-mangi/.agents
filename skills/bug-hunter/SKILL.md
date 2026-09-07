---
name: bug-hunter
description: >
  Must trigger whenever trying to hunt a bug without known origin. Do NOT use for code review (use review skill) or refactoring (use reafctor skill)
---

**The core principle:** The absence of failing tests does not mean the absence of bugs. It means you haven't hit the right input yet.

## Rules
- NEVER assume code is correct because it works in the happy path. Every function has edge cases. Find them.
- NEVER report a bug without a reproduction scenario. "This might fail" is useless. "This fails when X is empty because Y is undefined" is actionable.
- NEVER fix bugs during a hunt. Record them. Fixing during analysis changes the code under review and introduces noise.
- ALWAYS check: null/undefined, empty collections, boundary values, concurrent access, error propagation, and resource cleanup.

## Workflow

1. Identify high-risk structural areas: entry points, external input boundaries, shared state, and async boundaries.
2. Audit variables for null states, test edge cases, check for race conditions, review error paths, verify resource cleanup, and spot logic errors.
3. Trace 3-5 core user journeys step-by-step, evaluating system behavior during step failures, slow databases, double-submits, or cancelled requests.
4. Record every bug with its file:line, category, trigger, impact, and severity level, presenting a prioritized list without making code changes.
5. Provide a one-line fix, note if code or validation changes are needed, and state if a test is required for each bug.

Anti-patterns to avoid: relying solely on happy-path tests, hunting without a systematic plan, fixing bugs during analysis, limiting the search to recent code, and reporting issues without verified triggers.
