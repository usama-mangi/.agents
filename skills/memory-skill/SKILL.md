---
name: memory-skill
description: >
  Long-term memory for research and learning, stored in the memory MCP knowledge graph. Use when the user asks to learn, research, study, explore, or investigate a topic, says "remember this", "store this", "take notes on", asks to save findings, or asks "what do we know about X". Triggers: learn, research, study, explore, investigate, remember, store, take notes, deep dive, what do we know about, look into. Always load this skill before any research or learning task.
---

# Memory skill

All long-term knowledge lives in the memory MCP knowledge graph: entities, observations, relations. It survives context resets, and searching it beats reading files. If the memory MCP is unavailable, say so and stop rather than guessing what the graph contains.

## Tools

| Tool | Use |
|------|-----|
| `search_nodes` | First move for any recall. Search by topic keyword. |
| `read_graph` | Load the whole graph when orienting on what is known. |
| `open_nodes` | Pull named entities and their neighbors. |
| `create_entities` | Add a topic: one entity per topic. |
| `add_observations` | Append facts or findings to an existing entity. |
| `create_relations` | Link topics: one relation per connection. |
| `delete_entities` / `delete_observations` / `delete_relations` | Prune. Only on explicit request. |

Entity format: one entity per topic, named after the topic. `entityType` is the domain from the categories below. One observation per atomic fact, with its source. Never stuff a whole file into one observation.

## Research and store

1. **Search first.** `search_nodes` on the topic and its key terms. If results look thin, `read_graph` for the full picture. You will otherwise duplicate work and miss connections.
2. **Research.** Gather concepts, mechanisms, and sources. Note why each finding matters and what it connects to in the graph.
3. **Store.**
   - New topic: `create_entities`, `entityType` from the categories, one observation per finding.
   - Existing topic: `add_observations`. Skip observations already present.
   - `create_relations` for every genuine connection. Use concrete types: `builds-on`, `contrasts-with`, `applies-to`, `prerequisite-for`, `similar-to`. One relation per connection.
4. **Verify.** The entity has observations and relations. Connections are bidirectional where meaning allows (if A `builds-on` B, add B `prerequisite-for` A). Sources are cited in observations. No placeholders.

## Retrieval

`search_nodes` for the topic and related terms, then `open_nodes` on the matches to pull observations and neighbors. Follow relations to adjacent topics when the question is broad. Present a synthesis; connect ideas across entities instead of listing observations one by one.

## Updating

`open_nodes` to load current state, `add_observations` for new findings, `create_relations` for new connections. Delete an observation only when it is factually wrong or the user asks.

## Linking

- Links carry context: the relation type says how two topics relate.
- Links are earned. Relate entities with a genuine conceptual connection, not surface similarity.
- `related-to` on everything makes the graph useless for traversal. Pick the concrete type.

For worked examples of good and bad relations, density targets, and the full type list, read `linking-guide.md` next to this skill.

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

- **Skipping the search.** Always `search_nodes` before researching.
- **One giant observation.** A blob of text in one observation is unsearchable.
- **Vague relations.** `related-to` on everything makes traversal useless.
- **Storing raw dumps.** Synthesize before writing.
- **Deleting without a request.** Prune only on explicit instruction.
