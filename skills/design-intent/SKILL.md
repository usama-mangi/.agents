---
name: design-intent
description: >
  Must load for any UI generation or remediation: forces named decisions (persona, style
  direction, motion personality) before a screen is written, and fixes existing AI output.
  Load for: new screens/pages/apps, "make this look better", remediation of AI-generated UI,
  design system choice, motion, marketing copy on UI surfaces. Composes with ui-ux-workflow
  (which keeps its four output gates).
---

# Skill: design-intent

**Core principle**: Decisions before pixels. The training-data mean is the default outcome of
any unsteered generation; the antidote is *named decisions made before generation* plus *rubric
judged after*. Knowledge files do not change behavior — decision points, sealed rollouts, and
visible gates do (the SkillsBench lesson: curated skills +16.6 pts, but only when the workflow
forces them to fire).

Mechanism being countered (see references for full research):
1. **Distributional convergence** — prediction returns the training-data mean (Krebs: 22% heavy
   slop across 1,590 Show HN pages; Inter/Tailwind-purple/3-card-grid/glassmorphism).
2. **RLHF diversity collapse** — Kirk et al. (arXiv:2310.06452): RLHF significantly reduces
   output diversity vs SFT; unprompted style choices land on the modal output.
3. **Prompter-as-reader** — the only reviewer an agent can see is the prompter, so copy drifts
   developer-ward unless a written persona gates it.
4. **Artifact boundary** — agents stop at "it compiles" (METR: ~50-min reliable horizon);
   market-ready is a deliverable matrix + gates, not a demo.

## Modes

Pick by the user's ask:

- **CREATE** — new UI from a brief. Run Phase A (intent), then build, then gate the output.
- **REMEDIATE** — UI already exists (often AI-generated) and must be improved: "make it look
  better / intentional / human / less AI". Run Phase R first, then gate.

If both apply (new pages in an existing remediated app), run CREATE for the new surface and
REMEDIATE once for the existing app before starting.

## Phase A — CREATE: the intent phase (nothing is built before this is green)

### A1. Audience block (persona gate)

Write the persona block before any copy or layout exists. Blocked until it exists:

