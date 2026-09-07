---
name: system-design
description: >
  Must use when planning backend for system design, plan architecture, make design decisions, or evaluate trade-offs. Do NOT use for writing code (use implement-task) or UI design (use ui-specialist).
---

**Core principle:** Good systems are designed, not assembled. The cost of a design decision is measured in months of rework. Spend the hour now to save the week later.

## Rules
1. NEVER recommend a technology without understanding the constraints. "Use Kubernetes" without knowing team size, scale, and budget is bad advice.
2. NEVER skip the requirements. Before designing anything, understand: what it does, who uses it, how many users, what are the performance requirements, what are the budget constraints.
3. NEVER present one option. Always present at least two approaches with trade-offs. The user decides, not you.
4. ALWAYS ground design in the project's reality. A solo developer building an MVP does not need the same architecture as a 50-person team building for 1M users.

## Workflow

### Step 1: Understand requirements. Before designing, answer:
  - **What does it do?** Core functionality in one paragraph
  - **Who uses it?** User types and their workflows
  - **Scale?** Users, data volume, request rate
  - **Performance?** Latency requirements, throughput needs
  - **Constraints?** Budget, team size, timeline, existing tech stack
  - **Non-functional?** Security, compliance, availability, durability

### Step 2: Identify the core challenge. Every system has one primary design challenge. Name it:
  - "High write throughput for real-time data"
  - "Complex authorization across multiple resource types"
  - "Low-latency search across millions of records"
  - "Consistent data across distributed services"
  The core challenge drives the architecture.

### Step 3: Present approaches. For each approach, describe:
  - **What it is:** one paragraph
  - **How it works:** key components and data flow
  - **Pros:** why it might be the right choice
  - **Cons:** what it costs (complexity, performance, operational burden)
  - **When to choose it:** the specific conditions where this wins
  Present 2-3 approaches. Include one that's simpler than what the user might expect (the "do you really need this?" option).

### Step 4: Evaluate trade-offs. For each approach, rate on dimensions relevant to the project:
  - Complexity (how hard to build and maintain)
  - Performance (latency and throughput)
  - Scalability (can it grow)
  - Operational burden (monitoring, deployment, debugging)
  - Team fit (does the team have the skills)
  - Time to implement

### Step 5: Recommend. Pick one approach and explain why:
  - Why this one over the others (for THIS project's constraints)
  - What you're giving up (every choice has costs)
  - What to watch out for (known pitfalls)
  - When to revisit (what would change the decision)

### Step 6: Produce design artifact. Write a design document or ADR (Architecture Decision Record):
  - Context: what and why
  - Decision: what was chosen
  - Consequences: what follows from the choice
  - Alternatives considered: what was rejected and why

## Design Patterns by Challenge

| Challenge | Common Approaches |
|-----------|-------------------|
| High read throughput | Cache layer, CDN, read replicas, materialized views |
| High write throughput | Write-ahead log, event sourcing, message queues, sharding |
| Real-time updates | WebSockets, SSE, polling, pub/sub |
| Complex auth | RBAC, ABAC, policy engines, OAuth/OIDC |
| Full-text search | Inverted index, Elasticsearch, Meilisearch, pg_trgm |
| File storage | Object storage (S3), CDN, pre-signed URLs |
| Data consistency | Transactions, sagas, outbox pattern, CQRS |
| Microservice communication | REST, gRPC, message queues, event-driven |
