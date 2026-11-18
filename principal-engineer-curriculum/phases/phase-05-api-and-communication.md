# Phase 5 — Advanced API & Communication Architecture
> **Domain:** API Protocols, Gateway Patterns, Microservice Communication & Traffic Management  
> **Duration:** Month 7  
> **Practical Project:** Multi-Protocol API Platform (REST + gRPC + GraphQL + WebSockets)

---

## 🎯 Objective
Master modern inter-service and client-to-service communication mechanisms. Understand serialization efficiency, protocol buffers, schema federation, rate limiting algorithms, and how to build high-performance, fault-tolerant API gateways.

---

## 📋 Topic Breakdown

### 5.1 Communication Protocols & Serialization
- **REST Architecture:** Richardson Maturity Model (Levels 0–3), HATEOAS, Idempotent HTTP methods (PUT, DELETE vs POST), caching headers (`ETag`, `If-None-Match`).
- **gRPC & Protocol Buffers (Protobuf):**
  - Binary wire format: Varints, wire types, tag-length-value encoding.
  - RPC Styles: Unary, Server Streaming, Client Streaming, Bidirectional Streaming.
  - HTTP/2 Transport: Multiplexing, stream IDs, headers vs data frames, gRPC status codes.
  - Channel management, subchannels, connection pooling, and client-side load balancing.
- **GraphQL Architecture & Internals:**
  - AST execution engine, Resolvers, Schema Definition Language (SDL).
  - The N+1 Query Problem and DataLoader batching/caching pattern.
  - GraphQL Federation (Apollo Federation): Supergraphs, subgraphs, gateway query plan synthesis.
  - GraphQL Subscriptions via WebSockets.
- **Real-Time Protocols:**
  - WebSockets: Full-duplex TCP framing, masking keys, ping/pong heartbeats, socket scale-out architectures.
  - Server-Sent Events (SSE): HTTP-based unidirection streaming, automatic reconnection, text/event-stream.
- **HTTP/3 & QUIC Protocol:** 0-RTT handshakes, connection migration (IP change survival), elimination of TCP head-of-line blocking.

### 5.2 API Gateway & Traffic Management
- **API Gateway Internals:** Envoy Proxy, Traefik, Kong, NGINX architecture.
- **Dynamic Routing & Service Discovery:**
  - Client-side discovery (Consul, Eureka) vs Server-side discovery (Kubernetes CoreDNS, Envoy EDS).
  - Health checking: Active vs passive health checks, outlier detection.
- **API Composition & Aggregation:** Orchestration layer, parallel request dispatch, fan-out limits.
- **Advanced Traffic Routing:**
  - Request Hedging: Mitigating tail latency by sending duplicate requests after a threshold.
  - Request Coalescing (Singleflight): Collapsing concurrent duplicate requests into a single backend fetch.
  - Shadowing / Dark Launching: Mirroring live production traffic to test candidate microservice versions.

### 5.3 API Governance, Contracts & Evolution
- **Contract-Driven Development:**
  - Consumer-Driven Contracts (Pact framework)
  - OpenAPI 3.1 / Swagger tooling
  - AsyncAPI for event-driven message contracts.
- **API Versioning Strategies:** URI path versioning, Header versioning, Query param versioning, Content negotiation (Accept header).
- **Backward & Forward Compatibility:** Protobuf field numbering rules, schema deprecation cycles.

### 5.4 Rate Limiting & Concurrency Control Algorithms
- **Rate Limiting Algorithms:**
  - **Token Bucket:** Burst handling with continuous token replenishment.
  - **Leaky Bucket:** Constant outflow rate, smoothing traffic spikes.
  - **Fixed Window Counter:** The boundary-burst vulnerability.
  - **Sliding Window Log:** Precise timestamp counting, high memory consumption.
  - **Sliding Window Counter:** Hybrid weighted approximation, low memory footprint.
- **Distributed Rate Limiting:**
  - Redis + Lua scripts for atomic token decrement.
  - Local caching with asynchronous batch sync to reduce Redis IOPS.
- **Adaptive Concurrency Limits:** TCP Vegas-style delay-based concurrency limiting (Netflix Concurrency Limits library) to protect servers under strain without fixed thresholds.

---

## 💻 Practical Hands-On Project
Build a **Unified Multi-Protocol API Gateway & Edge Platform**:
1. Implement an edge gateway in Go or Rust that exposes a public REST and GraphQL endpoint, routing internally to backend **gRPC microservices**.
2. Implement **Distributed Rate Limiting** using the Sliding Window Counter algorithm backed by Redis and Lua scripts.
3. Implement **Singleflight (Request Coalescing)** to protect backend services from cache stampedes on hot resource queries.
4. Support **Real-Time Notifications** streaming updates to connected web clients via WebSockets and SSE.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** An enterprise e-commerce platform with 30 backend teams wants to modernize their external public API and mobile client interfaces.
- **Decision:** Should the company standardize on **Apollo GraphQL Federation** or **Backend for Frontend (BFF) pattern using gRPC + REST**?
- **Deliverable:** Write an ADR comparing query flexibility, caching at CDN edge, schema coordination overhead, and client-side payload optimization.

---

## ✅ Completion Criteria
- [ ] Inspect and decode a raw Protobuf byte stream into tag-length-value components.
- [ ] Implement a sliding window rate limiter in Lua and verify zero race conditions under concurrent load.
- [ ] Demonstrate gRPC bidirectional streaming with client-side load balancing and subchannel reconnects.
- [ ] Complete the multi-protocol API gateway and run benchmark comparisons against standard REST gateways.
