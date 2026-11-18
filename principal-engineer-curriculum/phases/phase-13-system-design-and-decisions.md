# Phase 13 — Advanced System Design & Architecture Decision Making
> **Domain:** Enterprise System Design, Capacity Estimation, ADRs & Trade-off Defense  
> **Duration:** Months 17–18  
> **Depth:** Architectural Judgement, Evaluation Frameworks & 15 Complex Systems

---

## 🎯 Objective
At the Principal Engineer and Solution Architect level, technology implementation is secondary to **architectural judgement**. Master the ability to structure ambiguous requirements, produce rigorous capacity models, evaluate trade-offs using industry-standard frameworks (ATAM), write defensible Architecture Decision Records (ADRs), and design complex, planet-scale distributed architectures.

---

## 📋 Topic Breakdown

### 13.1 Systematic Architecture Design Methodology
- **Requirements Engineering for Architects:**
  - Clarifying ambiguous business visions into hard engineering requirements.
  - Functional Requirements (User-facing actions, workflows, inputs/outputs).
  - Non-Functional Requirements (NFRs / Quality Attributes): Latency, Throughput, Availability, Durability, Consistency, Security, Observability, Compliance, Cost.
- **Mathematical Capacity & Resource Estimation:**
  - **Traffic Estimation:** Daily Active Users (DAU), Read/Write ratio, Average RPS, Peak RPS multiplier (e.g., $3\times$ or $5\times$).
  - **Storage Estimation:** Payload size per record, daily ingestion volume, replication factor multiplier, 5-year retention capacity.
  - **Bandwidth Estimation:** Ingress bandwidth (bytes/sec) and Egress bandwidth (bytes/sec).
  - **Memory & Caching Estimation:** Applying the 80/20 Pareto principle to RAM sizing ($20\%$ hot keys cached for 1 day).
- **Failure Domain & Blast Radius Analysis:**
  - Single Points of Failure (SPOF) identification.
  - Multi-AZ vs Multi-Region fault domains.
  - Cell-Based Architecture: Segmenting users into autonomous, blast-radius-limited "cells".
- **Architecture Documentation Standards:**
  - **The C4 Model:** Context, Containers, Components, and Code diagrams.
  - Sequence Diagrams, Deployment Topologies, Entity-Relationship (ER) diagrams.

### 13.2 Architecture Evaluation & Decision Making (ADR / ATAM)
- **Architecture Decision Records (ADRs):**
  - Documenting context, decision drivers, considered options, decision outcome, and positive/negative consequences.
  - Michael Nygard ADR format and MADR (Markdown Architectural Decision Records).
- **Architecture Trade-off Analysis Method (ATAM):**
  - Identifying architectural sensitivities, trade-off points, and risks.
  - Quality Attribute Scenarios (Source, Stimulus, Artifact, Environment, Response, Response Measure).
- **Evolutionary Architecture & Fitness Functions:**
  - Automated tests that verify architectural constraints (e.g., package cyclic dependency checks, API response latency thresholds in CI/CD).
- **Technical Debt Management:**
  - Technical Debt Quadrant (Deliberate/Prudent vs Inadvertent/Reckless).
  - Measuring technical debt interest and formulating refactoring investment proposals for executives.

---

## 🏛️ 15 Real-World Enterprise System Design Exercises

Every Principal Engineer candidate must design and document the following 15 systems with complete HLD, LLD, Database Schemas, API contracts, Failure Analysis, and Cost Models:

1. **Global URL Shortener (Bitly at Scale):** 10B URLs, 100k read RPS, sub-10ms latency, custom hash collision resolution, multi-region CDN caching.
2. **Distributed Payment Gateway (Stripe-like):** Zero double-charge guarantee, idempotent API keys, Two-Phase Commit / Saga orchestrator, PCI-DSS tokenization vault, ledger consistency.
3. **Global Multi-Channel Notification Platform:** Push, SMS, Email, WhatsApp; rate limiting per user, preference management, priority queues, provider failover.
4. **Ride Matching & Geospatial Dispatch System (Uber-like):** QuadTrees / Google S2 / Uber H3 spatial indexing, dynamic driver heartbeat updates, driver-rider matching algorithm under peak surge.
5. **Real-Time Global Messaging Platform (WhatsApp-like):** 2 billion users, WebSocket / XMPP connection managers, E2E encryption key exchange, offline message spooling, read receipt fanout.
6. **Large-Scale Video Streaming Platform (YouTube/Netflix):** Video chunking, adaptive bitrate streaming (HLS/DASH), multi-CDN distribution, distributed transcoding pipeline.
7. **Global E-Commerce Flash Sale System:** Handling 1,000,000 concurrent checkout attempts in 10 seconds; Redis atomic inventory reservation, Virtual Waiting Room (queueing), transactional outbox.
8. **Distributed Multi-Tenant Rate Limiter:** Edge-deployed token bucket, sliding window counter with Redis cluster, adaptive load shedding, header propagation.
9. **Multi-Region Core Banking Ledger System:** Strict serializability, immutable double-entry bookkeeping, multi-region active-active with CockroachDB / Spanner, zero data loss guarantee (RPO = 0).
10. **Real-Time Credit Card Fraud Detection Platform:** Evaluating 50,000 transactions/sec within a 50ms SLA; Apache Flink stateful rules engine + online machine learning inference.
11. **Distributed Search Engine & Indexer:** Distributed crawler, inverted index shards, TF-IDF / BM25 ranking, distributed query coordinator with top-K merge.
12. **Global Identity & SSO Platform (Auth0-like):** Multi-tenant identity brokering, SAML/OIDC federation, token exchange, tenant directory isolation, brute force protection.
13. **Enterprise Multi-Tenant SaaS Platform:** Data isolation models (silo vs pool), dynamic tenant onboarding, tenant metering, noisy neighbor throttling.
14. **Enterprise Generative AI & RAG Platform:** Semantic caching, multi-model routing, hybrid vector/graph retrieval, token rate limiting, automated evaluation and guardrails.
15. **Distributed Durable Workflow Engine (Temporal-like):** Event sourcing history, state machines, worker polling, determinism enforcement, long-running timers and retries.

---

## 💻 Practical Hands-On Project
Select **System #2 (Distributed Payment Gateway)** or **System #9 (Multi-Region Core Banking Ledger)**:
1. Write a complete 10-page **System Architecture Document (RFC)** using the template in `templates/system-design-doc-template.md`.
2. Include full capacity math (CPU cores, RAM, Disk IOPS, Network bandwidth).
3. Produce C4 Context and Container diagrams.
4. Detail the failure scenario when the primary payment processor times out mid-transaction.
5. Include 2 completed **Architecture Decision Records (ADRs)** defending database and messaging engine choices.

---

## ✅ Completion Criteria
- [ ] Calculate the accurate 5-year hardware footprint and AWS/GCP monthly cost for 1 billion daily events.
- [ ] Diagram a C4 Container architecture showing clear separation of concerns across tiers.
- [ ] Write and defend 2 production-ready ADRs in standard format.
- [ ] Deliver a 45-minute whiteboard/presentation walkthrough defending an enterprise system design against adversarial questions.
