# Phase 10 — Observability & Production Intelligence
> **Domain:** Telemetry Pipelines, Distributed Tracing, eBPF & Continuous Profiling  
> **Duration:** Month 12 (Integrated with Phase 9)  
> **Practical Project:** [Production Observability Platform](../projects/07-production-observability-platform.md)

---

## 🎯 Objective
Move beyond basic monitoring to true **System Observability**—the ability to infer the internal states of complex distributed systems solely from external outputs. Master the OpenTelemetry standard, trace context propagation across asynchronous workers, continuous profiling, and telemetry cost management.

---

## 📋 Topic Breakdown

### 10.1 Observability Foundations: The Three Pillars & Beyond
- **Metrics, Logs & Traces Interconnection:**
  - Metrics: Aggregatable numeric measurements over time (Counters, Gauges, Histograms, Summaries).
  - Logs: Timestamped discrete structured events (JSON, key-value).
  - Traces: Directed Acyclic Graphs (DAG) representing a request's journey across service boundaries.
  - The Fourth Pillar: **Continuous Profiling** (On-CPU, Off-CPU, memory allocation continuous flame graphs).
- **Core Monitoring Frameworks:**
  - **The RED Method:** Rate, Errors, Duration (Ideal for request-driven microservices).
  - **The USE Method:** Utilization, Saturation, Errors (Ideal for hardware and resource bottlenecks).
  - **Google's Four Golden Signals:** Latency, Traffic, Errors, Saturation.
- **High Cardinality Challenge:**
  - Definition of cardinality in time-series databases (TSDB).
  - How label explosion (`user_id`, `order_id` in metric tags) crashes TSDBs like Prometheus.
  - Solutions: Exemplars (linking metrics directly to sample traces), M3DB, VictoriaMetrics, Thanos.

### 10.2 Distributed Tracing & OpenTelemetry (OTel)
- **OpenTelemetry Standard Architecture:**
  - OTel API vs OTel SDK vs OpenTelemetry Collector.
  - Collector Pipelines: Receivers, Processors (batch, memory limiter, attribute filter), Exporters.
  - OpenTelemetry Protocol (OTLP) over gRPC and HTTP/Protobuf.
- **Context Propagation & W3C Trace Context:**
  - `traceparent` header format: `version-trace_id-parent_id-trace_flags`.
  - `tracestate` header for vendor-specific routing.
  - Baggage API for transmitting cross-cutting application metadata across boundaries.
- **Context Propagation Across Async Boundaries:**
  - Thread-local context loss in async runtimes (Goroutines, Tokio async tasks, Java Virtual Threads / CompletableFuture).
  - Propagating trace contexts through message brokers (Kafka record headers, RabbitMQ properties).
- **Sampling Strategies:**
  - Head-Based Sampling: Deciding whether to sample at the root span (fast, but misses rare errors).
  - Tail-Based Sampling: Buffering spans in the collector until the trace completes; sampling 100% of traces that contain errors or exceed latency thresholds.

### 10.3 Advanced Production Intelligence & Telemetry Engineering
- **eBPF-Based Zero-Code Observability:**
  - Inspecting TCP connections, HTTP requests, and DNS lookups at the Linux kernel layer without application modification (e.g., OpenTelemetry eBPF, Pixie).
- **Continuous Profiling in Production:**
  - Low-overhead continuous sampling profilers (Pyroscope, Parca).
  - Distributed Flame Graphs: Comparing flame graphs before and after deployment to catch CPU regressions.
- **Service Dependency Mapping & Root Cause Analysis:**
  - Graph-based topology inference from distributed trace spans.
  - Correlating metric anomalies with span duration changes.
- **Synthetic Monitoring & Real User Monitoring (RUM):**
  - Synthetics: Proactive automated health probes simulating user journeys.
  - RUM: Browser navigation timing API, Core Web Vitals (LCP, FID/INP, CLS).
- **Telemetry Cost Optimization & FinOps:**
  - Tiered storage for telemetry (SSD hot storage $\rightarrow$ S3 cold object storage).
  - Dynamic log level switching in production without restarts.
  - Metric aggregation at the collector layer to discard raw high-frequency data.

---

## 💻 Practical Hands-On Project
Build a **Complete Production Observability Platform with OpenTelemetry**:
1. Deploy an **OpenTelemetry Collector** with pipelines for metrics, logs, and traces.
2. Instrument a multi-service polyglot application (e.g., Go service calling Python worker via Kafka).
3. Implement **W3C Trace Context Propagation** through Kafka record headers so the trace graph stays unbroken across asynchronous consumers.
4. Configure **Tail-Based Sampling** in the OTel collector to retain 100% of HTTP 5xx errors and any request exceeding 500ms, while sampling only 1% of successful fast requests.
5. Deploy **Pyroscope** for continuous CPU profiling and correlate a trace span with a specific function-level CPU flame graph.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** An organization generates 15 terabytes of logs daily, resulting in a \$40,000/month third-party SaaS monitoring bill.
- **Decision:** As Principal Architect, evaluate migrating to an **In-House Open-Source Observability Stack (OTel + Prometheus/Thanos + Grafana Loki + Tempo)** vs renegotiating SaaS contracts.
- **Deliverable:** Write an ADR factoring in compute/storage infrastructure costs, dedicated SRE staffing overhead, compliance retention, and feature velocity.

---

## ✅ Completion Criteria
- [ ] Inspect raw HTTP headers and identify valid W3C `traceparent` syntax.
- [ ] Implement trace context injection and extraction across a Kafka consumer loop.
- [ ] Configure tail-based sampling rules in an OpenTelemetry Collector YAML configuration.
- [ ] Diagnose a live CPU spike using Pyroscope flame graph differential analysis.
