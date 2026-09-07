---
name: review
description: >
  Must use when a task is proposed as complete. It is the last gate before record-progress.
---

**Core principle:** You should never review your own work. Check the changes from third person perspective.

## Rules
1. NEVER skip review because "it's a small change." Small changes cause big bugs. The review takes 2 minutes; debugging the unreviewed change takes 20.
2. NEVER approve without checking: TODOs, secrets, error handling, naming. These four categories catch 80% of real issues.
3. NEVER review only the files you changed. Check how your changes fit with surrounding code. Does the import make sense? Does the naming match the module's conventions?

## Workflow
1. Read the plan. For each implementation step: Did the code do what the plan said? Were any steps skipped? Were any unplanned changes made? Report deviations to the user.
2. Search the diff for `TODO`, `FIXME`, `HACK`, `XXX`, `WORKAROUND`, `console.log`, `console.debug`, `console.warn` (leftover debugging), commented-out code blocks, `debugger` statements, hardcoded values that should be configurable. If found, fix or remove before recording done.
3. Scan the diff for API keys, tokens, passwords, connection strings, hardcoded credentials, `.env` files or secret values in code, secrets in log messages or error output. If found, remove immediately. Never commit secrets.
4. For every external input in the diff, check:
  - User input: validated? Sanitized?
  - API response: handled? Error case covered?
  - File read: exists? Permission error handled?
  - Database query: connection error? Query error?
5. For every function that can fail: Is the error caught and handled? Is the error message useful (not just "Error")? Does the caller know it failed? Compare the diff with surrounding code:
  - Variable/function names follow the project's naming convention?
  - File naming matches the module's pattern?
  - Import style matches (named vs default, path style)?
  - Error handling pattern matches (throw vs return null vs Result type)?
7. Check test coverage. Does the plan's Definition of Done have test requirements? Are there tests for the new/changed code? Do the tests cover error paths? Do tests actually assert meaningful outcomes?
8. Report findings. Summarize:
  - **Issues found:** list each with file:line and severity (block/warn/info)
  - **Issues fixed:** what you corrected during review
  - **Pass/overall:** can this proceed to record-progress?
