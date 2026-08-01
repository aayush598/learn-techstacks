# PKI, Certificates, and TLS in Depth

> **TL;DR**: TLS 1.3 secures every HTTPS connection by using a certificate (PKI) to bind a server's public key to its identity, an ephemeral ECDHE key exchange for forward secrecy, and AEAD encryption (AES-GCM/ChaCha20) for confidentiality + integrity — with the full handshake completing in one round trip.

## 1. Why Does This Exist?
Encryption alone can't secure the web — an attacker can impersonate a server and negotiate a key with you (the MITM problem). TLS exists to give *authenticated* encryption: prove you're talking to the real server, then protect the channel. The hard part is *identity*: how does a browser know that the key it's negotiating with belongs to `example.com`? That's what **PKI (Public Key Infrastructure)** solves: a hierarchy of **Certificate Authorities (CAs)** issue **X.509 certificates** that bind public keys to domain names; browsers trust the CAs (the root store) and verify the chain of signatures. TLS then *uses* that PKI in the handshake to authenticate the server, agree a session key with forward secrecy, and protect records with AEAD. Without PKI there'd be no "secure website" signal; without TLS there'd be no use for PKI in the browser. They're two halves of one system.

## 2. How Does It Work?
**PKI**: a CA signs a certificate (public key + identity + validity + extensions) with its private key; verifiers trust the CA and check the signature chain root→intermediate→leaf. **Validation** (RFC 5280): signature valid, not expired, not revoked (CRL/OCSP), name matches (SAN), chain to a trusted root. **TLS 1.3 handshake** (RFC 8446, 1-RTT):
1. Client → `ClientHello` (key_share: ephemeral ECDHE public key, supported ciphers, random).
2. Server → `ServerHello` (its ECDHE key, cipher choice) + `EncryptedExtensions` + `Certificate` (chain) + `CertificateVerify` (signature over the handshake) + `Finished`.
3. Client verifies cert chain + signature, computes the shared secret, sends `Finished`; both sides derive session keys via HKDF; handshake complete in **1 RTT**.
4. Application data flows in AEAD-protected records (AES-128/256-GCM or ChaCha20-Poly1305).

## 3. When Is It Used?
- **HTTPS**: every browser connection — the dominant use; HTTP/2 and HTTP/3 (QUIC uses TLS 1.3 directly).
- **mTLS**: both sides present certs — service-to-service, API mTLS, smart cards.
- **Email/TLS**: SMTPS, IMAPS (STARTTLS) — opportunistic or required.
- **VPN/SSH**: TLS-based VPNs (OpenVPN, Cloudflare Access), and SSH's host keys are a PKI-like trust model.
- **Code/artifact signing**: signed packages, firmware, container images (cosign/Sigstore), software updates.
- **Machine identity**: SPIFFE/SPIRE service certs in zero-trust meshes; EAP-TLS for 802.1X.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: pin a single key (TOFU) instead of CAs.* SSH uses TOFU (first-use trust) — simple, but key changes break silently and there's no revocation; the web needs *revocable, transferable* identity across billions of sites, which is what CA-issued certificates provide (a browser can't pre-store every site's key).
- *Alternative: trust the first connection (opportunistic TLS).* No authentication at all — a MITM on the first connection owns you. TLS authenticates every time via the certificate.
- *Alternative: RSA static key exchange (TLS 1.2).* Forward secrecy requires ephemeral keys; if a server's long-term key is stolen later, static RSA lets an attacker decrypt *recorded past* traffic. TLS 1.3 mandates ephemeral ECDHE so sessions are never decryptable after the fact.
- *Alternative: skip the CA hierarchy, self-sign everything.* Self-signed certs can't be verified by browsers without manual trust — impractical at web scale; the CA hierarchy centralizes issuance and revocation. (The trade: CA compromise = huge blast radius, hence certificate transparency + pinning.)
- *Alternative: encrypt-then-MAC vs AEAD debates.* TLS 1.3 settled it — only AEAD ciphers, eliminating the padding-oracle/ordering bugs of CBC+HMAC designs.

## 5. Intuition
TLS is a **bank vault with a notarized key**. PKI is the notary system: a trusted notary (root CA) signs a document (certificate) saying "this public key belongs to example.com." Your browser trusts the notary's stamp (root store), so when the server shows you a signed certificate, you can verify the whole chain of stamps to a root you trust — and *only then* trust the key. The handshake is then: "here's my key (certificate), here's my signature proving I own it (CertificateVerify), let's both derive a shared secret from our ephemeral keys (ECDHE), and from now on everything is in a tamper-evident locked box (AEAD records)." The ephemeral keys mean even the bank itself can't decrypt old recordings later (forward secrecy).

