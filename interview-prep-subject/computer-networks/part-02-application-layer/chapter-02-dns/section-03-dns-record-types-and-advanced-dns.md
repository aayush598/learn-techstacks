# DNS Record Types and Advanced DNS

> **TL;DR**: DNS records encode everything DNS knows — A/AAAA (addresses), CNAME (aliases), MX (mail), NS (delegation), TXT (SPF/DKIM/proof), SRV (services), SOA (zone metadata), PTR (reverse) — and advanced DNS (DNSSEC, DoH/DoT, anycast, round-robin, GeoDNS, split-horizon) turns a name lookup into a *secure, private, load-balanced, geographically-optimized routing system*.

## 1. Why Does This Exist?
DNS isn't just "name → IP"; real systems need to encode *mail routing, service discovery, authentication proofs, anti-spam records, delegation, and reverse lookups* — so the record system exists as a **generic typed database** where each RR type has defined semantics. And because DNS sits *before* almost every connection, it's become a **control/routing plane**: DNSSEC exists because unauthenticated answers let attackers hijack traffic; DoH/DoT exists because plaintext DNS leaks browsing; anycast/round-robin/GeoDNS exist because authoritative DNS is a cheap, high-leverage place to distribute load and route users to the nearest server. This section covers "what can DNS store" and "how production DNS is hardened and scaled."

## 2. How Does It Work?
**Core record types (RFC 1035 + additions):**
| Type | Purpose | Example value |
|---|---|---|
| **A** | IPv4 address | `www.example.com. 300 IN A 93.184.216.34` |
| **AAAA** | IPv6 address | `www.example.com. 300 IN AAAA 2606:2800:220:1::1` |
| **CNAME** | Canonical name (alias) | `www.example.com. CNAME example.com.` |
| **MX** | Mail exchanger + priority | `example.com. MX 10 mail.example.com.` |
| **NS** | Authoritative nameservers (delegation) | `example.com. NS ns1.example.com.` |
| **TXT** | Arbitrary text (SPF, DKIM, verification) | `example.com. TXT "v=spf1 include:_spf.google.com ~all"` |
| **SRV** | Service location (host, port, weight) | `_sip._tcp.example.com. SRV 10 60 5060 sip.example.com.` |
| **SOA** | Zone authority metadata | `example.com. SOA ns1.example.com. hostmaster.example.com. (serial refresh retry expire minttl)` |
| **PTR** | Reverse (IP → name) | `34.216.184.93.in-addr.arpa. PTR example.com.` |
| **CAA** | Which CAs may issue certs | `example.com. CAA 0 issue "letsencrypt.org"` |
| **NAPTR/DNAME** | Regex rewrite / alias subtree | tel, legacy |

**Advanced DNS mechanisms:**
- **DNSSEC** (RFC 4033-4035): zone signs records (RRSIG), delegation signed by DS records, root signed → chain of trust; resolvers validate signatures. KSK/ZSK key split; algorithms (RSASHA256, ECDSAP256SHA256, Ed25519).
- **DoH/DoT** (RFC 8484/7858): encrypt the client→resolver leg over HTTPS 443 / TLS 853.
- **Anycast**: the same DNS server IP served from many locations; routing picks the nearest.
- **Round-robin / weighted RR**: multiple A records returned (and rotated) for load distribution.
- **GeoDNS / ECS**: authoritative answers differ by resolver location / client subnet.
- **Split-horizon**: different answers for internal vs external resolvers.
- **Health-check DNS**: authoritative server removes failed IPs (Route53 failover, Cloudflare).

