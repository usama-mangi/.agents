# design.yaml schema

The `design.yaml` file lives at the project root next to `AGENTS.md` and `project-backlog.json`. It is the single source of truth for design. Read it on orient. Update it on record-progress. Check every diff against it.

```yaml
project:
  name: <project name>
  description: <one line>
  audience: <primary persona in one sentence>

brand:
  voice:
    adjectives: [<3-5 voice adjectives>]
    anti_patterns: [<words or phrasings the brand never uses>]
    reference_lines: [<2-3 sentences that sound exactly like the brand>]
  differentiators:
    deliberate_choices: [<the 10-20 decisions that distinguish this product>]
    name_swap_test: <a sentence; replace the brand name with a competitor; if it still fits, rewrite>

tokens:
  color:
    primitives: { <primitive-name>: <hex>, ... }   # raw scale; do not consume directly
    semantic:    { <use-name>: <token-path>, ... } # bg, fg, accent, status; consumes primitives
    component:   { <component-name>: <token-path>, ... } # button.primary.bg; consumes semantic
  typography:
    heading_family: <distinct family>
    body_family: <distinct family>
    mono_family: <mono family if used>
    scale: [<step>, <step>, <step>, <step>, <step>]  # 5 to 7 tiers
  spacing:
    base: 4px
    scale: [4, 8, 12, 16, 24, 32, 48, 64]
  radius:
    scale: [0, 4, 8, 12, 9999]   # last is pill
  shadow:
    scale: [none, sm, md, lg]
  motion:
    durations_ms: [100, 200, 300, 500]
    easings: { standard: <cubic-bezier>, emphasized: <cubic-bezier> }
  status:
    a11y_aa_pass: true|false
    slop_scan_pass: true|false

components:
  <ComponentName>:
    states: [<rest>, <hover>, <active>, <focus>, <loading>, <disabled>, <empty>, <error>]
    a11y:
      role: <ARIA role>
      keyboard: [<keys handled>]
      contrast_pairs: [{ fg: <token>, ratio: <n:1>, pass: true|false }, ...]
    tokens_consumed: [<list of semantic tokens; primitive consumption is a violation>]

screens:
  <ScreenName>:
    dominant_action: <the one verb the screen asks for>
    dominant_message: <the one thing the screen says>
    ctas: <count; 1 to 2 is correct, 3 or more is a violation>
    uses_components: [<list>]
    slop_scan: clean|mild|heavy     # heavy blocks ship
    hci_scan: pass|fail

log:
  last_updated: <ISO date>
  recent_changes: [<list of design decisions with rationale>]
```

## The `intent:` block (owned by design-intent)

`design-intent` owns this block; `ui-ux-workflow` reads it on orient and never writes it. It is
merged mechanically: `python3 ~/.agents/skills/design-intent/scripts/intent.py merge --payload
<payload.json>` deep-merges a JSON payload into this block only, byte-preserving the rest of the
file. Gate evaluation: `intent.py gates` exits 1 while any field below is missing, reads as the
default ("clean modern minimal"), or results are not all-pass.

```yaml
intent:
  audience:                      # the persona gate — must exist BEFORE any copy
    identity: <role, company type, seniority, one line>
    pains: [<3-5 phrases in the persona's own words>]
    objections: [<top 3 reasons they don't buy>]
    say: [<native phrases they use>]
    never_say: [<words they'd never use>]
    triggers: [<events that make them look for a solution>]
    proof_formats: [<evidence types their role trusts>]
    operator_vs_prosperer: <who operates vs who prospers, one line each>
  style:
    direction: <one-sentence system name; "clean modern minimal" fails the gate>
    rubric: { <candidate>: <total score>, ... }   # sealed-rollout scores incl. runners-up
    rejected: [<one-line reasons each runner-up lost>]
  motion:
    personality: playful|productive|editorial|technical
    signature: <the one L3+ signature motion on brand surfaces, one line>
  delivery:
    gates_run: <ISO date>
    results: { audience: pass|fail, style: pass|fail, motion: pass|fail, delivery: pass|fail }
    exceptions: [<criterion-cited exceptions, e.g. "reduced-motion fallback only on hero —
                 internal dashboard; compensating control: static opacity swap">
                ]
```
