---
name: add-dependency
description: >
  This skill must be used whenever adding a new dependency to a project.
---

- NEVER add unmaintained package
- NEVER add without checking license. A GPL package in a proprietary project creates legal liability.
- NEVER add for one utility function. Write the function yourself.
- ALWAYS record the addition as per the dev-workflow.
- ALWAYS verify after adding.** Build, tests, and lint must still pass.
- Search the codebase: does similar functionality already exist?
- Check if a transitive dependency already provides what you need. If it exists, use it. Do not add a duplicate.
- Try build, lint, and typecheck. If anything fails after installation, revert the installation and investigate.

Check these metrics:
- **Last publish date:** < 6 months is good; > 1 year is risky
- **Weekly downloads:** > 10K is established; < 1K is risky
- **Open issues:** > 100 unresolved is a red flag
- **Bundle size (frontend):** check bundlephobia or similar
- **Maintainers:** more than 1 = bus factor > 1

If the package fails multiple checks, look for alternatives.