## 3. When Is It Used?
- **A/AAAA**: normal web/API resolution.
- **CNAME**: aliasing `www` → apex, CDN vendor mapping (`cdn.example.com` → `vendor.cloudfront.net`), domain verification.
- **MX**: email routing (every mail server must be discoverable via MX).
- **TXT/SPF/DKIM/DMARC**: anti-spam authentication — mail servers verify senders.
- **SRV**: service discovery (SIP, XMPP, LDAP, Kubernetes sometimes), zero-config protocols.
- **PTR**: reverse DNS — mail anti-spam (verify PTR matches), logging, security investigations.
- **CAA**: certificate issuance restriction (defense against rogue CA issuance).
- **DNSSEC**: signed zones for gov, banking, high-value domains; validation by resolvers (8.8.8.8, 1.1.1.1).
- **DoH/DoT**: browsers (Chrome/Firefox), OS (Android), privacy-focused users; corporate policy.
- **Anycast/GeoDNS/round-robin**: all CDNs (Cloudflare, Akamai), global DNS providers, load balancing at the DNS layer.

## 4. Why Wasn't Another Approach Chosen?
- **Why typed records instead of one "address" string?** Applications need structured, typed metadata (mail vs web vs service discovery); typed RRs let DNS act as a *generic directory*, not just a phone book. Alternatives (LDAP, custom config files) were heavier and not universally deployed.
- **Why CNAME instead of "duplicate the A record"?** CNAME = single source of truth; when the target IP changes, only the canonical record changes. Duplication would break. But CNAME has limits (can't coexist with other records at a name, can't alias the apex per DNS rules — solved by "ANAME/ALIAS" extensions).
- **Why DNSSEC vs "just use TLS"?** TLS protects *data* but DNS runs *before* TLS — you need signed answers to prevent hijacking/poisoning at the lookup stage. Alternatives (DNS curve cryptography, DNSCurve) never deployed; DNSSEC won by committee + adoption.
- **Why DoH over HTTPS instead of DoT?** DoT (853) is distinguishable (firewalls can block it); DoH rides standard HTTPS (443) — it looks like normal web traffic, better for privacy from censors, harder for middleboxes. DoT is simpler/cheaper; the industry now ships both.
- **Why anycast for DNS?** Unicast to one server = latency + DDoS target. Anycast = nearest instance + attack absorption (traffic spreads). For a protocol that must be available at all times, anycast is the availability design.
- **Why DNS-based load balancing vs L4/L7 LBs?** DNS is the *first* opportunity to steer: clients get a region-appropriate IP *before* connecting (no extra hop, no LB bottleneck). Downsides (no session stickiness, TTL-cached) are accepted because it's cheap and scalable; it complements, not replaces, real LBs.

## 5. Intuition
The DNS **record types** are like **different departments in a company directory**: A = "phone number," AAAA = "newer phone number," MX = "which courier takes this company's mail," TXT = "sticky notes with proof/instructions," SRV = "which desk handles service X," SOA = "the directory's own update metadata," PTR = "reverse directory (look up name from number)." **Advanced DNS** is the directory going high-tech: DNSSEC = the entries are *signed* so nobody can forge them; DoH = the lookup itself is done in a *private booth*; anycast = the directory is *replicated on every corner* so you always find one nearby; GeoDNS = it gives you the *branch office nearest to you*.

## 6. Real-World Analogy
**The corporate directory + security + facilities**: The directory (DNS) lists: employee phone (A), extension (AAAA), who handles mail (MX), a signed memo proving an announcement is genuine (DNSSEC signature), and notes for couriers (TXT/SPF). The company replicates its directory at every office (anycast) so you always get the local one fast. When you call, the switchboard checks you're actually talking to the real office by verifying the memo's signature (DNSSEC validation) and conducts the query in a private room (DoH) so competitors can't see who you're calling. And if you're calling from Mumbai, the receptionist gives you the Mumbai branch's number (GeoDNS) rather than New York's.

## 7. Formal Definition
**Resource records** (RRs, RFC 1035) are the unit of DNS data: `owner, TTL, class (IN), type, rdata`. Types: A (IPv4), AAAA (IPv6), CNAME (alias), MX (mail exchange, priority), NS (delegation), TXT (free text), SRV (RFC 2782, `_service._proto.name` → target/port/priority/weight), SOA (zone authority: serial, refresh, retry, expire, minimum), PTR (reverse), CAA (RFC 8659), DNAME. **DNSSEC** (RFC 4033-4035) adds RRSIG/DNSKEY/DS/NSEC/NSEC3 records and resolver-side signature validation over a chain of trust from the root. **DoH** (RFC 8484) and **DoT** (RFC 7858) encrypt the resolution query. **Anycast** presents a single IP served from multiple sites; **GeoDNS/ECS** (RFC 7871) vary answers by location.

