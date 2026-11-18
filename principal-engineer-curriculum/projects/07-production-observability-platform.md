# Project 07 — Production Observability & Distributed Intelligence Platform
> **Phase Alignment:** [Phase 10 — Observability & Production Intelligence](../phases/phase-10-observability-and-intelligence.md)  
> **Target Complexity:** Staff / Principal SRE & Observability Architect  
> **Recommended Technologies:** OpenTelemetry, Prometheus / Thanos, Grafana Tempo, Loki, Pyroscope

---

## 🎯 Project Overview
Build a high-scale, unified production telemetry platform processing metrics, distributed traces, structured logs, and continuous CPU/memory profiles. The platform demonstrates end-to-end W3C trace context propagation across asynchronous message boundaries, cost-optimized tail-based sampling, and continuous flame graph analysis.

---

## 🏗️ Architecture & Component Design

```mermaid
flowchart TD
    subgraph Microservices["Instrumented Services"]
        SvcA["Service A (Go)"] -->|Trace Context HTTP| SvcB["Service B (Java)"]
        SvcB -->|Inject Context into Kafka Header| Kafka["Kafka Topic"]
        Kafka -->|Extract Context| SvcC["Async Worker C (Python)"]
    end

    SvcA & SvcB & SvcC -->|OTLP gRPC (Traces, Metrics, Logs)| OTelAgent["OTel Collector DaemonSet"]
    SvcA & SvcB & SvcC -->|Profiling Data| Pyroscope["Pyroscope Server"]
    
    subgraph CentralTelemetry["Central Observability Cluster"]
        OTelAgent --> OTelGateway["OTel Collector Gateway<br/>(Tail-Based Sampling Processor)"]
        
        OTelGateway -->|Sampled Traces| Tempo["Grafana Tempo / Jaeger"]
        OTelGateway -->|Aggregated Metrics| Prometheus["Prometheus / Thanos"]
        OTelGateway -->|Filtered Logs| Loki["Grafana Loki"]
        
        GrafanaUI["Grafana Unified Dashboard<br/>(Metrics + Trace Exemplars + Logs + Flame Graphs)"]
        Prometheus & Tempo & Loki & Pyroscope --> GrafanaUI
    end
```

---

## 📋 Core Architectural Requirements

1. **Polyglot OpenTelemetry Instrumentation:**
   - Instrument applications in Go, Java, and Python using the OpenTelemetry SDK.
   - Enforce RED (Rate, Errors, Duration) metrics for all HTTP/gRPC endpoints.
2. **Asynchronous Trace Context Propagation:**
   - Inject W3C `traceparent` and `tracestate` headers into Kafka record metadata before publishing.
   - Extract headers in asynchronous consumer workers and create child spans, maintaining unbroken distributed trace graphs.
3. **Tail-Based Sampling Pipeline:**
   - OpenTelemetry Collector Gateway configured with a 30-second in-memory span buffer.
   - Retain 100% of traces containing HTTP status codes $\ge 500$ or span errors.
   - Retain 100% of traces with overall duration $>1,000$ms.
   - Probabilistically sample 1% of normal fast traces to reduce downstream storage costs by 80%.
4. **Continuous Production Profiling:**
   - Integrate Pyroscope eBPF / runtime profiling agents across services.
   - Correlate distributed trace spans directly with corresponding CPU/memory flame graphs.
5. **SLO Alerting & Error Budget Dashboard:**
   - Configure multi-window multi-burn-rate Prometheus alerts for 99.9% availability and latency SLOs.

---

## 🧪 Verification & Acceptance Criteria
- Trigger an unexpected runtime exception in the asynchronous Python background worker; verify in Grafana Tempo that the complete distributed trace is rendered continuously from the initial frontend HTTP click down to the worker error span.
- Verify that under 10,000 RPS load, tail-based sampling keeps trace storage consumption within the designated budget while capturing 100% of anomalous slow queries.
