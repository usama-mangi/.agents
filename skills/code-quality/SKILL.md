---
name: code-quality
description: >
  Must use this when code quality, code smell, code complexity, code duplication, clean code, technical debt, or maintainability is in question. Do not use for debugging (use debug/bug-hunter skill), ui assessment (use ui-specialist skill), securety audit (use security-audit skill)
---

**Core principle:** Prefer easy to understand, change and extend code over easy to write code. Prefer generic types over specific types. One type used to support multiple function signatures is better than 4 different functions serving almost same functionality. Modularity over simplicity.

## Critical Rules

1. NEVER report style issues as quality issues. Formatting is the linter's job. Quality is about structure, complexity, and maintainability.
2. NEVER report a smell without context. "Long function" is a smell. "This function is 200 lines, handles 3 concerns, and has 8 branches" is actionable.
3. NEVER suggest fixes during analysis. Record the smell, its location, and its impact. Fixes come after analysis.
4. ALWAYS quantify. "High complexity" is vague. "Cyclomatic complexity of 14 in function X" is useful.

## Workflow

1. Run whatever quality tools the project has configured. Linter (eslint, ruff, clippy, golangci-lint), complexity analyzer (plato, radon, complexity-report), duplicate code detector (jscpd, PMD CPD, similarity detector). If nothing's configured, note that as a finding.

2. Analyze by category
  - Check complexity: flag functions with cyclomatic complexity > 10, nesting > 3 levels deep, functions with > 3 parameters (especially booleans), and switch/case blocks with > 5 branches.
  - Check duplication: find copy-pasted blocks over 5 lines, similar functions that only differ by parameters, and repeated patterns that should be extracted into shared code.
  - Check size: flag files over 300 lines, functions over 50 lines, classes over 500 lines, and modules exporting too much.
  - Check coupling: look for circular dependencies, god objects that know about everything, tight coupling between layers (e.g. UI importing DB types), and parameters passed through multiple layers unnecessarily.
  - Check cohesion: flag functions doing multiple unrelated things, classes whose methods don't share data, and modules mixing business logic with I/O or formatting.
  - Check naming: flag single-letter variables (except loop counters), obscure abbreviations, names that don't match behavior, and inconsistent conventions within a module.
  - Check for dead code: unreachable paths, unused imports/variables/functions, commented-out blocks, and feature flags permanently stuck on.

3. Rate readability, modifiability, testability, and consistency each 0-4. Ask: can you understand it in one pass, change it safely, test it in isolation, does it match established patterns.

4. For each smell, log category, location (file:line or file:function), quantification (lines, complexity score, duplication count), impact (what it makes harder), and priority (fix now / fix soon / backlogged).

5. Sort findings into: high-impact quick wins first, high-impact heavy lifts to plan properly, low-impact quick fixes for spare time, low-impact heavy lifts to leave alone.
