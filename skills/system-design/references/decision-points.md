# Decision Points by Stage

## Stage 1: Requirements Clarification

| Decision Point | What to Decide | Rationale |
|----------------|----------------|-----------|
| Functional scope | Who uses it, core use cases, inputs/outputs | Ambiguous requirements produce wrong architecture |
| Non-functional requirements | Scale, latency, availability, consistency, durability, data volume, read/write ratio | Drive every subsequent storage, caching, partitioning choice |
| Constraints | Runtime, regulatory, team, budget | Design inputs, not limitations to "work around" |
| Security | Data classification, access model, encryption, auditability | Should not appear first in incident postmortems |
| Capacity targets | QPS, payload sizes, growth, retention | No capacity envelope → no credible load strategy |
| Intent statement | Falsifiable value statement | If untestable after launch, it's a slogan |

## Stage 2: Capacity Estimation

| Decision Point | What to Decide | Rationale |
|----------------|----------------|-----------|
| QPS | Average and peak requests per second | Determines sharding, caching, CDN needs |
| Storage | Total data volume and growth rate | Constrains database choice |
| Bandwidth | Network throughput requirements | Affects CDN and network decisions |
| Latency budget | Max hops within p99 target | Determines architectural feasibility |

## Stage 3: Component Decomposition

| Decision Point | What to Decide | Rationale |
|----------------|----------------|-----------|
| Service boundaries | Cohesive logic owning invariants and data | Boundaries scale engineering and reliability |
| Component identification | Client, LB, app, cache, DB, queue, CDN, workers | Standard checklist prevents omissions |
| SPOF identification | Single points of failure | Ignoring guarantees incidents |
| Failure-first design | Which component fails most often | Most incidents are partial failures |

## Stage 4: Data Flow & API Design

| Decision Point | What to Decide | Rationale |
|----------------|----------------|-----------|
| Protocol | HTTP/REST, gRPC, WebSocket, queue | Each has different latency, coupling, failure characteristics |
| Sync vs async | Which block, which defer | Protects hot path |
| Consistency per hop | Strong vs eventual at each boundary | Major architectural implications |
| Failure per hop | Behavior when hop fails | Failure handling only in code comments is not design |
| API contract | Shape, errors, idempotency, versioning | Prevents over-building |

## Stage 5: Tradeoff Articulation

| Tradeoff | Axis A | Axis B | Resolution |
|----------|--------|--------|------------|
| CAP | Consistency | Availability | Choose by business requirement |
| Performance | Latency | Throughput | Optimize for bottleneck |
| Storage | Read perf | Write perf | Denormalize for reads; normalize for writes |
| Complexity | Simplicity | Flexibility | Simplicity until concrete driver |
| Economics | Cost | Performance | Cheapest op is the one not made |

## Stage 6: Validation

| Decision Point | What to Decide | Rationale |
|----------------|----------------|-----------|
| Hypothesis | Testable statement of assumption | Ambiguous assumptions are expensive |
| PoC scope | Highest-risk unknowns only | Experiments, not mini-projects |
| Measurement | Latency distributions, throughput, errors, recovery | Weak measurement → opinion-based decisions |
| Testing strategy | Contract, load, fault-injection, migration | Testing properties, not just code |
| Change cost | Cost of reversing if hypothesis fails | High reversal cost needs higher evidence |

## Stage 7: Decision & Delivery

| Decision Point | What to Decide | Rationale |
|----------------|----------------|-----------|
| Measured decision | Reference concrete findings | No evidence = preference, not decision |
| Trade-off docs | What was accepted | Unwritten trade-offs become surprise outages |
| Revisit triggers | When to re-evaluate | Prevents churn and dangerous inertia |
| Implementation scope | Core path first, optional deferred | Avoids speculative infrastructure |
| Rollout strategy | Canary → % → full after SLOs | Designed, not improvised |
| Migration | Dual-write, cutover, backfill, consistency | Migration failures are design sequencing failures |
| Operational readiness | SLOs, dashboards, runbooks, on-call | If on-call can't explain failures, design is incomplete |
