# DNS Hierarchy and Name Spaces

> **TL;DR**: DNS is a globally distributed, hierarchical database that maps domain names to records (IPs, mail servers, etc.), organized as a tree — root `.` → TLDs (`.com`) → authoritative zones (`example.com`) — because a single global phone book couldn't scale, survive, or be owned by anyone.

## 1. Why Does This Exist?
Two problems: (1) humans can't memorize IPv4/IPv6 addresses, so we need **names**; (2) the mapping name→data must be *queryable at planetary scale, always*. A single centralized "phone book" server would fail (single point of failure), not scale (billions of queries), and raise control issues (who owns it?). DNS solves this with a **distributed, delegated, hierarchical database**: no one owns it all, no one server holds it all, failures are contained, and the load is spread across millions of servers. The hierarchy exists to make *delegation* possible — each level of the tree controls only its subtree.

## 2. How Does It Work?
The namespace is a tree (RFC 1034/1035):
- **Root (`.`)**: 13 root server identities (a.root-servers.net … m.root-servers.net), operated by 12 organizations, served via **anycast** (hundreds of physical instances). Roots know *nothing* except where TLD servers are.
- **Top-Level Domains (TLDs)**: generic (`.com`, `.org`, `.net`, `.io`, `.dev`) + country-code (`.in`, `.uk`, `.jp`) + new gTLDs (`.app`, `.xyz`). Each TLD has authoritative servers that know where the *second-level* domains are.
- **Second-level / subdomains**: `example.com`, `www.example.com` — this is where *your* zone lives. The zone's **authoritative nameservers** hold the actual records (A, AAAA, MX, …).
- **Zones**: a contiguous subtree with authority delegated to a set of nameservers. `example.com` zone = `example.com` + all subdomains unless *further delegated* (e.g., `api.example.com` could be a separate zone/nameserver).
- **Names**: FQDN (fully-qualified domain name) = `host.subdomain.tld.` with trailing dot; DNS labels are case-insensitive, ≤63 chars, FQDN ≤255 chars.

Delegation = "I (parent) tell you (resolver) who is *authoritative* for this child zone" — done via **NS records** + **glue records** (A records for the child's nameservers when they're inside the delegated zone).

## 3. When Is It Used?
- **Every name lookup on the Internet** (web, email MX routing, API endpoints).
- **Zone management**: companies delegate subdomains (`mail.example.com`, `cdn.example.com`) to different providers/teams.
- **DNSSEC**: signed zones for integrity.
- **Split-horizon**: internal `internal.example.com` vs public — internal resolver serves private IPs.
- **Dynamic DNS**: IoT/home devices register changing IPs.

## 4. Why Wasn't Another Approach Chosen?
- **Single global server**: rejected — SPOF, no scale, single trust/control point. The ARPANET's original `HOSTS.TXT` (one file, FTP-issued) broke at ~1000 hosts.
- **Flat files / broadcast lookups**: N² update traffic, no hierarchy, doesn't scale. The hosts-file model is still used only for local overrides (`/etc/hosts`).
- **Centralized registry + CDN-like caching**: was considered; but *delegation* (each zone owner controls its data) is what lets a billion zone owners update their own records without a central authority — the web's "self-service" model. Hierarchy is the chosen answer to ownership + scale.
- **Alternative naming systems (X.500, LDAP)**: heavier, directory-oriented, never gained deployment; DNS's simplicity won.

## 5. Intuition
The DNS tree is a **phone directory organized like a file system**: root `/` → directories (`com`, `org`) → files (`example.com`) → details (A record = phone number). You don't need to know *where* the answer lives — the resolver starts at the root (who knows where the TLDs are), the TLD tells it who owns `example.com`, and the owner's server gives the answer. It's like dialing through a chain of directory-assistance operators, each pointing to the next, until one actually knows your friend's number.

## 6. Real-World Analogy
**The corporate phone system with departments**: You call the main switchboard (root) — it only knows department extensions (TLDs). The operator transfers you to "Sales" (`.com`), whose directory knows "Tech Company Inc." (example.com). Tech Company's own receptionist (authoritative nameserver) tells you Bob's direct line (the A record). Everyone only needs to know *their own level's* directory; no single person knows every number on Earth. Delegation = "Tech Company manages its own directory" — they update Bob's new number themselves, and nobody else needs to know.