## 6. Real-World Analogy
A **passport system**. The passport authority (root CA) issues passports (certificates) binding your photo (public key) to your name (domain) and validity dates; airport staff (browsers) trust the authority and check the passport's security features (signature chain), expiry, and wanted-list (revocation). A traveler (client) checking into a hotel: the hotel shows its business license (server cert), the traveler verifies it's issued by the licensing board (CA) and covers this hotel's name (SAN), then signs the guestbook (CertificateVerify), and they set a unique room-safe combination only they both know (ECDHE shared secret) — the room key changes each stay (forward secrecy). If the hotel's license is revoked (compromise), the traveler refuses (revocation).

## 7. Formal Definition
- **X.509 certificate** (RFC 5280): version, serial number, signature algorithm, issuer, validity (notBefore/notAfter), subject, subject public key info, extensions (SAN, KeyUsage, EKU, CRL/OCSP endpoints), signature.
- **Certificate chain**: leaf → intermediate(s) → root; validation walks to a *trusted root* in the store, verifying each signature, validity period, revocation status, and that the leaf covers the expected name (SAN) and purpose (EKU).
- **Revocation**: **CRL** (certificate revocation list, periodically fetched) and **OCSP** (online, real-time check) — both have adoption/availability gaps; OCSP stapling fixes the fetch cost.
- **TLS 1.3** (RFC 8446): (EC)DHE key exchange (mandatory, ephemeral), AEAD (AES-GCM, ChaCha20-Poly1305), HKDF key derivation, 1-RTT handshake + 0-RTT resumption (PSK), signature algorithms (RSA-PSS, ECDSA, Ed25519), TLS 1.2 downgrade protection, optional **Certificate Transparency** (public log of issued certs).
- **Cipher suite naming** (1.3): `TLS_AES_128_GCM_SHA256` = key exchange implied (DHE), AEAD + HKDF hash — far simpler than 1.2's 4-part suites.

## 8. Example
**Verify a chain by hand (conceptually).** Browser trusts root `R`. Server presents leaf `L` signed by intermediate `I`, `I` signed by `R`.
1. Check `L.notBefore ≤ now ≤ L.notAfter` and SAN contains `example.com`.
2. Verify `L`'s signature with `I`'s public key ✓.
3. Verify `I`'s signature with `R`'s public key ✓ (R is in the trust store).
4. Check revocation (OCSP/CRL) — still valid.
5. Trust `L`'s public key for ECDHE; the handshake proceeds.

**TLS 1.3 handshake bytes (what a capture shows):**
```
C->S: ClientHello  (random, TLS_AES_128_GCM_SHA256..., key_share: X25519 pubkey)
S->C: ServerHello  (cipher choice, key_share: X25519 pubkey)   <- first flight over in 1 RTT
S->C: EncryptedExtensions, Certificate (chain), CertificateVerify (signature), Finished
C->S: Finished
C->S: application_data (HTTP request, AEAD-encrypted)
```
One round trip to first byte; resumption (PSK) → 0-RTT.