## 8. Example
A full zone file with records + the DNSSEC extras:
```
$ORIGIN example.com.
$TTL 300
@            IN SOA  ns1.example.com. hostmaster.example.com. (
                      2026080101 ; serial
                      7200       ; refresh
                      3600       ; retry
                      1209600    ; expire
                      300        ; negative TTL (min)
                    )
@            IN NS   ns1.example.com.
@            IN NS   ns2.example.com.
@            IN MX   10 mail.example.com.
@            IN TXT  "v=spf1 ip4:203.0.113.10 -all"
@            IN A    93.184.216.34
@            IN AAAA 2606:2800:220:1::1
www          IN CNAME example.com.
mail         IN A    203.0.113.10
_sip._tcp    IN SRV  10 60 5060 sip.example.com.
@            IN CAA  0 issue "letsencrypt.org"
; --- DNSSEC ---
@            IN DNSKEY 257 3 8 <public key>       ; KSK
@            IN RRSIG  A example.com. ...          ; signature over A set
```

## 9. Internal Working
1. **A/AAAA selection**: resolvers/browsers prefer AAAA if the network has IPv6 (Happy Eyeballs RFC 6555 races A/AAAA). Records can be multiple (round-robin).
2. **CNAME semantics**: a CNAME *replaces* other records at that name; the resolver follows it (may chain). Modern resolvers resolve the chain and return the final IP (CNAME flattening). Root/apex CNAME is disallowed by the DNS spec (fixed via ANAME at providers).
3. **MX**: the resolver looks up MX (priority, lower = better); equal-priority = load balance; then A for the chosen mail server. Mail never uses the domain's A for delivery — MX is authoritative for mail.
4. **TXT/SPF**: sender's domain publishes SPF (`v=spf1 ...`); receivers query TXT, evaluate `ip4/include/-all`, and combine with DKIM (signs mail with a key published in TXT `_domainkey`) and DMARC (`_dmarc.example.com TXT "v=DMARC1; p=reject; rua=..."`).
5. **SRV**: clients query `_service._proto.domain`, choose by priority then weight → target:port. Zero-config discovery (Avahi/mDNS in the LAN uses a similar model).
6. **PTR/reverse**: the IP is reversed into `.in-addr.arpa` (IPv4) / `.ip6.arpa` (IPv6) — owned by the *IP provider*, not the domain owner. Used for anti-spam, security, diagnostics.
7. **DNSSEC validation chain**: root KSK (trust anchor) → signs root ZSK → signs TLD keys (DS) → TLD signs domain DS → domain signs its RRSIGs. Resolver validates RRSIG→DNSKEY→DS→...→root. A broken signature → `SERVFAIL` (resolver refuses the answer — validated failure, not absence).
8. **DoH flow**: browser → HTTPS POST/GET to `https://1.1.1.1/dns-query` with a DNS wire-format message — the resolution itself is unchanged, only the transport to the resolver is encrypted. DoT: TLS to port 853.
9. **Anycast mechanics**: the same IP (e.g., 1.1.1.1) is advertised from hundreds of sites via BGP; the network routes you to the nearest; a site's failure withdraws the route and traffic flows elsewhere. Combined with **unbound/resolver anycast** for public DNS.
10. **Round-robin**: authoritative server rotates multiple A records in answers (and EDNS0-aware rotation). Caveat: not per-request-sticky, TTL-cached by resolvers — coarse-grained LB, great for stateless.

