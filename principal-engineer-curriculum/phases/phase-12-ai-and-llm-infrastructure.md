# Phase 12 — Advanced AI / LLM Infrastructure & Agentic Systems
> **Domain:** LLM Internals, High-Throughput Serving, Agentic Frameworks & AI Gateways  
> **Duration:** Months 14–15  
> **Practical Project:** [Enterprise Multi-Tenant AI Platform](../projects/08-enterprise-ai-platform.md)

---

## 🎯 Objective
Master the engineering, serving, and orchestration of Large Language Models (LLMs) and autonomous AI agents at production scale. Understand model architectures, inference acceleration algorithms (PagedAttention), high-performance serving engines (vLLM), hybrid RAG pipelines, and agent communication protocols (MCP).

---

## 📋 Topic Breakdown

### 12.1 Large Language Model Internals & Theory
- **Transformer Architecture Foundations:**
  - Encoder-Decoder vs Encoder-Only vs Decoder-Only (GPT family, Llama, Gemma).
  - Multi-Head Attention (MHA), Multi-Query Attention (MQA), Grouped-Query Attention (GQA).
  - Positional Encodings: Sinusoidal vs Learned vs Rotary Position Embedding (RoPE).
  - Feed-Forward Networks (FFN), SwiGLU activation functions, Layer Normalization (RMSNorm).
- **The KV Cache & Memory Footprint:**
  - Why autoregressive generation is memory-bound rather than compute-bound during the decode phase.
  - Mathematical derivation of KV Cache size: $2 \times 2 \times n_{layers} \times d_{model} \times seq\_len \times batch\_size \times bytes\_per\_element$.
- **Tokenization & Embeddings:**
  - Byte-Pair Encoding (BPE), WordPiece, SentencePiece.
  - High-dimensional vector spaces, cosine similarity, Euclidean distance, dot product.
- **Model Quantization & Efficient Fine-Tuning:**
  - Quantization techniques: FP16 $\rightarrow$ INT8 $\rightarrow$ INT4 (GPTQ, AWQ, bitsandbytes).
  - Parameter-Efficient Fine-Tuning (PEFT): Low-Rank Adaptation (LoRA), QLoRA, rank and alpha hyperparameter tuning.
- **Distributed Training Paradigms:**
  - Data Parallelism (DDP), Tensor Parallelism (Megatron-LM), Pipeline Parallelism, ZeRO stages (1, 2, 3).
  - Mixture of Experts (MoE): Sparse routing, gating networks, capacity factor.

### 12.2 Retrieval-Augmented Generation (RAG) Systems
- **Advanced RAG Pipeline Architecture:**
  - Document Ingestion: Parsing, chunking strategies (fixed-size, semantic chunking, recursive character splitting, parent-child chunking).
  - Dense vs Sparse Retrieval: Dense vectors (BERT/BGE/OpenAI embeddings) vs Sparse lexical search (BM25).
  - Hybrid Search & Reciprocal Rank Fusion (RRF).
- **Vector Database Internals:**
  - Approximate Nearest Neighbor (ANN) Indexing: HNSW (Hierarchical Navigable Small World), IVF-PQ (Inverted File with Product Quantization).
  - Vector DB Engines: Qdrant, Milvus, Weaviate, pgvector.
- **Reranking & Context Refinement:**
  - Cross-Encoder models (Cohere Rerank, BGE-Reranker) vs Bi-Encoder embeddings.
  - Query Rewriting, HyDE (Hypothetical Document Embeddings), Step-Back Prompting.
- **GraphRAG & Knowledge Graphs:**
  - Extracting entities and relationships with LLMs, Neo4j graph storage, combining vector similarity with graph traversal.
- **Evaluation & Guardrails:**
  - RAG Evaluation Frameworks: RAGAS, DeepEval (Faithfulness, Answer Relevance, Context Precision, Context Recall).
  - Security & Guardrails: Prompt injection defense, Jailbreak detection (Llama Guard, NeMo Guardrails), PII masking.

### 12.3 Autonomous Agentic Systems & Protocols
- **Agent Architectures & Decision Loops:**
  - ReAct (Reasoning + Acting) loop, Plan-and-Solve, Reflection and Self-Correction.
  - Tool Calling & Function Calling: JSON schema generation, structured output validation.
- **Multi-Agent Orchestration:**
  - Hierarchical agent swarms, supervisor patterns, peer-to-peer delegation (LangGraph, CrewAI, AutoGen).
  - Agent State Management: Persistent checkpointing, memory stores (short-term conversation window vs long-term vector/summary memory).
  - Human-in-the-Loop (HITL) approval workflows and state rollbacks.
- **Agent Communication & Open Protocols:**
  - **Model Context Protocol (MCP):** Architecture of MCP Hosts, Clients, and Servers. Exposing tools, resources, and prompts over standard transports (stdio, SSE).
  - Agent Security: Sandboxing code execution, least-privilege tool access, rate limiting agent API calls.

### 12.4 High-Performance AI Inference & Serving Infrastructure
- **Modern Serving Engines:**
  - **vLLM Internals:** PagedAttention (managing non-contiguous GPU memory for KV cache like virtual memory paging in OS), continuous batching.
  - TensorRT-LLM, TGI (Text Generation Inference), Triton Inference Server.
- **Inference Optimization Techniques:**
  - Continuous Batching (Iteration-level scheduling) vs Static Batching.
  - Speculative Decoding: Using a small draft model to generate tokens verified in parallel by a target foundation model.
  - Chunked Prefill: Interleaving compute-heavy prefill phases with memory-heavy decode phases.
- **AI Gateway & Traffic Routing:**
  - Intelligent Model Routing: Directing simple queries to 8B models and complex reasoning to 70B/405B models.
  - Semantic Caching: Caching responses for semantically similar prompts using vector distance thresholds (GPTCache).
  - Inference Autoscaling: Autoscaling GPU pods based on queue depth and KV cache memory utilization rather than standard CPU/memory metrics.

---

## 💻 Practical Hands-On Project
Build an **Enterprise Multi-Tenant AI Platform**:
1. Deploy **vLLM** with PagedAttention serving an open foundation model (e.g., Llama 3 or Mistral).
2. Build an **AI Gateway** featuring semantic caching via Redis vector search, token rate limiting, and prompt guardrails.
3. Construct an **Agentic System** using **LangGraph** and the **Model Context Protocol (MCP)** to securely query internal databases and search engines.
4. Implement automated **RAGAS Evaluation** asserting that faithfulness scores exceed 0.85 across test datasets.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** An enterprise wants to build an automated legal contract intelligence agent.
- **Decision:** As Principal AI Architect, compare **Standard Vector RAG (Hybrid Search + BGE Rerank)** vs **GraphRAG (Knowledge Graph extraction + Neo4j)** vs **Ultra-Long Context Foundation Models (1M+ context window direct injection)**.
- **Deliverable:** Write an ADR factoring in token ingestion costs, query latency, multi-hop reasoning capability, and operational data freshness.

---

## ✅ Completion Criteria
- [ ] Calculate the exact GPU VRAM requirement for serving a 70B FP16 model with a 4,096 token context across a batch of 32 concurrent users.
- [ ] Diagram how PagedAttention eliminates internal and external KV cache memory fragmentation.
- [ ] Implement an MCP Server providing structured database tools to an autonomous agent.
- [ ] Deploy and benchmark a vLLM serving cluster under continuous batching.
