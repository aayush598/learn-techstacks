# Part: Network Security

## What this part covers
Layer-by-layer and topically — the full security story: why security exists (the threat model), the CIA triad and its extension to AAA (Part 07 ch-01), the crypto primitives (symmetric vs asymmetric encryption, hashing, MACs, key exchange) and how authentication/access control work, then the attack landscape (DDoS, phishing, XSS, SQLi, MITM) and the defenses (firewalls, IDS/IPS, PKI, TLS in depth, VPN/IPsec, zero trust). This part connects every earlier protocol topic (DNS, TCP, HTTP, ARP, routing) to its attack and defense, and it is one of the highest-value interview areas — security questions appear in nearly every FAANG/MAANG round, and "walk through the TLS handshake" is a canonical question.

## Chapter map (table: chapter → sections → key skills)

| Chapter | Sections | Key skills you gain |
|---|---|---|
| ch-01 Security Fundamentals | Security Goals & CIA Triad, Encryption & Hashing, Authentication & Access Control | Build a threat model, apply the CIA triad + AAA, choose symmetric vs asymmetric crypto, explain hash/MAC/HMAC vs encryption, walk authentication factors and OAuth/OIDC/SAML, RBAC/ABAC |
| ch-02 Attacks and Defenses | Common Attacks (DDoS/Phishing/XSS/SQLi), Firewalls & IDS/IPS, PKI/Certificates/TLS, Secure Channels & VPN, Zero Trust & Best Practices | Describe and defend each attack class; firewall types (packet/stateful/APP); IDS vs IPS; X.509 PKI, CA hierarchy, TLS 1.3 handshake; IPsec (IKE/ESP/AH) vs TLS vs SSH; zero-trust architecture and secure coding/ops |

## Study order
1. **ch-01 first** — you can't discuss attacks or TLS without the goals (CIA), the crypto primitives, and the identity model (authn/authz). Every defense in ch-02 uses these tools.
2. **ch-02 in order**: attacks (Section 01) motivate firewalls/IDS (Section 02), which are then hardened by cryptographic infrastructure (Section 03 PKI/TLS), applied in secure channels (Section 04), and finally institutionalized in zero-trust architecture (Section 05).
3. Within ch-01: goals → crypto → access control. Within ch-02: attacks → defense-in-depth layers → crypto → architecture.

## Interview importance (0-5 stars) + which companies emphasize it
- **Importance: ⭐⭐⭐⭐⭐ (5/5)** — security is the single most-tested area after core protocols. The TLS handshake, symmetric-vs-asymmetric, hashing vs encryption, and "how would you defend against XSS/SQLi/DDoS?" are asked at every level from new-grad to staff.
- **Emphasized by**: every security role (CISSP-track), platform/infra teams (AWS/Azure/GCP IAM, VPC security), Cloudflare/Fastly (edge WAF, TLS), Stripe/PayPal (PCI, crypto), and any backend interview that includes "how do you secure an API?"
- Typical asked: "Walk through the TLS 1.3 handshake", "When symmetric vs asymmetric?", "Why can't you 'decrypt' a password hash?", "What is a birthday attack / what does SHA-256 collision resistance mean?", "How do you stop a DDoS?", "Explain certificate pinning", "Zero trust — what does it actually mean?"

## How the parts connect (roadmap)
- **Part 02 (Application layer)**: HTTPS/TLS secures HTTP; DNS has its own attacks (spoofing, DNSSEC); email (SPF/DKIM/DMARC) is security; cookies/sessions (Part 02) are the auth targets.
- **Part 03/04 (Transport/Network)**: TCP attacks (SYN flood, spoofing, session hijacking), IPsec at L3, ARP poisoning (Part 05), BGP hijacking — the attack surface this part defends.
- **Part 05 (Data link)**: MAC-based attacks (ARP spoofing, MAC flooding, VLAN hopping) are defended by the switch-security tools mentioned in ch-02.
- **Part 08 (Advanced)**: DDoS-mitigation architectures, anycast scrubbing, and edge security designs apply everything in this part at scale.

## Checklist before moving on
- [ ] I can define CIA and AAA and map an attack to the pillar it violates.
- [ ] I can explain symmetric (AES) vs asymmetric (RSA/ECC) crypto, key exchange (Diffie-Hellman), and when each is used.
- [ ] I can distinguish hashing from encryption, and MAC/HMAC from signatures.
- [ ] I can walk the TLS 1.3 handshake step by step (and the TLS 1.2 differences).
- [ ] I can describe XSS/SQLi/CSRF/DDoS and the standard mitigations.
- [ ] I can compare firewalls (packet/stateful/APP/WAF), IDS vs IPS.
- [ ] I can explain IPsec (IKE/ESP/AH), VPNs (IPsec/SSL), and SSH's design.
- [ ] I can articulate zero-trust principles and how they change architecture.
