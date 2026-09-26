# Design Patterns by Challenge

| Challenge | Common Approaches |
|-----------|-------------------|
| High read throughput | Cache layer (Redis/Memcached), CDN, read replicas, materialized views |
| High write throughput | Write-ahead log, event sourcing, message queues, sharding |
| Real-time updates | WebSockets, SSE, polling, pub/sub |
| Complex auth | RBAC, ABAC, policy engines, OAuth/OIDC |
| Full-text search | Inverted index, Elasticsearch, Meilisearch, pg_trgm |
| File storage | Object storage (S3), CDN, pre-signed URLs |
| Data consistency | Transactions, sagas, outbox pattern, CQRS |
| Microservice communication | REST, gRPC, message queues, event-driven |
| Rate limiting | Token bucket, sliding window, fixed window |
| Idempotency | Idempotency keys, deduplication tables, at-most-once delivery |
| Circuit breaking | Hystrix pattern, bulkhead isolation, fallback responses |
| Eventual consistency | CRDTs, vector clocks, last-write-wins with conflict resolution |

## Scaling Interventions (order of complexity)

1. Add caching (cheapest; reduces DB load)
2. Add read replicas (read-heavy workloads)
3. Vertical scale (buy time; not long-term)
4. Horizontal scale / stateless services (app layer)
5. Database sharding (single DB node bottleneck)
6. CDN (static assets, geographically distributed reads)
7. Async offload via message queue (decouple slow operations)

## Latency Reference Numbers

| Operation | Latency |
|-----------|---------|
| L1 cache | 0.5 ns |
| Main memory | 100 ns |
| SSD random read | 150 µs |
| Datacenter round trip | 500 µs |
| HDD seek | 10 ms |
| Cross-continent round trip | 150 ms |

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Starting with architecture before requirements | Ask questions first |
| Over-engineering from the start | MVP first; add complexity only with a specific driver |
| Ignoring failure modes | Every component fails; identify SPOF in every design |
| "It can be cached" as magic answer | Specify the invalidation strategy |
| Proposing microservices without justification | Monolith is correct by default; state the driver |
| Skipping capacity estimation | Can't choose DB or caching strategy without knowing scale |
| Not defining consistency requirements | Eventual vs strong has major architectural implications |
