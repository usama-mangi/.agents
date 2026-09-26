---
name: system-design
description: >
  Must use when planning backend for system design, plan architecture, make design decisions, or evaluate trade-offs. Do NOT use for writing code (use implement-task) or UI design (use ui-specialist).
---

**Core principle:** Design is iterative. Revisit earlier stages as constraints sharpen.

## Rules

1. NEVER skip requirements. Ambiguous requirements produce the wrong architecture.
2. NEVER present one option. Always present at least two approaches with trade-offs. The user decides, not you.
3. NEVER choose technology without understanding constraints. "Use Kubernetes" without knowing team size, scale, and budget is bad advice.
4. ALWAYS ground design in the project's reality. A solo developer building an MVP does not need the same architecture as a 50-person team building for 1M users.
5. ALWAYS articulate trade-offs explicitly. Trade-offs not articulated are not made consciously.
6. ALWAYS document revisit triggers. No decision is permanent.

## Workflow

### Step 1: Requirements Clarification

Before drawing any boxes, define what the system must do and what constraints it operates under.

**Functional requirements** — answer:
- Who uses this system and how?
- What are the 3–5 most critical user flows?
- What are the inputs and outputs?
- What operations must be supported? (read, write, delete, search, stream)

**Non-functional requirements** — answer for each dimension:

| Dimension | Question |
|-----------|----------|
| Scale | How many users? QPS? Peak vs average? |
| Latency | Acceptable p99? Read vs write latency? |
| Availability | 99.9%? 99.99%? |
| Consistency | Tolerate stale reads? For how long? |
| Durability | Cost of data loss? |
| Data volume | Stored? Growth rate? |
| Read/write ratio | 10:1? 100:1? 1:1? |

**Constraints** — list:
- Runtime/language standards
- Regulatory requirements
- Team size and expertise
- Deployment environment and budget

**Security** — list:
- Data classification
- Access model
- Encryption requirements
- Auditability expectations

**Intent** — one falsifiable statement of value the system provides.

### Step 2: Capacity Estimation

Back-of-the-envelope calculations. Do not skip.

- **QPS:** DAU × actions/day ÷ 86400 = avg QPS. Peak = avg × 2–10.
- **Storage:** records/day × record size × retention = total.
- **Bandwidth:** QPS × avg response size.
- **Latency budget:** available p99 ÷ per-hop latency = max hops.

### Step 3: High-Level Component Decomposition

Sketch major components and interactions.

- Client layer, load balancer, app servers, caching, datastore, queue, CDN, workers.
- One box per bounded responsibility.
- Draw data flow, not just components.
- Identify the single point of failure in first sketch.
- Ask: which component fails most often? Design for that first.

### Step 4: Data Flow & API Contract Design

Trace request path from client to storage and back.

For each hop, specify:
- Protocol (HTTP/REST, gRPC, WebSocket, message queue)
- Sync vs async
- Consistency requirement
- Failure behavior

Define API contracts before internals:
- Request/response shape
- Error semantics
- Idempotency expectations
- Versioning strategy

### Step 5: Tradeoff Articulation & Design Options

Generate 2–3 candidate architectures. For each, state:

- **What it is:** one paragraph
- **Key components and data flow**
- **Pros / cons**
- **When to choose it**

Articulate trade-offs on these axes:

| Axis A | Axis B | Resolution method |
|--------|--------|-------------------|
| Consistency | Availability | CAP — choose by business requirement |
| Latency | Throughput | Optimize for the bottleneck |
| Read perf | Write perf | Denormalize for reads; normalize for writes |
| Simplicity | Flexibility | Prefer simplicity until concrete driver exists |
| Cost | Performance | Cheapest DB op is the one not made |

For each tradeoff:
1. State the constraint
2. Identify what violates it
3. Name the tradeoff
4. Assert acceptability with business reason

### Step 6: Validation & Measurement

Treat assumptions as hypotheses.

- Write assumptions as testable statements
- PoC scope: validate highest-risk unknowns, not rebuild
- Measure: latency distributions (not averages), throughput, error rates, recovery time
- Testing: contract tests, load tests, fault-injection, migration tests

Core loop: Hypothesis → Experiment → Measure → Learn → refine

### Step 7: Decision & Delivery

**Decision:**
- Select option with evidence (not intuition)
- Document trade-offs accepted
- Define revisit triggers (e.g., sustained 70% load, p99 breach for 2 cycles, regulatory change)

**Delivery:**
- Implementation scope: core path first, optional deferred, risk-heavy behind flags
- Rollout: canary → percentage → full after SLO guardrails
- Migration: dual-write windows, read-path cutover, data backfill, consistency checks
- Operations: SLOs/alerting, dashboards, runbooks, on-call ownership

### Step 8: Document

Write an ADR or design doc:
- Context: what and why
- Decision: what was chosen
- Evidence: validation findings
- Trade-offs: what was accepted
- Revisit triggers: when to re-evaluate
- Alternatives considered: what was rejected and why

## Handoff Gates

Between stages, verify:
- Foundation → Design: Did we define the right constraints?
- Design → Validation: Did we make assumptions testable?
- Validation → Decision: Do we have evidence, not confidence?
- Decision → Delivery: Can this be rolled out and operated safely?

## Design Patterns by Challenge

See [references/patterns.md](references/patterns.md).

## Decision Point Reference

See [references/decision-points.md](references/decision-points.md).
