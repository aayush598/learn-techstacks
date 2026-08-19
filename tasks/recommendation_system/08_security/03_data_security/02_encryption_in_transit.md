# Encryption in Transit

## 1. Overview

Encryption in transit protects data as it moves between services, clients, and databases.
For recommendation systems handling sensitive user data, encryption in transit is a
regulatory requirement and a security best practice. This document covers TLS 1.3,
mutual TLS (mTLS), certificate management, rotation, cipher suite selection, and perfect
forward secrecy.

### 1.1 Encryption Requirements

| Data Flow | Encryption Requirement | Protocol |
|---|---|---|
| Client → API Gateway | TLS 1.3 mandatory | HTTPS |
| API Gateway → Services | mTLS recommended | gRPC/TLS |
| Service → Database | TLS mandatory | Database TLS |
| Service → Cache | TLS recommended | Redis TLS |
| Service → Feature Store | TLS mandatory | HTTPS/gRPC+TLS |
| Service → Kafka | TLS mandatory | Kafka TLS |
| Cross-region replication | TLS mandatory | mTLS |

---

## 2. TLS 1.3

### 2.1 TLS 1.3 Improvements Over TLS 1.2

| Feature | TLS 1.2 | TLS 1.3 | Benefit |
|---|---|---|---|
| Handshake rounds | 2-RTT | 1-RTT | Lower latency |
| 0-RTT resumption | Not supported | Supported | Near-instant reconnection |
| Cipher suites | 300+ | 5 | Reduced attack surface |
| Forward secrecy | Optional | Mandatory | All sessions protected |
| Key exchange | RSA, DHE, ECDHE | Only (EC)DHE | Stronger security |
| Header encryption | No | Yes (within record) | Metadata protection |

### 2.2 TLS 1.3 Configuration

```
Recommended TLS 1.3 Configuration:
├── Protocol: TLS 1.3 only (disable 1.2 and below)
├── Cipher suites (in preference order):
│   ├── TLS_AES_256_GCM_SHA384
│   ├── TLS_CHACHA20_POLY1305_SHA256
│   └── TLS_AES_128_GCM_SHA256
├── Key exchange: X25519 (preferred) or P-256
├── Certificate: ECDSA P-256 or Ed25519
└── Session tickets: Enabled with rotation
```

### 2.3 TLS 1.3 Handshake Flow

```
Client                              Server
  │                                    │
  │── ClientHello + key_share ────────>│  (1-RTT)
  │── (supported_versions: TLS 1.3)    │
  │                                    │
  │<── ServerHello + key_share ───────│
  │<── EncryptedExtensions ───────────│
  │<── Certificate ───────────────────│
  │<── CertificateVerify ─────────────│
  │<── Finished ──────────────────────│
  │                                    │
  │── Finished ──────────────────────>│
  │                                    │
  │<── Application Data ─────────────│  (0-RTT with resumption)
```

---

## 3. Mutual TLS (mTLS)

### 3.1 mTLS Architecture

```
Service A                        Service B
  │                                │
  │── ClientHello ────────────────>│
  │<── ServerHello + CertRequest ──│
  │── Client Certificate ─────────>│
  │<── Server Certificate ─────────│
  │                                │
  │   Both verify each other's    │
  │   certificates                │
  │                                │
  │<──── Encrypted Communication ──│
```

### 3.2 mTLS Implementation

| Component | Implementation |
|---|---|
| Certificate issuance | Internal CA (Vault PKI, cert-manager) |
| Certificate distribution | Kubernetes secrets, service mesh |
| Certificate validation | Service mesh sidecar (Envoy, Istio) |
| Certificate rotation | Automated via cert-manager |
| Revocation | CRL or OCSP stapling |

### 3.3 mTLS Service Mesh Integration

Using Istio/Envoy for automatic mTLS:

```
Service Pod
├── Application Container (no TLS awareness)
├── Envoy Sidecar Proxy
│   ├── Handles mTLS termination
│   ├── Validates peer certificates
│   ├── Enforces authorization policies
│   └── Logs all TLS connections
└── Certificate volume (auto-rotated)
```

### 3.4 mTLS Adoption Strategy

| Phase | Scope | Duration |
|---|---|---|
| Phase 1 | Critical services (model serving, feature store) | Month 1-2 |
| Phase 2 | All internal services | Month 3-4 |
| Phase 3 | External-facing services (with client certs) | Month 5-6 |
| Phase 4 | Full mesh with strict mTLS | Month 7+ |

---

## 4. Certificate Management

### 4.1 Certificate Types

| Type | Use Case | Lifetime | Issuer |
|---|---|---|---|
| Root CA | Trust anchor | 10 years | Internal |
| Intermediate CA | Issues leaf certs | 5 years | Root CA |
| Server cert | Service identity | 90 days | Intermediate CA |
| Client cert | Client identity | 90 days | Intermediate CA |
| Wildcard cert | *.example.com | 90 days | Public CA |
| Let's Encrypt | Public-facing domains | 90 days | Let's Encrypt |

### 4.2 Let's Encrypt Integration

```
cert-manager + Let's Encrypt:
1. Create Certificate resource in Kubernetes
2. cert-manager creates ACME challenge
3. Let's Encrypt validates domain ownership
4. Certificate issued and stored in Secret
5. cert-manager auto-renews before expiry
```