## 9. Internal Working
1. **Key exchange**: both sides generate ephemeral X25519/P-256 keys; the shared secret = ECDHE result. Because keys are ephemeral, even long-term-key compromise can't decrypt past traffic.
2. **Authentication**: `CertificateVerify` signs a transcript hash with the server's private key — proves *possession* of the key bound in the certificate; the client verifies it after checking the chain.
3. **Key derivation (HKDF)**: shared secret → `HKDF-Extract` → handshake traffic keys → `Derive-Secret` for application keys, using the transcript hashes so keys are bound to the exact handshake.
4. **Record protection**: each record encrypted with AES-GCM (nonce from a sequence number) — confidentiality + integrity + anti-replay in one primitive.
5. **Resumption**: session tickets (PSK) allow 0-RTT for repeat visits — first request encrypted immediately, at the cost of a replay window (mitigated by anti-replay for idempotent GETs).
6. **Downgrade protection**: the server inserts a special value if it detects a version-downgrade attempt; 1.3 also mandates `signature_algorithms` to prevent cipher/version rollback.
7. **Certificate Transparency**: CAs must log issued certs to public logs; monitors detect misissuance (e.g., an attacker's fake CA) — browsers can require SCTs.

## 10. Time Complexity / Performance
- **Handshake cost**: 1 RTT (1.3) vs 2 RTT (1.2 RSA); 0-RTT for resumption. At 30 ms RTT: ~30 ms added to first request.
- **Crypto cost**: ECDHE ≈ sub-ms; cert signature verify (RSA-2048/ECDSA) ≈ 0.1-1 ms; AEAD records ≈ GB/s with AES-NI. TLS overhead is ~1-3% of total load on modern servers with session resumption and hardware.
- **Session resumption**: TLS tickets (PSK) avoid a full handshake per connection — critical for high connection rates (HTTP/2 reuses connections anyway).
- **OCSP/CRL checks**: latency/availability costs — mitigated by OCSP stapling (server includes a signed, fresh OCSP response in the handshake).

## 11. Advantages
- **Authenticated encryption**: confidentiality + integrity + *server identity* — the MITM fix.
- **Forward secrecy** (1.3): ephemeral ECDHE — past sessions survive key compromise.
- **Speed**: 1-RTT handshake, 0-RTT resumption, hardware-accelerated AEAD; HTTP/2/3 multiplexing minimizes connection churn.
- **Standard, interoperable**: one protocol for the whole web; browser root stores are universal trust.
- **PKI scalability**: CAs issue/revoke/rotate; Certificate Transparency provides accountability; pinning optional hardening.

## 12. Disadvantages
- **PKI trust is fragile**: CA compromise = forged certs for any domain (mitigated by CT, pinning); a malicious CA in a root store is a systemic risk.
- **Revocation is weak**: CRL/OCSP adoption gaps mean revoked certs are sometimes still trusted.
- **Handshake latency** (still): 1 RTT minimum; 0-RTT has replay risk; client network effects (censorship of unknown ciphers, middleboxes) cause fallback issues.
- **TLS inspection trade-off**: interception breaks end-to-end (the privacy vs detection debate).
- **Complexity**: cipher/cert confusion attacks (a historic TLS 1.2 pain), key-management burden (rotation, HSMs).
- **Not app security**: TLS doesn't protect the app from XSS/SQLi (Section 01) — it's channel security.

## 13. Interview Questions
1. **Q: What problem does TLS solve that encryption alone can't?** A: Encryption gives confidentiality but not *authentication* — an attacker can MITM and negotiate a key with you. TLS authenticates the server (certificate chain) and binds the key exchange to that identity, closing the MITM hole.

2. **Q: Walk through the TLS 1.3 handshake.** A: Client sends ClientHello with an ephemeral ECDHE key share; server replies with ServerHello (its ECDHE key + cipher), then EncryptedExtensions + Certificate + CertificateVerify + Finished; client verifies the chain and signature, computes the shared secret, sends Finished. Done in 1 RTT. Application data then flows AEAD-encrypted.

3. **Q: How is the TLS 1.3 handshake different from TLS 1.2?** A: 1.3 is 1-RTT (vs 2-RTT RSA exchange), mandates ephemeral (EC)DHE for forward secrecy, uses only AEAD ciphers (no CBC/HMAC combos), simplifies cipher suites, adds 0-RTT resumption, and includes downgrade protection. RSA key exchange and most legacy ciphers are gone.

4. **Q: What is a certificate chain and how is it validated?** A: Leaf → intermediates → root. The verifier walks: check validity dates and SAN name, verify each signature up to a *trusted root in the store*, and check revocation. Only then is the leaf's public key trusted for the handshake.

5. **Q: What is the difference between a root CA and an intermediate CA?** A: Roots are pre-installed in trust stores and rarely issue leaf certs directly (offline, high-security). Intermediates are cross-signed by roots and issue leaf certs — they can be revoked/rotated independently without touching the root, containing CA-compromise blast radius.

6. **Q: What are CRL and OCSP and what's the difference?** A: CRL: a periodically-fetched list of revoked serials (stale, bulk). OCSP: a real-time query ("is this cert revoked?") — fresher but adds a network dependency; OCSP stapling lets the server attach a fresh signed OCSP response to the handshake, removing the client's extra fetch.

7. **Q: TRICKY — Why is forward secrecy important and how does TLS 1.3 guarantee it?** A: If a server's long-term private key is stolen, an attacker with *recorded* traffic could decrypt everything exchanged with a static key exchange. 1.3 uses ephemeral ECDHE keys that are discarded after the session — even with the long-term key, past sessions can't be decrypted. It's a *guarantee* because no key-exchange mode other than ephemeral DH remains.

8. **Q: What is the CertificateVerify message for?** A: It's a signature over the transcript hash using the server's private key — proving the server actually *possesses* the private key matching the certificate's public key (not just that it can replay a cert). Without it, a MITM could forward a legit certificate and still be an impostor.

9. **Q: What is certificate pinning and when is it used?** A: Pinning hard-codes a trusted certificate/public key (or a hash) in the client, so only that cert is accepted — bypassing the CA system's risks. Used in high-value apps (mobile banking, API clients) to stop CA-compromise and interception. Costs: certificate rotation requires client updates (a classic operational trap).

10. **Q: PRODUCTION — A service's TLS cert expired. What are the failure modes?** A: Clients fail validation (handshake error) — for browsers, a full-page warning; for APIs, connection failures and downtime; automated clients may retry and pile on. The fix: automate renewal (ACME/certbot, k8s cert-manager), monitor expiry (alert at T-30/14/7 days), and test rotation with staged environments. Real-world outages from cert expiry are extremely common.

11. **Q: What is mTLS and how is it different from server-only TLS?** A: mTLS (mutual TLS): both client and server present certificates and verify each other — the client proves its identity too. Used for service-to-service auth (kubernetes, API gateways, zero-trust meshes). Cost: client-cert management.

12. **Q: What is Certificate Transparency and why does it matter?** A: CAs must append every issued cert to public, append-only logs; browsers can require inclusion proofs (SCTs). This makes misissuance (a rogue/fake CA issuing a cert for a domain it doesn't own) detectable by monitors — accountability against the CA-trust risk.

13. **Q: TRICKY — Why can't a browser just trust self-signed certificates?** A: Because there's no chain to a trusted root — the signature verifies only that *you* made it, not that a trusted authority vouches for the identity. Self-signed = "I say I'm example.com," which is exactly what a MITM would also say. They're fine only where trust is out-of-band (internal services, TOFU like SSH).

14. **Q: What is 0-RTT and what's its security trade-off?** A: With a previously-established PSK, a client can send its first application request *with* the ClientHello (0 RTT). Benefit: instant resumption. Risk: replay (an attacker can replay the early data) and no forward secrecy on that first message — mitigations: anti-replay windows, restrict 0-RTT to idempotent requests.

15. **Q: SCENARIO — An app shows "certificate not trusted" on an internal network but works from home. Why?** A: The internal network uses TLS interception (a proxy/corp CA) — the corp root isn't in the client's trust store, or the client doesn't support the interception. Also possible: internal-only CA with a chain not installed on that device. Fix: install the corporate root CA on managed devices, or stop intercepting.

16. **Q: What is the difference between TLS and SSL?** A: SSL (2/3) are the deprecated predecessors; TLS 1.0-1.3 are the modern protocol. SSLv3 is broken (POODLE); TLS 1.0/1.1 are deprecated; TLS 1.2 and 1.3 are current. People say "SSL" colloquially but the protocol is TLS — browsers now *refuse* SSL/TLS 1.0-1.1.

17. **Q: What is the "downgrade attack" and how does TLS 1.3 prevent it?** A: An attacker tries to force client and server to negotiate an old, weak protocol/cipher. TLS 1.3 servers insert a random-looking marker (the "downgrade sentinel") in the ServerHello that clients detect and abort on; the version/cipher negotiation is also covered by the transcript signature — any tampering breaks the handshake.

18. **Q: PRODUCTION — Design a certificate lifecycle for a fleet of 10,000 services.** A: (1) A managed internal CA (or ACME) issuing short-lived certs (e.g., 24h-90d) with automation (cert-manager/ACME DNS-01); (2) SPIFFE/SPIRE or similar for identity-based issuance; (3) automatic renewal + rotation monitoring; (4) mTLS between services; (5) CT logging and revocation tooling; (6) expiry alerts and a runbook. Short TTL + automation beats long TTL + manual rotation.

## 14. Follow-Up Questions
1. **Q: What is the difference between the SAN and CN fields in a certificate?** A: CN (common name) is legacy/ignored by modern browsers; the Subject Alternative Name (SAN) lists the valid hostnames and is what RFC 5280 says must be checked. A cert without the right SAN fails name validation even if CN matches.

2. **Q: What is a "certificate authority confusion" / algorithm confusion attack?** A: An attacker tricks a verifier into using the wrong public-key algorithm for the chain (e.g., an RSA key verifying an ECDSA signature) — historical TLS 1.2 attacks. TLS 1.3 removes ambiguity by carrying explicit signature algorithm identifiers in the handshake.

3. **Q: Why are OCSP and CRL considered "best-effort" revocation?** A: A client that can't reach the OCSP responder may "fail-open" (allow), and CRLs are only as fresh as their fetch interval; plus some CAs never issue CRLs for short-lived certs. Short-lived certs (hours-days) are now the strongest practical revocation: the cert is gone before it matters.

4. **Q: What is the difference between key exchange and authentication in TLS?** A: Key exchange (ECDHE) establishes the shared secret — secrecy + forward secrecy. Authentication (certificate + CertificateVerify) establishes *who* — binds the key to an identity. Both are required; one without the other is insecure (secret with anyone vs identity without secrecy).

## 15. Coding Example
```python
# Inspect certificates and TLS in Python (real crypto, no library needed for parsing)
import ssl, socket, hashlib

def inspect_tls(host="example.com", port=443):
    ctx = ssl.create_default_context()          # uses the OS trust store (PKI roots)
    with ctx.wrap_socket(socket.socket(), server_hostname=host) as s:
        s.connect((host, port))
        print(f"negotiated: {s.version()} {s.cipher()}")
        cert = s.getpeercert()                   # parsed X.509 (chain-verified by Python)
        print("subject:", cert.get("subject"))
        print("SAN:", [v for k, v in cert.get("subjectAltName", [])])
        print("issuer:", dict(cert.get("issuer", [])))
        print("notAfter:", cert.get("notAfter"))
        print("signature_algo:", cert.get("signatureAlgorithm"))

def parse_x509_der(pem_path):                    # minimal field walk
    from cryptography import x509
    cert = x509.load_pem_x509_certificate(open(pem_path, "rb").read())
    print(f"{cert.subject} | {cert.not_valid_after_utc} | {cert.public_key().key_size} bits")

inspect_tls()
```
```bash
# The production toolset for TLS/PKI
openssl s_client -connect example.com:443 -tls1_3 -showcerts 2>/dev/null \
    | grep -E "New, TLSv1.3|Cipher is|Verify return code"          # negotiated + chain verify
openssl s_client -connect example.com:443 -servername example.com 2>/dev/null \
    | openssl x509 -noout -text | grep -E "Issuer|Subject|Not After|Subject Alternative Name"
openssl x509 -in <cert.pem> -noout -text | grep -A1 "Authority Information Access"  # OCSP endpoint
# Generate a self-signed cert (for lab/dev) + view a CSR/chain:
openssl req -x509 -newkey rsa:2048 -nodes -keyout k.pem -out c.pem -days 365 -subj "/CN=lab.local"
openssl verify -CAfile root.pem intermediate.pem leaf.pem          # chain validation
# Test expiry/revocation across a fleet:
ssldump -i any port 443 | head -20 || echo "install ssldump for capture-level TLS"
```

## 16. Industry Usage
- **Browsers**: Chrome/Firefox/Safari/Edge — the root stores (Mozilla CA Program, Apple, Microsoft) and Certificate Transparency are the PKI's day-to-day governance.
- **CDNs/edge**: Cloudflare, AWS CloudFront, Fastly — free ACME certs, automated issuance at massive scale, 0-RTT/HTTP-3, TLS 1.3 everywhere.
- **Cloud**: ACM (AWS Certificate Manager), GCP/Let's Encrypt — automated cert lifecycle.
- **Zero trust/mTLS**: Istio/Linkerd service mesh certs (SPIFFE/SPIRE), Google BeyondCorp — machine identity via certs.
- **Compliance**: PCI-DSS requires strong crypto/TLS; auditors check TLS versions and key strength.
- **Incident landscape**: cert-expiry outages and CA-incident responses (DigiNotar 2011, Let's Encrypt 2020 bug) are classic postmortems.

## 17. References
- RFC 8446 (TLS 1.3) — https://datatracker.ietf.org/doc/html/rfc8446
- RFC 5280 (X.509 PKI) — https://datatracker.ietf.org/doc/html/rfc5280
- RFC 6960 (OCSP) — https://datatracker.ietf.org/doc/html/rfc6960 ; RFC 6962 (Certificate Transparency)
- Let's Encrypt / ACME (RFC 8555) — https://letsencrypt.org/ ; https://datatracker.ietf.org/doc/html/rfc8555
- Mozilla CA Certificate Program — https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/
- Kurose & Ross, *Computer Networking*, 8th ed., §8.3 (SSL/TLS).
- cloudflare TLS/SSL docs — https://developers.cloudflare.com/ssl/

## 18. Cheat Sheet
- TLS = authenticated encryption: confidentiality + integrity + server identity (MITM fix).
- PKI: root CA → intermediates → leaf; trust store; validate chain, dates, SAN, revocation.
- TLS 1.3: 1-RTT handshake, mandatory ephemeral ECDHE (forward secrecy), AEAD only, 0-RTT resumption.
- Cipher suites (1.3): `TLS_AES_128_GCM_SHA256` — key exchange implied, AEAD + HKDF hash.
- CertificateVerify proves private-key possession; without it a MITM can relay the cert.
- Revocation: CRL (list) vs OCSP (query); OCSP stapling; short-lived certs = best revocation.
- Forward secrecy: ephemeral keys — stolen long-term keys can't decrypt past sessions.
- mTLS = both sides verified; used for service-to-service.
- CT (Certificate Transparency) makes misissuance detectable.
- Downgrade sentinel + transcript signature kill version/cipher rollback.

## 19. Quiz
1. TLS 1.3 handshake round trips: a) 2 b) 1 c) 0 d) 3 → **b**
2. TLS 1.3 mandates: a) RSA key exchange b) ephemeral ECDHE c) CBC ciphers d) SSLv3 → **b**
3. Forward secrecy means: a) longer keys b) past sessions survive key compromise c) faster handshake d) no MITM → **b**
4. The certificate's valid hostnames live in: a) CN b) SAN c) issuer d) serial → **b**
5. Which proves the server owns its key? a) Certificate b) CertificateVerify c) ServerHello d) Finished → **b**
6. OCSP checks: a) key size b) revocation in real time c) chain depth d) cipher → **b**
7. Self-signed certs are untrusted because: a) too short b) no chain to a trusted root c) weak crypto d) no SAN → **b**
8. CertificateVerify signs: a) the record b) the transcript hash c) the cert d) the key → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: What does TLS add over plain encryption?** → **A:** Server authentication via certificates + integrity via AEAD — the MITM fix.
- **Q: Walk TLS 1.3 handshake** → **A:** ClientHello (ECDHE) → ServerHello (ECDHE) + cert + CertificateVerify + Finished → Finished; 1 RTT.
- **Q: How is a chain validated?** → **A:** Dates + SAN + signatures up to a trusted root + revocation check.
- **Q: Why is 1.3 forward-secret?** → **A:** Only ephemeral ECDHE exists; stolen long-term key can't decrypt recorded sessions.
- **Q: CRL vs OCSP?** → **A:** Periodic list vs real-time query; OCSP stapling cuts the client's fetch.
- **Q: What is mTLS?** → **A:** Both sides present certs — service-to-service identity.
- **Q: What is 0-RTT and its risk?** → **A:** Send data with ClientHello via PSK; replay risk + no forward secrecy on early data.

