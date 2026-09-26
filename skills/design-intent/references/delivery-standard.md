# AI Agents — Market-Ready Delivery Standard

> **Category:** Design / AI / Delivery
> Companion to [[ai-agent-design-failures]]. The "how" for Failure 4 (artifact stopping point).
> Convergence of all four companion notes: the definition-of-done that turns "the code runs" into
> "the market can use it." Pairs with [[design-system-checklist]] (how the system gets built)
> and the Actionable checklists (the per-screen gates).

## Summary

An **artifact** is a technically-verified output: a snippet, demo, PoC, "hero section" — it runs,
so it passes the agent's only reward signal. A **product** is a market-verified output: all
deliverables exist, all gates pass, and the deliverables address a named audience through a
chosen style and motion system. The agent stops at the artifact boundary because artifacts are
what it can verify alone; the fix is a **delivery standard** — a deliverable matrix and gate
table that make the market-side of done *checkable*, so finishing the market-side earns the
reward. The run is done when the matrix is green, not when the code compiles.

## Artifact vs product (the boundary, precisely)

| Dimension | Artifact (agent default) | Product (market-ready) |
|---|---|---|
| Verified by | runs / compiles / renders | passes the gate table below + named-audience test |
| Design system | none / Tailwind defaults | named style direction + token sheet ([[ai-agent-style-matrix]]) |
| Motion | ambient fade-ins | personality-decided motion system ([[ai-agent-motion-craft]]) |
| Copy | developer-speak for the prompter | persona-block copy with proof formats ([[ai-agent-marketing]]) |
| States | happy path only | rest/hover/active/focus/loading/empty/error/success — the full state matrix |
| Content | lorem / placeholder | real copy, real imagery, real numbers or none |
| Deliverables | 1–2 code files | the full matrix below |
| Definition of done | code complete | matrix green + gates green |

## The deliverable matrix (all rows required for market-ready)

- [ ] **All pages/sections built** (not just hero or demo of one screen) — per the sitemap.
- [ ] **All states built** — rest/hover/active/focus/loading/empty/error/success for every
  interactive element (the state matrix from [[Interaction Design]]).
