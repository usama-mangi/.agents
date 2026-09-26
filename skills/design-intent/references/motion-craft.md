# AI Agents — Motion Craft Beyond Fade & Bounce

> **Category:** Design / AI / Motion
> Companion to [[ai-agent-design-failures]]. The "how" for Failure 1 (animation collapse).
> Extends [[Animation & Microinteraction]] (the vault's motion *science*: Saffer's four jobs,
> 150–500ms budgets, reduced-motion) with the *craft* layer agents skip: named motion systems,
> curve literacy, spring tuning, and choreography. Read the science note first; this note is
> what "the animation is designed" means operationally.

## Summary

Agents produce fade-ins because fade-in is the **modal answer** to "add animation" — and asking
for "smooth animations" makes it worse, because "smooth" is also a token of the default. Escape
requires the same move as human craft: a **motion system decided up front** (personality →
curves → durations → choreography rules), and then **implementation budget spent on
transform-driven, interruptible, causally-motivated motion** — springs for physical properties,
staggered choreography instead of uniform delays, and shared-element transitions instead of
cross-fades. The output test: an animation should be describable as a *sentence* ("the card lifts
toward you and the page dims behind it"), never as a *property* ("opacity 0 to 1").

## Step 1 — Decide the motion personality BEFORE any keyframe (the gate)

Motion personality must derive from **brand character**, not from "what looks alive." Decide in
writing, name it, forbid silence:

| Personality | Physics | Typical curves | Spring tuning (stiffness/damping/mass) |
|---|---|---|---|
| **Playful / consumer** | Exaggerated overshoot, fast attack | springy; anticipation before action | soft springs (stiffness ~120–180, damping ~12–14) |
| **Productive / utility** | Snappy, minimal overshoot | ease-out entrances, ease-in exits | stiff springs (stiffness 300–500, damping 25–40) |
| **Editorial / luxury** | Weighted, deliberate, longer travel | long ease-out tails, big distance-proportional durations | heavy mass (1.2–1.5), low stiffness |
| **Technical / dense** | Instant, tiny travel | 80–150ms, nearly linear | no springs; duration-based only |

The gate: **if the personality line is empty, generation does not start.** ("Smooth and modern"
is not a personality; it is the default wearing a hat.)

## Step 2 — Curve & duration literacy (the vocabulary agents lack)

- **Ease-out for entrances, ease-in for exits, never bare `linear` for UI** — linear reads
  mechanical because nothing in the world moves that way. Complex `cubic-bezier` curves with
  long tails read *designed*; the CSS default (`ease`) reads *generated*.
- **Distance-proportional duration** — larger travel = slightly longer time so *speed* feels
  constant. A fixed 200ms on a 10px travel and a 400px travel is the tell of generated motion.
- **Micro vs macro budgets** (from [[Animation & Microinteraction]] / NN/g): micro-transitions
  150–300ms; scene/page transitions 300–500ms; nothing routine above 500ms.
- **Frequency scaling** — the more often a user meets an animation, the shorter and subtler it
  must be. (NN/g: "the more frequent the animation, the more subtle and shorter you'll want it.")
- **The language of beats** — treat a transition as *arrive → settle → rest*; a single tween is
  one beat. Choreography (Step 4) is what adds beats.

## Step 3 — Spring physics over keyframes for anything physical

The single highest-leverage technical switch: animate **compositor-friendly physical properties**
(`transform: translate/scale/rotate`, `opacity`, `filter: blur`) and drive positional/scale
change with **springs, not durations**. Springs carry velocity through interruptions (a user
re-targets mid-flight and the motion *reattaches* instead of restarting), which is the
"interruptability" property Rauno identifies as the invisible signature of great interaction.

- Libraries: Motion (Framer Motion) — `type: "spring"` for x/scale/rotate; duration-easing only
  for opacity/color. GSAP timelines for sequences. CSS `linear()` easing for one-off custom
  curves without JS.
- **Tune, don't accept defaults.** Default spring = generated look. Adjust stiffness/damping/mass
  per the personality table; overshoot should exist where playfulness lives, be absent where
  precision lives.
- **FLIP for layout changes** (First-Last-Invert-Play): element moves are measured, inverted, and
  played as transforms — this is how shared-element transitions (card → detail page) work and
  why they feel physical instead of like a cross-fade.

## Step 4 — Choreography: stagger, orchestrate, exit (the anti-uniform rule)

Agents animate every element identically and simultaneously; humans choreograph:

- **Stagger children** 20–60ms per item (lists, cards, nav items) — the arrival reads as a
  *wave*, not a wall. Uniform timing on 6+ elements is the #1 generated-motion tell.
- **Orchestrate exits differently from entrances** — exits are faster, ease-in, and often
  collapse toward the trigger (not the reverse of the entrance).
- **Shared-element continuity** — when navigating, one element (image, card, title) visibly
  *becomes* the next screen's element (Gestalt common fate; the user tracks object identity).
  Cross-fade + slide is what you do when you haven't decided what continues.
- **One direction system** — forward = left→right, back = right→left, modal = rises from its
  trigger, destruction = downward/away. Mixed directions = no decided spatial model.
- **Hierarchy of motion** — one element leads (largest/longest), others follow shorter and
  quieter. Everything moving with equal weight = motion noise (cognitive-load failure per
  [[Animation & Microinteraction]]).

## Step 5 — The motion-superpower ladder (what agents never attempt)

Escalation ladder from "safe" to "signature." Any UI above "L2" signals a human decision:

- **L1 — State feedback** (press, hover, toggle, focus rings): table stakes; Saffer's
  confirm/signal/prevent jobs.
- **L2 — Entrance/exit choreography** (staggered lists, orchestrated modals): the minimum bar
  for "designed."
- **L3 — Spatial continuity** (shared-element transitions, view transitions API, FLIP morphs,
  tab indicators that slide with the selection): the UI has a *physics model*.
- **L4 — Scroll-driven scenes** (scrub-tied parallax with `scroll-timeline`/IntersectionObserver,
  pinned sections, progress-linked reveals — velocity-matched, not time-based): the page
  responds to *input energy*.
- **L5 — Generative/canvas/shader motion** (WebGL/canvas particles, liquid/mesh shaders,
  physics sims as brand moments): costly; deploy in one hero moment, never everywhere.
- **L6 — Adaptive motion** (reduced-motion fallbacks that aren't just "no motion" — opacity
  and contrast paths; prefers-reduced-data; input-responsive micro-detail like cursor magnets,
  magnetic buttons, drag-with-momentum).

**Gate:** every generated UI must reach **L2 minimum**, and every brand surface (hero, landing,
campaign) must include at least one **L3+** signature motion. If everything is L1, the run is
not done.

## Step 6 — The QA gates (each must pass or the note "fails")

| Gate | Check |
|---|---|
| **Interruptible** | re-click mid-animation → no restart jump, no dead click during transition |
| **Reduced-motion** | `prefers-reduced-motion` honored — fades/opacity swaps, never raw removal |
| **Compositor-safe** | no `top/left/width/height` animation in hot paths; transforms/opacity only (no layout thrash in DevTools performance trace) |
| **60fps budget** | no frame drops on a mid-range device; blur/backdrop-filter counted as cost |
| **Beat check** | every transition describable as a sentence with a direction and a settling beat |
| **Uniformity check** | no two sibling elements share identical delay+duration+curve |
| **Loop budget** | autoplaying loops only where they relay status; pause/stop/hide per WCAG 2.2.2 |
| **Focus persistence** | focus never lost mid-transition (focus moved after settle, ARIA announced) |

## Common agent failure patterns (name them in review)

- **The fade-in carpet** — everything fades, everywhere, same duration. (No choreography, no
  direction, no personality.)
- **The bounce default** — spring overshoot on *everything*, including settings rows and
  enterprise tables. (Personality mismatch.)
- **Scroll-jacking** — time-based auto-animation on scroll (NN/g: parallax/scroll-jacking
  "frequently frustrating, dizzying, and annoying"); the fix is scrub-tied, velocity-matched,
  escapable motion.
- **The hover that lies** — hover lifts a card that is not clickable. (Signifier violation.)
- **The 600ms modal** — above the 500ms budget; feels laggy, trains users to stop waiting.
- **Decoration-without-causality** — slide-in from the left for no spatial reason (the exact
  AI-slop pattern from [[ai-slop-web-design]]).

## Connections

- **related to:** [[Animation & Microinteraction]] — the science this executes (four jobs,
  duration budgets, reduced-motion, WCAG 2.2.2).
- **related to:** [[ai-agent-design-failures]] — Failure 1; the personality-first gate is the
  "named decision point" fix.
- **related to:** [[ai-slop-web-design]] — "scroll-reveal fade-in on everything, same
  timing/easing" is the slop fingerprint this note replaces.
- **related to:** [[Buttons & CTAs]], [[Toast, Notification & Feedback]] — L1 surface
  implementations.
- **related to:** [[design-system-checklist]] — motion tokens (duration scale, curve set,
  spring presets) are part of the three-tier token architecture.
- **related to:** [[good-vs-bad-frontend-design]] — motion sits in "affordance & feedback" and
  "performance & polish" factors.

## Study / recall questions

1. Why is "add smooth animations" guaranteed to produce fade-ins, and what replaces it?
2. Recite the personality table (4 rows) and its spring-tuning ranges.
3. Why do springs beat keyframes for physical properties (name the interruption property)?
4. What is FLIP and which Gestalt principle does shared-element motion exploit?
5. State the L-ladder rule: minimum level everywhere, required level on brand surfaces.
6. Name four QA gates and what each catches.

## Sources

- NN/g — *Executing UX Animations: Duration and Motion Characteristics* (Page Laubheimer, 2020)
  (nngroup.com/articles/animation-duration): trigger/transform/duration/easing model; frequency
  scaling; parallax warnings; vestibular guidance.
- Rauno Freiberg — *Invisible Details of Interaction Design* (rauno.me/craft/interaction-design):
  interruptability, momentum retention, trigger-during-gesture, metaphor reuse.
- Motion (motion.dev) — *React Animation* docs: spring vs duration-based defaults per property
  type; independent transform axes; `type: "spring"` transitions; MotionScore for Agents.
- Vault: [[Animation & Microinteraction]] (Saffer's four jobs; 150–500ms; WCAG 2.2.2),
  [[ai-slop-web-design]] (the motion tells), [[design-system-checklist]] (token architecture).
