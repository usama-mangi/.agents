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

current_task:
  id: TASK-XX
  title: <title>
  plan_approved: true|false
  gates_passed: [<gate numbers>]

log:
  last_updated: <ISO date>
  recent_changes: [<list of design decisions with rationale>]
```