## 7. Formal Definition
DNS (RFC 1034/1035) is a hierarchical, distributed, delegated naming system for resources on IP networks. The namespace is a **labeled tree** where each node has a domain name (sequence of labels ending in the root `.`). The name space is partitioned into **zones**, each administered by one or more **authoritative nameservers** (NS records), which hold resource records (RRs) for names in that zone. Parent zones delegate authority to child zones via NS records (with glue A/AAAA records when necessary). The **root zone** contains the 13 root server identities; each TLD zone delegates to second-level and lower zones. A fully-qualified domain name (FQDN) is the concatenation of labels from a node up to the root, dot-separated.

## 8. Example
The zone delegation chain for `api.example.co.in`:
```
.                     root      -> knows .co.in servers (via NS)
.co.in                TLD       -> knows example.co.in servers (NS + glue A)
example.co.in         zone      -> holds records: api.example.co.in A 93.184.216.34
api.example.co.in     record    -> A 93.184.216.34 (an address record, not a zone)
```
Hierarchy of authority, bottom-up: root → `.co.in` → `example.co.in` → `api.example.co.in`. The resolver starts at the root (or a cached TLD pointer), walks down the tree, and stops at the *most authoritative* server for the queried name. Number of levels = depth of delegation: root (1) → TLD (2) → domain (3) → subdomain (4).

## 9. Internal Working
1. **Zone file structure**: an authoritative server serves a **zone file**: `$ORIGIN`, `$TTL`, then RRs (owner name, TTL, class IN, type, value). Example:
```
$ORIGIN example.com.
$TTL 3600
example.com.  IN  NS     ns1.example.com.
example.com.  IN  NS     ns2.provider.net.
ns1.example.com.  IN  A  192.0.2.10
www            IN  A     93.184.216.34
mail           IN  MX 10 mail.example.com.
```
2. **Delegation mechanics**: `example.com` NS records tell resolvers "ask ns1.example.com for this zone." If ns1 is *inside* the zone, the parent must also provide **glue records** (the A address of ns1) so the resolver can reach the delegated server (chicken-and-egg avoided).
3. **Root servers**: 13 lettered identities (`a`-`m`), run by Verisign, ICANN, etc., on **anycast** — a query to `a.root-servers.net` lands on the nearest physical instance (hundreds worldwide). Roots answer only referrals to TLDs.
4. **TLD registries** (e.g., Verisign for `.com`, ICANN for new gTLDs): authoritative for the TLD zone; they record which nameservers each domain points to (the "registrar" step creates domain→NS records).
5. **Authoritative servers**: own the zone's records; answer authoritatively (AA bit set). Must be redundant (≥2, geographically diverse) per RFC 2182.
6. **Zone transfer (AXFR/IXFR)**: secondary servers pull the zone from the primary (SOA serial comparison) — how a zone stays replicated across multiple authoritative nameservers.

## 10. Time Complexity
- **Namespace lookup**: worst case 3-5 levels of delegation (root → TLD → domain [→ subdomain]) — *constant* depth in practice; each level = one RTT if uncached.
- **Cache effectiveness**: the hierarchy's depth is exactly why caching matters — repeated lookups hit the recursive resolver's cache in O(1), and popular domains resolve with 0 upstream queries.
- **Scale**: ~13 root identities + thousands of TLD servers + millions of authoritative servers — the load is spread by delegation (no O(N) central table). Query volume: trillions/day worldwide, each ~O(1) hops.

## 11. Advantages
- **Distributed & fault-tolerant**: no single point of failure; root/TLD/authoritative redundancy.
- **Delegated authority**: zone owners update their own data (self-service, scalable).
- **Hierarchical & cacheable**: constant-depth lookups + heavy caching → sub-ms typical resolution.
- **Open & standardized**: RFC-driven, universal (every device uses it).
- **Extensible**: new record types (A, AAAA, MX, TXT, SRV…) and mechanisms (DNSSEC, DoH) added without breaking the tree.