## 10. Time Complexity
- **Record lookup**: A/AAAA/NS etc. = O(1) cache hit; DNSSEC adds O(signature verify) ≈ 50-200 µs per validation chain.
- **DoH/DoT**: +1 RTT to resolver over HTTPS/TLS (handshake) but reuses HTTP connection pools/browser caches; typically still sub-ms-50ms.
- **Round-robin/GeoDNS**: O(1) — just a different answer selected; no extra lookups (ECS adds the client-subnet prefix to the query).
- **DNSSEC zone size**: +~30-50% RRs (RRSIG/NSEC) and larger responses → more TCP fallbacks; validation CPU is negligible at resolver scale.
- **Anycast**: O(1) routing decision (BGP) — the latency win is *geographic*: nearest instance ≈ tens of ms saved.

## 11. Advantages
- **Rich directory**: typed records serve web, mail, discovery, security, anti-spam, and cert policy from one system.
- **DNSSEC**: end-to-end integrity of answers; cache-poisoning becomes detectable/ineffective; validated SERVFAIL on tampering.
- **DoH/DoT**: privacy from on-path observers; DoH evades censorship/blocking; integrates with existing HTTPS infra.
- **Anycast**: availability, latency, DDoS absorption for a must-always-work service.
- **DNS routing (RR/GeoDNS/ECS)**: cheap, scalable, region-aware steering before any connection; complements L4/L7 balancing.
- **Split-horizon**: same names, safe internal/private answers, no public leakage of internal topology.

## 12. Disadvantages
- **DNSSEC**: deployment complexity (key rotation, KSK/ZSK, NSEC walking), larger zones/answers (TCP fallbacks), old resolvers/libraries without validation, TTL propagation of key changes.
- **DoH**: centralizes DNS at browser vendors (privacy paradox), breaks enterprise filtering/visibility, complicates local network DNS (must be explicit), can't see the query's client behind shared IPs (mitigate with ECS).
- **Record limitations**: CNAME can't coexist/apex (ANAME is nonstandard), TTL-cached LB is coarse and sticky-problems, SRV/NAPTR support is patchy in clients.
- **Anycast**: needs BGP and multiple sites — only feasible at provider scale; a misconfigured route affects everyone (route-leak risk).

