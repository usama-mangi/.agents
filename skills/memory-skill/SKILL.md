---
name: memory-skill
description: >
  Long-term memory for research and learning, stored in a native JSON knowledge graph. Use when the user asks to learn, research, study, explore, or investigate a topic, says "remember this", "store this", "take notes on", asks to save findings, or asks "what do we know about X". Triggers: learn, research, study, explore, investigate, remember, store, take notes, deep dive, what do we know about, look into. Always load this skill before any research or learning task.
---

# Memory skill

All long-term knowledge for research and learning lives in a native JSON
knowledge graph: `memory-graph.json` at the skill root, driven by a script:
`python3 ~/.agents/skills/memory-skill/scripts/graph.py`. It is separate from the
project memory bank (`memory.json`) that dev-workflow manages. That bank holds
verified decisions, facts, and lessons. This graph holds topics worth remembering
across projects, investigations, and sessions.

The graph survives context resets. Searching it beats reading files. The script
does the reading and writing, so this skill loads the rules, not the data.

## State, read and written cheap

State lives in one JSON store, driven by `graph.py`:

| Store | Script | Covers |
|-------|--------|--------|
| `memory-graph.json` | `graph.py` — `get --keyword K` fetches only matching entities, `get --entity E` fetches one topic + its relations, `traverse`/`check`/`suggest`/`synthesize`/`stale` read state, `add`/`update`/`relate`/`remove` write state | topics, atomic observations, cross-topic relations |

- Fetch by keyword, entity, or graph traversal — never dump the whole store into context.
- The graph is the single source of truth for what we know. Everything else is a copy.
- If the store file is missing or corrupt, say so and stop rather than guessing what the graph contains.

## Commands

`graph.py` takes a subcommand and an optional `--dir DIR` (defaults to the skill
directory). Reads return full JSON objects; writes are atomic.

| Command | Use |
|---------|-----|
| `init` | Create an empty store. |
| `get --keyword K` | Search entities by name, type, observation text, or relation type. |
| `get --entity E` | Open one topic: full entity plus all its relations (out and in). |
| `add --entity E --type T --text N [--source S] [--confidence C] [--valid-from F] [--valid-until U]` | Create a topic with its first observation, with provenance and confidence. |
| `update --entity E --text N --append [--source S] [--confidence C] [--valid-from F] [--valid-until U]` | Append an enriched observation. Without `--append`, replace the observations. |
| `relate --from F --to T --type R` | Link two topics. `R` names how they connect. |
| `remove --entity E` | Delete a topic and all its relations. |
| `remove-relation --from F --to T --type R` | Delete one link. |
| `traverse --entity E [--depth N]` | Follow relations N hops from E; returns the neighborhood with relation types. |
| `check --entity E` | Surface observations in E that contradict other entities' observations. |
| `suggest --entity E` | Recommend links to existing entities with shared keywords or entityType. |
| `synthesize --entity E` | Produce a narrative summary of E and its connected neighborhood. |
| `stale [--days N]` | Surface observations older than N days as possibly stale. |
| `list [--type T]` | One-line summaries so you can see what exists without loading it all. |

## Entity format

One entity per topic, named after the topic. `entityType` is one of the
categories below. Each observation is `{text, source, confidence, valid_from, valid_until, updated}`.
- `source` cites where the fact came from.
- `confidence` is `high`, `medium`, or `low` — how sure we are.
- `valid_from`/`valid_until` mark when the fact applies.

Never stuff a whole file into one observation. Every entity gets an `updated` timestamp from
the script, so recency is visible without reading the entry.

## Research and store

1. Search first. `get --keyword K` on the topic and its key terms. If results look
   thin, `list` for the full picture. Skip this and you will duplicate work and
   miss connections.
2. Research. Gather concepts, mechanisms, and sources. Note why each finding
   matters and which topic it connects to.
3. Store.
   - New topic: `add --entity E --type T --text N --source S --confidence C`.
     One observation per finding, with provenance.
   - Existing topic: `update --entity E --text N --append --source S --confidence C`.
     Skip observations already present.
   - `relate --from F --to T --type R` for every genuine connection. Use a
     concrete type, not a bucket. One relation per connection.
   - After adding, run `suggest --entity E` to catch links you missed, and
     `check --entity E` to catch contradictions.
4. Verify. The entity has observations with sources and confidence. Connections are
   bidirectional where meaning allows. No placeholders.

## Retrieval

`get --keyword K` for the topic and related terms, then `get --entity E` on the
matches to pull observations and relations. For broad questions, use `traverse --entity E --depth N`
to surface the connected neighborhood, then `synthesize --entity E` to produce a coherent
summary. `suggest --entity E` recommends new links. `check --entity E` flags contradictions.
`stale --days N` surfaces aging facts that may need re-verification.

## Updating

`get --entity E` to load current state, `update --append` for new findings (with source and
confidence), `relate` for new connections. Delete an observation only when it is factually
wrong or the user asks. Run `stale` periodically to catch facts that need re-verification.

## Linking

- Links carry context. The relation type says how two topics connect.
- Links are earned. Relate entities with a genuine conceptual connection, not
  surface similarity.
- `related-to` on everything makes the graph useless for traversal. Pick the
  concrete type from the list below.
- After storing new knowledge, use `suggest` to discover latent connections and
  `check` to ensure consistency.

For worked examples of good and bad relations, density targets, and the full type
list, read `linking-guide.md` next to this skill.

## Categories

`entityType` values match these domains:

| Domain | Contents |
|--------|----------|
| Mathematics | Pure math, problem solving, combinatorics |
| ML/AI | Models, architectures, training methods, agent development |
| Design/Web | UI/UX, frontend, aesthetics, brand systems |
| Cognition | Human cognition, learning, visual processing |
| Career | Resumes, job search, hiring, interviews, market data |
| LLM Interaction | Prompt engineering, agent skills, context, vault operations |
| Agent Skills | Skills installed in this environment |

## Anti-patterns

- Searching by dumping the whole file instead of `get --keyword`.
- One giant observation. A blob of text in one observation is unsearchable.
- Vague relations. A generic type on everything makes traversal useless.
- Storing raw dumps. Synthesize before writing.
- Deleting without a request. Prune only on explicit instruction.
- Adding observations without `source` or `confidence`. Unattributed facts erode trust in the graph.
- Ignoring staleness. Facts without `valid_until` or age checks become false knowledge.

Base directory for this skill: /home/usama-mangi/.agents/skills/memory-skill
Relative paths in this skill (e.g. scripts/) are relative to this base directory.