## 12. Disadvantages
- **Security historically weak**: unauthenticated answers (DNS spoofing/cache poisoning) — mitigated by DNSSEC (slow adoption).
- **Privacy**: plaintext DNS exposes browsing to the resolver/ISP — mitigated by DoH/DoT/ECH.
- **Centralization risk**: a few TLD registries and the root are concentrated control points (a .com outage affects huge fraction of the web).
- **Cache staleness**: TTL trade-offs — updates can take up to the previous TTL to propagate.
- **Failure blast radius**: a misconfigured authoritative server (or expired domain) takes an entire zone down.

## 13. Interview Questions
1. **Q: What is DNS and why is it hierarchical?** A: A distributed naming system mapping names to records. Hierarchical because delegation lets each zone owner control its subtree, scales to billions of names, and contains failures (no central server).
2. **Q: What are the root servers?** A: 13 identities (a.root-servers.net … m) run by 12 organizations, served over anycast from hundreds of physical locations. They only point resolvers to the correct TLD servers.
3. **Q: What is a zone vs a domain?** A: A *domain* is any subtree of the namespace (label hierarchy). A *zone* is a contiguous portion of the domain space with a single point of authority (a set of authoritative nameservers). `example.com` is a zone; `sub.example.com` is a domain that may be delegated out of the zone.
4. **Q (tricky): Why does the parent need glue records?** A: If `example.com`'s nameservers are `ns1.example.com` (inside the zone), a resolver must reach ns1 to get the zone, but the zone tells it who ns1 is — a chicken-and-egg. Glue = the parent zone's A/AAAA record for that nameserver, letting the resolver bootstrap.
5. **Q: What is delegation in DNS?** A: The parent zone (e.g., `.com`) pointing to the child zone's authoritative nameservers via NS records. It's how authority is pushed down the tree — I control my subtree, you control yours.
6. **Q (production): Why are root servers anycasted?** A: Anycast lets the same identity be served from hundreds of sites; queries route to the nearest instance — lower latency, DDoS resilience (attack traffic spreads), and no single physical target.
7. **Q: What is a FQDN?** A: Fully-Qualified Domain Name — the complete name ending in the root dot (`www.example.com.`). Resolvers append the root dot implicitly; relative names in configs get it appended.
8. **Q: How many levels deep can a name go?** A: Labels ≤63 chars, total ≤255 chars; hierarchy is arbitrary depth (practically a handful). RFC 1034/1035 limits. Deep delegation is a design choice (e.g., `a.b.c.d.example.com`).
9. **Q (scenario): A colleague says "the DNS is down." What do you actually mean?** A: Be precise — a *specific* zone's authoritative servers down, the recursive resolver down, a TLD issue, or root reachability? 99% of "DNS down" is one zone or one resolver, not the global system (which is designed to be unbreakable).
10. **Q: What is the role of registrars and registries?** A: Registries (Verisign for .com, ICANN-managed) operate the TLD zone — they record which nameservers a domain points to. Registrars (GoDaddy, Namecheap) sell/register domains and submit NS changes to the registry. The registrant owns the name, not the zone data.
11. **Q: What does an NS record do?** A: Declares the authoritative nameservers for a zone — the delegation pointer. Resolvers use NS records to learn *who to ask* for a zone's answers.
12. **Q: Why can't one server hold all DNS data?** A: Scale (trillions of queries, billions of names), redundancy (SPOF), ownership (one party can't control everyone's names), and update latency (centralized updates would be a bottleneck). Delegation distributes all four.
13. **Q (production): How does DNS survive a TLD outage?** A: Resolvers cache TLD NS referrals (usually 48h TTL for root/TLD hints); traffic mostly continues from cache. Authoritative data (A records) isn't affected — only *new* domain lookups would stall.
14. **Q: What is a "hint" file in a resolver?** A: The bootstrap list of root-server addresses shipped with resolvers (e.g., `named.root`, `root.hints`) — the resolver's starting point when its cache is empty. Without hints, it can't find TLDs.
15. **Q: What's the difference between authoritative and recursive servers?** A: Authoritative = owns the zone's records, answers with AA bit, never asks others. Recursive (resolver) = asks on behalf of clients, walks the tree, caches. A server can be both for different zones (split-brain setups).
16. **Q (tricky): Can a zone be delegated to a nameserver outside its domain?** A: Yes — glue is only *required* when the nameserver is inside the delegated zone. Outside nameservers (e.g., `ns1.provider.net`) need no glue (their A record is in another zone), only NS records.
17. **Q: What is the root zone and who manages it?** A: The top of the tree (the `.` zone). Managed by ICANN (IANA) in cooperation with Verisign (operator); it contains NS records for all TLDs. Its integrity matters so much that DNSSEC (root KSK) was the first thing signed.