## 13. Interview Questions
1. **Q: What is the difference between A and AAAA?** A: A = IPv4 address record; AAAA = IPv6 (quad-A) address record. Both map a name to an IP; clients prefer AAAA when IPv6 is available (Happy Eyeballs).
2. **Q: What is a CNAME and when is it used?** A: An alias pointing one name to another canonical name (e.g., `www.example.com → example.com`). Used for CDN mapping, subdomain aliasing, and keeping one source of truth. Rule: a CNAME cannot coexist with other records at the same name, and the apex can't be a CNAME (spec).
3. **Q (tricky): Why can't the apex (example.com) be a CNAME?** A: Because the apex already has SOA/NS records (and usually MX) — the DNS spec says a CNAME must be the *only* record at its name. Providers solve this with "ALIAS/ANAME" records that resolve the CNAME *at the authoritative server* and return A/AAAA.
4. **Q: How does MX work and why is priority important?** A: MX declares the mail server(s) with priority (lower = preferred); if equal, the resolver/ mailer load-balances; fallback to the next priority on failure. Mail delivery follows MX, never the domain's A record.
5. **Q: What are SPF, DKIM, and DMARC?** A: SPF (TXT) = which IPs may send for the domain. DKIM = mail signed with a key published in TXT (`_domainkey`). DMARC = policy (`_dmarc`) telling receivers how to treat failing mail (quarantine/reject) + reporting. All TXT-based — DNS is email's authentication backbone.
6. **Q (production): What is a PTR record and when does it matter?** A: Reverse DNS (IP→name via `.in-addr.arpa`). Matters for: mail anti-spam (many MTAs reject mail from IPs without matching PTR), logging/forensics, and security tooling. Owned by the *IP provider*, not the domain owner.
7. **Q: What is DNSSEC and how does it work?** A: Cryptographic signatures on DNS records (RRSIG), keys published in DNSKEY, delegation secured via DS records, validation up a chain of trust from the root. Resolvers verify signatures; tampered answers → SERVFAIL. Prevents cache poisoning/hijacking.
8. **Q: What's the difference between DNSSEC and DoH/DoT?** A: DNSSEC = *integrity* (signs the answers so they can't be forged). DoH/DoT = *confidentiality* (encrypts the query between client and resolver). They're complementary: DNSSEC protects the data, DoH protects the conversation. Use both.
9. **Q (scenario): An engineer says "our DNSSEC broke; users can't resolve." What happened?** A: Typical: key rotation without updating DS at the parent, clock skew (signature validity), or a record added but not re-signed → RRSIG mismatch → validating resolvers return SERVFAIL. Diagnostics: `delv`/`dig +dnssec`, check DS at parent, verify timestamps.
10. **Q: What is anycast and why use it for DNS?** A: The same IP advertised from many sites via BGP; packets route to the nearest instance. For DNS: low latency, DDoS resilience (attack absorbed across sites), and automatic failover (route withdrawal). The 1.1.1.1/8.8.8.8 model.
11. **Q: How does GeoDNS / EDNS Client Subnet work?** A: The authoritative server varies the answer based on the *resolver's* IP or the client subnet (ECS, RFC 7871) sent by the resolver. Users near Mumbai get Mumbai edge IPs; near NYC get NYC IPs — "resolution as routing."
12. **Q: What is DNS round-robin and its limitations?** A: The authoritative server returns multiple A records, rotating order — clients pick the first. Cheap load distribution but: clients may pin one record (browser keep-alive), TTL caches the set, no health awareness (a dead IP stays in the set unless health checks remove it), and no session stickiness.
13. **Q (production): Route53 vs Cloudflare DNS — how do they differ for failover?** A: Both do health-check-based DNS failover (removing unhealthy IPs from answers). Route53: latency/routing policies + failover records. Cloudflare: proxied DNS (their LB/CDN in front) vs DNS-only. Both also offer DNSSEC. Choose by ecosystem + features (proxied vs authoritative-only).
14. **Q: What is split-horizon DNS?** A: The same name resolves differently for internal vs external resolvers (e.g., `internal.example.com` → 10.x internally, public IP externally). Used to expose private services without leaking topology; configured at the resolver/zone level.
15. **Q: What are CAA records?** A: Certificate Authority Authorization — `CAA 0 issue "letsencrypt.org"` tells CAs only Let's Encrypt may issue certs for this domain. Defense against mis-issuance; browsers/some CAs enforce it.
16. **Q (tricky): Why does DNS use "round-robin" but it doesn't work for sticky sessions?** A: Because DNS answers are cached by resolvers and clients pick the *first* record they see (order + caching breaks rotation over time); sessions need server affinity that DNS can't express. So DNS LB is for stateless/durable workloads; real session affinity needs L4/L7 LB.
17. **Q: What is the `.in-addr.arpa` space and who controls it?** A: The IPv4 reverse-lookup zone — `x.y.z.w.in-addr.arpa` for IP w.z.y.x. Owned by the IP address *allocation* holder (ARIN/RIPE/APNIC → ISP → customer). You need delegation from your IP provider to manage PTRs.
18. **Q: What's the difference between a hard failover (health-check DNS) and TTL-based?** A: Health-check: the authoritative server actively probes origins and *stops answering with* dead IPs (fast, no client change needed). TTL-based: clients just wait for expiry and re-resolve. Production (Route53/Cloudflare) combines both: short TTL + active health checks.

