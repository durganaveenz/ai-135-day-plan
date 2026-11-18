# Phase 9 — Reliability Engineering & Resilience (SRE)
> **Domain:** Site Reliability Engineering (SRE), Chaos Engineering & Disaster Recovery  
> **Duration:** Month 12 (Integrated with Phase 10)  
> **Practical Project:** Multi-Region Active-Active Failover & Chaos Simulation Lab

---

## 🎯 Objective
Design distributed architectures that treat failure as a guaranteed operational reality rather than an anomaly. Master Site Reliability Engineering (SRE) mathematics, error budgets, cascading failure mitigation, chaos engineering, and zero-downtime multi-region active-active architectures.

---

## 📋 Topic Breakdown

### 9.1 SRE Fundamentals & Reliability Mathematics
- **Service Level Terminology:**
  - SLI (Service Level Indicator): Quantifiable metric (e.g., successful requests / total requests).
  - SLO (Service Level Objective): Target percentage agreed upon by business and engineering (e.g., 99.95% over 30 days).
  - SLA (Service Level Agreement): Contractual commitment with financial penalties.
- **Error Budget Management:**
  - Calculating downtime allowance: 99.9% = 43.8 minutes/month; 99.99% = 4.38 minutes/month.
  - Burn Rate Alerting: Multiwindow multi-burn-rate alerts (detecting 2% burn in 1 hour vs 5% burn in 6 hours).
  - Freeze policies: Halting feature deployments when error budget is exhausted to focus on reliability.
- **System Availability Mathematics:**
  - Serial Availability: $A_{total} = A_1 \times A_2 \times A_3$.
  - Parallel Redundant Availability: $A_{total} = 1 - (1 - A_1)(1 - A_2)$.
  - Calculating MTBF (Mean Time Between Failures), MTTR (Mean Time To Recovery), MTTD (Mean Time To Detect).

### 9.2 Reliability Modeling & Failure Analysis
- **Fault Tree Analysis (FTA):** Deductive top-down analysis of catastrophic failure paths.
- **Failure Mode and Effects Analysis (FMEA):** Calculating Risk Priority Numbers (Severity $\times$ Occurrence $\times$ Detection).
- **Cascading Failures & Failure Amplification:**
  - Retry Storms: How unjittered client retries overwhelm recovering backends.
  - Thundering Herds on cache or database cold starts.
  - Deadlocks induced by thread pool exhaustion.
- **Resilience Design Patterns:**
  - Circuit Breakers (Closed, Open, Half-Open states) and failure rate thresholds.
  - Exponential Backoff with Full Jitter algorithm.
  - Bulkheading: Partitioning worker thread pools so failure of one downstream service does not exhaust global threads.
  - Graceful Degradation & Brownout Patterns: Disabling non-critical features (recommendations, reviews) under load to protect core checkout.
  - Load Shedding using Priority Levels (Critical vs Sheddable traffic).

### 9.3 Chaos Engineering & Fault Injection
- **Principles of Chaos Engineering:** Forming hypotheses about steady state, injecting realistic production faults, verifying recovery.
- **Fault Injection Dimensions:**
  - Network: Packet loss, latency injection (jitter), bandwidth throttling, asymmetric partitions.
  - Compute: CPU hogging, memory consumption, thread starvation, sudden kernel panic (`kill -9`).
  - Storage: Disk fill, I/O read/write latency spikes, corrupt block injection.
  - Clock: Clock skew injection, leap second simulation.
- **Chaos Tooling:** Chaos Mesh, LitmusChaos, Gremlin, AWS Fault Injection Simulator (FIS).
- **Game Days:** Organizing structured incident simulation drills with engineering teams.

### 9.4 Disaster Recovery & Multi-Region Architectures
- **Recovery Metrics:**
  - RTO (Recovery Time Objective): Maximum acceptable duration of downtime.
  - RPO (Recovery Point Objective): Maximum acceptable data loss duration.
- **Disaster Recovery Topologies:**
  - Backup & Restore (Cold Standby): High RTO (hours/days), low cost.
  - Pilot Light: Core data replicated, minimal compute idle in standby region.
  - Warm Standby: Scaled-down version of full environment running in second region.
  - Multi-Region Active-Passive: Automated DNS/Global routing failover.
  - Multi-Region Active-Active: Concurrent writes in multiple regions, CRDTs or Distributed SQL, multi-region routing.
- **Data Recovery Verification:** Automated continuous restoration testing (proving backups are actually restorable).

### 9.5 Incident Management & Postmortem Culture
- **Incident Response Framework:** Incident Commander (IC), Communications Lead, Operations Lead.
- **Blameless Postmortems:** Root cause analysis (The 5 Whys), systemic contributor identification rather than human blame.
- **Action Items & Tracking:** Ensuring postmortem remediation items prevent recurrence.

---

## 💻 Practical Hands-On Project
Build a **Multi-Region Resilient Architecture & Chaos Simulator**:
1. Deploy an application across two cloud regions with active-active traffic routing via Route53 / Cloudflare.
2. Configure **Envoy Circuit Breakers** and **Exponential Backoff with Full Jitter** on all inter-service clients.
3. Deploy **Chaos Mesh** and execute the following chaos experiments:
   - Inject 200ms latency and 30% packet loss between services.
   - Simulate an entire availability zone (AZ) network blackhole.
   - Kill primary database nodes unexpectedly under heavy write traffic.
4. Verify that client requests gracefully fall back to cached responses or degrade without cascading errors, and document recovery time.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** A global payments processing company must guarantee an RTO of $< 60$ seconds and an RPO of $0$ seconds (zero transaction loss) in the event of an entire cloud region failure.
- **Decision:** Evaluate **Active-Active Multi-Region with Distributed SQL (CockroachDB/Spanner)** vs **Active-Passive with Synchronous Cross-Region Storage Replication**.
- **Deliverable:** Write an ADR addressing physical speed-of-light roundtrip latencies (e.g., 70ms between US-East and EU-West), write commit latency overhead, and cost implications.

---

## ✅ Completion Criteria
- [ ] Calculate SLO error budgets and configure a multi-window multi-burn-rate alert in Prometheus.
- [ ] Prove mathematically why Exponential Backoff with Full Jitter eliminates retry clustering.
- [ ] Successfully conduct a simulated Chaos Mesh game day experiment with documented hypotheses and findings.
- [ ] Write a production-grade Blameless Postmortem for a simulated cascading failure outage.
