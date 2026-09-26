# AI Agents — Style Matrix Beyond Minimalism & Glassmorphism

> **Category:** Design / AI / Visual Systems
> Companion to [[ai-agent-design-failures]]. The "how" for Failure 2 (style collapse).
> Pairs with [[design-system-checklist]] (how to *build* the chosen system with tokens, before
> components) — the checklist builds it; this note makes sure the *choice* is deliberate and
> non-default.

## Summary

Minimalism and glassmorphism are the **low-variance attractors** of agent output: the two
aesthetics most common in training data, each plausibly "modern," each requiring almost no
composition risk. The escape is the same divergence-before-convergence structure human designers
use: a **sealed rollout** of 3–5 *named, tokenized* style directions explored **before** any
production work — each explored far enough to be scored honestly, then one is chosen against a
weighted rubric and tokenized through the [[design-system-checklist]] pipeline. The output test:
you can name the system in one sentence ("editorial print meets terminal"), and every screen
descends from it.

## The workflow (diverge → score → converge → tokenize)

**1. Sealed rollout — write 3–5 direction cards BEFORE looking at any layout.** A card =
one-sentence system idea + where it comes from. Sources for breadth (pick from different
categories, never three variants of "minimal but warm"):

- **Domain metaphors** — what physical world does this product live in? (cockpit, ledger,
  drafting table, newsroom, arcade, expedition gear)
- **Non-web media** — print, packaging, signage, exhibits, instrument panels, film titles.
- **Era / regional / subculture aesthetics** (not costume, but *logic*): Swiss, punk zine,
  risograph zine, brutalism, vaporwave-adjacent, terminal/monospace, metro maps.
- **Anti-averaging prompts**: "What would this look like if it were designed by a print magazine
  about the domain?" / "What if it were expensive?" / "What if it were free but had taste?"

**2. Score every card on a 5–7-criterion rubric (1–5 each), in writing, before building.**
Example rubric (adapt per project):

| Criterion | Question | Weight |
|---|---| scoring |
| Distinctiveness | would a designer recognize this system from one screenshot? | ×3 |
| Audience fit | does the persona's world (Step 3 of [[ai-agent-design-failures]]) look like this? | ×3 |
| Domain storytelling | does the style tell the product's story without words? | ×2 |
| Feasibility | buildable in CSS/DOM without heroics in this stack? | ×2 |
| A11y headroom | can it meet WCAG AA contrast/focus/motion? | ×2 |
| Scalability | does it survive 3 content types (marketing, app, docs)? | ×2 |

**3. Converge: pick ONE direction** (or a deliberate hybrid with a named dominant). Never
blend three directions equally — a blend is another average. **Name the tokenized variant** in
one sentence and write it into the brief.

**4. Tokenize through [[design-system-checklist]]** — primitive → semantic → component, motion
tokens included. The system is decided; screens are *instances*.

## The matrix — 16 non-default directions (use as raw material, not menu)

Each entry: the *idea*, the *type logic*, and the risk to watch. Type is called out because
type is where systems are recognized from one screenshot.

1. **Editorial print** — newspaper/magazine logic: strong serif display + grotesque body, hairline
   rules, dense asides, real column grid, drop caps, baseline-grid discipline. *Risk:*
   requires real photography/art direction to not read "template."
2. **Terminal / monospace** — monospace display, line numbers, prompt glyphs, syntax-highlight
   accents, scanline-free crispness, high-contrast on near-black *or* paper-white.
   *Risk:*
   developer-cosplay if the product is not technical.
3. **Swiss / International Typographic** — objective grid, Helvetica-or-better grotesque, red
   accent, huge scale contrast, asymmetric layout. *Risk:*
   everyone thinks they're doing Swiss; recognition requires *real* grid rigor.
4. **Brutalist (web)** — raw HTML honesty, default-ish controls styled *deliberately* unpolished,
   heavy borders, visible structure, oversized type. *Risk:* reads careless rather than
   intentional without typographic rigor.
5. **Neo-brutalism** — hard shadows (offset solid), thick strokes, candy-block color, chunky
   buttons with stateful press states. *Risk:* toy-like for serious domains.
6. **Risograph / print-shop** — 2–3 spot colors that visibly *overlap* (multiply blend),
   grain texture, misregistration, poster typography. *Risk:* texture as decoration without
   concept.
7. **Art-deco / revival** — geometric ornament, vertical emphasis, metallic accents, formal
   symmetry, elegant small caps. *Risk:* costume without structural symmetry discipline.
8. **Arcade / chiptune** — pixel type, limited palette, CRT-adjacent framing, game-feel motion
   (L5). *Risk:* nostalgia without interaction payoff.
9. **Cartographic / wayfinding** — map legends, path logic, numbered stations, line-weight
   systems, wayfinding typography (Frutiger-class). *Risk:* metaphor needs real navigation
   to mirror.
10. **Instrument panel / cockpit** — dense gauges, sectioned dials, exact labels, measured
   spacing, dark or panel-grey fields, function-first. *Risk:* dense ≠ cluttered; needs
   hierarchy discipline.
11. **Bauhaus / constructivist** — primary geometry, diagonal composition, strong figure-ground,
   type-as-image. *Risk:* ornament without grid logic = poster cosplay.
