# Encryption and Hashing

> **TL;DR**: Encryption is a *reversible* transformation of data under a key (AES symmetric for bulk, RSA/ECC asymmetric for keys and signatures), hashing is a *one-way* fingerprint (SHA-2/SHA-3 for integrity), and the two combine with MACs/HMACs and Diffie-Hellman key exchange into the hybrid recipe — encrypt with symmetric, authenticate with MAC, bootstrap with asymmetric — that powers TLS, SSH, IPsec, and password storage.

## 1. Why Does This Exist?
The Internet is an open channel: anyone can intercept packets. To make it trustworthy, we need four cryptographic guarantees — **confidentiality** (encryption), **integrity + authenticity** (MACs/signatures), **non-repudiation** (signatures), and **identity establishment** (key exchange + certificates). No single algorithm provides all of these, so cryptography is a *toolkit*: symmetric encryption (AES) is fast enough for bulk data but needs a shared secret; asymmetric encryption (RSA/ECC) needs no pre-shared secret but is too slow for payloads; hashes give one-way integrity but no key; MACs add a key to hashes; and Diffie-Hellman lets two strangers derive a shared secret in the open. Every secure protocol — TLS, SSH, IPsec, WhatsApp, git — is an *orchestration* of these primitives. Understanding which tool does what (and what it can't do) is the difference between "we use encryption" and "our design is sound."

## 2. How Does It Work?
- **Symmetric (AES-128/256)**: one secret key encrypts and decrypts; block ciphers in modes (GCM for encryption+integrity in one pass). Fast, hardware-accelerated (AES-NI).
- **Asymmetric (RSA, ECC/ECDSA, Ed25519)**: key *pair* — public (encrypt/verify) and private (decrypt/sign). RSA relies on factoring; ECC on elliptic-curve discrete log; ECC gives equal security at ~10× smaller keys (256-bit ECC ≈ 3072-bit RSA).
- **Diffie-Hellman (DH/ECDH)**: each side picks a private scalar, exchanges public values, computes a shared secret; an eavesdropper sees only the public values. Needs MITM protection (that's what certificates/signatures add).
- **Hashing (SHA-256/384/512, SHA-3)**: one-way, deterministic, collision-resistant; no key; used for integrity, password storage (with salt + slow KDF).
- **MAC/HMAC**: hash with a shared key → integrity *and* authenticity. HMAC = keyed SHA.
- **Digital signature**: sign with private key, verify with public → integrity + authenticity + non-repudiation.
- **Hybrid (real systems)**: DH/ECDH + signatures to agree a session key, AES-GCM to encrypt bulk, HMAC/signature to authenticate — this is the TLS recipe.

## 3. When Is It Used?
- **AES**: TLS/HTTPS records, IPsec ESP, disk encryption (LUKS/BitLocker), WiFi (CCMP), SSH — everywhere bulk data is encrypted.
- **RSA/ECC**: TLS handshake (key exchange + server signature), code signing, email (PGP), certificate authorities, blockchain.
- **SHA-2/3**: file/integrity checks (apt checksums, git object IDs), TLS record MACs, certificate fingerprints, password hashing (as part of KDFs).
- **HMAC**: TLS (with AEAD), IPsec, cookie signing, API request signing (AWS SigV4).
- **DH/ECDH**: TLS 1.3 (all key exchanges), IKE (IPsec), SSH, WireGuard — forward secrecy.
- **Password storage**: salt + argon2/bcrypt/scrypt/PBKDF2 (never plaintext, never fast hash alone).

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: use asymmetric for everything.* RSA encryption of every payload is 100-1000× slower than AES and has size limits (RSA can encrypt ~key-size bytes only). Asymmetric exists to solve the *key-distribution* problem; symmetric solves the *speed* problem; hybrid uses each where it's best.
- *Alternative: use a fast hash (MD5/SHA-1) for passwords.* Fast hashes are trivially brute-forced (billions/sec with GPUs). Passwords need *slow*, memory-hard KDFs (argon2/bcrypt) + per-user salt so each hash must be attacked individually.
- *Alternative: DH without authentication (no signatures).* DH alone is vulnerable to MITM — Mallory interposes two DH sessions. Signatures/certificates authenticate the parties and bind the key exchange → the reason TLS has certificates.
- *Alternative: rely on shared secrets pre-configured.* Symmetric-only systems (like early Kerberos) need a secret channel to bootstrap — which is the chicken-and-egg asymmetric/DH solves.
- *Alternative: encrypt-then-MAC vs MAC-then-encrypt ordering debates.* The community standardized on AEAD (AES-GCM/ChaCha20-Poly1305) precisely to make encryption+integrity atomic and avoid the ordering/padding-oracle bugs of ad-hoc combos.

## 5. Intuition
Encryption is a **lockbox**: a key opens it; without the key you can't read what's inside (confidentiality). But a lockbox says nothing about whether someone *rearranged the contents* — that's integrity, the **tamper-evident seal** (a hash/MAC). Hashing is a **fingerprint**: given any document you can compute a unique short fingerprint, but you can never reconstruct the document from the fingerprint (one-way). Diffie-Hellman is the **two-dye trick**: two people each pick a secret color, mix it with a shared public color, exchange the mixtures — then each combines their secret with the other's mixture to get the same final color, and anyone watching the exchanged mixtures *cannot* derive it. Asymmetric crypto is the **mailbox with a slot**: anyone can drop a letter in (public key encrypts), but only the owner's key opens it (private key decrypts); signatures are the **hand-written seal** only you can produce but everyone can verify.

## 6. Real-World Analogy
A **courier service with tamper-evident envelopes**. Encryption = the opaque envelope (nobody reads the contents). Integrity = the tamper-evident tape (a broken seal proves tampering — the hash). Authentication = the courier's signed delivery receipt (only the sender's signature validates origin). Key exchange = the two parties privately agreeing on a one-time pad *through* the mail (DH). Signatures = the notary's stamp only the notary can make, but anyone can verify. Password hashing = the safe that burns the paper when you try to read it — you can *check* by re-burning, but you can't recover the original.

## 7. Formal Definition
- **Encryption**: Enc(k, m) → c, Dec(k, c) → m; **symmetric** uses one key (AES), **asymmetric** uses (pub, priv) (RSA, ECC). Security notions: IND-CPA/IND-CCA.
- **Hash**: H: {0,1}* → {0,1}^n, one-way (preimage), second-preimage, and collision-resistant (2^(n/2) work for collision by birthday bound). SHA-256 n=256.
- **MAC/HMAC**: keyed function → tag; unforgeable without the key; provides integrity + authenticity, not non-repudiation.
- **Signature**: Sign(priv, m) → σ; Verify(pub, m, σ) — provides non-repudiation.
- **DH**: g^a, g^b exchanged; shared = g^ab; security = CDH/DLP. **ECDH**: elliptic-curve analog.
- **Hybrid (TLS)**: DH/ECDH key agreement + certificate signature (asymmetric) → session key; AES-GCM/ChaCha20-Poly1305 (symmetric AEAD) for records.
- **KDF**: password → key/verifier (PBKDF2/bcrypt/scrypt/argon2) — deliberately slow + salted.

## 8. Example
**DH key exchange with small numbers (illustrative, NOT secure sizes):** prime p = 23, generator g = 5.
- Alice picks a = 6 → sends A = g^a mod p = 5⁶ mod 23 = 8.
- Bob picks b = 15 → sends B = g^b mod p = 5¹⁵ mod 23 = 19.
- Alice computes s = B^a mod 23 = 19⁶ mod 23 = 2.
- Bob computes s = A^b mod 23 = 8¹⁵ mod 23 = 2.
- Shared secret s = 2 — but the wire carried only (23, 5, 8, 19). Eve can't feasibly compute a or b (discrete log) at real key sizes (2048-bit p).

**Password storage.** Register: store `argon2id(salt, password)`. Login: re-derive with the stored salt and compare. Attacker who steals the DB gets salted slow-hashes — must brute-force each password individually (~seconds each with argon2 parameters, vs nanoseconds for MD5).

## 9. Internal Working
1. **AES** (block cipher, 128-bit blocks, 10-14 rounds): SubBytes/ShiftRows/MixColumns/AddRoundKey per round; **GCM** mode wraps it: CTR encryption + GHASH authentication tag in one pass → AEAD (encrypt + MAC in hardware).
2. **RSA**: keygen (two large primes p,q; n=pq; e,d with ed≡1 mod φ(n)); encrypt c = m^e mod n, decrypt m = c^d mod n; 2048-4096-bit keys.
3. **ECC**: points on y²=x³+ax+b; scalar mult Q = k·P; ECDH shares k·(l·P) = l·(k·P) = kl·P; Ed25519/X25519 = fast constant-time curves.
4. **SHA-256**: Merkle-Damgård sponge-style compression over 512-bit blocks, 64 rounds; SHA-3 = Keccak sponge (different structure, immune to length-extension).
5. **HMAC**: H((K⊕opad) ∥ H((K⊕ipad) ∥ m)) — keyed twice, resistant to length extension.
6. **TLS 1.3 handshake (hybrid in action)**: ClientHello (key_share) → ServerHello + cert + signatures + Finished → session AES-GCM keys, HKDF-derived; forward secrecy because DH keys are ephemeral (Part 02 section has the full walk).

## 10. Time Complexity / Performance
- **AES**: ~1-10 Gbps with AES-NI; constant-time by design (no data-dependent branches).
- **RSA**: encrypt/verify fast (small exponent e=65537); decrypt/sign slow (~ms at 2048-bit) → never for bulk.
- **ECC (P-256/Ed25519)**: ~10× faster than RSA at equal security → modern default.
- **SHA-256**: ~1-2 GB/s (SHA-NI); HMAC ≈ similar.
- **Hashing passwords**: *deliberately* slow — argon2 target ~0.1-1 s per attempt (memory-hard, GPU-resistant).
- **Birthday bound**: collision resistance = 2^(n/2) — SHA-256 ~2¹²⁸ (why 128-bit security for 256-bit hash).

## 11. Advantages
- **Symmetric**: fast, hardware-accelerated, simple — the only viable choice for bulk data.
- **Asymmetric**: solves key distribution and enables signatures (non-repudiation, certificates, code signing).
- **DH/ECDH**: forward secrecy (ephemeral keys — past traffic survives future key compromise), no pre-shared secret needed.
- **Hashing**: one-way integrity, collision detection, cheap, no key management for checksums.
- **HMAC**: keyed integrity/authenticity without asymmetric cost; standard across protocols.
- **Hybrid design**: each primitive does what it's best at → TLS is both fast and forward-secret.

## 12. Disadvantages
- **Symmetric**: key distribution problem (the pre-shared-secret chicken-and-egg); key compromise = total loss.
- **Asymmetric**: slow, key-size limits, needs PKI (certificates) to bind public keys to identities.
- **DH**: vulnerable to MITM *without authentication* — the classic "DH alone is insecure" trap.
- **Hash**: one-way by design (can't recover data); collision attacks force migration (MD5/SHA-1 broken).
- **HMAC**: shared key = no non-repudiation (either party could have computed the tag).
- **Password hashing**: still crackable for weak passwords; needs salt + slow KDF + ideally MFA/breach monitoring.

## 13. Interview Questions
1. **Q: What's the difference between encryption and hashing?** A: Encryption is reversible with a key (you can decrypt); hashing is one-way (you can never recover the input). Encryption provides confidentiality; hashing provides integrity. "Decrypting a hash" is a contradiction — you crack it by brute force.

2. **Q: Symmetric vs asymmetric encryption — when is each used?** A: Symmetric (AES): fast, one key, bulk data (TLS records, disk). Asymmetric (RSA/ECC): key exchange + signatures, slow, used only for handshakes and authenticity. Real systems are hybrid: DH/asymmetric for the key, AES for the payload.

3. **Q: How does Diffie-Hellman work and why is it secure?** A: Both pick private values a,b; exchange g^a, g^b; compute g^ab. An eavesdropper sees g^a and g^b but computing a or b is discrete-log-hard (infeasible at 2048-bit p / 256-bit curves). Caveat: DH is MITM-vulnerable without authentication.

4. **Q: What is forward secrecy and how does TLS 1.3 provide it?** A: Each session uses *ephemeral* DH keys that are discarded after the session; even if the server's long-term private key is later stolen, past sessions can't be decrypted (the session key is gone). TLS 1.3 mandates ephemeral ECDH — no static RSA key exchange remains.

5. **Q: TRICKY — "We encrypt passwords with MD5." What's wrong?** A: MD5 is a fast hash (billions/sec brute force), has known collisions, and is unsalted — identical passwords give identical hashes and precomputed rainbow tables crack them instantly. Use a per-user salt + memory-hard KDF (argon2/bcrypt/scrypt).

6. **Q: What is a MAC and how does it differ from a hash?** A: A MAC (e.g., HMAC) is a *keyed* hash — only parties with the key can compute/verify it. A plain hash gives integrity against random corruption but not authenticity (anyone can recompute it). HMAC gives both integrity and authenticity (but not non-repudiation).

7. **Q: How do digital signatures give non-repudiation that HMAC doesn't?** A: A signature is created with a *private* key and verified with the *public* key — only the signer can produce it, so they can't deny it. HMAC uses a *shared* secret: either party could have created the tag, so it proves nothing about who.

8. **Q: What is a birthday attack and how does it affect hash strength?** A: To find *any* two inputs with the same hash (collision) requires only ~2^(n/2) evaluations (birthday paradox) — for SHA-256 that's 2¹²⁸. This is why 128-bit hashes (MD5, SHA-1 at 160) are broken: 2⁶⁴/2⁸⁰ work is feasible. Choose ≥256-bit hashes.

9. **Q: What is an AEAD cipher and why did TLS adopt it?** A: Authenticated Encryption with Associated Data — encryption and integrity in one primitive (AES-GCM, ChaCha20-Poly1305). It eliminates the ordering bugs of separate encrypt+MAC designs and the padding-oracle attacks on CBC. TLS 1.3 only allows AEAD.

10. **Q: PRODUCTION — Your TLS 1.2 server supports RSA key exchange and CBC. Why upgrade?** A: RSA key exchange lacks forward secrecy (static key decrypts all sessions) and CBC had padding-oracle attacks (POODLE, BEAST); 3DES is deprecated. Migrate to TLS 1.3 (or 1.2 with ECDHE + AES-GCM) — this is exactly what Cloudflare/Google pushed ("Supporting all TLS 1.3").

11. **Q: What is RSA actually based on?** A: The hardness of factoring large composites n = p·q (and the RSA assumption: computing m from c = m^e without the private exponent). 2048-bit RSA ≈ 128-bit security; 3072 ≈ 128, and ECC P-256 offers equivalent security at a fraction of the key size.

12. **Q: TRICKY — Why does ECC beat RSA at the same security level?** A: The best-known attacks on ECC (Pollard rho on the curve order) run in ~2^(n/2), while the best on RSA (NFS factoring) is subexponential in the key bits — so ECC's key sizes grow linearly, RSA's superlinearly. P-256 (256 bits) ≈ RSA-3072, P-384 ≈ RSA-7680.

13. **Q: What is a cryptographic salt and why do you need one?** A: A random per-user value mixed into the hash so identical passwords produce different hashes, defeating rainbow tables and cross-account correlation, and forcing attackers to brute-force each hash separately. Never omit the salt; never reuse it.

14. **Q: SCENARIO — An attacker stole your user database of argon2 hashes. What can they do?** A: Brute-force weak passwords one at a time (seconds each, parallelized), target high-value accounts, and wait for the same password reused elsewhere. They *cannot* reverse the hashes or read them directly. Response: force password resets, notify users, add MFA, and treat the incident as credential exposure.

15. **Q: What is the difference between encryption at rest and in transit?** A: At rest: data encrypted when stored (disk encryption, DB column encryption, object-store SSE) — protects against disk theft/leak. In transit: encrypted over the network (TLS/IPsec) — protects against sniffing. Both are needed; at-rest keys are managed separately (KMS).

16. **Q: Why does TLS 1.3 drop RSA key exchange and most ciphers?** A: Simplicity + safety: fewer options = fewer misconfigurations. Static RSA key exchange has no forward secrecy; CBC + SHA-1 had attack classes; TLS 1.3 keeps only (EC)DHE key exchange + AEAD, cutting the handshake to 1-RTT (or 0-RTT resumption) and removing whole bug classes.

17. **Q: TRICKY — If I encrypt a file with AES-256 and lose the key, can anyone help?** A: Only by brute force — 2²⁵⁶ keys is astronomically infeasible. There's no "backdoor" unless one was designed in (which defeats the purpose). This is the availability vs confidentiality trade: encryption makes data unreadable even to you without the key — hence key management (KMS, HSM, backups).

18. **Q: PRODUCTION — Design a secure file-transfer protocol from scratch.** A: (1) Authenticate both ends (certificates/signatures); (2) ECDH for forward-secret session key; (3) AES-GCM (AEAD) for each file/chunk with unique nonces; (4) key rotation + integrity of metadata; (5) at-rest encryption of stored files with KMS-managed keys; (6) audit logging. This mirrors SFTP/SCP/TLS design — a great "apply the primitives" answer.

## 14. Follow-Up Questions
1. **Q: What is the "length-extension attack" and how does HMAC resist it?** A: Given H(m) you can compute H(m∥pad∥x) for some constructions (SHA-2/MD) without knowing m — a forgery risk for naive MACs. HMAC nests the key twice so the inner/outer keyed hashes break the extension chain; SHA-3/Keccak is immune by design.

2. **Q: What is the difference between a KDF and a hash?** A: A KDF (PBKDF2, HKDF, argon2) is a hash *purpose-built* for deriving keys/verifiers: slow (iterations/memory), saltable, and length-stretching. Plain SHA-256 is fast (bad for passwords) and unsuitable as a direct KDF.

3. **Q: Why is AES-GCM preferred over AES-CBC+HMAC?** A: GCM is one pass (encrypt + tag), parallelizable in hardware, and constant-time — CBC+HMAC requires two passes and has a history of padding-oracle and IV-reuse bugs. GCM's one caveat: a nonce must never be reused.

4. **Q: What does "IND-CPA" mean and why do modes need random IVs/nonces?** A: Indistinguishability under chosen-plaintext attack: ciphertexts of chosen plaintexts must be unpredictable — which requires a fresh random IV/nonce per message (else identical messages produce identical ciphertexts, leaking equality).

## 15. Coding Example
```python
import hashlib, hmac, os

# Symmetric (AES-GCM via a stdlib-adjacent lib) — conceptual; use 'cryptography' in production
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, b"secret payload", b"aad")
    pt = AESGCM(key).decrypt(nonce, ct, b"aad")
    print(f"AES-GCM ok: {pt == b'secret payload'}, ct={len(ct)}B")
except ImportError:
    print("install 'cryptography' to run AES-GCM example")

# Hashing + salt (password storage sketch)
def hash_password(pw: str) -> tuple[str, str]:
    salt = os.urandom(16).hex()
    return salt, hashlib.pbkdf2_hmac("sha256", pw.encode(), bytes.fromhex(salt), 600_000).hex()

salt, h = hash_password("hunter2")
print(f"salted pbkdf2 hash: {salt[:8]}...{h[:16]}...")

# HMAC (integrity + authenticity)
def sign_message(msg: bytes, key: bytes) -> str:
    return hmac.new(key, msg, hashlib.sha256).hexdigest()

key = os.urandom(32)
print("HMAC:", sign_message(b"payload", key)[:16])
```
```python
# DH with real-size parameters via cryptography (X25519)
try:
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
    a, b = X25519PrivateKey.generate(), X25519PrivateKey.generate()
    shared_a = a.exchange(b.public_key())
    shared_b = b.exchange(a.public_key())
    print(f"ECDH shared secrets match: {shared_a == shared_b}, len={len(shared_a)}B")
except ImportError:
    pass
```
```bash
# Inspect real cryptography in use
openssl s_client -connect example.com:443 -tls1_3 2>/dev/null \
    | grep -E "New, TLSv1.3|Cipher is|Peer signing digest"     # negotiated cipher (AEAD)
openssl x509 -in /etc/ssl/certs/ca-certificates.crt -noout -text | grep -E "Signature|Public-Key" | head -3
journalctl -u sshd | grep "Accepted publickey" | tail -3       # SSH host-key auth in action
# Password file hygiene (Linux): /etc/shadow uses salted slow hashes
sudo getent shadow root | cut -d: -f2 | cut -d'$' -f1-3        # e.g. $6$ = sha512 (legacy) 
```

## 16. Industry Usage
- **TLS/HTTPS everywhere**: TLS 1.3 = (EC)DHE + AEAD (AES-128/256-GCM, ChaCha20) — Cloudflare, Google, AWS all-in.
- **IPsec**: IKEv2 + ESP with AES-GCM — VPNs (RFC 7296, RFC 8221 for AEAD).
- **SSH**: Ed25519/RSA host keys + ChaCha20-Poly1305 or AES-GCM (RFC 8332).
- **Password storage**: argon2id (OWASP first choice), bcrypt, scrypt in auth systems (Okta, Keycloak, Auth0).
- **Cloud KMS**: AWS/GCP KMS, HSMs, and envelope encryption — AES-256 data keys wrapped by asymmetric/master keys.
- **Signing**: code signing, container image signing (Sigstore/cosign), APT/Gem/NPM package verification, JWT signing (RS256/ES256).
- **Cryptocurrency**: ECDSA/secp256k1, Ed25519 — pure applied ECC.

## 17. References
- RFC 8446 (TLS 1.3) — https://datatracker.ietf.org/doc/html/rfc8446
- RFC 2631 (DH), RFC 3526 (MODP groups), RFC 7748 (X25519/448).
- NIST FIPS 197 (AES), FIPS 180-4 (SHA-2), FIPS 202 (SHA-3).
- OWASP Password Storage Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- RFC 2104 (HMAC) — https://datatracker.ietf.org/doc/html/rfc2104
- Ferguson, Schneier, Kohno, *Cryptography Engineering* (the practitioner text).
- Stallings, *Cryptography and Network Security* (the academic text).

## 18. Cheat Sheet
- Encryption = reversible (confidentiality); hash = one-way (integrity). Never "decrypt a hash."
- Symmetric AES: fast, bulk. Asymmetric RSA/ECC: keys + signatures, slow. Hybrid = DH + AES-GCM.
- DH: g^a/g^b → g^ab shared; MITM-vulnerable without auth; forward secrecy via ephemeral keys.
- HMAC = keyed hash → integrity + authenticity (not non-repudiation).
- Signature (private-key) → non-repudiation; verify with public key.
- Password storage: salt + argon2/bcrypt/scrypt (slow, memory-hard); never MD5/SHA-1.
- Birthday bound: collisions at 2^(n/2) → SHA-256 gives 2¹²⁸ security.
- AEAD (AES-GCM/ChaCha20-Poly1305): encrypt+MAC in one primitive; TLS 1.3 is AEAD-only.
- ECC P-256 ≈ RSA-3072 at ~10× smaller keys and faster.
- Encryption without MAC = tamperable (CBC bit-flip); always encrypt-then-authenticate.

## 19. Quiz
1. Encryption provides: a) integrity b) confidentiality c) non-repudiation d) authentication → **b**
2. Hashing is: a) reversible b) one-way c) keyed d) symmetric → **b**
3. Which is used for bulk encryption in TLS? a) RSA b) AES-GCM c) SHA-256 d) HMAC → **b**
4. DH provides: a) shared secret agreement b) signatures c) encryption of payload d) hashing → **a**
5. Forward secrecy comes from: a) static RSA b) ephemeral DH c) longer keys d) salt → **b**
6. Password storage should use: a) MD5 b) salt + argon2/bcrypt c) plaintext d) AES → **b**
7. Non-repudiation requires: a) HMAC b) digital signatures c) hash d) salt → **b**
8. P-256 ECC ≈ which RSA key size? a) 1024 b) 2048 c) 3072 d) 512 → **c**

