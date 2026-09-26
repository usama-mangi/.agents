# AI Agent Design Failures — Why Models Play It Safe (Animation, Design Systems, Marketing)

> **Category:** Design / AI / Agents
> Root cause file for four observed agent behaviors: (1) animations collapse to fade-in/bounce;
> (2) visual systems collapse to minimalism or glassmorphism; (3) marketing copy targets
> developers instead of the buyer; (4) output is "code-generated artifacts" (snippets, demos)
> instead of market-ready product. Companion "how" notes:
> [[AI Agents — Motion Craft Beyond Fade & Bounce]],
> [[AI Agents — Style Matrix Beyond Minimalism & Glassmorphism]],
> [[AI Agents — Market-Ready Marketing That Sells to the Audience]],
> [[AI Agents — Market-Ready Delivery Standard]].
> Extends the mechanism already documented in [[ai-slop-web-design]] to *agent* behavior.

## Summary

The four failures are the same failure. A generation step inside a long task is **risk-loaded,
unattributed, and unsupervised** — so the model reaches for the **modal output** (the training-data
mean), the **lowest-variance** choice (the one least likely to break the run), and the **audience it
can verify against** (the person who wrote the prompt). None of this is a taste defect; it is a
reward structure. Every fix must therefore change the *reward structure* the agent experiences —
named decision points, sealed rollouts, ad hoc scoring rubrics, named audiences, hard delivery
gates — not just ask for "more creativity," which reliably produces louder defaults, not different
ones.

The three mechanisms (from the vault's [[ai-slop-web-design]] plus agent-behavior research):

1. **Distributional convergence (regression to the mean).** LLMs are prediction engines: the most
   likely completion is the most common one in training data, and the most common web aesthetic
   is Inter, fade-ins, Tailwind indigo, minimalism and glassmorphism. Asking for "modern" *narrows*
   the distribution further, because "modern" is culturally codified as one narrow look. (Krebs'
   16-pattern fingerprint: 22% heavy slop on 1,590 real Show HN pages.)
2. **RLHF-driven diversity collapse.** Kirk et al. (arXiv:2310.06452, Meta AI): RLHF "significantly
   reduces output diversity compared to SFT." Instruction-tuning optimizes for the response most
   raters called good → a narrow preference ridge, so when agents choose a style unprompted they
   choose the modal one. ("Mode collapse" is the colloquial term.)
3. **No fixed reviewer to design against.** Human designers iterate against art directors, users,
   and payers. An agent has none, so it cannot receive aesthetic pushback, and "trust my aesthetic
   call" is exactly the judgment RLHF taught it to defer. (LangChain's own agent-reliability
   guidance: unbroken tasks fall out of sync "without external feedback in the loop.")

## The four failures, one by one

### Failure 1 — Animations collapse to fade-in, bounce, "not enough motion"

Agent frugality: transitions are **risk tokens**. Every keyframe is a chance to break layout,
drop frames, or clip — and (see Failure 4) the run's real reward is not breaking things. So the
agent emits the cheapest tokens that satisfy "animated" (opacity 0→1, spring overshoot) and spends
its budget on wiring state. Secondary causes: UI-event data is scarce in training corpora
(hover/drag/scroll micro-motion is under-represented next to static screenshots); springs animate
**physical properties** (x, scale, rotate, blur — compositor-friendly) while gradients, widths and
shadows trigger layout and paint; and RLHF raters scored "subtle" animations good and "showy" ones
bad, so unsteered agents regress to no-motion-at-all.

### Failure 2 — Visual systems collapse to minimalism or glassmorphism

The two styles are the **low-variance attractors** of the training distribution (Tailwind/shadcn
defaults + the frosted-glass card), each reads "safe/modern" on its own, and glassmorphism is
computationally *expensive* (per-frame blur = rasterization cost) which makes it look like craft
without any composition risk. Notably, Krebs' data shows these styles appear **with** the slop
tells (Inter, Tailwind purple, 3-card grids) — they're not the slop's *opposite*, they're its
*uniform*. Asking for either by name is asking for the prior.

### Failure 3 — Marketing collapses to developer-speak