## 21. Revision
TLS 1.3 = authenticated, forward-secret encryption: 1-RTT handshake where ClientHello/ServerHello exchange ephemeral ECDHE keys, the server presents its certificate chain and signs the transcript (CertificateVerify), both derive keys via HKDF, and records flow AEAD-protected. PKI (X.509, RFC 5280) binds public keys to identities: root→intermediate→leaf chains validated against a trust store (dates, SAN, signatures, revocation via CRL/OCSP-stapling). The killer features: forward secrecy (ephemeral keys), AEAD-only (no CBC bugs), 0-RTT resumption (replay risk), downgrade protection, and Certificate Transparency for CA accountability. Anchors: *1.3 is 1 RTT, ephemeral, AEAD-only; certificates solve identity, ECDHE solves secrecy, CertificateVerify proves possession; mTLS both ways for services.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What does TLS add over encryption?" | 13-Q1 |
| "Walk the TLS 1.3 handshake" | 8 / 13-Q2 |
| "TLS 1.3 vs 1.2" | 13-Q3 |
| "Certificate chain validation" | 13-Q4 / 8 |
| "Root vs intermediate CA" | 13-Q5 |
| "CRL vs OCSP / stapling" | 13-Q6 |
| "Forward secrecy and why it matters" | 13-Q7 |
| "What is CertificateVerify?" | 13-Q8 |
| "Certificate pinning" | 13-Q9 |
| "Cert expired — outage + fix" | 13-Q10 |
| "What is mTLS?" | 13-Q11 |
| "What is 0-RTT and its risk?" | 13-Q14 |
| "Downgrade attacks" | 13-Q17 |