**Answers**: 1-b, 2-b, 3-b, 4-a, 5-b, 6-b, 7-b, 8-c.

## 20. Flashcards
- **Q: Encryption vs hashing?** → **A:** Reversible with key vs one-way fingerprint; confidentiality vs integrity.
- **Q: Why hybrid (AES + DH/RSA)?** → **A:** AES fast for bulk, asymmetric/DH for key agreement + auth; use each where it's best.
- **Q: How does DH work?** → **A:** Exchange g^a, g^b; compute g^ab; discrete-log hard; needs auth vs MITM.
- **Q: What is forward secrecy?** → **A:** Ephemeral keys per session; compromise of long-term key can't decrypt past sessions.
- **Q: HMAC vs signature?** → **A:** HMAC = shared-key integrity+authenticity; signature = private-key non-repudiation.
- **Q: How to store passwords?** → **A:** Per-user salt + memory-hard slow KDF (argon2/bcrypt/scrypt).
- **Q: What is the birthday bound?** → **A:** 2^(n/2) for collisions → use ≥256-bit hashes (SHA-256).

## 21. Revision
Encryption (reversible, confidentiality) vs hashing (one-way, integrity) vs MAC/HMAC (keyed → integrity+authenticity) vs signature (private-key → non-repudiation). Symmetric AES-GCM encrypts bulk; asymmetric RSA/ECC and DH/ECDH do key exchange + signatures; TLS 1.3 is (EC)DHE + AEAD with forward secrecy. Password storage = salt + argon2/bcrypt/scrypt (never plaintext/fast hash). Key numbers: birthday bound 2^(n/2) (SHA-256 → 2¹²⁸), ECC P-256 ≈ RSA-3072, AES-NI ~Gbps. Anchors: *encrypt-then-MAC always; DH alone is MITM-able; encryption ≠ integrity ≠ authenticity; forward secrecy means stolen long-term keys can't decrypt old sessions.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Encryption vs hashing" | 13-Q1 / 7 |
| "Symmetric vs asymmetric, when each" | 13-Q2 / 4 |
| "How does DH work / MITM risk" | 13-Q3 / 8 |
| "What is forward secrecy?" | 13-Q4 |
| "How should passwords be stored?" | 13-Q5 / 8 |
| "MAC vs hash vs signature" | 13-Q6,7 |
| "Birthday attack / hash strength" | 13-Q8 |
| "Why AEAD / why TLS 1.3 dropped RSA+CBC" | 13-Q9,10,16 |
| "Why ECC beats RSA at same security" | 13-Q12 |
| "Design a secure file transfer" | 13-Q18 |
