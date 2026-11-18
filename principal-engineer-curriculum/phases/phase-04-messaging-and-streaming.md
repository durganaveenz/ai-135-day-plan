# Phase 4 — Advanced Messaging & Streaming Systems
> **Domain:** Message Brokers, Event Streaming, Apache Kafka & Apache Flink  
> **Duration:** Months 5–6 (Integrated with Phase 3)  
> **Practical Project:** [Real-Time Event Processing Platform](../projects/04-realtime-event-processing-platform.md)

---

## 🎯 Objective
Master the architecture of event backbones that decouple modern distributed applications. Understand disk-based immutable commit logs, end-to-end delivery guarantees, partition rebalancing algorithms, and real-time stateful stream processing with event-time semantics.

---

## 📋 Topic Breakdown

### 4.1 Messaging Architecture & Delivery Guarantees
- **Message Broker Paradigms:** Traditional Queue (RabbitMQ, SQS) vs Distributed Commit Log (Kafka, Pulsar).
- **Pub/Sub vs Point-to-Point Messaging:** Fanout, topic subscriptions, worker queues.
- **Message Ordering Guarantees:** Total order vs Per-key / Per-partition ordering.
- **Delivery Semantics:**
  - At-Most-Once (Acknowledge before processing, risk of message drop)
  - At-Least-Once (Retry on failure, requires idempotent consumer processing)
  - Exactly-Once Processing (Transactional producers + stateful checkpointing).
- **Idempotency Patterns:** Deduplication keys, Bloom filters, database unique constraints.
- **Dead Letter Queues (DLQ) & Resilience:** Poison pill isolation, delayed retry queues, exponential backoff consumers.
- **Backpressure & Flow Control:** Consumer push vs pull models, TCP window backpressure, reactive streams.

### 4.2 Apache Kafka Internals & Architecture
- **Cluster Architecture:** Brokers, ZooKeeper vs KRaft (Kafka Raft Metadata Mode), Controller broker election.
- **Topic & Partition Internals:**
  - Append-only commit log on disk, `.log` and `.index` segment files.
  - Zero-Copy data transfer (`sendfile()` system call from OS page cache directly to network socket).
  - Log Compaction: Cleaning old keys, maintaining latest value state, tombstones.
- **Replication & Fault Tolerance:**
  - Replication Factor, In-Sync Replicas (ISR), Leader and Follower replicas.
  - High Watermark (HW) vs Log End Offset (LEO).
  - Unclean Leader Election risks and trade-offs (`min.insync.replicas` and `acks=all`).
- **Producer Internals:** Batching, buffer pool, compression (Snappy, LZ4, Zstandard), partitioner hashing, idempotent producer (PID + sequence numbers).
- **Consumer Internals:**
  - Consumer Groups, partition assignment strategies (Range, RoundRobin, Sticky, Cooperative Sticky).
  - Group Coordinator, heartbeats, session timeouts, rebalance protocols (Eager vs Incremental Cooperative Rebalancing).
  - Offset Management: `__consumer_offsets` topic, manual vs auto-commit.
- **Kafka Transactions & Exactly-Once Semantics (EOS):** Transaction Coordinator, Two-Phase Commit over Kafka topics, markers.
- **Schema Governance:** Confluent Schema Registry, Avro, Protobuf, schema compatibility modes (Backward, Forward, Full).

### 4.3 Stateful Stream Processing (Apache Flink & Kafka Streams)
- **Time Semantics in Stream Processing:**
  - Event Time vs Ingestion Time vs Processing Time.
  - Time Skew and Out-of-Order Events.
- **Watermarking Algorithms:** Monotonous watermarks, bounded-out-of-orderness watermarks, late event handling.
- **Windowing Strategies:**
  - Tumbling Windows (Fixed-size, non-overlapping)
  - Sliding Windows (Fixed-size, overlapping)
  - Session Windows (Gap-based inactivity)
  - Global Windows with custom triggers.
- **Stateful Stream Processing Internals:**
  - Keyed State, Operator State, Broadcast State.
  - State Backends: In-Memory (HashMap) vs Embedded RocksDB state backend.
- **Fault Tolerance & Checkpointing:**
  - Chandy-Lamport variant (Asynchronous Barrier Snapshotting - ABS).
  - Alignment vs Unaligned Checkpoints under high backpressure.
  - Savepoints for operational upgrades and state migrations.
- **Stream-Table Duality:** Changelog stream to Table ($KTable$) and Table to changelog stream.
- **Architectural Paradigms:** Lambda Architecture (Batch + Speed layers) vs Kappa Architecture (Pure stream processing with replayable log).

---

## 💻 Practical Hands-On Project
Build a **Real-Time Financial Fraud Detection & Transaction Streaming Pipeline**:
1. Ingest credit card transactions into Apache Kafka at 10,000+ events/sec.
2. Build an **Apache Flink** stateful streaming application.
3. Use **Event-Time Watermarks** and **Sliding Windows (e.g., 5-minute sliding by 10 seconds)** to detect velocity anomalies (e.g., more than 3 transactions across different countries within 5 minutes).
4. Maintain user profiles in Flink RocksDB state and emit flagged fraud alerts to a dedicated Kafka topic.
5. Demonstrate state recovery from a Flink Savepoint after an intentional worker failure.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** An analytics platform requires ingestion of 2 billion IoT telemetry events daily with 1-second queryability.
- **Decision:** Compare **Kafka + Apache Flink** vs **Apache Pulsar** vs **AWS Kinesis + Managed Flink**.
- **Deliverable:** Write an ADR focusing on tiered storage, multi-tenancy, partition scalability, operational complexity, and cloud egress costs.

---

## ✅ Completion Criteria
- [ ] Explain how Linux Zero-Copy (`sendfile`) works in Kafka and why it minimizes CPU and memory bandwidth.
- [ ] Trace an Incremental Cooperative Rebalance in Kafka and explain why it prevents "stop-the-world" consumer pauses.
- [ ] Diagram Flink's Asynchronous Barrier Snapshotting algorithm across 3 chained operators.
- [ ] Complete the practical fraud detection streaming pipeline with automated tests.