**cert-manager configuration:**

- **Issuer**: ClusterIssuer with ACME server
- **Challenge**: HTTP-01 or DNS-01
- **Renewal**: 30 days before expiry (automatic)
- **Storage**: Kubernetes TLS Secret
- **Distribution**: Mounted as volume in pods

### 4.3 Certificate Rotation

| Cert Type | Rotation Period | Method | Downtime |
|---|---|---|---|
| Server cert | 90 days | cert-manager auto | Zero |
| Client cert | 90 days | Auto-rotation | Zero |
| CA cert | 5 years | Manual with overlap | Zero (with planning) |
| Root CA | 10 years | Manual, multi-month process | Zero (with planning) |

### 4.4 Certificate Monitoring

| Metric | Alert Threshold | Action |
|---|---|---|
| Days until expiry | < 30 days | Auto-renewal triggered |
| Renewal failure | Any failure | Alert + manual intervention |
| Revoked certificate | Any revocation | Alert + investigate |
| Certificate mismatch | Any mismatch | Alert + block connections |
| Invalid certificate chain | Any invalidity | Alert + block connections |

---

## 5. Cipher Suite Selection

### 5.1 Recommended Cipher Suites

| Priority | Cipher Suite | Key Exchange | Encryption | Hash |
|---|---|---|---|---|
| 1 | TLS_AES_256_GCM_SHA384 | X25519 | AES-256-GCM | SHA-384 |
| 2 | TLS_CHACHA20_POLY1305_SHA256 | X25519 | ChaCha20-Poly1305 | SHA-256 |
| 3 | TLS_AES_128_GCM_SHA256 | P-256 | AES-128-GCM | SHA-256 |

### 5.2 Cipher Suite Configuration by Component

| Component | Protocol | Cipher Suites | Notes |
|---|---|---|---|
| Nginx/HAProxy | TLS 1.3 only | All three suites | High performance |
| Envoy proxy | TLS 1.3 only | All three suites | Service mesh |
| Java services | TLS 1.3 only | AES-GCM preferred | JVM configuration |
| Python services | TLS 1.3 only | System defaults | OpenSSL configuration |
| PostgreSQL | TLS 1.2+ | AES-GCM preferred | Database connections |
| Redis | TLS 1.2+ | AES-GCM preferred | Cache connections |

### 5.3 Deprecated Cipher Suites

Never use these cipher suites:

- **RC4** (arcfour): Broken encryption
- **DES/3DES**: Weak encryption
- **MD5-based**: Collision attacks possible
- **NULL ciphers**: No encryption
- **Export ciphers**: Intentionally weak
- **CBC mode ciphers**: Vulnerable to padding oracle attacks

---

## 6. Perfect Forward Secrecy (PFS)

### 6.1 What is PFS?

Perfect Forward Secrecy ensures that even if a private key is compromised, past sessions
cannot be decrypted. Each session uses a unique ephemeral key.

```
Without PFS:
Session key = f(static_private_key)
→ If private key compromised, all past sessions decryptable

With PFS (ECDHE):
Session key = f(ephemeral_private_key, peer_public_key)
→ Each session has unique key, past sessions remain secure
```

### 6.2 PFS Implementation

- **Key exchange**: Use ECDHE (Elliptic Curve Diffie-Hellman Ephemeral)
- **Curve preference**: X25519 (fastest, most secure) > P-256 > P-384
- **DHE fallback**: Use DHE only if ECDHE unavailable (slower but still PFS)
- **RSA key exchange**: Never use for key establishment (no PFS)

### 6.3 PFS Verification

```
Verification Steps:
1. Capture TLS handshake with Wireshark
2. Verify ServerKeyExchange message present
3. Verify ephemeral key parameters (named curve)
4. Verify signature on key exchange
5. Confirm no RSA key exchange used
```

---

## 7. TLS Configuration Management

### 7.1 Centralized TLS Configuration

```yaml
tls_configuration:
  min_version: "1.3"
  max_version: "1.3"
  cipher_suites:
    - "TLS_AES_256_GCM_SHA384"
    - "TLS_CHACHA20_POLY1305_SHA256"
    - "TLS_AES_128_GCM_SHA256"
  curves:
    - "X25519"
    - "P-256"
  client_auth: "require_and_verify"
  session_tickets: true
  session_ticket_rotation: "1h"
```

### 7.2 TLS Testing

| Test | Method | Frequency |
|---|---|---|
| Protocol version | sslyze scan | Weekly |
| Cipher suite | sslyze scan | Weekly |
| Certificate validity | Monitoring | Continuous |
| Certificate chain | openssl verify | Per deployment |
| PFS verification | Wireshark capture | Monthly |
| Vulnerability scan | testssl.sh | Monthly |

### 7.3 TLS Incident Response

If a TLS vulnerability is discovered:

1. **Assess impact**: Determine affected services and data
2. **Emergency patching**: Update TLS configuration immediately
3. **Certificate rotation**: Rotate all certificates if key compromised
4. **Revocation**: Revoke compromised certificates
5. **Audit**: Review all TLS connections during vulnerable period
6. **Communication**: Notify stakeholders of incident and remediation
