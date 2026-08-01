# HTTPS and the TLS Handshake

> **TL;DR**: HTTPS is HTTP inside TLS (RFC 8446), and the TLS handshake is the cryptographic ritual — certificate exchange + (EC)DH key agreement + cipher-suite negotiation — that establishes a confidential, authenticated, tamper-evident channel in 1-RTT (TLS 1.3), because the web is public and attackers sit in the middle.

## 1. Why Does This Exist?
HTTP is plaintext — anyone on the path (Wi-Fi eavesdropper, ISP, router, malicious proxy) can read passwords, tokens, and content, and can *modify* responses (inject ads, malware). HTTPS exists to give HTTP three guarantees:
1. **Confidentiality** — payload encrypted (nobody can read it).
2. **Authentication** — the server (and optionally client) is genuinely who it claims (nobody can impersonate).
3. **Integrity** — data cannot be modified in transit undetected.
The *handshake* exists to set these up safely before any application data flows, using certificates (public-key identity), key exchange (shared secrets without ever transmitting the secret), and cipher negotiation (agreed algorithms). Without HTTPS, the entire commercial web (payments, logins, APIs) would be insecure; modern browsers mark plain HTTP as "Not Secure" and increasingly refuse it (HSTS, HTTPS-only mode).

## 2. How Does It Work?
High-level flow (TLS 1.3, RFC 8446):
1. **ClientHello** (1st message, client→server): TLS version, random nonce, supported cipher suites (e.g., TLS_AES_128_GCM_SHA256), supported groups (e.g., X25519), optional SNI (which site), session/resumption ticket.
2. **ServerHello** (server→client): chosen cipher suite, random nonce, server's **key share** for (EC)DH. Encrypted Extensions (ALPN, etc.).
3. **Certificate + CertificateVerify** (server→client): the server's **X.509 certificate** (public key + identity, signed by a CA chain), plus a signature proving possession of the private key.
4. **Finished** (both directions): the derived session keys are confirmed (all messages so far are keyed).
After the 1-RTT handshake, **application data flows encrypted** (HTTP). On resumption, a client with a cached ticket can send the first application data immediately: **0-RTT** (with replay caveats).

Key mechanics:
- **Asymmetric crypto** (certificate public/private keys) is used *only* for identity + the (EC)DH handshake; bulk data uses **symmetric** (AES-GCM/ChaCha20-Poly1305) via keys derived with HKDF from the DH shared secret.
- **Certificate validation**: client verifies signature chain → root CA (trust store), checks hostname (CN/SAN), validity dates, revocation (CRL/OCSP).
- **Forward secrecy**: ephemeral (EC)DH keys are destroyed after the session → past traffic can't be decrypted later even if the server's long-term key leaks (PFS).

## 3. When Is It Used?
- **Every website that takes credentials or payments** — HTTPS is effectively *mandatory* (Google ranks HTTPS higher; Chrome labels HTTP "Not secure").
- **APIs**: all REST/gRPC APIs run over TLS (443). Cloud LBs terminate TLS.
- **mTLS** (mutual TLS): *both* sides present certs — used in service-to-service auth (Kubernetes, zero-trust), B2B APIs, IoT device auth.
- **Tunnels**: HTTPS to a CONNECT proxy tunnels arbitrary traffic (VPN-over-TLS, corporate egress).
- **Everywhere**: DNS-over-HTTPS (DoH), secure email (SMTPS/IMAPS), WebSockets over TLS (wss).

