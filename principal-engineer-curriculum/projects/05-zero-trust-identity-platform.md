# Project 05 — Zero Trust Identity & Policy-Based Access Platform
> **Phase Alignment:** [Phase 6 — Advanced Security Architecture](../phases/phase-06-advanced-security.md)  
> **Target Complexity:** Staff / Principal Security & Platform Architect  
> **Recommended Technologies:** Keycloak, SPIFFE/SPIRE, Open Policy Agent (OPA), Envoy, Go

---

## 🎯 Project Overview
Architect and deploy an enterprise **Zero Trust Identity & Access Platform** that eliminates static secrets and perimeter assumptions. The platform authenticates end-users via OIDC/PKCE, issues cryptographically verifiable, short-lived workload identities to microservices via SPIFFE/SPIRE, and decouples fine-grained authorization policies using Open Policy Agent (OPA).

---

## 🏗️ Architecture & Component Design

```mermaid
flowchart TD
    User["End User / Browser"] -->|1. OIDC PKCE Login| Keycloak["Keycloak IAM<br/>(OAuth 2.1 / OIDC)"]
    Keycloak -->|2. Issue JWT Access Token| User
    
    User -->|3. Request + JWT Bearer| Ingress["Envoy Ingress Gateway"]
    
    subgraph ServiceMesh["Zero Trust Workload Boundary"]
        SPIREServer["SPIRE Server (CA)"]
        SPIREAgent["SPIRE Agent (Node Daemon)"]
        SPIREServer -.->|Attest & Issue SVID| SPIREAgent
        
        Ingress -->|4. Strict mTLS (X.509 SVID)| SvcA["Microservice A (Go)"]
        SPIREAgent -.->|Rotate SVID Certs| SvcA
        
        SvcA -->|5. Consult Policy| OPA["OPA Sidecar (Rego Engine)"]
        OPA -->|6. Allow / Deny Verdict| SvcA
        
        SvcA -->|7. mTLS (SPIFFE ID in SAN)| SvcB["Microservice B"]
    end
```

---

## 📋 Core Architectural Requirements

1. **User Identity (OIDC & OAuth 2.1):**
   - Centralized Keycloak cluster supporting multi-factor authentication (MFA).
   - Secure Authorization Code Flow with PKCE; tokens include cryptographically signed claims (JWS) with automated JWKS key rotation.
2. **Workload Identity (SPIFFE / SPIRE):**
   - SPIRE agent running as a node daemon attesting workloads using Linux kernel cgroups and container attributes.
   - Dynamic issuance and automated 1-hour rotation of X.509 SVID certificates without service restarts.
3. **Mutual TLS (mTLS) Mesh:**
   - Envoy proxy sidecars configured to mandate strict mTLS on all inter-service connections.
   - Validation of caller SPIFFE ID (`spiffe://prod.domain/ns/default/sa/service-a`) embedded in certificate Subject Alternative Names (SAN).
4. **Policy-as-Code Authorization (OPA & Rego):**
   - Externalized authorization: Microservice business code delegates permission evaluation to local OPA sidecars via gRPC/REST.
   - Rego policies evaluating caller identity, requested resource, HTTP method, user tenancy, and time-of-day attributes.
5. **Audit Logging & Tamper-Proof Tracing:**
   - Cryptographic signing of every authorization verdict into an immutable audit log.

---

## 🧪 Verification & Acceptance Criteria
- Verify that untrusted containers without a valid SPIFFE SVID are immediately rejected with TLS handshake failures at the network layer.
- Update a Rego authorization policy dynamically; verify zero-downtime policy propagation and immediate enforcement across all cluster nodes within 500ms.
