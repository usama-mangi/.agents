---
name: ideate
description: >
  Must load this skill when the user has a vague concept, rough idea, or half-formed thought about a project and needs to convert it into a concrete, actionable project brief. This is the FIRST step before initialize-project. Do NOT use when the user already has clear requirements, go straight to initialize-project.
---

**Core principle**: A rough idea is not a requirement. The agent's job is not to agree with the idea it is to **pressure-test it, fill gaps, surface assumptions, and force specificity**. The interview should feel like talking to a sharp technical co-founder who pushes back on hand-waving.

## Rules

1. NEVER accept the first answer as final. The user's first response is always vague. Follow up. Ask "why", "who specifically", "what does that look like", "can you give an example". Push for specificity.
2. NEVER skip a round.
3. If the user hasn't specified something, ask. NEVER guess the tech stack, the users, or the quality bar. The brief must come from the user's intent, not the agent's.
4. NEVER output the brief until the user confirms it. After writing project brief, show it to the user. Ask: "Is this accurate? What am I missing?" Revisions are expected.
5. NEVER let the interview run forever. If after 3 rounds on a topic the user is still vague, note it as an open question in the brief and move on. Perfect clarity on everything is not required clarity on the core is.

## Interview Rounds

Conduct these rounds in order. Each round has a focus and specific questions. Adapt follow-ups based on answers: these are starting points, not scripts.

### Round 1: The Seed

**Goal:** Get the raw idea in the user's own words.
Ask:
  - "In one or two sentences, what do you want to build?"
  - "What sparked this idea?"
  - "Is this for you, for others, or both?"
Listen for: the core action (what does the thing DO), the motivation (WHY), the audience (WHO). If the user gives a one-liner, push for one more sentence.

### Round 2: The Problem

**Goal:** Understand what problem this solves and why current solutions fail.
Ask:
  - "What problem does this solve? Who has this problem?"
  - "How do people solve this today? What tools/workarounds do they use?"
  - "What's broken or frustrating about the current way?"
  - "How would you know this problem is real — have you seen it yourself?"
Listen for: concrete pain points (not abstract ones), evidence the problem exists, existing alternatives and their gaps.

### Round 3: The User

**Goal:** Define exactly who will use this and what they need.
Ask:
  - "Who is the primary user? Be specific — not 'developers' but 'junior frontend devs at startups with 2-10 people'."
  - "What is their workflow today? Walk me through a typical session."
  - "What would they do differently with your tool?"
  - "Are there secondary users? Who else interacts with this?"
Listen for: user personas emerging, workflow steps that map to features, constraints the user faces.

### Round 4: The Product

**Goal:** Define what the thing actually does.
Ask:
  - "What are the 2-3 core things this must do on day one?"
  - "What does the user SEE? Is it a web app, CLI, API, mobile app?"
  - "What's the most important user journey — from start to finish?"
  - "What's explicitly NOT in v1? What can wait?"
Listen for: feature boundaries, concrete UI/interaction descriptions, MVP scope vs future vision.

### Round 5: The Tech

**Goal:** Define technical constraints and preferences.
Ask:
  - "Do you have a preferred tech stack? Or should I recommend one?"
  - "Is there existing code? What's already built?"
  - "Any constraints? (must use X, cannot use Y, budget, timeline)"
  - "Does this need authentication, a database, real-time features?"
Listen for: hard constraints (must-use / cannot-use), existing code to integrate with, scale expectations.

### Round 6: The Standard

**Goal:** Define quality bar and success criteria.
Ask:
  - "What's the quality bar? Production-grade, MVP, or learning project?"
  - "How will you know it's working? What does 'done' look like?"
  - "Any accessibility, performance, or security requirements?"
  - "How many users do you expect in the first month? First year?"
Listen for: quality expectations, measurable success criteria, scale assumptions.

### Round 7: The Boundaries

**Goal:** Define what is explicitly out of scope.
Ask:
  - "What should this NEVER do? What's explicitly out?"
  - "Any features you've seen in similar tools that you DON'T want?"
  - "Any moral/ethical/privacy constraints?"
Listen for: negative scope, anti-features, hard boundaries.

## Output

After all rounds, synthesize the interview into a project brief. The brief serves as input for `initialize-project`. Show the brief to the user and ask: **"Is this accurate? What should I change?"** Revisions are expected. Do not proceed until the user confirms.

## Handoff to initialize-project

After the user confirms the brief, run `initialize-project` to create the full workflow files (`AGENTS.md`, `project-backlog.json`, and `docs/`) from this brief.