## 14. Follow-Up Questions
1. **Q: What is a "stub resolver"?** A: The minimal client-side resolver in your OS (libc `getaddrinfo`) — it knows the recursive resolver's IP (from DHCP) and does *recursive* queries on your behalf; it caches little/nothing. Distinguish from *full/recursive* resolvers (8.8.8.8).
2. **Q: How does DNS handle name collisions in private space?** A: Split-horizon / split-DNS: the *same* name resolves to different addresses depending on who asks (internal vs external resolver). This is zone+resolver cooperation, not a hierarchy change.
3. **Q: What's the role of SOA records in zone replication?** A: The SOA record carries the serial number, refresh/retry/expire timers; secondary nameservers use it to detect zone changes (AXFR/IXFR triggers). It's the zone's "metadata + replication clock."
4. **Q: Why are there exactly "13" root servers?** A: Legacy: the original DNS UDP packet responses were limited to 512 bytes, fitting 13 server identities. Modern roots use anycast (many machines per identity), so the number is symbolic — scalability is via anycast, not more identities.
5. **Q: What is IDNA (internationalized domain names)?** A: Unicode domain names encoded as punycode labels (e.g., `xn--...`) so non-ASCII names fit the ASCII label rules. The hierarchy is unchanged — the *labels* are just encoded.

## 15. Coding Example
```python
# Build a miniature DNS tree to make the hierarchy tangible
class DNSNode:
    def __init__(self, label):
        self.label = label
        self.children = {}          # label -> DNSNode
        self.records = {}           # record type -> value (leaf)
        self.authoritative = False  # zone authority marker

    def insert(self, fqdn, rtype, value):
        labels = fqdn.rstrip(".").split(".")[::-1]   # ["com","example","www"]
        node = self
        for lab in labels:
            node = node.children.setdefault(lab, DNSNode(lab))
        node.records[rtype] = value
        node.authoritative = True

    def lookup(self, fqdn):
        node = self
        for lab in fqdn.rstrip(".").split(".")[::-1]:
            if lab not in node.children:
                return None
            node = node.children[lab]
        return node.records

root = DNSNode(".")                                  # the root zone
root.insert("com.",                "NS",  "a.gtld-servers.net.")  # delegation
root.insert("example.com.",        "NS",  "ns1.example.com.")
root.insert("www.example.com.",    "A",   "93.184.216.34")
root.insert("example.com.",        "MX",  "mail.example.com.")

print("Resolve www.example.com:", root.lookup("www.example.com."))   # {'A': '93.184.216.34'}
print("Authority for com:", root.lookup("com."))                     # {'NS': ...}
# The tree shows: root -> com -> example.com -> www, each level delegating downward.
```
```
# Real world: query each level of the hierarchy
$ dig +trace example.com            # walks root -> .com -> authoritative, showing delegation
# .                    120504 IN NS a.root-servers.net.        (root -> .com)
# com.                 172800 IN NS a.gtld-servers.net.        (.com -> example.com)
# example.com.         3600  IN NS a.iana-servers.net.         (authoritative)
# example.com.         3600  IN A  93.184.216.34               (the answer)
```

## 16. Industry Usage
- **Verisign**: operates `.com`/`.net` registries + two root servers (a, j) — a global-scale delegation example.
- **Google (8.8.8.8/8.8.4.4) & Cloudflare (1.1.1.1)**: public recursive resolvers using anycast across the globe; they serve trillions of queries with sub-ms cache hits.
- **Route53 (AWS)**: authoritative DNS as a service — `example.com` zone on Route53 nameservers; supports alias records, health-check-based failover, latency-based routing, and DNSSEC.
- **Kubernetes**: uses **CoreDNS** for cluster DNS — a hierarchical-ish in-cluster resolver mapping service names (`mysvc.ns.svc.cluster.local`) — the delegation concept applied inside a datacenter.
- **Every CDN**: authoritative DNS + anycast + GeoDNS to route users to the nearest edge PoP — the "DNS as a routing layer" pattern.