## 4. Why Wasn't Another Approach Chosen?
- **Why not just encrypt at the transport layer (IPsec) instead?** IPsec encrypts *all* IP traffic — hard to deploy per-application, per-host (kernels, NAT), and coarse-grained. TLS sits in the application (any port), works with existing TCP/UDP/QUIC, and is per-connection, per-app, certificate-based identity — it matched the web's model.
- **Why not use pre-shared keys / Kerberos?** No public-key identity, no scale, no "just works on the public Internet." Certificates + CA trust model scale to billions of endpoints.
- **Why (EC)DH instead of RSA-only key exchange?** RSA key transport (TLS ≤1.2's RSA_KX) lets the server decrypt everything later if its private key leaks → **no forward secrecy**. Ephemeral DH/ECDH generates fresh per-session keys so compromise of the long-term key can't decrypt past traffic. TLS 1.3 *mandates* PFS (only (EC)DHE suites).
- **Why TLS 1.3's streamlined handshake instead of 1.2?** 1.2's handshake was 2-RTT and bloated with legacy algorithms (RSA, CBC, weak ciphers, renegotiation). 1.3: 1-RTT (0-RTT resumption), removed RSA_KX + CBC, integrated HKDF, encrypted handshake extensions — faster and safer. "Why not another approach" = remove everything that proved dangerous; standardize what worked.

## 5. Intuition
Think of the handshake as **meeting a notary in a café with a magic lockbox**:
1. Server shows you a **notarized ID** (certificate signed by a trusted authority).
2. You both use the **Diffie-Hellman handshake** — you each pick a private ingredient, combine public mixtures, and both compute the same secret *without ever sending it*. Eavesdroppers can't reconstruct it.
3. You agree on a **cipher suite** — "we'll use this strong lock (AES) with this key-derivation recipe."
4. Now you can pass messages in the lockbox (encrypted with the shared secret) — anyone watching only sees boxes, not contents.
5. Next time, you recognize the server's **stamp** (session ticket) and can start talking immediately (0-RTT) — but only after you've done the ritual once.

## 6. Real-World Analogy
**Passport + tamper-evident sealed envelope**: The certificate = a passport issued by a trusted passport office (CA), containing the server's public identity and photo (public key). You (client) check the passport against your known-good list (trust store). The (EC)DH step = agreeing on a secret by exchanging *padlocks that combine*: each side sends a padlock, both combine them into a shared key that neither party transmitted. Then every letter goes in a **tamper-evident sealed envelope** (AEAD encryption + authentication): if anyone opens or alters it, the seal breaks and the recipient detects it. The CA is the *third party everyone trusts to vouch for identities* — this is why "certificate not trusted" warnings exist.

## 7. Formal Definition
**HTTPS** = HTTP over a TLS (or QUIC) secure connection, conventionally on TCP port 443. **TLS 1.3** (RFC 8446) is a cryptographic protocol providing confidentiality, integrity, and authentication between two communicating peers. It consists of: a **handshake protocol** (client/server hello, certificate, key exchange via ephemeral Diffie-Hellman or ECDHE, Finished) that establishes session keys; a **record protocol** that encrypts application data using AEAD (AES-GCM, ChaCha20-Poly1305) with HKDF-derived keys; and **alert/callback mechanisms**. Certificates are X.509 (RFC 5280) bound to a domain via SAN/CN and signed by a certificate authority (CA) hierarchy that clients validate against a trust store.

## 8. Example
A TLS 1.3 handshake walk, cipher `TLS_AES_128_GCM_SHA256`, group X25519:
```
Client                                            Server
  |  ClientHello
  |  random_c, key_share: X25519(c), ciphers, ALPN:h2
  |---------------------------------------------------->|
  |                                                     |  ServerHello
  |                                                     |  random_s, key_share: X25519(s), cipher=TLS_AES_128_GCM_SHA256
  |                                                     |  EncryptedExtensions (ALPN: h2)
  |                                                     |  Certificate (leaf + chain)
  |                                                     |  CertificateVerify (sig over transcript)
  |                                                     |  Finished
  |<----------------------------------------------------|
  |  Finished
  |  [ 1 RTT total — application data can now flow encrypted ]
```
- Both compute `shared_secret = X25519(s, c_private) = X25519(c, s_private)` — same value, never transmitted.
- Keys derived via HKDF(handshake traffic): `client_handshake_key`, `server_handshake_key`, then `client_app_key`, `server_app_key` after Finished.
- Client verifies: (1) cert chain → trusted root; (2) hostname `example.com` ∈ SAN; (3) CertificateVerify signature over the full transcript using the cert's public key (proves the holder owns it); (4) Finished MAC.
- Result: 1-RTT handshake, then `HTTP/2 GET /` flows as encrypted TLS records.

0-RTT on revisit: client cached the ticket + PSK → sends `ClientHello (psk) + Finished + GET /` together → first application data arrives in the same round trip as the handshake (replay risk noted).

## 9. Internal Working
1. **ClientHello** — nonce, version, cipher suites (ordered), key share, SNI. (TLS 1.3: the client sends its DH share *up front* — this is why 1-RTT.)
2. **ServerHello** — picks the suite + group; includes server key share. Server then derives handshake keys → **EncryptedExtensions** (ALPN, server params) are the first encrypted message.
3. **Certificate message** — the leaf certificate + intermediates (NOT the root; clients already trust it). Optionally OCSP stapling (fresh revocation status).
4. **CertificateVerify** — ECDSA/RSA signature over `transcript hash (all prior messages)` — proves possession of the private key *and* binds the handshake to this transcript (prevents MITM swaps).
5. **Finished** — MAC over the transcript with handshake keys; both sides confirm integrity of the whole negotiation.
6. **Record layer** — application data split into records (≤16 KB), each AEAD-encrypted with a unique nonce (AES-GCM) or ChaCha20; the record's auth tag detects any tampering → attacker-modified records fail the tag check and the connection dies.
7. **Key update / renegotiation** — TLS 1.3 supports key updates (fresh keys) without a full handshake; renegotiation is removed (it caused MITM bugs in 1.2).
8. **Session resumption** — tickets (PSKs) handed to the client; on return, `PreSharedKey` extension allows abbreviated handshake: 1-RTT (or 0-RTT). Binders prove the client knows the PSK.
9. **Failure paths** — `bad_certificate`, `handshake_failure`, `insufficient_security`, `certificate_unknown` alerts; handshake timeout; client aborts on cert validation failure (the browser warning page).

## 10. Time Complexity
- **Handshake latency**: TLS 1.3 full = **1 RTT**; resumption = 1 RTT (0-RTT for early data). TLS 1.2 full = 2 RTTs. With QUIC (HTTP/3) the QUIC+TLS handshake is also 1 RTT (0-RTT on resume).
- **Per-record cost**: AEAD encryption is O(record size), hardware-accelerated (AES-NI, ChaCha via SIMD) → ~GB/s throughput; the overhead per record ≈ 0.5-2% (TLS record header + auth tag).
- **Certificate verification**: signature verification O(1) per cert in chain; revocation checks (OCSP) add latency if not stapled; chain depth usually 2-4 certs.
- **(EC)DH**: X25519 = ~50-100 µs; ECDSA verify ~50 µs — handshake crypto is sub-millisecond; the RTTs, not CPU, dominate latency.

## 11. Advantages
- **Confidentiality**: AES-GCM/ChaCha20 — no plaintext on the wire.
- **Integrity**: AEAD tags — tampering is detected and fatal.
- **Authentication**: X.509 certificates + CA trust → no impersonation (unless a CA or private key is compromised).
- **Forward secrecy** (1.3): ephemeral keys → past sessions safe even if long-term keys leak.
- **1-RTT / 0-RTT**: minimal latency; ALPN negotiates h2/h3 in the same handshake.
- **Deployable**: any port, no kernel changes, works with proxies/ALB termination; mandatory in modern practice.

## 12. Disadvantages
- **PKI trust model fragility**: a compromised CA or stolen cert → impersonation (hence CT logs, cert pinning, HPKP's rise and fall).
- **0-RTT replay risk**: replayed early data must be handled server-side (idempotency).
- **Performance overhead** (mild): crypto CPU, handshake RTTs, and TLS-in-TLS (proxies) complications.
- **Termination vs end-to-end**: if a CDN/LB terminates TLS, the last mile to origin may be plaintext (or re-encrypted) — an attack surface.
- **Config complexity**: cipher choices, HSTS, OCSP, cert rotation, mTLS — misconfig = vulnerabilities (e.g., TLS 1.0/1.1, weak ciphers).

## 13. Interview Questions
1. **Q: What is HTTPS and how does it differ from HTTP?** A: HTTPS = HTTP over TLS (RFC 8446). Adds confidentiality (encryption), authentication (certificates), and integrity (AEAD). Port 443 vs 80.
2. **Q: Explain the TLS 1.3 handshake in steps.** A: ClientHello (nonce, ciphers, key share) → ServerHello (choice + key share) → EncryptedExtensions + Certificate + CertificateVerify (signature over transcript) + Finished → client verifies cert chain/hostname/signature, sends Finished. 1 RTT total; then encrypted app data.
3. **Q (tricky): Why is the CertificateVerify message necessary if the certificate already proves identity?** A: The cert proves the *public key* belongs to the domain, but not that the *server actually holds the private key right now*. CertificateVerify = a signature over the transcript with that private key — proving live possession and binding the handshake to this exact negotiation (blocks MITM transcript-swapping).
4. **Q: What is forward secrecy and why is it required in TLS 1.3?** A: Each session uses ephemeral DH keys; even if the server's long-term cert key leaks, previously recorded sessions can't be decrypted. TLS 1.3 *mandates* PFS by removing RSA key exchange (only (EC)DHE suites exist).
5. **Q: How does a client verify a certificate?** A: (1) Build the chain leaf→root and verify each signature against the parent; (2) the root must be in the client trust store; (3) check hostname matches SAN/CN; (4) check validity dates; (5) optionally check revocation (OCSP/CRL). Any failure → fatal alert / browser warning.
6. **Q: What is the difference between TLS termination and end-to-end TLS?** A: Termination: the LB/CDN holds the cert, decrypts, and re-encrypts (or sends plaintext) to origins — you lose client-visible trust at the origin. End-to-end: the origin holds the cert; the LB passes through (TCP/UDP) — full trust chain, but you lose L7 features. Production: terminate at edge for inspection; re-encrypt to origin (mTLS internally) as best practice.
7. **Q (production): What is SNI and why does it matter?** A: Server Name Indication — the client sends the hostname in ClientHello so the server can pick the right certificate (virtual hosting). Encrypted in TLS 1.3 (ESNI/ECH now). Without SNI, servers with multiple certs can't serve correctly.
8. **Q: What is 0-RTT and what are its risks?** A: With a cached PSK/ticket, the client sends its first request in the same flight as the handshake. Risk: **replay** — capture and replay of 0-RTT data. Mitigations: replay windows, anti-replay caches, only idempotent methods, server-configured limits.
9. **Q (scenario): A user sees "certificate expired" on your API. What do you check?** A: (1) Cert validity dates (expired/renewal missed — check your cert-rotation automation); (2) server time sync (NTP — a skewed clock falsely flags expiry); (3) clock-skew on the *client*; (4) wrong cert served (SNI/ALB confusion). Renewal automation + monitoring is the fix.
10. **Q: What is a cipher suite and how is it negotiated?** A: A named combination: key exchange + authentication + bulk cipher + AEAD + PRF (e.g., `TLS_AES_128_GCM_SHA256` = HKDF with SHA-256 + AES-128-GCM). Client lists preferences; server picks (in 1.3 it must pick a suite it supports from the client list).
11. **Q: What is mTLS and when is it used?** A: Mutual TLS — the *client* also presents a certificate. Used for service-to-service auth (zero-trust, Kubernetes, microservices), B2B API identity, and IoT device auth. Server validates client certs the way clients validate server certs.
12. **Q (tricky): Why do security experts prefer TLS 1.3 over 1.2?** A: 1.3 removes: RSA key exchange (no PFS), CBC modes (padding-oracle), renegotiation (MITM bugs), SHA-1, weak ciphers — while adding 1-RTT/0-RTT, EncryptedExtensions, HKDF, and AEAD-only. Fewer algorithms = smaller attack surface.
13. **Q: What happens if a MITM presents their own certificate?** A: The certificate won't chain to a trusted root (unless the MITM has a stolen/CA-issued cert) and/or the hostname won't match → client aborts with a certificate error. This is exactly the protection against "fake login page" phishing on the network path.
14. **Q: What is OCSP stapling?** A: The server *attaches* its freshness proof (OCSP response from the CA) to the Certificate message, so the client needn't contact the CA per connection (privacy + latency). Clients still validate the staple's signature.
15. **Q (production): How would you debug "TLS handshake timeout"?** A: Check TCP reachability (nc to 443), MTU/fragmentation (packets blocked), SNI/cipher mismatch at LBs/WAFs, client hello being dropped by DPI, and TLS-inspection proxies. Use `openssl s_client -connect` and tcpdump to see where the handshake stalls.
16. **Q: What is HSTS and why does it exist?** A: HTTP Strict Transport Security — a response header (`Strict-Transport-Security`) telling browsers to *only* use HTTPS for the domain for a period, preventing downgrade attacks (HTTP→HTTPS redirect interception). Preload list makes it permanent.
17. **Q: What is the "downgrade attack" that TLS version negotiation prevents?** A: An attacker could force a client/server pair to use the *weakest* common version (e.g., SSL 3.0) by blocking the ClientHello versions. TLS 1.3 includes a **downgrade protection** signal (a specific value in ServerHello random) and deprecates old versions.
18. **Q: Why is TLS often terminated at a load balancer rather than origins?** A: Central cert management (one cert), centralized inspection (WAF/DPI), hardware crypto offload, and connection pooling to origins. The trade-off: origin must trust the LB (use mTLS or at least keep traffic in the private network).

## 14. Follow-Up Questions
1. **Q: What exactly does "CertificateVerify signature over the transcript" prevent?** A: It's a *binding* — the signature commits both sides to the exact cipher/keys/params chosen, so a MITM can't swap ServerHello parameters or replay an old handshake (transcript binding = the core anti-MITM property).
2. **Q: How does QUIC/TLS 1.3 interplay work for HTTP/3?** A: QUIC's handshake *is* TLS 1.3 (the CRYPTO frames carry the handshake); QUIC transport parameters live inside the ClientHello/ServerHello extensions. One handshake establishes both crypto and transport → 1-RTT, 0-RTT.
3. **Q: What is certificate transparency and why does it help?** A: CT logs every public cert in append-only logs (must present SCTs). Detects *misissued* certs (a CA or attacker issuing certs for your domain) — browsers can require SCTs and revoke/flag anomalies.
4. **Q: What's the role of randomness (client/server nonces) in TLS?** A: Prevents replay of a whole handshake and ensures fresh session keys even with reused DH parameters (with nonces + ephemeral keys, each session's keys are unique).
5. **Q: What is "SSL" vs "TLS"?** A: SSL (1.0-3.0) was the predecessor; TLS 1.0 = SSL 3.1. All SSL versions are broken/deprecated (POODLE, BEAST, DROWN); modern "SSL certs" are actually X.509 certs used by TLS. Say TLS in interviews.

## 15. Coding Example
```python
# Python: a TLS client + verifying the handshake the way libraries do
import socket, ssl

ctx = ssl.create_default_context()            # trusts system CAs (trust store)
ctx.minimum_version = ssl.TLSVersion.TLSv1_2  # enforce modern TLS

with socket.create_connection(("example.com", 443), timeout=5) as sock:
    with ctx.wrap_socket(sock, server_hostname="example.com") as tls:
        print("Version:", tls.version())               # TLSv1.3
        print("Cipher:", tls.cipher())                 # ('TLS_AES_128_GCM_SHA256', ...)
        print("Peer cert SAN:", tls.getpeercert().get("subjectAltName"))
        tls.sendall(b"GET / HTTP/1.1\r\nHost: example.com\r\nConnection: close\r\n\r\n")
        print(tls.recv(4096)[:200])
```
```bash
# Inspect a real TLS 1.3 handshake
$ openssl s_client -connect example.com:443 -tls1_3 -brief
# Protocol version: TLSv1.3
# Ciphersuite: TLS_AES_128_GCM_SHA256
# Server certificate: CN = example.com
$ curl -v https://example.com/ 2>&1 | grep -E "SSL|TLS|subject|issuer"
# * TLSv1.3, TLS handshake, Client hello (1)
# * subject: CN = example.com
# * issuer:  C = US, O = DigiCert Inc, ...
```

## 16. Industry Usage
- **AWS**: ALB/CLB terminate TLS (ACM certs, automatic rotation); CloudFront does edge TLS with DDoS protection; mTLS supported for service mesh (App Mesh).
- **Google**: TLS 1.3 default on all services; Chrome drives web-wide TLS 1.3 + HTTPS adoption; Google's "HTTPS-first mode" for all users.
- **Cloudflare**: terminates TLS at every edge PoP (huge scale), runs QUIC/TLS 1.3, offers "0-RTT," and Universal SSL (free certs) for the whole web.
- **Kubernetes**: mTLS via service meshes (Istio/Envoy, Linkerd) — every pod-to-pod call encrypted with per-service certs, auto-rotated.
- **Fintech**: PCI-DSS mandates TLS 1.2+; e-commerce and banking use strict HSTS, OCSP stapling, and monitor cert expiry religiously.

## 17. References
- RFC 8446 — TLS 1.3: https://www.rfc-editor.org/rfc/rfc8446
- RFC 5246 — TLS 1.2 (legacy): https://www.rfc-editor.org/rfc/rfc5246
- RFC 5280 — X.509 certificates: https://www.rfc-editor.org/rfc/rfc5280
- RFC 7258/8446 §downgrade protection; RFC 6961/6066 — OCSP stapling/SNI.
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 8 (Security / TLS).
- MDN "How TLS works" — https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security

## 18. Cheat Sheet
- HTTPS = HTTP over TLS, port 443.
- TLS 1.3 handshake = 1 RTT: ClientHello(keyshare) → ServerHello + EncryptedExt + Cert + CertVerify + Finished → app data.
- 0-RTT resumption with PSK/tickets (replay risk).
- PFS: ephemeral (EC)DH — mandatory in 1.3.
- Cert verify: chain→trust store, hostname (SAN), validity, (OCSP).
- Cipher suite example: TLS_AES_128_GCM_SHA256.
- AEAD (AES-GCM/ChaCha20) = confidentiality + integrity.
- mTLS = client also authenticates with cert.
- SNI for virtual hosting (now encrypted). HSTS prevents downgrade.
- TLS termination at LB vs end-to-end — trust boundary decision.

## 19. Quiz
1. TLS 1.3 full handshake RTTs: a) 2 b) 1 c) 0 d) 3 → **b**
2. Forward secrecy requires: a) RSA exchange b) ephemeral (EC)DH c) static DH d) AES → **b**
3. CertificateVerify proves: a) CA is trusted b) possession of the private key + transcript binding c) hostname d) expiry → **b**
4. AEAD provides: a) only encryption b) encryption + authentication c) only auth d) compression → **b**
5. 0-RTT risk: a) slow b) replay c) no PFS d) broken cert → **b**
6. Which is NOT verified by a TLS client? a) chain to trust store b) hostname in SAN c) server's disk usage d) validity dates → **c**
7. HTTPS default port: a) 80 b) 443 c) 53 d) 22 → **b**
8. HSTS prevents: a) MITM of keys b) downgrade to HTTP c) 0-RTT replay d) cert expiry → **b**
9. mTLS means: a) mutual termination b) client also has a cert c) multiple CAs d) no certs → **b**
10. TLS 1.3 removed: a) RSA key exchange b) AEAD c) ECDHE d) certs → **a**

