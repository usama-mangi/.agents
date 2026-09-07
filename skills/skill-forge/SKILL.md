---
name: skill-forge
description: >
  Use whenever the user asks to create a new skill, write a SKILL.md, build an agent skill, define behavioral rules for an AI, generate guardrails, or craft enforcement mechanisms.
---

**Core principles**: A skill is a **contract between the human and the model**. The model's training makes it helpful but not necessarily correct. A skill exists to close the gap: to force specific behavior that would not emerge from general-purpose instructions alone.

**What makes enforcement work:**
1. **Unambiguous commands**: "MUST", "NEVER", "ALWAYS" over "should", "prefer", "consider"
2. **Sequential workflows**: numbered steps that cannot be reordered or skipped
3. **Gate conditions**: explicit checkpoints that block progress until satisfied
4. **Negative space**: anti-patterns that name the failure modes explicitly
5. **Concrete examples**: before/after pairs that disambiguate instructions

## Workflow
1. Before writing anything, answer these questions:
  - **What behavior should the model exhibit?** (be specific, not vague)
  - **What behavior should the model NOT exhibit?** (name the failure modes)
  - **What is the trigger condition?** (when does this skill activate?)
  - **What is the scope?** (what is in-bounds vs out-of-scope?)
  - **What is the consequence of non-compliance?** (what breaks if ignored?)
  If the user cannot answer these, interview them. Do not write a skill based on vague intent. Vague skills produce vague behavior.
2. Not every skill needs the same rigor. Match the level to the stakes:
  | Level | When to Use | Characteristics |
  |-------|-------------|-----------------|
  | **Hard** | Security, data integrity, production safety | "MUST", "NEVER", verification gates, abort on failure |
  | **Medium** | Consistency, quality standards, workflows | "ALWAYS", "DO NOT", checklists, validation steps |
  | **Soft** | Preferences, style, conventions | "prefer", "typically", guidance with exceptions noted |
  When in doubt, go harder. A skill that is too soft will be ignored; one that is too hard can be relaxed. The reverse is not true.
3. Use action verbs to emphasise action. Avoid explaining why, focus on what. The model needs commands not knowledge. Examples are welcome.
4. Follow this structure. Every section is load-bearing. Do not omit sections without reason. Always use unslop skill for generating the text.
```markdown
  ---
  name: <kebab-case-name>
  description: >
    <One paragraph: when to use it, trigger words, and what is explicitly excluded. The description is what the model sees in the available_skills list. It must be precise enough to determine activation.>
  ---
  
  **Core principles**: <One paragraph framing the skill's purpose. State the behavioral goal upfront. Do not add why, just what.>
  
  ## Rules
  
  <Non-negotiable constraints. Each rule is a standalone statement. Use MUST/NEVER/MUST NOT. No wiggle room.>
  1. **Rule one.** Explanation.
  2. **Rule two.** Explanation.
  
  ## Workflow
  
  <Numbered steps. Sequential. Each step has exactly one of:
  - A command to run
  - A file to read/write
  - A decision to make (with branching)
  - A verification to pass>
  
  ### Step N: <Action Verb> <Object>
  
  <Concrete instructions. Include example commands, file paths, and expected outputs where applicable.>
  
  ## Examples
    
  <Before/after pairs or concrete request → action mappings. Each example should demonstrate the skill in action.>
  
  - "User says X" → Model does Y (not Z)
```

4. Validate the Skill. Run every generated skill through this checklist before saving:
  - [ ] **Trigger precision:** Does the description narrow activation to the correct tasks? Would a model correctly activate this skill 95%+ of the time?
  - [ ] **Rule enforceability:** Can every "MUST" rule be verified by inspecting the output? If a rule cannot be checked, it is not a rule, it is a wish.
  - [ ] **Step sequential-ability:** Can a model follow the workflow in order with no context beyond what the skill provides?
  - [ ] **Example concreteness:** Are examples specific enough to resolve ambiguity? Would two different models produce similar outputs from the same example?
  - [ ] **Scope boundaries:** Is it clear when NOT to use this skill?
  - [ ] **No orphan dependencies:** Does the skill reference files or tools that may not exist? If it references external files, those files must be included in the skill directory.
5. Complex skills benefit from reference files in the same directory. These are loaded alongside SKILL.md when the skill is invoked.
  **When to create a reference file:**
    - The skill has more than 3 decision branches
    - The skill references domain-specific knowledge
    - The skill has multiple workflows for different scenarios
    - The skill needs templates or checklists
  **File naming:** `<topic>.md` in the same directory as SKILL.md.
  **Linking:** Reference files are linked from SKILL.md as `[text](filename.md)`.
6. Save the skill at `~/.agents/skills/<skill-name>/SKILL.md`. For it to appear in `available_skills`, it must be registered in the opencode/cline configuration. Check if auto-registration is enabled, or add it manually to`~/.config/opencode/opencode.json` or the relevant config.

## Enforcement Patterns: Techniques That Work

1. A checkpoint that blocks progress until a condition is met:

```markdown
  ### Step 3: Run `scripts/lint.py` against the output. If it fails, STOP and fix errors. Do NOT proceed to Step 4 until lint passes. There are no exceptions.
  ### Pattern: The Decision Tree. Branching logic that handles ambiguity.
```

2. Decision Framework
  1. Is the request about **frontend**? → Load the design skill first.
  2. Is the request about **system config**? → Load the omarchy skill first.
  3. Is the request about **research**? → Load the memory skill first.
  4. None of the above? → Proceed without a skill.

### Pattern: The Checklist

A verification gate that forces completion:

```markdown
## Before Shipping

- [ ] All tests pass
- [ ] No TODO/FIXME comments remain
- [ ] Secrets are not in code
- [ ] Error messages are user-facing, not stack traces
```

### Pattern: The Contract

An absolute rule with no exceptions:

```markdown
## Rules

1. **NEVER log secrets.** API keys, tokens, passwords, and connection strings must never appear in logs, error messages, or output. If a secret is accidentally logged, that is a P0 incident.
```

## Meta: How to Improve This Skill
This skill itself should be refined over time. When a generated skill fails to enforce behavior:
  1. Identify which enforcement pattern was too weak
  2. Add the failure mode to the Anti-Patterns section
  3. Strengthen the relevant rule or add a new one
  4. Add an example of the failure and the correct behavior
