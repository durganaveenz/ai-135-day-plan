# Phase 3 — Advanced Database Engineering
> **Domain:** Storage Engines, Transaction Internals, Distributed SQL & NewSQL  
> **Duration:** Months 5–6 (Integrated with Phase 4)  
> **Practical Project:** [Mini Database Storage Engine](../projects/03-mini-database-storage-engine.md)

---

## 🎯 Objective
Demystify how relational, NoSQL, and NewSQL databases store, index, and recover data. Understand storage data structures at the byte and disk level, master ACID isolation phenomena, and explore the architecture of globally distributed SQL databases.

---

## 📋 Topic Breakdown

### 3.1 Database Storage Engine Internals
- **Storage Hierarchy & Hardware:** HDD spinning disks vs SSD/NVMe flash, write amplification factor (WAF), block devices.
- **Page-Based Storage Layout:**
  - Page header, slotted page architecture, tuple pointers, free space management.
  - Row-Oriented Storage (PostgreSQL heap files) vs Columnar Storage (Parquet, ClickHouse, DuckDB).
- **Index Data Structures & Storage Engines:**
  - **B-Trees & B+ Trees:** Internal nodes vs leaf nodes, page splitting, balancing, search and range scans.
  - **LSM Trees (Log-Structured Merge-Trees):**
    - MemTable (in-memory skiplist/red-black tree)
    - Write-Ahead Log (WAL) for durability
    - Immutable MemTable and SSTables (Sorted String Tables) on disk
    - Compaction algorithms: Size-Tiered Compaction vs Leveled Compaction
    - Bloom Filters: Avoiding unnecessary disk reads for non-existent keys.
- **Buffer Pool Management:** LRU-K, Clock sweep algorithm, dirty pages, flush policies (checkpointing).
- **Write-Ahead Logging (WAL) & Crash Recovery:**
  - ARIES recovery algorithm (Analysis, Redo, Undo phases)
  - Physiological logging, fuzzy checkpointing.

### 3.2 Transaction Internals & Concurrency Control
- **ACID Deep Dive:** Atomicity, Consistency, Isolation, Durability definitions and implementations.
- **ANSI SQL Isolation Levels & Anomalies:**
  - Dirty Read, Non-Repeatable (Fuzzy) Read, Phantom Read
  - Advanced Anomalies: Lost Update, Read Skew, Write Skew (Snapshot Isolation vulnerability).
- **Isolation Level Mechanisms:**
  - Read Uncommitted, Read Committed, Repeatable Read, Serializable.
- **Concurrency Control Approaches:**
  - **Two-Phase Locking (2PC / 2PL):** Growing phase, shrinking phase, Strict 2PL, Rigorous 2PL.
  - **Deadlock Handling:** Wait-For graphs, cycle detection, timeout-based detection, wound-wait vs wait-die.
  - **Optimistic Concurrency Control (OCC):** Read phase, validation phase, write phase.
  - **Multi-Version Concurrency Control (MVCC):**
    - Row versioning (xmin, xmax in Postgres; Undo logs in InnoDB)
    - Snapshot Isolation (SI)
    - Serializable Snapshot Isolation (SSI): Detecting dangerous read-write dependency cycles (rw-antidependencies).
    - Vacuuming & Garbage Collection: PostgreSQL VACUUM / AUTOVACUUM bloat vs MySQL Undo tablespace purge.

### 3.3 Distributed Databases & NewSQL
- **Distributed SQL Architecture:** CockroachDB, YugabyteDB, Google Spanner, TiDB.
- **Data Sharding & Tablet Distribution:** Range-based partitioning vs Hash-based partitioning.
- **Distributed Query Execution & Optimization:**
  - Distributed Cost-Based Optimizer (CBO)
  - Broadcast Join vs Hash Join vs Colocated Join
  - Global Secondary Indexes (GSI): Asynchronous vs Synchronous index maintenance.
- **Distributed Transactions at Scale:**
  - Google Spanner TrueTime API + Multi-Paxos + 2PC
  - CockroachDB Hybrid Logical Clocks (HLC) + Raft + Read-Restart / Write intents.
- **Zero-Downtime Schema Migrations:**
  - Online DDL algorithms (gh-ost, pt-online-schema-change)
  - Multi-version schema evolution without blocking concurrent writes.

### 3.4 Deep Architectural Comparisons
- **PostgreSQL Internals:** Process-based architecture, shared buffers, WAL writer, autovacuum, TOAST tables.
- **MySQL InnoDB Internals:** Thread-pool, buffer pool, doublewrite buffer, adaptive hash index, change buffer.
- **Redis Internals:** Single-threaded event loop, RESP protocol, SDS (Simple Dynamic Strings), ziplist, dict resharding, RDB & AOF persistence.
- **Cassandra / ScyllaDB:** Wide-column store, Ring architecture, Token ranges, Gossip, Read repair, Tombstone compaction penalty.
- **ClickHouse:** Vectorized query execution, SIMD instructions, MergeTree engine family, block-level compression.

---

## 💻 Practical Hands-On Project
Build a **Mini Storage Engine with WAL and Compaction**:
1. Implement a Write-Ahead Log (WAL) that flushes appends to disk with `fsync()`.
2. Implement an in-memory **MemTable** backed by a SkipList.
3. When MemTable reaches a threshold, freeze it and flush an immutable **SSTable** file with index block and Bloom filter.
4. Implement a **Leveled Compaction Worker** that merges overlapping SSTables and eliminates deleted tombstones.
5. Implement crash recovery by replaying the WAL upon startup.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** An international neo-bank with 50 million accounts requires a primary ledger database supporting ACID multi-region transactions, sub-20ms reads globally, and 99.999% availability.
- **Decision:** Compare **PostgreSQL (with Aurora Global Database)** vs **CockroachDB / YugabyteDB** vs **Amazon DynamoDB (with Global Tables and DynamoDB Transactions)**.
- **Deliverable:** Write an ADR addressing cross-region write latencies (speed of light constraints), consistency guarantees (SSI vs Eventual), and operational risk.

---

## ✅ Completion Criteria
- [ ] Diagram and trace an ARIES recovery cycle (Analysis, Redo, Undo) with sample WAL log records.
- [ ] Explain how Write Skew happens under Snapshot Isolation with a concrete SQL transaction example.
- [ ] Successfully implement the mini LSM storage engine and demonstrate crash recovery without data loss.
- [ ] Defend an ADR on Single-Region RDBMS vs Distributed SQL for a mission-critical financial system.
