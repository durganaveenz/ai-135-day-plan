# Phase 0 — Engineering Foundations (Prerequisite)
> **Domain:** Computer Science, Operating Systems, Networking & Runtime Internals  
> **Duration:** Months 1–2 (Integrated with Phase 1)  
> **Depth:** Core Underlying CS Principles

---

## 🎯 Objective
High-level architectural abstractions are only as reliable as the underlying hardware, OS, and network on which they run. This phase solidifies the low-level systems foundation required to diagnose distributed deadlocks, memory leaks, CPU starvation, and network latency anomalies.

---

## 📋 Topic Breakdown

### 0.1 Computer Science & OS Internals
- **Operating System Architecture:** Monolithic vs Microkernel vs Hybrid.
- **Process vs Thread:** Thread execution models, kernel threads vs user-space green threads.
- **User Mode vs Kernel Mode:** Privilege rings (Ring 0 vs Ring 3), context switching overhead.
- **System Calls:** `read()`, `write()`, `epoll()`, `kqueue()`, `mmap()`, syscall interception and overhead.
- **CPU Scheduling Algorithms:** CFS (Completely Fair Scheduler), Real-Time priority, CPU affinity.
- **Memory Management:** Virtual Memory, Paging, Segmentation, TLB (Translation Lookaside Buffer) misses.
- **Stack vs Heap:** Memory allocation mechanisms, fragmentation, arena allocators.
- **Garbage Collection Foundations:** Tracing vs Reference Counting, Mark-Sweep-Compact, Generational hypothesis.
- **File Systems & Inodes:** Directory structure, disk blocks, page cache, VFS (Virtual File System).
- **Interrupts & Signals:** Hardware vs software interrupts, signal handling, POSIX signals.
- **Deadlocks & Starvation:** Coffman conditions, deadlock prevention, detection, and avoidance.
- **Concurrency Primitives:** Mutex, Semaphore, Spinlocks, Reader-Writer locks.
- **Atomic Operations & Lock-Free:** Compare-and-Swap (CAS), Memory barriers, Memory Models (Relaxed, Acquire-Release, Sequential Consistency).
- **CPU Cache Hierarchy:** L1/L2/L3 caches, cache lines (64-byte), False Sharing, Cache Coherence protocols (MESI/MOESI).

### 0.2 Networking Internals
- **OSI and TCP/IP Models:** Encapsulation, packet headers, framing.
- **TCP Three-Way Handshake & Teardown:** SYN, SYN-ACK, ACK, FIN-WAIT, TIME-WAIT state exhaustion.
- **TCP Congestion Control:** Slow Start, Congestion Avoidance, Fast Retransmit, Cubic vs BBR algorithms.
- **TCP Flow Control:** Sliding Window, TCP Window Scale option, Zero Window probes.
- **UDP Internals:** Connectionless datagrams, UDP buffer sizing, multicast.
- **HTTP Evolution:** HTTP/1.1 (Pipelining, HOL blocking) → HTTP/2 (Multiplexing, HPACK) → HTTP/3 (QUIC, 0-RTT, UDP-based).
- **TLS 1.2 vs TLS 1.3:** Handshake latency, Perfect Forward Secrecy, cipher suites, resumption.
- **DNS Resolution & Routing:** Recursive vs Authoritative resolvers, DNS TTL, Anycast DNS, DNS caching issues.
- **Routing & Gateways:** BGP (Border Gateway Protocol), NAT (Network Address Translation), Port forwarding.
- **Reverse Proxy & Load Balancing:** L4 (TCP/UDP) vs L7 (HTTP) load balancing, consistent hashing, round-robin, least connections.
- **Connection Management:** Connection pooling, Keep-Alive, HTTP/2 multiplexing, WebSocket protocol handshake.
- **Network Impairments:** Packet loss, out-of-order delivery, retransmission timers (RTO), network partitioning.

### 0.3 Programming Language & Runtime Internals
- **Compilation Pipelines:** Lexical analysis, Parsing, AST (Abstract Syntax Tree), IR (Intermediate Representation), Code generation.
- **JIT Compilation vs AOT Compilation:** Hotspot optimization, deoptimization, tiered compilation.
- **Runtime Virtual Machines:** JVM, V8, Go Runtime internals.
- **Memory Ownership & Safety:** Rust ownership and borrow checker vs Go/Java GC vs C/C++ manual memory management.
- **Async Runtimes & Event Loops:** Reactor pattern, Proactor pattern, epoll/kqueue integration, Tokio (Rust) vs Go Goroutine Netpoller.
- **Thread Pools & Work Stealing:** Fork-Join pools, work-stealing queues, scheduling starvation.
- **Lock-Free Data Structures:** Lock-free queue (Michael-Scott queue), lock-free ring buffers, ABA problem and tagged pointers.
- **Type Systems & Reflection:** Static vs Dynamic typing, compile-time generics vs runtime reflection performance costs.

---

## 💻 Practical Hands-On Project
Build the following primitives from scratch in **Go, Rust, or C/C++**:
1. **Custom Thread Pool:** Work-stealing thread pool with task queue and graceful shutdown.
2. **Lock-Free Ring Buffer:** Single-producer single-consumer (SPSC) and multi-producer multi-consumer (MPMC) circular buffer.
3. **High-Performance In-Memory Cache:** LRU/LFU cache with lock striping or fine-grained concurrency and TTL eviction.
4. **Simple Raw Socket HTTP/1.1 Server:** Non-blocking socket listener handling keep-alive connections without relying on high-level framework wrappers.

---

## ✅ Completion Criteria
- [ ] Diagram the lifecycle of a Linux system call from user-space application to kernel execution and return.
- [ ] Explain how False Sharing degrades multi-core performance and demonstrate how memory padding fixes it.
- [ ] Trace a full TCP handshake and TLS 1.3 handshake using Wireshark or tcpdump.
- [ ] Successfully implement the lock-free ring buffer and benchmark it against a standard mutex-locked queue.
