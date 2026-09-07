---
name: debug
description: >
  Use when trying to debug after tests fail, errors occur, or code breaks. Use alongside implement-task when code fails. Do NOT use when issue is unknown (use bug-hunter skill first)
---

**Core principle:** Don't fix without reproducing. Read the error message first, try to solve later. Avoid random fixes.

## Rules

1. NEVER fix without reproducing. Run the exact command that fails. Capture the full error output. Don't fix without full context.
2. NEVER apply more than one fix at a time. Change one thing, re-verify.
3. NEVER ignore the error message. Read it. Extract: error type, file path, line number, message text, stack trace.
4. NEVER guess at a fix. Form a hypothesis ("I think X is null because Y"), verify the hypothesis by reading the code, then fix based on evidence.
5. NEVER add try/catch to swallow the error. That hides the symptom, not the cause. The error will surface elsewhere, worse.

## Workflow

1. Run the exact command that produces the error: the specific failing test, the build, or the code path that triggers the runtime error, and capture the full output or stack trace. If it doesn't reproduce, don't shrug it off as "works on my machine"; check for a different Node version, env vars, OS, or data, and reproduce in the same environment it actually failed in. Save the output; you'll reference it throughout.

2. Extract the error type (TypeError, ReferenceError, compilation error, assertion failure), the file and line number, the exact message, and the stack trace showing what called what. Read the stack trace bottom-up — it tells you exactly where the error originates, so don't skip past it. Write a one-sentence summary: "The error is [type] in [file:line] because [message]."

3. Narrow it down: is it one file or multiple, new code or existing, what changed last (check git log/diff), can you reproduce it with a minimal example. Find the smallest change that still produces the error.

4. State the suspected root cause in one sentence: "I think [variable] is undefined because [reason]," "I think [function] returns [unexpected value] because [reason]," "I think [dependency] changed its API because [evidence]." Then verify by actually reading the code and tracing the data flow. Don't assume something "should be null" without checking. If the hypothesis doesn't match the code, form a new one. Don't skip this step.

5. Apply one fix based on your hypothesis, not several changes at once hoping one sticks. Fix the cause, not the symptom: a null check that hides why something is null isn't a fix, and a try/catch that swallows the error just buries it for later. If line 47 is buggy, fix line 47. Don't rewrite the whole function. Re-run the exact command from Step 1: if it passes, proceed; if it fails, the hypothesis was wrong, go back to Step 4; if the same error persists, you missed something in Step 2, go re-read it.

6. Run the full test suite, build, and lint to confirm the fix didn't break anything else.
