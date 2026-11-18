# Phase 7 — Advanced Cloud & Infrastructure Engineering
> **Domain:** Cloud Architecture, Kubernetes Internals, eBPF & Platform Engineering  
> **Duration:** Months 9–10  
> **Practical Project:** [Kubernetes Internal Developer Platform (IDP)](../projects/06-internal-developer-platform.md)

---

## 🎯 Objective
Master enterprise multi-account cloud landing zones, deep Kubernetes control plane and node agent internals, container runtime isolation mechanisms, eBPF-based high-performance networking, and modern internal developer platforms (IDP).

---

## 📋 Topic Breakdown

### 7.1 Enterprise Cloud Architecture & Multi-Region Design
- **Cloud Foundation:**
  - Multi-Account Organizations (AWS Organizations, GCP Resource Hierarchy).
  - Enterprise Landing Zones, Control Tower, Guardrails, Service Control Policies (SCPs).
- **Network Topology & Segmentation:**
  - Virtual Private Cloud (VPC) design: Public, Private, Isolated subnets, CIDR planning.
  - Inter-VPC Connectivity: VPC Peering, AWS Transit Gateway, Cloud Interconnect, Direct Connect.
  - Private Connectivity: AWS PrivateLink / VPC Endpoints, GCP Private Service Connect.
  - Cloud NAT, Egress Gateways, Cloud Load Balancers (ALB/NLB, Google Global External HTTP(S) LB).
- **Multi-Region & Hybrid Cloud:**
  - Global Anycast IP routing.
  - Multi-region database replication topologies, cross-region latency models.
  - Disaster Recovery topologies: Warm Standby, Pilot Light, Multi-Region Active-Active.

### 7.2 Kubernetes Control Plane & Node Internals
- **Control Plane Architecture:**
  - **`kube-apiserver`:** Request lifecycle (Authentication, Authorization Webhooks, Mutating/Validating Admission Controllers), etcd storage schema.
  - **`etcd`:** Raft cluster consistency, watch API, resource versioning, MVCC compaction.
  - **`kube-scheduler`:** Filtering (Predicates), Scoring (Priorities), Custom scheduling plugins, Scheduling Framework.
  - **`kube-controller-manager`:** Reconciliation loops, state convergence, Informers, Listers, Workqueues.
- **Node-Level Internals & Interfaces:**
  - **`kubelet`:** Pod worker, PLEG (Pod Lifecycle Event Generator), status sync.
  - **CRI (Container Runtime Interface):** CRI-O, containerd, OCI (Open Container Initiative) runtime specification (runc).
  - **CNI (Container Network Interface):** IPAM (IP Address Management), veth pairs, network namespaces, routing tables.
  - **CSI (Container Storage Interface):** PersistentVolumes, PersistentVolumeClaims, StorageClasses, dynamic provisioning, volume attachments.
- **Advanced Workload Constructs:**
  - Custom Resource Definitions (CRDs) & Kubernetes Operators (Kubebuilder / Operator SDK).
  - StatefulSets, DaemonSets, Jobs, CronJobs.
  - Pod Disruption Budgets (PDB), Resource Requests & Limits, QoS Classes (Guaranteed, Burstable, BestEffort).
  - Autoscaling: HPA (Horizontal Pod Autoscaler with custom Prometheus metrics), VPA (Vertical Pod Autoscaler), Cluster Autoscaler, Karpenter (Just-in-Time node provisioning).

### 7.3 Container Isolation, Linux Primitives & eBPF
- **Linux Kernel Primitives Under Containers:**
  - **Namespaces:** pid, net, ipc, mnt, uts, user, cgroup isolation.
  - **Cgroups (Control Groups v1 & v2):** CPU shares, CPU quota, memory limits, OOM killer mechanisms.
  - Rootless containers, user namespaces mapping.
  - Container boundary breakout vulnerabilities and defense-in-depth.
- **eBPF (Extended Berkeley Packet Filter) & Modern Networking:**
  - Kernel execution of sandboxed bytecode, JIT compilation, BPF verifier.
  - **Cilium:** eBPF-based service mesh, replacement of iptables/kube-proxy, direct server return (DSR), micro-segmentation at layer 7.
- **Service Mesh Architecture:**
  - Istio vs Linkerd: Control plane vs Data plane (Envoy proxy sidecars vs ambient mesh / daemonset mode).
  - Mutual TLS (mTLS), traffic splitting, fault injection, canary rollouts.

### 7.4 Platform Engineering, GitOps & IaC
- **GitOps & Continuous Delivery:**
  - Declarative infrastructure, Git as the single source of truth.
  - ArgoCD vs Flux: Reconciliation loops, self-healing, automated drift detection.
  - Progressive Delivery: Canary analysis, Blue-Green deployments with Argo Rollouts and Flagger.
- **Infrastructure as Code (IaC) Internals:**
  - Terraform / OpenTofu: State file management, distributed state locking (DynamoDB/S3), DAG (Directed Acyclic Graph) dependency resolution.
  - Pulumi: Programming language-driven infrastructure (TypeScript/Python/Go).
  - Policy-as-Code: OPA Gatekeeper, Kyverno, HashiCorp Sentinel.
- **Internal Developer Platforms (IDP):**
  - Developer Portals (Backstage), Golden Paths, ephemeral environments on pull requests.
  - Platform as a Product: Treating internal software developers as primary customers.

---

## 💻 Practical Hands-On Project
Build a **Kubernetes-Based Internal Developer Platform (IDP)**:
1. Deploy a multi-node Kubernetes cluster with **Cilium** as the CNI (eBPF mode, no kube-proxy).
2. Write a **Custom Kubernetes Operator** using Go and Kubebuilder that provisions an isolated tenant environment (Namespace, NetworkPolicies, ResourceQuotas, Vault secrets injection).
3. Set up **ArgoCD** to manage all cluster infrastructure and applications via GitOps.
4. Implement automated **Canary Deployments** with Argo Rollouts and Prometheus metrics analysis.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** An organization running 200 microservices on Kubernetes is experiencing severe CPU overhead (15% cluster CPU dedicated to Envoy sidecars) and latency degradation.
- **Decision:** Evaluate migrating from **Sidecar-based Service Mesh (Istio Envoy sidecars)** to **eBPF-based Ambient Mesh (Cilium Service Mesh / Istio Ambient)**.
- **Deliverable:** Write an ADR comparing Layer 7 inspection capabilities, mTLS certificate distribution, CPU/memory savings, and operational debugging complexity.

---

## ✅ Completion Criteria
- [ ] Inspect a running container's Linux namespaces and cgroups using low-level tools (`nsenter`, `lscgroup`).
- [ ] Diagram the complete Kubernetes API admission and reconciliation workflow.
- [ ] Successfully deploy a custom Kubernetes Operator that reconciles a Custom Resource Definition (CRD).
- [ ] Implement an Argo Rollouts canary deployment with automated rollback on error rate spikes.