- [ ] **Real content loaded** — real copy, real imagery, real numbers (no lorem, no "AI-generated
  illustration with 6 fingers", no placeholder pricing).
- [ ] **Responsive behavior** — 3 breakpoints with *decided* behavior, not shrunk desktop.
  (Mobile is the default per the Actionable quick reference.)
- [ ] **A11y pass** — keyboard operable, visible focus, WCAG AA contrast, reduced-motion honored.
- [ ] **Performance pass** — compositor-safe motion, lazy images, no layout thrash; Lighthouse
  or equivalent run and reported.
- [ ] **Launch assets** — OG images, favicon set, meta descriptions, email assets if promised.
- [ ] **Ops section** — integration/security/uptime copy for the operator ([[ai-agent-marketing]]).
- [ ] **Style statement + token sheet** — the one-sentence system + primitive tokens on file.
- [ ] **Persona block on file** — audience, pains, objections, vocabulary, proof formats.
- [ ] **Motion personality + QA table** — personality row + gate results recorded.
- [ ] **QA artifacts recorded** — screenshot set, Lighthouse scores, gate table results.

## The gate table (each row yes/no; a no blocks shipping)

| Gate | Yes requires |
|---|---|
| **Audience gate** | persona block exists, predates copy; no prompter-only sentence (mirror-check) |
| **Style gate** | named direction ≠ "clean modern minimal"; token sheet exists; no Tailwind-default colors/spacing |
| **Motion gate** | personality chosen; L2 minimum everywhere, ≥1 L3+ on brand surfaces; 8 motion QA checks pass |
| **State gate** | full state matrix on every interactive element; empty/error states are helpful, not blank |
| **Content gate** | zero lorem/placeholder content; claims have proof formats the persona trusts |
| **A11y gate** | keyboard, focus-visible, WCAG AA contrast, reduced-motion, touch targets ≥44px |
| **Performance gate** | compositor-safe motion; no layout thrash; lazy media; scores recorded |
| **Ops gate** | operator section exists with operator vocabulary, separate from user path |

### Gating rule (make skipping visible)

A skipped gate must be **visible**: the run report includes the gate table with explicit yes/no
per row and a written rationale for any "no." (Rationale must cite a criterion, not a
rationalization — "animations might break" is a rationalization, "we reduced-motion fallback only
on the hero because internal dashboard" is a criterion-cited exception.) The difference is
criterion vs rationalization: a criterion-cited exception names the criterion and the
compensating control; a rationalization names a fear. This is the vault's
[[ai-agent-skills]] lesson: rules bind only when violations are visible.

## The run loop (how a market-ready run actually goes)

1. **Brief** — audience/persona block, product story, channel list, success metric.
2. **Style Matrix** — sealed rollout of 3–5 directions → scored rubric → named direction →
   primitive tokens.
3. **Motion personality** — chosen from brand character; curves/durations/springs tokenized.
4. **Build** — tokenized build per [[design-system-checklist]]; screens as instances of the
   system; state matrix per element.
5. **Content** — persona copy with proof formats; real imagery; ops section.
6. **QA gates** — the gate table, run and recorded; exceptions with cited criteria.
7. **Launch assets** — OG/meta/favicons/email.
8. **Retrospective** — score the shipped page against the 60-second self-audit in
   [[ai-agent-design-failures]].

## Common agent failure patterns

- **The demo trap** — one beautiful screen, no states, no content, no other pages.
- **The placeholder economy** — lorem, gray boxes, "Screenshot coming soon", fake numbers.
- **The promised-matrix gap** — claims "responsive" without decided breakpoints, or "a11y" without keyboard pass.
- **The gate skip** — gates exist, run report claims all green without recording results (the Rationalization Loophole in delivery form).
- **The retrospective skip** — no self-audit run; next run inherits the same defaults.

## Connections

- **related to:** [[ai-agent-design-failures]] — Failure 4; the artifact-vs-product boundary.
- **related to:** [[ai-agent-style-matrix]], [[ai-agent-motion-craft]], [[ai-agent-marketing]] —
  the three companion "how" notes the gates enforce.
- **related to:** [[design-system-checklist]] — the build pipeline after style convergence.
- **related to:** [[Interaction Design]] — the state matrix requirement.
- **related to:** [[Usability & User Testing]] — the 5-user test as the empirical gate where
  budget allows.
- **related to:** [[UX Metrics & Measurement]] — success metric from the brief becomes the
  measured outcome.
- **related to:** [[ai-agent-skills]] — visibility rule; rationalization vs criterion.
- **related to:** [[good-vs-bad-frontend-design]] — the factors the gates enforce.
- **related to:** [[ai-slop-web-design]] — the tells the gates catch (badge-over-H1, lorem, fake
  numbers, "screenshot coming soon").

## Study / recall questions

1. Artifact vs product — name the dimension list from memory.
2. The deliverable matrix: name 6 of the 12 rows.
3. Gate table: what makes an exception legitimate (criterion vs rationalization)?
4. The run loop: name the 8 steps in order.
5. Why must a skipped gate be visible in the run report?

## Sources

- Vault: [[ai-agent-design-failures]] (artifact boundary, METR horizon), [[ai-agent-skills]]
  (Rationalization Loophole, eval-gated changes), [[design-system-checklist]] (token pipeline),
  [[Interaction Design]] (state matrix), [[UX Metrics & Measurement]] (success metric),
  [[ai-agent-style-matrix]] / [[ai-agent-motion-craft]] / [[ai-agent-marketing]] —
  the three "how" notes the gates enforce.
- METR — *Measuring AI Ability to Complete Long Software Tasks* (arXiv:2503.14499).
