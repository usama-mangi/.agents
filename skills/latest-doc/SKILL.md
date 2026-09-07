---
name: latest-doc
description: >
  Must use this skill before using any library, framework, API, or platform the agent is not certain about. Use when the agent encounters an unfamiliar tool, version-specific behavior, config options, API signatures, or anything it might guess wrong about. Also use when implementing with any third-party dependency even familiar ones if the project uses a recent version. This is a cross-cutting skill: load it alongside plan-task, implement-task, or any skill that touches external code.
---

**Core principle**: Admit uncertainty and fetch real documentation instead of hallucinating API details, config options, or version-specific behavior.

## Rules

1. NEVER state an API signature, config option, or method name without verification. If you cannot fetch the docs, say "I don't know the exact signature, let me check."
2. NEVER assume the version. "React supports X" is meaningless without knowing which React version. Always check what version the project uses, then verify against that version's docs.
3. NEVER use training data as ground truth for external APIs. Your training data is months to years old. APIs change, methods are deprecated, config options are renamed. Always verify.
4. ALWAYS say "I don't know" when you don't know. This is not a failure, it is the correct behavior. Hallucinating a wrong answer IS a failure.
5. ALWAYS prefer official docs over secondhand sources. Official documentation > GitHub README > Stack Overflow > blog posts. Fetch the official source first.

## Self-Assessment Gate

Before using any external library/framework/API, answer these three questions:
### Question 1: Have I used this specific version before?
- **Yes, in this project** → Proceed (you've seen the actual code)
- **Yes, but a different version** → FETCH DOCS (versions diverge)
- **No** → FETCH DOCS
### Question 2: Can I state the exact API signature from memory?
- **Yes, exactly** → VERIFY (double-check, you might be wrong)
- **Approximately** → FETCH DOCS (approximate = wrong)
- **No** → FETCH DOCS
### Question 3: Has this library released a major version recently?
- **No / Not sure** → FETCH DOCS
- **Yes, but I know the changes** → VERIFY

**If ANY answer is "FETCH DOCS" or "VERIFY", fetch the docs. Do not proceed from memory alone.**

## Workflow

1. Read the `memory.md` file once. If the library, framework, or API is already documented use that information.
2. If the required information is not in `memory.md` file, fetch official docs for the specific use case.
3. After fetching docs, note in `memory.md`:
  - "Verified: `ComponentProps` is the correct type in React 19 (not `Props`)"
  - "Checked: Next.js 16 removed `next/image` legacy API, use `next/legacy/image`"
  This prevents re-fetching the same docs and documents the verification.
4. Docs > Personal knowledge. If docs differ from your expectations use docs.
