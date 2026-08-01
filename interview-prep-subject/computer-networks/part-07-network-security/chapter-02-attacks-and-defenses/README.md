# Chapter: Attacks and Defenses

## What you'll learn
- The attack landscape: DDoS, phishing, XSS, SQL injection, CSRF, MITM, and how each maps to a CIA/AAA violation and a concrete mitigation.
- Network defense layers: firewalls (packet filter → stateful → application/WAF), IDS/IPS, and how they fit "defense in depth."
- Public Key Infrastructure: X.509 certificates, CAs and chains, certificate validation, pinning, and the TLS 1.3 handshake in full.
- Secure channel protocols: IPsec (IKE/ESP/AH), VPNs (IPsec vs SSL/TLS), SSH, and when each is right.
- Zero Trust Architecture and operational best practices: identity-based access, microsegmentation, least privilege, and secure SDLC/ops.

## Prerequisites (linked)
- [Chapter 01 — Security Fundamentals](../chapter-01-security-fundamentals/README.md): the CIA/AAA goals and the crypto primitives every defense in this chapter deploys.
- HTTP and TLS basics from [Part 02](../part-02-application-layer/README.md) (XSS/SQLi live in HTTP; TLS secures it).
- Network layers (Part 03/04/05): DDoS and firewalls operate at every layer; IPsec sits on the network layer.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Common Attacks: DDoS, Phishing, XSS, SQLi](section-01-common-attacks-ddos-phishing-xss-sql-injection.md) | Each major attack: mechanism, impact, and the standard mitigations |
| [Section 02 — Firewalls and IDS/IPS](section-02-firewalls-and-ids-ips.md) | Packet-filter, stateful, application firewalls, WAF, NIDS/HIDS, IDS vs IPS, deployment |
| [Section 03 — PKI, Certificates, and TLS in Depth](section-03-pki-certificates-and-tls-in-depth.md) | X.509, CA hierarchy, chains, validation, revocation, pinning, full TLS 1.3 handshake |
| [Section 04 — Secure Channel Protocols and VPN](section-04-secure-channel-protocols-and-vpn.md) | IPsec (IKE/ESP/AH) vs TLS vs SSH; VPN types; WireGuard; tunnels |
| [Section 05 — Zero Trust Architecture and Best Practices](section-05-zero-trust-architecture-and-best-practices.md) | Zero trust principles, BeyondCorp/Cloudflare Access, microsegmentation, secure ops |

## One-paragraph narrative connecting all sections
Attacks exploit the gaps between what a system *assumes* and what it *enforces* — a DDoS starves availability, phishing steals authentication, XSS and SQLi break input trust, and MITM breaks channel trust (Section 01). The first line of defense is *network enforcement*: firewalls filter by packet/state/application, IDS/IPS detect and stop suspicious behavior, and WAFs catch web-app attacks — a layered "defense in depth" (Section 02). But filtering can't fix a broken trust chain: the crypto that authenticates endpoints and encrypts traffic is only sound if *identities* are bound to keys — that's PKI, X.509 certificates, and the TLS 1.3 handshake (Section 03). Those identities and keys then get deployed in secure channels: IPsec, TLS-based VPNs, SSH, and WireGuard — each chosen for its layer and use case (Section 04). Finally, no single control suffices, so modern architecture institutionalizes the lessons: never trust the network, verify every request, segment access, and automate detection — Zero Trust (Section 05).

## Common interview trap in this chapter
1. **IDS vs IPS**: IDS *detects* (passive, alerts); IPS *prevents* (inline, drops). Saying "IDS blocks" is wrong.
2. **Firewall generations**: packet filters don't track state; stateful firewalls track connections; next-gen/app firewalls understand applications (e.g., SNI/DNS). "A firewall inspects every payload" overstates packet filters.
3. **TLS handshake order**: TLS 1.3 is 1-RTT (ClientHello/ServerHello + Finished), NOT the 2-RTT RSA exchange of TLS 1.2. Forgetting that 1.3 removed RSA key exchange and uses ephemeral ECDH (forward secrecy) is a common miss.
4. **XSS vs SQLi**: XSS = script injected into *HTML the victim's browser renders* (client-side); SQLi = query injected into *SQL the server runs* (server-side). Both are input-validation failures but attack different interpreters.
5. **VPN type**: IPsec works at L3 (IP packets); TLS VPN works at L4/L5 (app traffic). "IPsec secures HTTP" is imprecise — it secures IP, not the app layer.

## Checklist before moving on
- [ ] I can describe each attack class (DDoS/phishing/XSS/SQLi/CSRF/MITM) with mechanism + mitigation.
- [ ] I can compare packet-filter, stateful, and application firewalls, and IDS vs IPS.
- [ ] I can walk the full TLS 1.3 handshake and explain certificate validation (chains, trust store, revocation).
- [ ] I can compare IPsec vs TLS vs SSH and explain VPN architecture (site-to-site vs remote access).
- [ ] I can articulate zero-trust principles and how they change network design.
