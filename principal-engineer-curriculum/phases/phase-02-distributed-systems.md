# Phase 2 — Distributed Systems: Deep Internals
> **Domain:** Distributed Algorithms, Consensus, Time, Consistency & Fault Tolerance  
> **Target Audience:** Principal Systems Engineers, Distributed Systems Architects  
> **Duration:** Months 3–4  
> **Practical Project:** [Distributed Key-Value Database with Raft Consensus](../projects/01-distributed-key-value-store.md)

---

## 🧭 Why This Phase is the Core of Principal Engineering
Distributed systems are fundamentally counter-intuitive. In a single process, failure is binary; in a distributed system, failure is partial, unpredictable, and masked by network latencies. A Principal Engineer must possess an instinctual understanding of consensus, logical clocks, failure detectors, and consistency trade-offs to design systems that survive real-world chaos.

---

## 📋 Topic Breakdown

### 2.1 Distributed Systems Fundamentals & Failure Models
- **System Models:** Synchronous vs Asynchronous vs Partially Synchronous systems.
- **The Fallacies of Distributed Computing:** Bandwidth is infinite, latency is zero, network is reliable.
- **Partial Failure & Network Partitions:** The impossibility of distinguishing a dead node from a slow network.
- **Failure Classifications:**
  - Crash-Stop Failures
  - Crash-Recovery Failures
  - Omission Failures (dropped packets, buffer overruns)
  - Byzantine Failures (arbitrary or malicious behavior).
- **The FLP Impossibility Theorem:** Impossibility of distributed consensus in an asynchronous system with even a single crash failure.
- **CAP Theorem & PACELC Theorem:** Trade-offs between Consistency, Availability, Latency, and Partition tolerance.

### 2.2 Time, Ordering & Logical Clocks
- **The Problem of Physical Time:**
  - Quartz clock drift, thermal drift, leap seconds
  - NTP (Network Time Protocol) limitations and Clock Skew / Clock Drift
  - TrueTime API (Google Spanner atomic clocks and GPS receivers).
- **Logical Clocks & Causal Ordering:**
  - Lamport Timestamps: Partial ordering of events
  - Happens-Before Relationship ($a \rightarrow b$)
  - Vector Clocks: Causality violation detection, concurrent event detection
  - Version Vectors in distributed key-value stores
  - Hybrid Logical Clocks (HLC): Combining physical time bounds with logical monotonicity.

### 2.3 Distributed Consensus Protocols
- **Consensus Definition:** Agreement, Validity, Termination.
- **Paxos Family:**
  - Single-decree Paxos: Proposer, Acceptor, Learner roles; Prepare/Promise and Propose/Accept phases.
  - Multi-Paxos: Leader election, log replication, pipelining.
- **Raft Consensus Protocol:**
  - Leader Election: Heartbeats, election timeouts, split votes, randomized timers
  - Log Replication: AppendEntries RPC, log matching invariant, committing entries
  - Safety Invariants: Election safety, Leader append-only, Log matching, Leader completeness, State machine safety
  - Cluster Membership Changes: Single-server transitions vs Joint Consensus
  - Log Compaction & Snapshotting.
- **Other Consensus Protocols:**
  - Zab Protocol (Apache ZooKeeper atomic broadcast)
  - Viewstamped Replication (VR Revisited)
  - Byzantine Fault Tolerance (PBFT - Practical Byzantine Fault Tolerance).

### 2.4 Consistency Models & Linearizability
- **Strong Consistency vs Linearizability:** Real-time ordering constraint on concurrent operations.
- **Sequential Consistency:** Valid order consistent across all observers, independent of physical real-time.
- **Causal Consistency:** Causally related operations are seen in the same order by all nodes.
- **Eventual Consistency:** System converges if no new updates are made.
- **Client-Centric Consistency Models:**
  - Read-Your-Writes Consistency
  - Monotonic Reads Consistency
  - Monotonic Writes Consistency
  - Writes-Follow-Reads Consistency.
- **Quorum Consistency:** $R + W > N$, Read repair, Hinted handoff, Sloppy quorums.

### 2.5 Replication, Partitioning & Hash Rings
- **Replication Topologies:** Single-Leader, Multi-Leader (conflict resolution: LWW, CRDTs), Leaderless (Dynamo-style).
- **Synchronous vs Asynchronous Replication:** Semi-sync replication, replication lag, stale reads.
- **Chain Replication:** High-throughput strong consistency with clean failure recovery.
- **Data Partitioning (Sharding):**
  - Consistent Hashing with Virtual Nodes (mitigating hot spots and cascading rebalance)
  - Rendezvous Hashing (Highest Random Weight hashing)
  - Online Data Migration and Rebalancing.
- **Split-Brain Mitigation:** Fencing tokens, majority quorums, hardware watchdog stonith (Shoot The Other Node In The Head).

### 2.6 Distributed Coordination & Conflict-Free Data Types (CRDTs)
- **Distributed Locks & Leases:** Chubby/ZooKeeper ephemeral nodes, Redis Redlock flaws and fencing token necessity.
- **Leader Election Implementations:** etcd lease keep-alive, ZooKeeper sequential ephemeral znodes.
- **Gossip Protocols & Failure Detection:** Epidemic algorithms, SWIM protocol, $\Phi$ (Phi) Accrual Failure Detector.
- **Conflict-Free Replicated Data Types (CRDTs):**
  - State-based (CvRDT) vs Operation-based (CmRDT)
  - Counters: G-Counter (Grow-only), PN-Counter (Positive-Negative)
  - Sets: 2P-Set, OR-Set (Observed-Remove Set), LWW-Element-Set
  - Registers: LWW-Register, Multi-Value Register.
- **Distributed Snapshots:** Chandy-Lamport distributed snapshot algorithm for global state capture.
- **Distributed Transactions:** Two-Phase Commit (2PC), Three-Phase Commit (3PC), Coordinator failure modes.

---

## 💻 Practical Hands-On Project
Build a **Distributed Replicated Key-Value Store with Raft Consensus**:
1. Implement the Raft consensus algorithm from scratch (Leader Election + Log Replication + Heartbeats).
2. Support dynamic cluster membership changes and snapshotting.
3. Simulate node crashes, network partitions (split-brain), and network message delays.
4. Verify linearizability of operations under partition using a test harness inspired by Jepsen.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** A global collaborative document editing system needs offline-first support with multi-device synchronization.
- **Decision:** Should the system employ **Operational Transformation (OT)**, **State-based CRDTs (CvRDT)**, or **Operation-based CRDTs (CmRDT)**?
- **Deliverable:** Write an ADR analyzing bandwidth consumption, state size explosion, tombstone garbage collection, and real-time collaboration UX.

---

## ✅ Completion Criteria
- [ ] Trace Raft leader election and log replication step-by-step with state machine transition diagrams.
- [ ] Prove why Two-Phase Commit (2PC) is a blocking protocol during coordinator crashes.
- [ ] Implement an OR-Set (Observed-Remove Set) CRDT and test concurrent adds and removes.
- [ ] Run a simulated 3-node network partition test on your Raft implementation demonstrating majority progress and minority stall.
