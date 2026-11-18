# Project 01 — Distributed Key-Value Database with Raft Consensus
> **Phase Alignment:** [Phase 2 — Distributed Systems Deep Internals](../phases/phase-02-distributed-systems.md)  
> **Target Complexity:** Senior / Staff / Principal Systems Engineering  
> **Recommended Languages:** Go, Rust, C++

---

## 🎯 Project Overview
Design and build a horizontally scalable, fault-tolerant, replicated key-value storage engine from scratch using the **Raft Consensus Protocol**. The database must guarantee linearizable reads and writes, handle concurrent node crashes, support dynamic cluster membership changes, and survive network partitions without split-brain anomalies.

---

## 🏗️ Architecture & Component Design

```mermaid
flowchart TD
    Client["Client Application"]
    
    subgraph Cluster["3-Node or 5-Node Raft Cluster"]
        subgraph Node1["Node 1 (Leader)"]
            RPC1["gRPC / Transport"]
            Raft1["Raft Engine<br/>(State Machine / Log)"]
            FSM1["State Machine<br/>(KV Store Engine)"]
            WAL1["Persistent WAL & Snapshots"]
            RPC1 --> Raft1
            Raft1 --> FSM1
            Raft1 --> WAL1
        end

        subgraph Node2["Node 2 (Follower)"]
            RPC2["gRPC / Transport"]
            Raft2["Raft Engine"]
            FSM2["State Machine (KV)"]
            WAL2["Persistent WAL & Snapshots"]
            RPC2 --> Raft2
            Raft2 --> FSM2
            Raft2 --> WAL2
        end

        subgraph Node3["Node 3 (Follower)"]
            RPC3["gRPC / Transport"]
            Raft3["Raft Engine"]
            FSM3["State Machine (KV)"]
            WAL3["Persistent WAL & Snapshots"]
            RPC3 --> Raft3
            Raft3 --> FSM3
            Raft3 --> WAL3
        end
    end

    Client -->|Put(key, val) / Get(key)| RPC1
    Raft1 -.->|AppendEntries RPC| Raft2
    Raft1 -.->|AppendEntries RPC| Raft3
```

---

## 📋 Core Architectural Requirements

### 1. Consensus Core (Raft Implementation)
- **Leader Election:** Randomized election timeouts (150ms–300ms), RequestVote RPC, heartbeat timers.
- **Log Replication:** AppendEntries RPC, leader commit index tracking, log entry consistency checks.
- **Safety Invariants:**
  - Election Safety: At most one leader per term.
  - Leader Append-Only: Leader never overwrites or truncates its own log entries.
  - Log Matching: If two logs contain an entry with the same index and term, then logs are identical up to that index.
  - Leader Completeness: If a log entry is committed in a given term, it will be present in the logs of the leaders for all higher-numbered terms.
- **Log Compaction & Snapshots:** Snapshotting state machine state to disk and truncating compacted log entries; `InstallSnapshot` RPC for lagging nodes.
- **Cluster Membership Changes:** Dynamic single-node addition and removal (`AddServer`, `RemoveServer`).

### 2. Key-Value State Machine
- Thread-safe in-memory or disk-backed key-value store.
- Operations: `Get(key)`, `Put(key, value)`, `Delete(key)`, `CompareAndSwap(key, oldVal, newVal)`.
- Client session tracking to enforce strict **linearizability** (deduplicating retried client commands).

### 3. Sharding & Hash Ring (Advanced Milestone)
- Consistent hashing ring with virtual nodes (e.g., 256 vnodes per physical node).
- Data distribution across multiple independent Raft consensus groups (Multi-Raft architecture like TiKV / CockroachDB).

---

## 🧪 Verification & Chaos Testing Harness
- **Partition Simulation:** Form a network partition isolating the leader into a minority partition (1 node vs 2 nodes). Verify that:
  - The minority leader rejects or stalls commits.
  - The majority partition elects a new leader and makes continuous progress.
  - When the partition heals, the old leader steps down, updates its term, and synchronizes its log without data corruption.
- **Crash Recovery:** Kill random nodes mid-flight during 10,000 concurrent client write operations; verify zero lost committed updates.