- **Identity:** role, company type, seniority, day-in-the-life.
- **Pains** in their words (3–5 phrases they would actually say).
- **Objections:** top 3 reasons they don't buy.
- **Say / never-say vocabulary table** (the words they use vs. the words they'd never use).
- **Buying triggers:** the event that makes them look for a solution.
- **Proof formats they trust** (numbers, peer logos, case study, security docs, trial, phone).

Distill into one line for `design.yaml`: `project.audience`, plus `intent.audience` fields
(identity, pains, objections, say, never_say, triggers, proof_formats).

Distinguish **operator** (installs, maintains) vs **prosperer** (feels the outcome). Write for
the prosperer; give the operator their own section. Copy that exists before this block is a
violation — delete and rewrite, don't patch.

### A2. Style direction (sealed rollout + rubric)

A "direction" is one sentence naming a *system*, not a mood. "Clean modern minimal" is the
default wearing a hat — rejected on sight. Run a **sealed rollout**: 3–5 direction cards from
*different* source categories (domain metaphor / non-web media / era or subculture — never
three variants of "minimal but warm"), each written before any layout or screenshot. Then score
each on the weighted rubric and pick ONE:

| Criterion | Question | Weight |
|---|---|---|
| Distinctiveness | recognizable from one screenshot? | ×3 |
| Audience fit | does the persona's world look like this? | ×3 |
| Domain storytelling | does the style tell the product's story without words? | ×2 |
| Feasibility | buildable in this stack without heroics? | ×2 |
| A11y headroom | can it meet WCAG AA contrast/focus/motion? | ×2 |
| Scalability | survives 3 content types (marketing/app/docs)? | ×2 |

Record all scores (winners and runners-up) in `intent.style.rubric` in design.yaml. A hybrid is
allowed only with a named dominant. Tokenize the winner through ui-ux-workflow's token pipeline.

For raw material, consult [references/style-matrix.md](./references/style-matrix.md) — 16
non-default directions (editorial print, terminal, Swiss, neo-brutalist, risograph, cockpit,
botanical, …) with per-style type logic and token hints. Pick from different categories; three
variants of "minimal but warmer" is not divergence.

### A3. Motion personality (the motion gate)

Decide in writing before any keyframe exists. If this line is empty, generation does not start
("smooth and modern" is not a personality; it is the default wearing a hat):

| Personality | Physics | Springs (stiffness/damping) |
|---|---|---|
| Playful / consumer | overshoot, fast attack | soft (120–180 / 12–14) |
| Productive / utility | snappy, minimal overshoot | stiff (300–500 / 25–40) |
| Editorial / luxury | weighted, deliberate, long tails | heavy (mass 1.2–1.5, low stiffness) |
| Technical / dense | instant, tiny travel | none; duration-based |

Then implement to the craft bar in [references/motion-craft.md](./references/motion-craft.md):
springs for physical properties (transform/opacity/blur — never top/left/width/height in hot
paths), stagger children 20–60ms, exits faster and ease-in, shared-element continuity (FLIP) for
navigation, one direction system. The L-ladder: **L2 minimum everywhere** (choreographed
entrances/exits, stagger), **≥1 L3+ signature motion on brand surfaces** (shared-element, FLIP,
scroll-scrub, view transitions). Uniform delay+duration+curve on sibling elements is the #1
generated-motion tell — forbid it.

### A4. The intent gates (run before and after build)

- **Audience gate:** persona block exists, predates copy; zero prompter-only sentences
  (mirror-check: re-word each key claim into the persona's own words — if the native phrase is
  missing, rewrite). Operator/prosperer split mapped.
- **Style gate:** named direction ≠ "clean modern minimal"; rubric scores recorded; tokens
  derived from the direction (not Tailwind defaults); type is NOT Inter/Geist/Space Grotesk/
  Instrument Serif as the lone family unless the brief demands it.
- **Motion gate:** personality chosen; L2 min everywhere; ≥1 L3+ on brand surfaces; no uniform
  sibling timing; reduced-motion honored (fades/opacity, never raw removal); compositor-safe.
- **Delivery gate (market-ready):** all pages/states built (rest/hover/active/focus/loading/
  empty/error/success), real content (zero lorem/placeholder), launch assets (OG/meta/favicons),
  ops section if an operator exists. The run is done when the matrix is green, not when the
  code compiles. See [references/delivery-standard.md](./references/delivery-standard.md) for
  the full deliverable matrix and gate table.

A gate failure blocks ship. An exception must cite a **criterion and a compensating control**
("reduced-motion fallback only on hero — internal dashboard, no vestibular risk") — never a
fear ("animations might break"). Criterion vs rationalization is the enforcement line; a
rationalization names a fear, a criterion names the rule and the compensating control.

## Phase R — REMEDIATE: fixing existing AI-generated UI

The user brings existing UI. Do not rewrite from scratch; run this sequence:

### R1. Diagnose — run the intent scan, not just the slop scan

Run `python3 <this skill>/scripts/intent.py scan [--design-yaml design.yaml]` for a quick
structural read (checks design.yaml for intent blocks, tokens, slop flags; inspects source
files for the slop tells). Then read the screens and check the intent gates as *diagnostics*:

- **Audience diagnosis:** who is this for? Can you name the prosperer? Does any sentence only
  make sense to a developer/prompter? (Name-swap test on every headline.)
- **Style diagnosis:** name the system in one sentence. If the sentence is "clean modern
  minimal" (or unnamed), it has no direction — it is the default.
- **Motion diagnosis:** what job does each transition do (confirm/signal/relay/prevent)? Is
  anything above L2? Is sibling timing uniform? Is anything fade-in-carpet or bounce-everything?
- **Delivery diagnosis:** which deliverables are missing (states? real content? launch assets?
  ops section?). The gap list is the remediation backlog.

Produce a **diagnosis card**: named gaps per gate, each with the reference-file citation and a
severity (blocks-ship / hurts-trust / polish).

### R2. Re-decide — re-run Phase A on the gaps, with the existing constraints

For each blocking gap, re-run the corresponding intent phase (A1 for audience gaps, A2 for
style, A3 for motion, A4-delivery for artifact gaps), **reusing what survives**: tokens that
pass the slop scan and fit a direction, layouts that serve the persona, states that exist.
Preserve the user's working code where possible. The decisions must still be *named and
recorded* in design.yaml — remediation without recorded decisions recreates the default on the
next task.

### R3. Regenerate under constraints

Fix in this order (audience first — copy and structure follow it):
1. Audience: rewrite copy into persona vocabulary with proof formats; ops section if operator exists.
2. Style: apply the named direction's tokens (type, color, spacing, radius) across the surface.
3. Motion: add the personality-decided motion system (L2 everywhere, L3+ signature on brand).
4. States & delivery: fill the deliverable matrix gaps (empty/error/loading states, real
   content, launch assets).

### R4. Gate, then record

Run all four intent gates (A4) + the four ui-ux-workflow output gates (slop/a11y/system/
knowledge). Exceptions with cited criteria only. Then update design.yaml (`intent` block,
tokens, components, screens, log) and hand off to record-progress.

## design.yaml additions (this skill owns the `intent:` block)

```yaml
intent:
  audience:
    identity: <one line>
    pains: [<persona phrases>]
    objections: [<top 3>]
    say: [<native phrases>]
    never_say: [<words they'd never use>]
    triggers: [<buying triggers>]
    proof_formats: [<formats they trust>]
    operator_vs_prosperer: <who operates vs who prospers, one line each>
  style:
    direction: <one-sentence system name>
    rubric: { <candidate>: <total score>, ... }   # sealed rollout scores, incl. runners-up
    rejected: [<one-line reasons the runner-ups lost>]
  motion:
    personality: playful|productive|editorial|technical
    signature: <the one L3+ motion on brand surfaces, one line>
  delivery:
    gates_run: <ISO date>
    results: { audience: pass|fail, style: pass|fail, motion: pass|fail, delivery: pass|fail }
    exceptions: [<criterion-cited exceptions>]
```

## Rules

1. No generation before the intent block is green (A1–A3). No task closure before A4 + the four
   output gates.
2. REMEDIATE mode: never rewrite from scratch; diagnose → re-decide → regenerate under
   constraints → gate.
3. Every exception cites a criterion + compensating control; a fear is not a criterion.
4. The four output gates (slop/a11y/system/knowledge) still run — this skill adds the intent
   layer; it does not replace ui-ux-workflow.
5. Update `intent` block in design.yaml on every decision change; log in `log.recent_changes`.
6. Load `unslop` for any human-facing copy (persona copy especially).

## Study questions (loaded if the agent needs grounding)

1. Name the three mechanisms behind the four failure modes, with one line of evidence each.
2. What is a sealed rollout and why must it precede production work?
3. Operator vs prosperer — why does developer-marketing happen, and what's the fix?
4. What is the L-ladder rule (minimum everywhere, required on brand surfaces)?
5. Criterion vs rationalization — what makes a gate exception legitimate?

## References

- [references/design-failures.md](./references/design-failures.md) — the research: why agents
  play it safe (all four failure modes, with citations).
- [references/motion-craft.md](./references/motion-craft.md) — personality table, curves,
  springs, choreography, L-ladder, QA gates.
- [references/style-matrix.md](./references/style-matrix.md) — 16 non-default directions +
  token hints + rubric.
- [references/marketing.md](./references/marketing.md) — persona gate, operator/prosperer,
  segment-native vocabulary, channel gates.
- [references/delivery-standard.md](./references/delivery-standard.md) — artifact vs product,
  deliverable matrix, gate table, run loop.

Base directory for this skill: /home/usama-mangi/.agents/skills/design-intent
Relative paths are relative to this base directory.
