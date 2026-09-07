# HCI foundations

The science behind the UI rules. Load when designing or evaluating a surface, or when a checkpoint in `slop-checklist.md` or `a11y-checklist.md` is unclear.

## Heuristics (Nielsen 10)

1. Visibility of system status. Inform the user what is going on, within about a second. Spinners, progress, "you are here".
2. Match between system and real world. Speak the user's language. No jargon. Natural mapping and order.
3. User control and freedom. Obvious, always-available emergency exit. Undo, back, cancel.
4. Consistency and standards. Same actions look and behave the same everywhere. Follow platform conventions.
5. Error prevention. Disable invalid states. Confirm destructive actions. Constrain inputs.
6. Recognition rather than recall. Options, actions, and state visible. No memory tax.
7. Flexibility and efficiency of use. Accelerators for experts, hidden from novices, usable by all.
8. Aesthetic and minimalist design. Every extra element competes for attention. Keep only what the current task needs.
9. Help users recognize, diagnose, and recover from errors. Errors in plain language. Concrete next step.
10. Help and documentation. Ideally unnecessary. When present, searchable, focused on concrete steps.

## Cognitive laws

- **Fitts**: time to reach a target scales with distance and inversely with size. Make targets big and close.
- **Hick**: time to decide scales with log of number of choices. Reduce options at short decision points. No 3+ equal CTAs.
- **Jakob**: users spend most time on other sites. Follow platform and category conventions.
- **Miller**: working memory holds about 4 to 7 chunks. Chunk content. Keep screen essentials few.
- **Gestalt**: proximity, similarity, figure/ground, continuation, closure, common region. Group with proximity.
- **Von Restorff (isolation)**: the odd one out stands out. Use ONE visually distinct element for the primary CTA.
- **Pareto (80/20)**: 20% of features get 80% of use. Design flows for the common 20%.
- **Serial position**: first and last items in a list are remembered most. Put key nav and CTAs at the edges.

## Norman's three levels

- **Visceral**: automatic pre-cognitive first glance. Looks trustworthy, clean, polished. Decided in about 50ms.
- **Behavioral**: does it work, learnable, efficient. Governed by affordances, feedback, consistency, error-prevention.
- **Reflective**: conscious thought. Does it make me feel sense, do I trust it, do I brand-love it.

## Affordance / signifier / constraint / mapping / feedback

- **Affordance**: what an object lets the user do. A button affords pressing.
- **Signifier**: a cue that signals where the affordance is. The visual style of a button.
- **Constraint**: limiting the possible actions. Disabled states, valid input masks.
- **Mapping**: the relationship between controls and their effects. Natural mapping reduces learning.
- **Feedback**: a clear response to every action. Within about a second.

## Surface checklist

| Surface | Non-negotiables |
|---------|-----------------|
| Header / nav | Logo top-left linked to home. 5 to 7 items. Active state visible. Focus ring on every link. Skip-to-content first in tab order. Breadcrumbs on deep pages. |
| Hero | One headline within first viewport. One primary CTA with a specific verb. At most one quieter secondary. |
| Footer | Contact info, privacy, terms, legal path. Grouped columns. Quiet. No loud CTAs. |
| Card | Whole card or clear CTA inside, click target at least 44px. One primary interaction per card. Equal spacing. |
| Buttons / CTAs | Verb plus object label. State matrix: rest, hover, active, focus, loading, disabled. |
| Forms / inputs | Label proximity (placeholder is not a label). Inline validation. Errors in plain language next to field. |
| Modal / dialog | Focus trap. Escape closes. No nesting. No long multi-section forms inside modals. |
| Toast / notification | Transient for confirmation only. Errors that need fixes get an inline or modal treatment. Icon plus text, not color alone. |
| Search / filtering | Recognition with keyboard. Autocomplete. No dead-end zero result. Active filters visible. |
| Table / data grid | Sortable columns with visible affordance. Pagination. Bulk actions. No blank grid on no results. |
| Empty / error state | Context, cause, action. Plain language, no error codes alone. |
| Color / contrast | WCAG AA on every pair. One accent used sparingly. Never color alone for meaning. |
| Typography | 5 to 7 step scale with clear tiers. Line length 50 to 75 chars. Body 4.5:1 contrast. |
| Iconography | Icon plus label for ambiguous items. One set, one style. |
| Animation | Purpose: confirm, signal, relay, prevent. Respect reduced-motion. No scroll-reveal on every element. |
| Settings | Defaults over config. Instant-reversible. Grouped. No Save button for a single toggle. |
| Onboarding | First-success path. Progressive disclosure. Help where users get stuck. |
| A11y | POUR. Keyboard and focus. Semantics. Never one channel. |