# Phase 1 — Advanced Software Architecture
> **Domain:** Software Architecture Patterns, Domain-Driven Design (DDD) & Modularity  
> **Duration:** Months 1–2 (Integrated with Phase 0)  
> **Practical Project:** [Enterprise Microservices Platform](../projects/02-enterprise-microservices-platform.md)

---

## 🎯 Objective
Understand how to structure large-scale codebases for maximum maintainability, loose coupling, and evolutionary growth. Master Domain-Driven Design (DDD) to align business boundaries with software components, and learn when (and how) to transition from a Monolith to a Modular Monolith and distributed Microservices.

---

## 📋 Topic Breakdown

### 1.1 Architecture Fundamentals & Paradigms
- **Architectural Styles:**
  - Layered (N-Tier) Architecture
  - Hexagonal Architecture (Ports and Adapters)
  - Clean Architecture & Onion Architecture (Inversion of Control across domain layers)
  - Component-Based Architecture
  - Modular Monolith (In-process boundaries, package encapsulation, strict dependency graphs)
  - Microkernel Architecture & Plugin Frameworks
  - Microservices Architecture (Loose coupling, autonomous deployability, decentralized data)
  - Event-Driven Architecture (EDA): Event Notification, Event-Carried State Transfer, Event Sourcing
  - Space-Based Architecture (Tuple space, in-memory data grids, processing units)
  - Cell-Based Architecture: Bulkheading entire regional user cohorts into self-contained blast radius units.

### 1.2 Domain-Driven Design (DDD)
- **Strategic DDD:**
  - Domain, Core Domain, Supporting Subdomain, Generic Subdomain
  - Bounded Context: Identifying boundaries, Ubiquitous Language definition
  - Context Mapping: Shared Kernel, Customer-Supplier, Conformist, Anti-Corruption Layer (ACL), Open Host Service (OHS), Published Language.
- **Tactical DDD:**
  - Entity vs Value Object (Identity vs Mutability and Equivalence)
  - Aggregate & Aggregate Root: Consistency boundary enforcement
  - Domain Events: Decoupling side-effects within the domain model
  - Domain Services vs Application Services vs Infrastructure Services
  - Repository Pattern & Specification Pattern
  - Factory Pattern in complex aggregate construction.

### 1.3 Advanced Architecture Patterns
- **Modernization & Migration Patterns:**
  - Strangler Fig Pattern: Incrementally replacing legacy monoliths without rewrite risks
  - Branch by Abstraction: Long-running architecture migrations in trunk-based development.
- **Distributed Consistency & Coordination Patterns:**
  - Saga Pattern: Choreography vs Orchestration based Sagas, compensating transactions
  - CQRS (Command Query Responsibility Segregation): Read vs Write model optimization
  - Event Sourcing: State as an immutable append-only sequence of domain events
  - Transactional Outbox Pattern: Dual-write prevention using database transaction boundaries
  - Transactional Inbox Pattern: Exactly-once consumer processing and deduplication
  - Change Data Capture (CDC): Debezium, WAL streaming to Kafka.
- **Edge, Gateway & Resilience Patterns:**
  - Backend for Frontend (BFF): Tailored API composition per client channel (Web, Mobile, IoT)
  - API Composition vs API Gateway Aggregation
  - Sidecar Pattern, Ambassador Pattern, Adapter Pattern
  - Circuit Breaker, Bulkhead, Retry with Exponential Backoff and Jitter, Timeout patterns.
- **Scalability & Partitioning Patterns:**
  - Sharding Pattern: Range, Hash, and Directory-based sharding
  - Multi-Tenant Architecture: Database-per-tenant, Schema-per-tenant, Shared-database with tenant-ID.

---

## 💻 Practical Hands-On Project
Design and implement an **E-Commerce Order Fulfillment System**:
1. Start with a strict **Modular Monolith** using Hexagonal Architecture and Tactical DDD (Aggregates, Value Objects, Domain Events).
2. Enforce strict module boundaries using package visibility or architectural linter tools (e.g., ArchUnit in Java, Go internal packages).
3. Implement the **Transactional Outbox Pattern** to reliably publish domain events to an event bus during state commits.
4. Extract one subdomain (e.g., Payment or Inventory) into an independent **Microservice** using the **Strangler Fig Pattern** and an **Anti-Corruption Layer (ACL)**.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** An expanding fintech platform wants to break their 500k-line monolith into 40 microservices.
- **Decision:** As Principal Architect, evaluate whether to migrate directly to microservices or refactor into a **Modular Monolith** first.
- **Deliverable:** Write an ADR outlining Conway's law implications, operational overhead, transactional consistency risks, and your recommended phased architecture roadmap.

---

## ✅ Completion Criteria
- [ ] Produce a C4 Model Context & Container diagram demonstrating bounded contexts and context maps.
- [ ] Successfully implement an Aggregate Root with invariants and domain event dispatching.
- [ ] Demonstrate a working Transactional Outbox implementation with CDC or polling worker.
- [ ] Defend a complete ADR on Monolith vs Modular Monolith vs Microservices.
