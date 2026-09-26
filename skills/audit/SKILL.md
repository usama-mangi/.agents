---
name: audit
description: >
  Use for any code analysis: debug failures, hunt bugs, security audit, code quality, or review. Replaces debug, bug-hunter, security-audit, code-quality, and review skills.
---

**Core principle:** Analyze before acting. Record findings with file:line. Fix only after analysis is complete.

## Rules

1. NEVER fix without reproducing (debug mode). Run the exact command, capture output.
2. NEVER apply more than one fix at a time. Change one thing, re-verify.
3. NEVER assume input is safe (security mode). Every external input is hostile until validated.
4. NEVER store secrets in code or logs.
5. NEVER report style issues as quality issues (quality mode). Formatting is the linter's job.
6. NEVER report a smell without context. "Long function" is a smell. "This function is 200 lines, handles 3 concerns, and has 8 branches" is actionable.
7. NEVER fix bugs during a hunt (bug-hunter mode). Record them. Fixing during analysis changes the code under review.
8. NEVER skip review because "it's a small change" (review mode).
9. ALWAYS quantify findings. "High complexity" is vague. "Cyclomatic complexity of 14 in function X" is useful.
10. ALWAYS report with severity: Critical / High / Medium / Low / Info.

## Modes

### Mode: debug

Triggered by: "fix [bug]", "error", "test failed", "this is broken"

1. Run the exact command that fails. Capture full error output.
2. Extract: error type, file:line, message, stack trace. Read stack trace bottom-up.
3. Narrow scope: single file vs multiple, new code vs existing, git diff of recent changes.
4. Form one hypothesis. Verify by reading code. If hypothesis doesn't match code, form a new one.
5. Apply one fix. Re-run the exact command from step 1. If it passes, proceed. If fails, go back to step 4.
6. Run full test suite, build, lint to confirm no regressions.

### Mode: bug-hunter

Triggered by: "find bugs", "bug hunt"

1. Identify high-risk areas: entry points, external inputs, shared state, async boundaries.
2. Audit for: null/undefined, empty collections, boundary values, race conditions, error paths, resource cleanup.
3. Trace 3–5 core user journeys step-by-step with failure scenarios.
4. Record every bug: file:line, category, trigger, impact, severity.
5. Provide one-line fix recommendation per bug. Do NOT modify code during hunt.

### Mode: security

Triggered by: "security", "check vulnerabilities", "harden"

1. Audit all API endpoints, user inputs, external integrations, secrets, session management.
2. Check injection: parameterized queries? Shell exec with user input?
3. Check auth: password hashing (bcrypt/scrypt/argon2), rate limiting, session token quality.
4. Check authorization: every endpoint? IDOR/BOLA? Server-side enforcement?
5. Check secrets: hardcoded keys? `.env` in `.gitignore`? Secrets in logs?
6. Check CORS, rate limiting, error leakage.
7. Check dependency CVEs (npm audit, pip check).
8. Report each finding: severity, OWASP category, file:line, trigger, impact, fix.
9. Sort by severity. Critical/High must be fixed before deployment.

### Mode: quality

Triggered by: "code quality", "code smells", "technical debt"

1. Run project tooling (linter, complexity analyzer, duplicate detector). Note if none configured.
2. Analyze by category:
   - Complexity: cyclomatic > 10, nesting > 3, params > 3 (especially booleans)
   - Duplication: copy-pasted blocks > 5 lines
   - Size: files > 300 lines, functions > 50 lines, classes > 500 lines
   - Coupling: circular deps, god objects, tight layer coupling
   - Naming: single-letter vars, obscure abbreviations, inconsistent conventions
   - Dead code: unreachable paths, unused imports, commented-out blocks
3. Rate readability, modifiability, testability, consistency (0–4 each).
4. Log each smell: category, file:line, quantification, impact, priority.
5. Sort into: quick wins, planned lifts, low-impact items.

### Mode: review

Triggered by: "review", "check my code", or as last gate before record-progress

1. Read the plan. Compare implementation: did it do what the plan said? Steps skipped? Unplanned changes?
2. Scan diff for `TODO`, `FIXME`, `HACK`, `console.log`, `debugger`, commented-out code.
3. Scan for secrets/credentials in code, logs, error output.
4. Check every external input: user input validated? API response handled? File read error handled? DB query error handled?
5. Check error handling: caught and handled? Useful error messages? Caller knows it failed?
6. Check naming consistency with surrounding code.
7. Check test coverage against plan's Definition of Done.
8. Report: issues found (file:line, severity), issues fixed, pass/fail recommendation.

## Finding Format

All modes report findings as:

```
[Severity] file:line — <description>
  Trigger: <how to reproduce>
  Impact: <what goes wrong>
  Fix: <specific remediation>
```
