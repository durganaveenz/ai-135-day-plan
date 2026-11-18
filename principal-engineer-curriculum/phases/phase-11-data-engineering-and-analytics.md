# Phase 11 — Advanced Data Engineering & Analytics
> **Domain:** Lakehouse Architecture, Apache Iceberg, Distributed Query Engines & Data Mesh  
> **Duration:** Month 13  
> **Practical Project:** Real-Time Lakehouse Pipeline (CDC + Kafka + Flink + Iceberg)

---

## 🎯 Objective
Master the architecture of modern enterprise data platforms. Bridge the gap between transactional databases (OLTP) and analytical warehouses (OLAP). Understand open table formats, distributed query optimization, change data capture, and decentralized Data Mesh governance.

---

## 📋 Topic Breakdown

### 11.1 Modern Analytical Storage & Lakehouse Architecture
- **Evolution of Analytical Architectures:**
  - Traditional Enterprise Data Warehouses (EDW) vs Data Lakes (Hadoop/S3).
  - The Lakehouse Paradigm: Combining the ACID transactional guarantees of data warehouses with the low-cost object storage of data lakes.
- **The Medallion Architecture:**
  - **Bronze Layer (Raw):** Append-only raw ingestion, immutable source data preserving fidelity.
  - **Silver Layer (Cleansed/Enriched):** Deduplicated, validated, normalized, and joined domain entities.
  - **Gold Layer (Aggregated/Business):** High-performance star/snowflake schemas, dimensional modeling for business intelligence and reporting.
- **Open Table Formats Deep Dive:**
  - **Apache Iceberg:** Metadata tree architecture (Iceberg Catalog $\rightarrow$ Metadata File $\rightarrow$ Manifest List $\rightarrow$ Manifest Files $\rightarrow$ Parquet Data Files), snapshot isolation, time travel, schema evolution, partition evolution without rewriting data.
  - **Delta Lake:** Transaction log (`_delta_log` JSON + checkpoint Parquet files), ACID guarantees.
  - **Apache Hudi:** Copy-on-Write (CoW) vs Merge-on-Read (MoR) for ultra-low latency updates.
- **Columnar File Formats Internals:**
  - Apache Parquet & ORC: Column chunks, row groups, dictionary encoding, run-length encoding (RLE), bit-packing.
  - Min/Max statistics, dictionary filtering, and predicate pushdown at the file reader level.

### 11.2 Distributed Data Processing & Query Engines
- **OLTP vs OLAP Architecture:**
  - Row-store vs Column-store query execution models.
  - HTAP (Hybrid Transactional/Analytical Processing): TiFlash, SingleStore.
- **Apache Spark Internals:**
  - Catalyst Optimizer: Analysis, Logical Plan optimization, Physical Plan generation, Whole-Stage Code Generation (Janino).
  - Tungsten Execution Engine: Off-heap memory management, cache-aware computation, binary row formats.
  - Spark Partitioning, Shuffling, and Skew Join mitigation (Salting, Broadcast joins).
- **Distributed SQL Query Engines:**
  - **Trino (formerly PrestoSQL):** In-memory pipelined distributed query execution, coordinator and worker topology, connector architecture.
  - **DuckDB:** Embedded analytical database, columnar vectorized execution engine, zero-copy querying of Parquet files directly from local memory or S3.
- **Distributed ETL/ELT Pipelines:** Orchestration with Apache Airflow vs Dagster, idempotent pipeline design.

### 11.3 Enterprise Data Governance & Data Mesh
- **Data Mesh Architectural Paradigm:**
  - Domain-Driven Decentralized Data Ownership (Treating data as a product).
  - Federated Computational Governance.
  - Self-Serve Data Infrastructure as a Platform.
- **Data Contracts:**
  - Defining schema, SLA, and semantics between data producers and downstream consumers.
  - Schema registry validation, breaking change prevention.
- **Data Lineage & Cataloging:**
  - OpenLineage standard, automated lineage extraction from Spark/Flink jobs.
  - Data Discovery: Apache Atlas, Amundsen, DataHub.
- **Data Quality Engineering:**
  - Declarative data testing (Great Expectations, dbt tests, Soda).
  - Data observability: Detecting freshness anomalies, volume anomalies, and schema drift.

---

## 💻 Practical Hands-On Project
Build a **Real-Time CDC-to-Lakehouse Streaming Architecture**:
1. Capture row-level inserts, updates, and deletes from PostgreSQL using **Debezium (Change Data Capture)**.
2. Stream CDC events into **Apache Kafka**.
3. Use **Apache Flink** to consume the CDC changelog, process transformations, and stream writes into an **Apache Iceberg** table on MinIO/S3.
4. Execute concurrent SQL analytics on the Iceberg table using **Trino / DuckDB**.
5. Demonstrate an **Iceberg Time Travel Query** inspecting table state at a previous snapshot timestamp.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** A multinational enterprise currently maintains both a Snowflake cloud data warehouse (\$1.2M/year) and a raw S3 data lake.
- **Decision:** As Principal Data Architect, evaluate transitioning to an **Open Lakehouse Architecture (Apache Iceberg on S3 + Trino/Spark)** vs remaining on Snowflake.
- **Deliverable:** Write an ADR analyzing query performance, table lock contention, vendor lock-in, storage-compute decoupling, and engineering maintenance overhead.

---

## ✅ Completion Criteria
- [ ] Inspect an Apache Iceberg metadata JSON file and trace how snapshots reference manifest files.
- [ ] Explain Parquet predicate pushdown and demonstrate how dictionary encoding accelerates string filtering.
- [ ] Implement an automated data contract test that rejects schema-breaking CDC events before lakehouse ingestion.
- [ ] Execute the CDC $\rightarrow$ Kafka $\rightarrow$ Flink $\rightarrow$ Iceberg pipeline with verified ACID time-travel queries.
