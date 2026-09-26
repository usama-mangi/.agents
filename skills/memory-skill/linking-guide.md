# Cross-linking guide

Relations are how knowledge gets found by more than one path. A topic linked from five places is five times as likely to surface as one linked from nowhere.

## What makes a good relation

| Good | Bad |
|------|-----|
| JEPA `builds-on` Energy-Based Models (JEPA is an EBM) | JEPA `related-to` Energy-Based Models |
| AI Slop `contrasts-with` Design System Checklist (the problem, the fix) | AI Slop `related-to` Design Systems |
| Representation Collapse `similar-to` AI Slop (same failure in two domains: output collapse vs design homogeneity) | Representation Collapse `related-to` AI Slop |

Every relation must answer "how", not just "whether". The observation text can carry the detail; the relation type names the mechanism.

## Relation types

- **Mechanism analogy:** the same process in two domains. `similar-to`.
- **Methodological sibling:** the same approach, different application. `similar-to`.
- **Problem and fix:** `contrasts-with`.
- **Prerequisite chain:** A must be understood before B. A `prerequisite-for` B, B `builds-on` A.
- **Conceptual bridge:** an abstract connection across fields. Only if the mechanism is nameable.

## Bidirectionality

If A `builds-on` B, add B `prerequisite-for` A. If A `contrasts-with` B, the reverse pair is the same type. Never create a one-way link when a matching reverse type exists; unlinked directions are dead ends during traversal.

## When not to link

- Surface similarity only: two topics share a keyword but no mechanism.
- Forced connections: the link exists to make the graph look connected.
- Redundant links: A to B and A to C where B and C already connect and C is a subtopic of B.

## Density

| Topic kind | Target relations |
|------------|------------------|
| Foundational (EBMs, ViTs) | 3-5 |
| Applied (resume, job search) | 2-4 |
| Hub (AI Slop, JEPA) | 5-8 |
| Standalone (modular arithmetic) | 1-3 |

An entity with zero relations means you missed something. Ten or more means some are redundant or a subtopic should have absorbed them.

## Staleness

Relations and observations can age. `stale --days N` surfaces facts and links older than N days. Career and market topics decay fastest; Mathematics and foundational concepts hold longer. Revisit stale nodes with `check` to confirm they still hold and `update` with fresh sources and confidence. A link that no longer reflects the current state should be removed rather than left as a dead end.

## Verification workflow

After storing new knowledge:
1. Run `suggest --entity E` to discover latent connections you may have missed.
2. Run `check --entity E` to surface contradictions with existing observations.
3. Run `traverse --entity E --depth 2` to review the neighborhood for coherence.
4. Run `stale --days 30` to flag aging facts for re-verification.
