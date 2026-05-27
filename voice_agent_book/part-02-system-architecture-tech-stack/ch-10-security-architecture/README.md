# Chapter 10: Security Architecture

> **Part:** 02 - System Architecture & Technology Stack

---

## Sections

| # | Section | Description |
|---|---------|-------------|
| 01 | [Zero-Trust Security Model](sec-01-zero-trust-security-model.md) | Never trust, always verify, micro-perimeters, least privilege, continuous validation |
| 02 | [Network Security Architecture](sec-02-network-security-architecture.md) | VPC design, subnet segmentation, security groups, network policies, VPN access |
| 03 | [Secrets Management](sec-03-secrets-management.md) | HashiCorp Vault, secret rotation, DB credentials, API keys, encryption keys |
| 04 | [API Security](sec-04-api-security.md) | TLS 1.3, request signing, CSRF protection, XSS prevention, SQL injection prevention |
| 05 | [Authentication & Session Security](sec-05-authentication-session-security.md) | Secure cookies (httpOnly, sameSite), session rotation, brute force protection, account lockout |
| 06 | [Container & Orchestration Security](sec-06-container-orchestration-security.md) | Image scanning (Trivy), runtime security (Falco), pod security policies, network policies |
| 07 | [Supply Chain Security](sec-07-supply-chain-security.md) | Dependency scanning (Renovate/Dependabot), SBOM generation, signed commits, artifact verification |
| 08 | [Incident Response Security](sec-08-incident-response-security.md) | Detection, containment, eradication, recovery, postmortem, tabletop exercises |

---

## Security Controls Map

| Control | Implementation | Verification |
|---------|---------------|-------------|
| Encryption at rest | AES-256, envelope encryption | Vault audit logs |
| Encryption in transit | TLS 1.3, mTLS | Certificate transparency |
| Authentication | Auth.js, OAuth 2.0, SAML | Pen testing |
| Authorization | RBAC, Casbin | Access review |
| Audit logging | Structured, immutable | SIEM monitoring |
| Secrets management | HashiCorp Vault | Rotation compliance |
| Container security | Trivy, Falco | CI/CD gates |

---

## Key Takeaways

- Zero-trust: verify every request regardless of origin
- Network segmentation: public subnet, private subnet, data subnet
- Secrets never in code — always in Vault with auto-rotation
- Every API call requires authentication and authorization
- Supply chain security: signed commits, dependency scanning, SBOM
- Regular penetration testing and security audits