12. **Field notes / ledger** — ruled paper, stamps, handwriting accents, serial numbers,
   archival numbering. *Risk:* skeuomorph without workflow meaning.
13. **Toy / playful** — rounded geometry, chunky type, sticker/patch motifs, squash-stretch
   motion, soft depth. *Risk:* infantilizing for B2B.
14. **High-tech minimal** — not "minimal" as default: *precision minimal* with machined
   materials, exact hairlines, engineering-drawing annotations, small caps. *Risk:*
   indistinguishable from default minimalism without the annotation layer.
15. **Botanical / organic** — organic forms, layered botanical illustration, organic motion
   (springy, overshooting), warm neutrals + deep green accent. *Risk:* wellness cliché.
16. **Vaporwave-adjacent** — chrome type, retro terminal windows, scanlines as motif (sparingly),
   surreal palette. *Risk:* costume without concept; a11y contrast usually fails AA.

**Usage rule:** pick from *different* source categories for the rollout (e.g., one domain
metaphor, one print-era, one subculture) — three variants of "minimal but warmer" is not
divergence, it's the default with three hats.

## Per-style token hints (the "make it real" layer)

Style without tokens is a mood board. Each direction implies a token *shape*:

- **Editorial:** serif display (Tiempos/GT Sectra-class) + grotesque body; 8pt baseline grid;
  hairline rules; tight display tracking (-0.01 to -0.02em); spot color ≤2 + paper neutral.
- **Terminal:** monospace display + system body; syntax-palette accents (4-color max); hairline
  borders; near-black or paper-white; no soft shadows (crisp 1px lines).
- **Swiss:** single grotesque (Akzidenz/Neue Haas class); strict 12-col grid; one red accent;
  huge type scale (1.4–1.6 modular); asymmetric composition.
- **Neo-brutalist:** system-ui-ish display + chunky grotesque; 2–4px solid strokes; offset
  solid shadows (4–8px, no blur); candy palette (yellow/pink/cyan/green); press-state depth.
- **Risograph:** 2 spot colors + paper; multiply blend mode; grain overlay (SVG turbulence at
  low opacity); poster scale contrast.
- **Cockpit:** technical sans (Inter-class ok *here*, deliberately) + tabular numerals; panel
  greys; gauge greens/amber for status only; dense-but-ruled spacing (4px base).
- **Botanical:** serif or humanist display + humanist body; layered organic illustration; warm
  neutrals + deep green accent; springy motion tokens.

(The rest: derive tokens from the era's *production logic* — what would the print shop,
sign shop, or instrument shop have used? Production logic → material honesty → tokens.)

## The convergent gate (what "decided" means)

- One named direction with a one-sentence system statement.
- A scored rubric card for it and for the runners-up (kept in the brief).
- A primitive token sheet (color/type/space/motion) derived from the direction.
- The gate passes when a stranger could reproduce "the look" from the token sheet + system
  statement alone.

## Common agent failure patterns

- **The default with a hat** — "minimal, but warm/beige/warm-neutral" is still the default.
- **The blend** — equal mix of 3 directions = another average; hybrid must have a dominant.
- **Costume without concept** — era styling with default spacing/type logic underneath
  (risograph colors on Inter/Tailwind spacing = costume).
- **Token-skip** — direction named, then screens built with default Tailwind spacing/colors
  anyway (the direction evaporates on contact with implementation defaults).
- **Audience-blind style** — neo-brutalism for hospital software (style is loud where trust
  must be quiet).

## Connections

- **related to:** [[ai-agent-design-failures]] — Failure 2; the sealed rollout + rubric is the
  fix for modal/low-variance collapse.
- **related to:** [[design-system-checklist]] — supplies the token pipeline after convergence;
  tokens before components.
- **related to:** [[ai-slop-web-design]] — the antidote list ("one strong layout primitive",
  "type that is not Inter") operates at style-selection time here.
- **related to:** [[Creativity — Ideation Methods]] — sealed rollout = formalized divergent
  phase (SCAMPER, analogy, what-if) applied to visual systems.
- **related to:** [[Visual Design Craft]] — the execution layer once a direction is chosen.
- **related to:** [[Good vs Bad Frontend Design]] — audience fit and feasibility criteria come
  from its fit/trust factors.

## Study / recall questions

1. Why are minimalism and glassmorphism attractors, and why does asking for them by name
   reproduce the prior?
2. What is a sealed rollout and why must it precede any production work?
3. What makes a hybrid direction legitimate (vs. another average)?
4. Why do type choices identify systems "from one screenshot"?
5. What is the convergent gate — what must exist for "decided" to be true?

## Sources

- Vault: [[design-system-checklist]] (token architecture, audit → tokens → components → governance),
  [[ai-slop-web-design]] (the attractor fingerprint; Krebs 16 patterns; "clean" antidote list),
  [[Creativity — Ideation Methods]] (divergence toolbox).
- Rauno Freiberg — *Contrasting Aesthetics* (rauno.me/craft/contrasting-aesthetics) — case for
  deliberate aesthetic contrast over default aesthetics.
- Material Design 3 — *Expressive motion* / style system (m3.material.io) — style systems as
  decided personality, not decoration.
- DTCG Design Tokens format (design-tokens.github.io) — primitive→semantic→component layering.
