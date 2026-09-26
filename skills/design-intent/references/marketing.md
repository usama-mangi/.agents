# AI Agents — Market-Ready Marketing That Sells to the Audience

> **Category:** Design / AI / Marketing
> Companion to [[ai-agent-design-failures]]. The "how" for Failure 3 (developer-marketing).
> Extends [[UX Writing & Microcopy]] (the vault's interface-word science) from *interface* copy
> to *market* copy — landing pages, ads, onboarding, campaigns, launch posts.

## Summary

Agents write for **the prompter**, because the prompter is the only reviewer they can see.
Market-ready marketing inverts the order: **persona before copy** — a written audience block
(role, pains, objections, vocabulary, buying triggers) is produced *before* any sentence of
copy, and every claim is written in the persona's vocabulary and backed by a proof format that
persona trusts. The output test: read the landing page aloud to a mental image of the persona —
if any sentence only makes sense to the person who wrote the prompt, it's not done.

## Step 1 — The persona gate (copy does not exist before the persona block)

Copy production is **blocked** until this block exists, in writing, for each audience segment:

- **Identity:** role, company type, seniority, day-in-the-life.
- **Pains (in their words):** the 3–5 phrases the persona would actually say out loud.
  (From interviews/research per [[Discovery & User Research]]; never invented.)
- **Objections:** the top 3 reasons they *don't* buy (price, trust, switching cost, compliance).
- **Vocabulary:** the words they use vs. the words they'd never say ("increase throughput" yes,
  "unleash the power of" no). Build a **say / never-say** table.
- **Buying triggers:** what event makes them look for a solution (hiring froze, audit failed,
  churn spiked, season started).
- **Proof they need:** the evidence type their role trusts (benchmark, case study, security
  doc, peer logo, free trial, phone number).

## Step 2 — The operator/user distinction (the #1 developer-marketing fix)

For any product, identify **who operates it** (installs, integrates, maintains) vs. **who
prospers** (feels the outcome). In dev tools they overlap; in most products they don't. Write
for the person who prospers; give the operator their own section. Examples:

- Hiring tool — operator: recruiter-ops/IT; prospers: hiring manager.
- Design library — operator: web dev; prospers: marketing lead.
- Billing API — operator: engineer; prospers: finance lead.

The classic agent failure is writing **operator copy for a prosperer audience** —
features-and-integration talk to someone who wants outcomes.

### Vocabulary table, operator vs user (format — each product fills its own rows)

| Product | Operator says | User/prosperer says | Copy addresses |
|---|---|---|---|
| Rendering tool | "reduces render time", "CPU-bound" | "my renders finish while I sleep" | user; ops section for operator |
| Hiring tool | "ATS-integrated" | "I stopped dreading Monday hiring calls" | user; ops section for operator |
| Design library | "drop-in React components" | "our landing page converts 2×" | user; ops section for operator |

## Step 3 — Segment-native vocabulary (no category-agnostic copy)

Every segment has its own language; copy that ignores it reads as outsider. The *shape*:

- **Trades/contractors:** quote, crew, callback, permit, lead time, warranty.
  Never: "workflow", "leverage", "my business runs itself".
- **Healthcare admin:** patients, slots, no-shows, referrals, waitlist, compliance.
  Never: "seamless experience".
- **Educators:** rosters, grading, prep time, curriculum, parents.
  Native benefit: "get 5 hours of grading back".
- **Hospitality:** covers, turn a table, food cost, slow season.
  Not native: "increased operational efficiency" (no one says this).

**Mirror-check:** re-word every key claim into the segment's own words. If the segment's native
phrase for the benefit doesn't appear in your copy, the copy is not segment-native.

## Step 4 — Proof-before-voice (claims are cheap; evidence formats are the product)

Market copy = **claim + evidence**, where the evidence format is one the persona's role trusts
(from the persona block):

- **Concrete numbers** — "cut no-shows 31% in 6 weeks" beats "reduces no-shows"
  (the "reachable claims" rule from [[ai-slop-web-design]]).
