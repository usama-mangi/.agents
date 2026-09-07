---
name: write-tests
description: >
  Guides test writing for any test type (unit, integration, e2e). Use when the
  user asks to write tests, add tests, improve coverage, or when implement-task
  needs tests written as part of a plan. Triggers: write tests, add tests, test
  this, need tests, testing, coverage, unit test, integration test, e2e, playwright,
  vitest, jest, pytest. This skill is loaded alongside implement-task when the plan
  includes test-writing steps. Do NOT use for running existing tests — just run them.
---

# Write Tests — Test Behavior, Not Implementation

This skill guides writing tests that verify behavior, catch real bugs, and
survive refactoring. It enforces the red-green pattern: see the test fail
before you see it pass.

**The core principle:** A test that always passes is not a test — it is theater.
A test that catches real bugs is worth maintaining. Write the latter.

## When This Skill MUST Be Used

- Plan includes "write tests" or "add test coverage"
- User asks to write tests for existing code
- implement-task step says "write test for X"
- User wants to improve test coverage

## When This Skill MUST NOT Be Used

- Running existing tests (just run the command)
- Debugging a failing test (use debug skill)
- Writing e2e smoke tests for deployment (follow project conventions)

## Critical Rules

1. **NEVER write tests after implementation without seeing them fail first.**
   Write the test, run it, confirm it fails (red), then implement (green).
   If you write a test that passes immediately, it tests nothing.

2. **NEVER test implementation details.** Test what the code DOES, not how
   it does it. Test rendered output, return values, side effects — not
   internal variable names, private methods, or component state.

3. **NEVER write assertion-free tests.** Every test MUST assert a specific
   outcome. A test with no assertions always passes and catches nothing.

4. **ALWAYS test the error path.** For every happy-path test, consider:
   what happens with bad input? Missing data? Network failure? Timeout?

## Workflow

### Step 1: Determine test type

| Type | What it tests | When to use |
|------|--------------|-------------|
| **Unit** | One function/component in isolation | Pure logic, utilities, small components |
| **Integration** | Multiple components working together | API routes, form submissions, data flow |
| **E2E** | Full user journey through the running app | Critical paths (auth, checkout, submit) |

Read the project's existing tests to match the type and framework used.

### Step 2: Identify what to test

Read the plan's Definition of Done. Each checkbox maps to testable behavior:
- "User can sign up with email" → test successful signup
- "Invalid email shows error" → test validation error path
- "Redirects to dashboard after login" → test redirect behavior

Also test:
- Edge cases (empty input, boundary values, max length)
- Error cases (network failure, invalid data, unauthorized)
- State transitions (loading → success, loading → error)

### Step 3: Read existing test patterns

Before writing, read 2-3 existing test files in the project:
- What framework? (vitest, jest, pytest, etc.)
- What patterns? (describe/it, test(), direct assertions)
- What utilities? (render, screen, fireEvent, mock, etc.)
- What naming convention? (filename, test descriptions)

Follow existing patterns exactly. Do not introduce new patterns.

### Step 4: Write the test

```typescript
// Example: unit test for a validation function
describe("validateEmail", () => {
  it("rejects empty string", () => {
    expect(validateEmail("")).toBe(false);
  });

  it("rejects missing @ symbol", () => {
    expect(validateEmail("userexample.com")).toBe(false);
  });

  it("accepts valid email", () => {
    expect(validateEmail("user@example.com")).toBe(true);
  });
});
```

Key rules:
- One assertion per test (or closely related assertions)
- Test name describes the behavior: "rejects X" / "returns Y when Z"
- Arrange → Act → Assert structure
- No side effects between tests

### Step 5: Verify it fails (red)

Run the test. It SHOULD fail because the implementation doesn't exist yet.
If it passes immediately, it tests nothing — rewrite it.

If testing existing code, the test should pass (proving the code works).

### Step 6: Implement (if writing new code)

Write the implementation that makes the test pass. Minimal — do not add
features the test doesn't cover.

### Step 7: Verify it passes (green)

Run the test again. It should pass. Run the full suite to check for
regressions.

## Anti-Patterns

- **Testing `typeof Component === 'function'`.** This tests that JavaScript
  works, not that your component works.

- **Snapshot tests for everything.** Snapshots test that output hasn't changed,
  not that output is correct. Use them sparingly.

- **Tests with no assertions.** `it("should work", () => { doSomething(); })`
  has no assertion. It always passes. It catches nothing.

- **Testing the mock instead of the code.** If your test mocks the database
  and asserts the mock was called, you tested the mock, not the logic.

- **Ignoring the error path.** "What if the API returns 500?" — your test
  should cover that.

- **Testing framework internals.** Don't test that React renders components
  or that Express routes requests. Test YOUR code's behavior.

- **Writing 100 tests for a utility but zero for the main feature.**
  Prioritize tests for the code that matters most.