## 20. Flashcards
- **Q: TLS 1.3 handshake RTTs?** → **A:** 1 (0-RTT on resumption).
- **Q: What is forward secrecy?** → **A:** Ephemeral DH keys → past sessions safe if long-term key leaks.
- **Q: What does CertificateVerify bind?** → **A:** Private-key possession to the exact handshake transcript (anti-MITM).
- **Q: What is AEAD?** → **A:** Encryption + authentication in one (AES-GCM, ChaCha20).
- **Q: 0-RTT risk?** → **A:** Replay of early data.
- **Q: Certificate validation steps?** → **A:** Chain→trust store, hostname/SAN, dates, (OCSP/CRL).
- **Q: What is mTLS?** → **A:** Client + server both present certs.
- **Q: HSTS?** → **A:** Force HTTPS-only to prevent downgrade attacks.

## 21. Revision
HTTPS = HTTP over TLS. TLS 1.3: 1-RTT handshake — ClientHello (with X25519 keyshare) → ServerHello + EncryptedExtensions + Certificate + CertificateVerify (signature over transcript) + Finished → encrypted app data. PFS via ephemeral DH (mandatory in 1.3, RSA key exchange removed). Cert validation: chain to trust store, SAN hostname, dates, OCSP. AEAD (AES-GCM/ChaCha20) gives confidentiality+integrity; HKDF derives keys. 0-RTT resumption (replay risk). ALPN negotiates h2/h3. mTLS for service-to-service. Terminate TLS at LB for inspection; prefer re-encryption to origin. HSTS blocks downgrade.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain the TLS 1.3 handshake." | 2 How It Works / 8 Example |
| "What is forward secrecy and why 1.3?" | 4 Why Another Approach / 13 Q&A |
| "How does a client verify a cert?" | 9 Internal Working / 13 Q&A |
| "TLS termination vs end-to-end?" | 13 Q&A / 16 Industry Usage |
| "What is 0-RTT and its risks?" | 13 Q&A / 10 Time Complexity |
| "What is mTLS?" | 13 Q&A / 3 When Used |
| "Why CertificateVerify exists?" | 13 Q&A / 14 Follow-Up |
| "Cert expired — debug?" | 13 Q&A / 15 Coding |