## 14. Follow-Up Questions
1. **Q: How does DNSSEC key management (KSK/ZSK) work?** A: ZSKs sign the zone's records (rotated often, cheap); KSKs sign the DNSKEY set (rotated rarely, must be published as DS at the parent). Separation = fast zone re-signing without parent coordination. KSK rollover is the risky operation (DS at parent + propagation).
2. **Q: What is NSEC walking and how does NSEC3 fix it?** A: NSEC proves "name doesn't exist" by listing adjacent names — but attackers can enumerate the whole zone by walking NSEC. NSEC3 hashes names, making enumeration impractical (at cost of more CPU).
3. **Q: Why do browsers push DoH even though enterprise admins hate it?** A: Privacy + integrity (ISP/on-path tampering). Enterprises dislike it because it bypasses their filtering/monitoring. The tension: privacy vs. centralized control — browsers provide policy (enterprise-managed DoH) as the compromise.
4. **Q: How does DNS fit into the "what happens when you type a URL" answer?** A: It's step 1 (after cache checks): browser → OS stub → recursive resolver → (root → TLD → authoritative) → IP → then TCP/TLS/HTTP. A complete answer includes HSTS preload, DoH if configured, and the caching layers.
5. **Q: What is DNS rebinding and how do you mitigate it?** A: An attacker's domain resolves to an attacker server first (passes same-origin checks) then re-resolves to a private IP (10.0.0.1), letting the browser's JS probe internal services. Mitigations: DNS rebinding protection in resolvers/browsers, validate Host headers, pin IPs at the app.

## 15. Coding Example
```python
import dns.resolver   # dnspython — query real record types

def query(name, rtype):
    try:
        ans = dns.resolver.resolve(name, rtype)
        return [str(r) for r in ans]
    except dns.resolver.NoAnswer:
        return "no answer"
    except dns.resolver.NXDOMAIN:
        return "NXDOMAIN"

print("A  example.com:",    query("example.com", "A"))
print("MX example.com:",    query("example.com", "MX"))    # mail routing
print("TXT example.com:",   query("example.com", "TXT"))   # SPF etc.
print("NS example.com:",    query("example.com", "NS"))
print("AAAA google.com:",   query("google.com", "AAAA"))
# A  example.com:  ['93.184.216.34']
# MX example.com:  ['10 mail.example.com.']   -> priority 10
# TXT example.com: ['"v=spf1 -all"']          -> anti-spam policy
```
```bash
# DNSSEC / DoH / advanced queries from the CLI
$ dig +dnssec example.com A                 # show RRSIG alongside the answer
$ dig +dnssec @8.8.8.8 example.com A        # ask a validating resolver (see flags: ad)
$ dig TXT _dmarc.example.com                # DMARC policy
$ dig SRV _sip._tcp.example.com             # service discovery
$ dig -x 93.184.216.34                      # reverse (PTR) lookup
$ curl -H "accept: application/dns-json" "https://cloudflare-dns.com/dns-query?name=example.com&type=A"   # DoH
```

## 16. Industry Usage
- **Cloudflare**: free DNS with DNSSEC, anycast (1.1.1.1), DoH/DoT, and proxied DNS (CDN/LB) — the reference production DNS stack; serves a huge fraction of the web's zones.
- **AWS Route53**: authoritative DNS with alias records (to AWS resources), health-check failover, latency/routing policies, DNSSEC, and Resolver for hybrid networks. Used at massive scale in AWS architectures.
- **Google Public DNS (8.8.8.8)**: validating resolver with DoH/DoT, ECS; powers Chrome's default DoH in some regions.
- **Verisign/ICANN**: operate `.com`/`.net` registries and the root zone with DNSSEC (root KSK) — the trust anchors everything validates against.
- **Enterprises**: split-horizon DNS + Infoblox/Bind for internal resolution; DNS is the control plane for internal service discovery and security (EDR queries domain reputation via DNS).

## 17. References
- RFC 1034/1035 — RRs and zone format.
- RFC 2782 — SRV records; RFC 8659 — CAA; RFC 7871 — EDNS Client Subnet.
- RFC 4033/4034/4035 — DNSSEC; RFC 6840 — DNSSEC clarifications.
- RFC 8484 — DoH; RFC 7858 — DoT; RFC 6891 — EDNS0.
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 2.4 (DNS + DNSSEC).
- O'Reilly, *DNS and BIND* (Albitz & Liu).

