# Phase 6 — Advanced Security Architecture
> **Domain:** Identity & Access Management (IAM), Cryptography, Zero Trust & Supply Chain  
> **Duration:** Month 8  
> **Practical Project:** [Zero Trust Identity & Access Platform](../projects/05-zero-trust-identity-platform.md)

---

## 🎯 Objective
Shift from perimeter-based security ("castle-and-moat") to modern **Zero Trust Architecture**. Master cryptographically verifiable identities, fine-grained relationship-based access control (ReBAC / Zanzibar), public-key infrastructure (PKI), and end-to-end software supply chain security.

---

## 📋 Topic Breakdown

### 6.1 Modern Identity & Access Management (IAM)
- **Protocols & Standards:**
  - OAuth 2.0 & OAuth 2.1 specifications (Deprecation of Implicit and Resource Owner Password Grant flows).
  - OpenID Connect (OIDC): ID Tokens vs Access Tokens vs Refresh Tokens.
  - SAML 2.0: Enterprise SSO integration, XML signatures, assertions.
- **Token Internals & Security:**
  - JWT (JSON Web Token), JWS (Signed), JWE (Encrypted), JWK/JWKS (Keysets).
  - Vulnerabilities: Algorithm confusion attacks (`none` algorithm), signature stripping.
  - DPoP (Demonstrating Proof-of-Possession at the Application Layer): Binding tokens to client private keys.
  - Token Exchange (RFC 8693) for downstream service impersonation.
- **Authentication Flows:**
  - Authorization Code Flow with PKCE (Proof Key for Code Exchange).
  - Client Credentials Flow for Machine-to-Machine (M2M) communication.
  - Device Authorization Flow for smart TVs and CLI tools.
- **Workload Identity & Service Authentication:**
  - The problem of static API keys and long-lived credentials.
  - SPIFFE (Secure Production Identity Framework for Everyone) and SPIRE runtime.
  - SVIDs (SPIFFE Verifiable Identity Documents) via X.509 certificates and JWTs.
  - Cloud Workload Identity Federation (GCP Workload Identity, AWS IAM Roles for Service Accounts - IRSA).

### 6.2 Modern Authorization Models
- **Authorization Paradigms:**
  - RBAC (Role-Based Access Control): Roles, role explosion problem.
  - ABAC (Attribute-Based Access Control): Dynamic attribute evaluation (user department, time, location).
  - PBAC (Policy-Based Access Control): Decoupling policy code from application business logic.
- **Relationship-Based Access Control (ReBAC) & Google Zanzibar:**
  - Tuple notation: `(object#relation@user)`.
  - Transitive closure, usersets, hierarchy traversal, and group expansion.
  - Zanzibar consistency model: Zookies (consistency tokens) preventing the "New Enemy" problem.
  - Open-source implementations: Ory Keto, Auth0 OpenFGA, SpiceDB.
- **Policy Evaluation Engines:**
  - Open Policy Agent (OPA) & Rego declarative language.
  - AWS Cedar policy language.

### 6.3 Applied Cryptography & Key Management
- **Symmetric vs Asymmetric Cryptography:**
  - AES-GCM (Authenticated encryption with associated data - AEAD), ChaCha20-Poly1305.
  - RSA vs Elliptic Curve Cryptography (ECC: ECDSA, Ed25519) - performance and key size benefits.
- **Hashing & Signatures:**
  - Cryptographic hash functions: SHA-256, SHA-3, BLAKE3.
  - Password hashing: Argon2id, bcrypt, PBKDF2 (work factors, salt, memory hardness).
  - HMAC (Hash-Based Message Authentication Code) for webhooks and request signing.
- **Public Key Infrastructure (PKI) & TLS:**
  - Certificate Authorities (CA), intermediate CAs, Certificate Revocation Lists (CRL), OCSP stapling.
  - Automated certificate issuance & rotation (ACME protocol / Let's Encrypt, cert-manager).
  - Mutual TLS (mTLS) for cryptographically verified zero trust service meshes.
- **Key & Secret Management:**
  - Envelope Encryption: Master Key (KEK) encrypting Data Encryption Keys (DEKs).
  - Key Management Services (AWS KMS, GCP Cloud KMS, HashiCorp Vault).
  - Hardware Security Modules (HSM): FIPS 140-2/3 compliance.
- **Post-Quantum Cryptography (PQC):** NIST-standardized lattice-based algorithms (ML-KEM / Kyber, ML-DSA / Dilithium) to mitigate "harvest now, decrypt later" threats.

### 6.4 Advanced Security Engineering & Supply Chain Security
- **Zero Trust Principles:** "Never trust, always verify" - context-aware identity verification, micro-segmentation.
- **Threat Modeling:**
  - STRIDE methodology (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).
  - Attack Trees and LINDDUN privacy threat modeling.
- **Software Supply Chain Security:**
  - Software Bill of Materials (SBOM): SPDX and CycloneDX specifications.
  - SLSA (Supply-chain Levels for Software Artifacts) framework (Levels 1–4).
  - Cryptographic artifact signing with Sigstore / Cosign.
- **Runtime & Container Security:**
  - Linux capability dropping, non-root containers, read-only root filesystems.
  - Seccomp profiles, AppArmor, eBPF runtime auditing (Tetragon, Falco).
- **Data Protection & Compliance:**
  - Data Classification (Restricted, Confidential, Internal, Public).
  - Tokenization, Data Masking, Pseudonymization.
  - Data Sovereignty and localization laws (GDPR, HIPAA, PCI-DSS Level 1).

---

## 💻 Practical Hands-On Project
Build an **End-to-End Zero Trust Microservices Platform**:
1. Deploy **Keycloak** as the central Identity Provider with OIDC and PKCE authentication.
2. Integrate **SPIFFE/SPIRE** to dynamically issue short-lived X.509 SVID certificates to backend services.
3. Configure an **Envoy** sidecar mesh enforcing strict **Mutual TLS (mTLS)** and extracting caller SPIFFE IDs.
4. Integrate **Open Policy Agent (OPA)** as an external authorization sidecar evaluating Rego policies on every RPC call.
5. Sign all application container images using **Cosign** and enforce admission control in Kubernetes using Kyverno/Gatekeeper.

---

## 🛡️ Architecture Decision Record (ADR) Exercise
- **Context:** A multi-tenant B2B healthcare SaaS system requires granular document sharing across teams, departments, and external auditors with strict HIPAA compliance.
- **Decision:** Should the engineering team adopt a traditional **PostgreSQL RBAC table design** or implement a **Zanzibar-style ReBAC architecture (e.g., SpiceDB)**?
- **Deliverable:** Write an ADR analyzing query complexity, recursive permission graph resolution latency, caching consistency, and auditability.

---

## ✅ Completion Criteria
- [ ] Construct a complete Threat Model for a public-facing payment checkout system using STRIDE.
- [ ] Diagram a Zanzibar relationship graph showing transitive inheritance (e.g., `member of team -> editor of folder -> viewer of file`).
- [ ] Successfully sign a container image with Cosign and verify its signature via automated policy.
- [ ] Demonstrate an operational SPIRE agent issuing rotated certificates to microservices with zero downtime.
