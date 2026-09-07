# AGENTS.md - The core

## What
<One paragraph: what the project is, what it does, who it is for. Be specific
about the product, not vague about "a tool for X". Name the audiences, the
core workflows, and the concrete value proposition.>

## Why
<Why does this project exist? What problem does it solve? What is the current
pain point or fragmented toolchain it replaces? Name the concrete alternatives
and why they are insufficient.>

## Standard
<What is the quality bar? Be specific. Examples:
- "Production grade for 1M+ users on every task"
- "MVP with real data, no mocks, but deferred polish"
- "Learning project, correctness over elegance"
Scope limits breadth, never depth: what is in the task is done completely.>

## Non-Negotiables
<List the hard constraints that apply to every task. Examples:
- Security: validate at boundaries, no secrets in code, least-privilege defaults
- Quality: tests before code where behavior matters; all gates green before commit
- Traceability: every change linked to a ROADMAP task via commit message
- Plans: no code without an approved plan file
- <Project-specific constraints> >

## Architecture
<What is the tech stack? Name languages, frameworks, key libraries, ports,
data flow. If there are multiple components (frontend, backend, database),
list each with its role.>
