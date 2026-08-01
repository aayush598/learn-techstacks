# Chapter: Security Fundamentals

## What you'll learn
- Why security exists and the vocabulary: the CIA triad (Confidentiality, Integrity, Availability), non-repudiation, AAA (Authentication, Authorization, Accounting), and how to build a threat model.
- Cryptography fundamentals: symmetric encryption (AES) vs asymmetric (RSA/ECC), key exchange (Diffie-Hellman), and the practical hybrid model (TLS).
- Hashing vs encryption, MACs/HMACs vs digital signatures — the integrity and authentication primitives that underpin TLS, SSH, IPsec, and password storage.
- Authentication and access control: factors (something you know/have/are), password storage, OAuth 2.0/OIDC/SAML, RBAC vs ABAC, and MFA.

## Prerequisites (linked)
- Basic networking layers ([Part 01](../part-01-network-fundamentals/chapter-02-osi-and-tcp-ip-models/README.md)) and HTTP/DNS ([Part 02](../part-02-application-layer/README.md)) — most security primitives protect those protocols.
- Modular arithmetic comfort (for RSA/DH math) — not required to pass, but helps.
- Part 05 (data link) and Part 04 (network layer) supply the attack surfaces (ARP, IP) this chapter's crypto defends.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Security Goals and the CIA Triad](section-01-security-goals-and-cia-triad.md) | Confidentiality/Integrity/Availability, AAA, non-repudiation, threat models, STRIDE |
| [Section 02 — Encryption and Hashing](section-02-encryption-and-hashing.md) | Symmetric (AES) vs asymmetric (RSA/ECC), DH key exchange, hashes/MACs/HMAC, hybrid crypto |
| [Section 03 — Authentication and Access Control](section-03-authentication-and-access-control.md) | Authn vs authz, factors + MFA, password storage (salt/argon2), sessions, OAuth/OIDC/SAML, RBAC/ABAC |

## One-paragraph narrative connecting all sections
Security is not a single feature; it's a set of *goals* (CIA + AAA + non-repudiation) that every protocol and system must serve (Section 01). The tools to serve those goals come from cryptography: symmetric and asymmetric encryption provide *confidentiality*, hashes and MACs provide *integrity* and *data authentication*, key exchange lets strangers build shared secrets, and the hybrid "encrypt with symmetric, authenticate with MAC, bootstrap with asymmetric" recipe is exactly what TLS/IPsec/SSH use (Section 02). But crypto only helps if the system knows *who* is asking and *what* they may do — so authentication (factors, MFA, password storage) and authorization (OAuth/OIDC, RBAC/ABAC) wrap the crypto in an identity layer (Section 03). Together the three sections form the "tools," which Chapter 02's attacks and defenses (TLS, firewalls, PKI, VPN, zero trust) then deploy in real systems.

## Common interview trap in this chapter
1. **Hashing vs encryption**: encryption is *reversible* with a key; hashing is *one-way*. "Decrypting a hash" is a category error (you crack it by brute force/dictionaries). Interviewers love this.
2. **Symmetric vs asymmetric roles**: asymmetric is *slow* and used for key exchange/signatures, never for bulk data; TLS encrypts the payload with AES (symmetric). Saying "TLS uses RSA for everything" is wrong.
3. **MAC vs signature**: both authenticate data, but HMAC uses a *shared* secret, signatures use a *private key* (public verification). Only signatures give non-repudiation.
4. **Confidentiality vs integrity vs authenticity**: encryption gives confidentiality; MAC/hash gives integrity (+authenticity with a key); they are *orthogonal* — encrypt-without-MAC is vulnerable to tampering.
5. **"Password stored in DB"**: never store plaintext; store a *salted* slow-hash (argon2/bcrypt/scrypt); "MD5(password)" is immediately crackable.

## Checklist before moving on
- [ ] I can state CIA + AAA and map an attack to a violated pillar.
- [ ] I can explain symmetric vs asymmetric with real algorithms and typical key sizes.
- [ ] I can walk Diffie-Hellman and say why it defeats eavesdropping but needs MITM protection.
- [ ] I can contrast hash vs MAC/HMAC vs signature, and pick the right one per use case.
- [ ] I can design a safe password-storage scheme (salt + argon2/bcrypt).
- [ ] I can explain authn vs authz, MFA factors, OAuth 2.0 grant types, OIDC vs SAML, RBAC vs ABAC.