- **Named results** — "approved 2.1× faster", not "improves efficiency".
- **Peer formats** — case study, peer logo, a quote from someone with the persona's job title
  (a "Head of Growth" testimonial is a mismatched proof for a contractor audience).
- **Trial/phone path** — self-serve trial when the persona self-serves; visible phone/WhatsApp
  where the segment buys by conversation (non-Western trust patterns, see
  [[ai-slop-web-design]] open questions).

## Step 5 — Channel gate (copy is written *into* a channel, not in abstract)

- **Landing page:** outcome headline; subhead states the mechanism; primary CTA uses a persona
  verb. "Learn more" is not a CTA. No badge-over-H1 (the slop tell).
- **Ads:** hook (persona's pain in their words) → proof → CTA; name the segment in the headline
  when segments are distinct.
- **Product UI copy:** persona verbs on actions; operator tasks (setup/admin) may use operator
  vocabulary, but the *default path* speaks user language.
- **Launch posts (HN / Product Hunt):** operator content is legitimate *here* — the audience is
  developers. This is the one channel where dev-speak is native, not a failure. Launch-post
  audience ≠ landing-page audience.
- **Ops section:** integration, security, uptime, SSO get their own section with operator
  vocabulary — never blended into the user path.

## Step 6 — The review gate (before any copy ships)

- [ ] Persona block exists and predates the copy.
- [ ] Every claim has a proof format the persona trusts.
- [ ] No sentence that only makes sense to the prompter (mirror-check).
- [ ] Name-swap test passes (from [[ai-slop-web-design]]): swap in a competitor's name — if the
      copy still reads fine, it described a category, not this product.
- [ ] No badge-over-H1, no exactly-five-item lists, no buzzword list (seamless, unlock,
      empower, leverage, synergy, cutting-edge, game-changer, revolutionize, delve).
- [ ] Operator/user distinction mapped; both addressed in separate sections.
- [ ] Trial/phone/self-serve path matches how the segment actually buys.
- [ ] Channel-native format respected (landing / ads / launch / ops).

## Common agent failure patterns

- **Prompter-as-reader:** every sentence valid to a developer; no persona vocabulary anywhere.
- **Vague aspirational headline** ("Build the future") — no segment, no proof, no verb.
- **Feature-list hero** ("X, Y, Z and more!") — features are not outcomes.
- **Dev-CTA fallback** ("Learn more" / "Get started" on a non-self-serve product).
- **Ops-blend** — integration talk mixed into the user path; operator section missing.
- **Proof-shaped-but-empty** ("Trusted by teams of all sizes" — no names, no numbers).

## Connections

- **related to:** [[ai-agent-design-failures]] — Failure 3; the persona gate is the
  "named audience" fix.
- **related to:** [[UX Writing & Microcopy]] — the interface-word rules this extends to
  market copy.
- **related to:** [[ai-slop-web-design]] — name-swap test, reachable claims, buzzword list,
  non-Western trust patterns.
- **related to:** [[Discovery & User Research]] — the persona block is synthesized from real
  research, not invented; the say/never-say table requires interview data.
- **related to:** [[Synthesis — Personas, Jobs & Journeys]] — persona format source (empathy
  map, JTBD) the block derives from.
- **related to:** [[good-vs-bad-frontend-design]] — fit/trust factor: copy is design.

## Study / recall questions

1. Why does the persona block gate copy production (mechanism: prompter-as-reader)?
2. Operator vs prosperer — define both and give one example product where they differ.
3. What is the mirror-check for segment-native vocabulary?
4. Why is dev-speak native in launch posts but a failure on landing pages?
5. Name four checks from the review gate.

## Sources

- Vault: [[ai-slop-web-design]] (name-swap test, reachable claims, buzzword list, 91% conversion
  gap, non-Western trust patterns), [[UX Writing & Microcopy]] (words as design),
  [[Synthesis — Personas, Jobs & Journeys]] (persona/JTBD methods), [[Discovery & User Research]]
  (interview grounding), [[ai-agent-design-failures]] (prompter-as-reader mechanism).
- Krebs fingerprint (badge-over-H1, mad-lib headlines) via [[ai-slop-web-design]] sources.
