# Design system

How to build a design system from scratch. Load when initializing a design system or auditing an existing one.

## Mental model

- **Component library**: tokens and components, maybe docs, no governance. Looks finished, dies the day it ships.
- **Design system**: tokens, components, documentation, governance. The full what / how / contract stack.
- **Pattern library**: documented reference patterns only. Token architecture often absent by design.
- **Brand Operating System**: a design system plus every non-product surface (voice, photography, motion, presentations). Every Brand OS contains a design system; not every design system rises to a Brand OS.

## Phases

### Phase 0: Decide scope and direction

- State the goal: consistent branding, faster building, better collaboration, governance.
- Choose the system scope tier:
  - Tier 1 tokens: color, typography, spacing, radius, shadow, motion. Build first.
  - Tier 2 core components: the 15 to 25 components in 80 to 90% of surfaces. Button, Input, Select, Checkbox, Radio, Modal, Toast, Tooltip, Accordion, Table, Card, Badge, Avatar, Loading, Empty states.
  - Tier 3 patterns, templates, full Brand OS.
- Pick the highest-repetition, lowest-tolerance-for-inconsistency surface first (control panel, not marketing).
- Skip the system if one product, one team. A style guide is enough. Systems pay off only when consistency is a recurring tax.

### Phase 1: Audit

Read-only. Open files, take notes, write nothing. Catalog every UI element on one board. Prioritization score: frequency in code times cost of inconsistency.

### Phase 2: Foundations (tokens)

- Three-tier token architecture:
  - **Primitives**: raw values. Palette, scale, raw sizes. Do not consume directly.
  - **Semantic**: purpose-named tokens. bg, fg, accent, status. Consume primitives.
  - **Component**: component-specific tokens. button.primary.bg. Consume semantic.
- Reference direction: primitive to semantic to component. Never upward.
- Naming: semantic, not literal. Never `purple-500`, never `gradient-start`.
- Spacing: 4px base, full scale.
- Type: 5 to 7 tiers. Distinct heading family plus distinct body family.

### Phase 3: Components

- Three real requests before a new component.
- State matrix: rest, hover, active, focus, loading, disabled, empty, error.
- Components consume semantic tokens only.

### Phase 4: Documentation

- Usage docs for every component.
- Do and don't examples.
- Machine-readable so AI can use it.
- Link design and code in one package.

### Phase 5: Governance

- One named owner or small owning group.
- Contribution path in five steps: discuss, draft, review, ship, document.
- Semver: patch for fixes, minor for new components or tokens, major for breaking changes.
- Deprecations: migration guide, minimum two-release window.
- One-offs go in a marked unsafe namespace and are reviewed monthly.

### Phase 6: Rollout and adoption

- Launch checklist: tokens complete, build pipeline outputs CSS and platform formats, 15 to 20 components with states and a11y, docs live, semver and changelog, named owner.
- Stage the rollout: foundations, then components, then patterns, then motion, then measurement.
- Build one real feature end-to-end with the system to find gaps.
- Measure adoption by component instance counts, screens built from the library, and detach rate.
- Add components only by request.

## Eight good-vs-bad factors

The evaluation lens. Apply on every screen.

1. **Hierarchy**: one dominant element per screen. Primary CTA larger and higher contrast than any other action. 5 to 7 step type scale. Whitespace and alignment do the work.
2. **Cognitive load**: chunked content. One section at a time. Dense but prioritized.
3. **Consistency**: every color, type, spacing from the design system. One repeated layout primitive.
4. **Fit and trust**: concrete claims with numbers. Real photos. Transparent contact and pricing. Name-swap test.
5. **Affordance and feedback**: clickable things look clickable. Immediate hover, focus, click feedback.
6. **Familiarity**: follow the conventions of the platform and the category.
7. **Accessibility**: WCAG AA, keyboard, focus, labels, alt text, reduced-motion.
8. **Performance and polish**: Core Web Vitals. Working states and progress. Optimized assets.