## 18. Cheat Sheet
- A=IPv4, AAAA=IPv6, CNAME=alias, MX=mail+priority, NS=delegation, TXT=text (SPF/DKIM), SRV=service+port, SOA=zone metadata, PTR=reverse, CAA=cert issuers.
- CNAME: sole record at a name; apex uses ANAME/ALIAS.
- MX priority: lower first; equal → balance.
- DNSSEC = RRSIG/DNSKEY/DS + chain of trust; broken sig → SERVFAIL.
- DoH (443) vs DoT (853) = encrypted client→resolver.
- Anycast = same IP, many sites, nearest wins; DDoS absorb.
- GeoDNS/ECS = location-based answers (CDN routing).
- Round-robin = multiple A records; coarse, non-sticky.
- Split-horizon = internal vs external answers.
- Happy Eyeballs races A/AAAA.

## 19. Quiz
1. Which record maps a name to IPv6? a) A b) AAAA c) CNAME d) PTR → **b**
2. CNAME rules: a) can coexist b) must be the only record, not at apex c) apex ok d) no target → **b**
3. Mail delivery uses: a) A b) MX c) CNAME d) TXT → **b**
4. DNSSEC guarantees: a) privacy b) integrity c) speed d) anonymity → **b**
5. DoH runs over port: a) 53 b) 853 c) 443 d) 25 → **c**
6. DoT runs over port: a) 53 b) 853 c) 443 d) 22 → **b**
7. PTR records live in: a) example.com b) .in-addr.arpa c) root d) MX → **b**
8. Anycast gives DNS: a) nearest instance b) single point c) slower d) more records → **a**
9. ECS tells the authoritative server: a) full query b) client subnet c) DNSSEC keys d) mail priority → **b**
10. NSEC enumeration is fixed by: a) NSEC3 b) DoH c) CNAME d) SOA → **a**

## 20. Flashcards
- **Q: Record type → purpose?** → **A:** A=IPv4, AAAA=IPv6, CNAME=alias, MX=mail, NS=delegation, TXT=text, SRV=service, SOA=metadata, PTR=reverse, CAA=certs.
- **Q: DNSSEC vs DoH?** → **A:** DNSSEC = integrity (signatures); DoH = privacy (encrypted transport).
- **Q: What port for DoH/DoT?** → **A:** 443 / 853.
- **Q: How does DNSSEC fail closed?** → **A:** Broken signature → SERVFAIL.
- **Q: Anycast purpose?** → **A:** Nearest instance + DDoS absorption for must-be-available services.
- **Q: GeoDNS?** → **A:** Different answers by resolver/client location.
- **Q: Why can't apex be CNAME?** → **A:** Apex has SOA/NS; CNAME must be sole record.

## 21. Revision
Records: A/AAAA (addresses), CNAME (alias; sole at name, not apex), MX (mail, priority), NS (delegation), TXT (SPF/DKIM/DMARC), SRV (service:port), SOA (zone metadata + serial), PTR (reverse), CAA (cert policy). Advanced: DNSSEC signs answers (RRSIG/DNSKEY/DS chain; SERVFAIL on tamper) = integrity; DoH/DoT encrypt client→resolver (443/853) = privacy; anycast gives nearest + DDoS-resilient instances; GeoDNS/ECS route by location; round-robin = coarse LB (non-sticky); split-horizon = different answers internally. DNS is both a directory and a routing/security control plane.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Explain the record types." | 2 How It Works / 8 Example |
| "What is DNSSEC and how does it work?" | 13 Q&A / 9 Internal Working |
| "DNSSEC vs DoH/DoT?" | 13 Q&A / 4 Why Another Approach |
| "How does a CDN route via DNS?" | 13 Q&A / 16 Industry Usage |
| "CNAME at the apex problem?" | 13 Q&A / 14 Follow-Up |
| "How do SPF/DKIM/DMARC use DNS?" | 13 Q&A / 9 Internal Working |
| "Reverse DNS / PTR?" | 13 Q&A / 9 Internal Working |
| "What is anycast for DNS?" | 13 Q&A / 10 Time Complexity |