## 17. References
- RFC 1034 — Domain Names — Concepts and Facilities: https://www.rfc-editor.org/rfc/rfc1034
- RFC 1035 — Domain Names — Implementation and Specification: https://www.rfc-editor.org/rfc/rfc1035
- RFC 2182 — Selection and Operation of Secondary DNS Servers.
- RFC 4033/4034/4035 — DNSSEC; RFC 8484 — DoH; RFC 7858 — DoT.
- IANA root zone file — https://www.iana.org/domains/root/files
- Kurose & Ross, *Computer Networking*, 8th ed., Ch. 2.4 (DNS).
- O'Reilly "DNS and BIND" (Albitz & Liu) — the classic reference.

## 18. Cheat Sheet
- DNS = distributed, hierarchical, delegated database (RFC 1034/1035).
- Tree: root `.` → TLD → second-level → subdomains; zones = contiguous authority.
- 13 root identities, anycasted; root only knows TLDs.
- Delegation = NS records (+ glue for in-zone nameservers).
- FQDN ends in `.`; labels ≤63, total ≤255.
- Authoritative = owns zone (AA bit); recursive = walks tree + caches.
- Registries run TLDs; registrars sell names; you own the zone.
- SOA = zone metadata + replication serial.
- Glue records = bootstrap A records from the parent.
- Hint file = resolver's root bootstrap.

## 19. Quiz
1. The root zone knows: a) all A records b) TLD nameservers c) every domain d) MX records → **b**
2. Glue records are needed when: a) nameserver is outside zone b) nameserver is inside the delegated zone c) DNSSEC d) always → **b**
3. A zone is: a) a domain b) a contiguous subtree with one authority c) a record type d) a resolver → **b**
4. FQDN maximum length: a) 63 b) 255 c) 512 d) 1024 → **b**
5. How many root identities? a) 4 b) 13 c) 100 d) 2 → **b**
6. Authoritative servers set the flag: a) AA b) TC c) RA d) QR → **a**
7. Which is not a role? a) root b) TLD c) resolver d) CDN record → **d**
8. NS records are: a) address records b) delegation pointers c) mail records d) text → **b**
9. Anycast makes root servers: a) slower b) nearby + DDoS-resilient c) single d) useless → **b**
10. Registrar↔registry: a) registrar runs TLD b) registry runs TLD, registrar sells c) same d) neither → **b**

## 20. Flashcards
- **Q: DNS = ?** → **A:** Distributed, hierarchical, delegated name→record database.
- **Q: Tree levels?** → **A:** root → TLD → second-level → subdomains.
- **Q: What are glue records?** → **A:** Parent A records for in-zone nameservers (bootstrap).
- **Q: Root servers?** → **A:** 13 identities, anycast, know only TLDs.
- **Q: Authoritative vs recursive?** → **A:** Authoritative owns answers (AA); recursive finds + caches.
- **Q: Zone vs domain?** → **A:** Zone = contiguous authority; domain = any subtree.
- **Q: What does SOA store?** → **A:** Zone metadata + serial for replication.
- **Q: Why 13 roots?** → **A:** Legacy 512-byte packet limit; scale is via anycast.

## 21. Revision
DNS is a distributed hierarchical tree: root (13 anycast identities) → TLDs → zones. Delegation via NS records (glue for in-zone nameservers). Zones = contiguous authority; domains = subtrees. Authoritative servers own answers (AA bit); recursive resolvers walk + cache. Registrar/registry split: registry runs TLD zone, registrar sells names. FQDN ≤255, labels ≤63. SOA = replication metadata. Root/TLD hints bootstrap resolvers. This hierarchy is why DNS scales, survives, and lets millions of zone owners self-serve.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is DNS and why hierarchical?" | 1 Why / 13 Q&A |
| "What are root servers / anycast?" | 9 Internal Working / 13 Q&A |
| "Zone vs domain / glue records?" | 7 Formal Definition / 13 Q&A |
| "Authoritative vs recursive?" | 13 Q&A / 14 Follow-Up |
| "Registrar vs registry?" | 13 Q&A / 9 Internal Working |
| "Why can't one server hold DNS?" | 4 Why Another Approach / 13 Q&A |
| "What is delegation?" | 13 Q&A / 8 Example |