The prompt *is* the reader. The only reviewer an agent reliably has is the person (or agent harness)
that wrote it, and that person **talks like a developer**. Optimizing for approval means writing
copy the prompter would upvote: technical claims, feature lists, architecture-speak — not the
persona's outcome language. Agents also lack a **market** (real users/buyers/competitor benchmarks)
to verify against, so "tech-bro marketing" is the modal safe output. Related defaults: vague
aspirational copy, mad-libs ("The AI-powered X for modern Y"), the buzzword list (seamless,
unlock, empower), exactly-five-item lists, em-dash rhythm.

### Failure 4 — Output is "code-generated artifacts," not a market-ready product

The agent optimizes **what it can verify**: code that runs, a demo that renders. Nobody scores
conversion, brand recall, or "would a buyer trust this with a credit card." So it ships snippets —
a hero mock, a fragment, a PoC — and stops. This is a **task-horizon problem** (METR, arXiv:2503.14499:
frontier agents' 50%-success horizon ≈ 50-minute human tasks) colliding with the fact that
**market-ready design is a long-horizon, multi-stage task** (brief → research → direction →
system → build → polish → QA → launch assets). The agent stops at the artifact boundary because
the artifact is where its verified competence ends. It also conflates *function* with *market*:
"it compiles" ≠ "someone would pay."

## The remediation map (why the companion notes are shaped the way they are)

Each fix targets the mechanism, not the symptom:

| Mechanism | Fix class | Where |
|---|---|---|
| Modal output / mean reversion | **Named decision points** — force an explicit style/motion/voice choice before generation; forbid defaults-by-silence | Style Matrix, Motion Craft |
| Low variance (risk aversion) | **Sealed rollouts** — generate explorations *before* deciding, never after; pick **before** you're attached | Style Matrix (divergent phase) |
| Unattributed, unsupervised choice | **Ad hoc scoring rubrics** — score every candidate against 5–7 weighted criteria on 1–5, in writing | Style Matrix, Motion Craft, Marketing |
| No reviewer → write for the prompter | **Named audience** — a written persona block (role, pains, objections, vocabulary, buying triggers) **before** any copy; the audience, never the prompter | Marketing |
| Artifact stopping point | **Definition of done as deliverable list** — the run is done when the listed assets exist and pass gates, not when code runs | Delivery Standard |
| Unverified aesthetic claims | **QA as reward** — reduced-motion, no-layout-thrash, contrast, mobile, dead-click checks | Motion Craft, Delivery Standard |

### Two meta-lessons from the vault's [[ai-agent-skills]] findings

1. **Skills alone don't fix this.** SkillsBench (2026): curated skill files add ~16.6 points on
   average, but 13/87 tasks *regressed*, and model-generated skills scored **below baseline**.
   Knowledge is only half the lever; the other half is a **reward structure** that makes the
   knowledge fire: gates, rubrics, named decisions. That's why each companion note is written as
   *procedure + gate*, not prose.
2. **Cheating happens.** UPSKILL.md's #1 failure is the "Rationalization Loophole": agents follow
   rules until they conflict with the goal, then rationalize ("animations might break layout, so
   fade-in is fine"). A skill with no consequence doesn't bind. Practical consequence here:
   write the rules as **checkable gates** (the Delivery Standard's table is a yes/no grid), so a
   skipped gate is *visible* in the transcript, not absorbed into a rationalization.

## The 60-second self-audit (run before shipping any generated UI)

1. **Motion:** what job does each transition do (confirm/signal/relay/prevent)? Is anything
   motion-superpower-class (parallax, shaders, FLIP, scroll-scene)? Or is it all fade/slide?
2. **Style:** name the system in one sentence ("editorial print," "Swiss brutalist," "playful toy").
   If the sentence is "clean modern minimal" — you have the default. Re-run the Style Matrix.
3. **Copy:** does any sentence only make sense to a developer? Run the name-swap test. Who is
   the named audience, and would *they* say these words?
4. **Artifact check:** list the deliverables the *market* needs (pages, states, assets, copy,
   launch plan). How many exist vs. how many exist? The gap is the slop.

## Concepts & terms

- **Distributional convergence / regression to the mean** — prediction returns the training-data
  mode; constraint is what breaks the default (see [[ai-slop-web-design]]).
- **Mode collapse / preference ridge** — RLHF narrows output diversity; the agent's unprompted
  style choice is the modal one (Kirk et al. 2023).
- **Unattributed design decision** — a choice with no owner, no rationale, no alternatives
  considered — the signature of agent output.
- **Artifact** — a technically-verified but market-unverified output: snippet, demo, PoC.
- **Reward-structure failure** — the agent's reward (completes-run, doesn't-break, prompter-
  approval) is misaligned with the user's reward (memorable, converts, market-ready). Fixes must
  change the reward, not the adjectives.
- **Sealed rollout** — generating N candidates before choosing, so the pick is made without
  attachment (divergence before convergence).

## Connections

- **related to:** [[ai-slop-web-design]] — the same distributional convergence, documented at
  *website* level; this note extends it to *agent behavior* level (frugality, artifact boundary,
  prompter-as-reader).
- **related to:** [[Representation Collapse]] (ML) — output-space collapse: generators collapse
  prompts toward the modal output; contrastive-style constraint layers (rubrics, named decisions)
  are the decode-side antidote.
- **related to:** [[good-vs-bad-frontend-design]] — the evaluative lens these failures violate
  (fit/trust, hierarchy, specificity).
- **related to:** [[design-system-checklist]] — the constructive build route: tokens *before*
  screens is what makes deliberate choices enforceable instead of aspirational.
- **related to:** [[ai-agent-skills]] and [[prompt-engineering]] — knowledge files only bind when
  paired with a reward structure (gates, rubrics, named decisions) — the SkillsBench + UPSKILL.md
  lesson.
- **related to:** [[JEPA]] (conceptual) — slop is what happens when prediction is unregulated by an
  abstraction/constraint layer; the rubric-and-gate stack here is that layer, agent-side.

## Study / recall questions

1. Name the three mechanisms behind all four failures and give one line of evidence each.
2. Why does RLHF reduce diversity (Kirk et al.), and what does that predict about unprompted
   style choices?
3. Why is "prompter-as-reader" the mechanism behind developer-marketing, and what's the fix?
4. What is the "artifact boundary," and which two facts (METR + verification asymmetry) produce it?
5. Why do the companion notes encode *gates* rather than advice? (Two meta-lessons from SkillsBench
   + UPSKILL.md.)

## Sources

- Kirk, Mediratta, Nalmpantis, Luketina, Hambro, Grefenstette, Raileanu — *Understanding the Effects
  of RLHF on LLM Generalisation and Diversity* (arXiv:2310.06452; Meta AI/FAIR & UCL, ICLR 2024):
  "RLHF significantly reduces output diversity compared to SFT across a variety of measures."
- Kwa et al. — *Measuring AI Ability to Complete Long Software Tasks* (arXiv:2503.14499; METR,
  NeurIPS 2025): 50%-task-completion time horizon ≈ 50 min for frontier models (doubling ~every 7
  months); gains driven mainly by reliability and error recovery.
- Adrian Krebs — *Scoring Show HN submissions for AI design patterns* (adriankrebs.ch/blog/design-slop):
  16 deterministic DOM/CSS checks on 1,590 pages; 22% heavy / 32% mild / 46% clean.
- LangChain — *How to Think About Agent Reliability* (blog.langchain.com): unbroken long tasks
  fall out of sync "without external feedback in the loop"; reliability is economic (late-failure
  costs rise with autonomy), which is why agents retreat to verified-safe steps.
- Motion (motion.dev) — *React Animation* docs: springs animate physical properties; opacity/color
  use duration-based easing; transform-only animation = compositor-safe; MotionScore for Agents.
- NN/g — *Executing UX Animations: Duration and Motion Characteristics* (Page Laubheimer, 2020):
  150–500ms budgets, easing, trigger/transform/duration/easing model, vestibular warnings.
- Rauno Freiberg — *Invisible Details of Interaction Design* (rauno.me/craft/interaction-design):
  real-world physics metaphors (interruptability, momentum, trigger-during-gesture), the craft
  vocabulary missing from agent output.
- Vault: [[ai-slop-web-design]], [[ai-agent-skills]], [[good-vs-bad-frontend-design]],
  [[design-system-checklist]].
