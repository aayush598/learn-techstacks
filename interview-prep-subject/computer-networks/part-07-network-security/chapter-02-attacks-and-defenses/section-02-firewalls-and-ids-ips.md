# Firewalls and IDS/IPS

> **TL;DR**: Firewalls are the network's access-control gate — evolving from packet filters (5-tuple rules) to stateful inspection (tracking connections) to next-gen/application firewalls and WAFs that understand protocols — while IDS passively detects suspicious traffic and IPS actively blocks it; together they form the enforcement and detection layers of defense in depth.

## 1. Why Does This Exist?
Not every host should accept every packet. The firewall exists to *enforce a security policy at the network boundary*: allow legitimate traffic, deny everything else, per rules (5-tuple: src/dst IP, src/dst port, protocol). It's the first automated gate between the untrusted Internet and the protected network. But filtering alone can't see *within* a connection or *inside* an application — so we add **stateful inspection** (track connection state: only reply to packets in an established connection) and **application-aware** filtering (WAF understands HTTP; NGFW understands apps via SNI/DNS). **IDS/IPS** exist because some attacks look like normal traffic: you need *detection* (IDS: passive, alert) and *prevention* (IPS: inline, drop) — pattern matching against known attack signatures plus anomaly detection. Together they operationalize "defense in depth": the firewall lets good traffic in, the IDS/IPS catches the bad that looks good.

## 2. How Does It Work?
- **Packet filter (stateless)**: examines each packet's 5-tuple against an ACL (allow/deny). Cheap but no connection awareness — a packet claiming "I'm a reply" is allowed even if no connection exists (spoofing risk).
- **Stateful firewall**: maintains a connection table (source/dest IP:port, state: NEW/ESTABLISHED/RELATED); a packet is allowed only if it belongs to an existing connection (or is a valid NEW SYN). This is what Linux `netfilter/iptables/nftables` does (`conntrack`).
- **Application/Next-Gen firewall**: inspects application-layer content — protocol validation, SNI/hostname, URL path, file types, user identity (Palo Alto/Cisco NGFW); **WAF** (Web App Firewall) inspects HTTP against OWASP patterns (SQLi/XSS signatures, bot detection).
- **IDS** (Network IDS): passive tap/SPAN port, analyzes traffic, alerts on signatures/anomalies — no inline action. **HIDS**: host-level (auditd, osquery).
- **IPS**: inline, drops/quarantines on detection — the active version. **Signature** (known attacks) + **behavioral/anomaly** (deviation from baseline) detection.
- **Deployment**: perimeter (border firewall), internal segmentation (zone firewalls), host (iptables/nftables, host-based), cloud (security groups, NACLs, WAF).

## 3. When Is It Used?
- **Every network boundary**: ISP/enterprise border, DMZ, VLAN-to-VLAN zones, cloud VPC (security groups = stateful; NACLs = stateless ACLs).
- **Host-level**: `iptables`/`nftables`/`firewalld` on Linux servers, Windows Defender Firewall — "allow only port 443/22."
- **Web**: WAF in front of every production HTTP app (Cloudflare WAF, AWS WAF, ModSecurity).
- **IDS/IPS**: enterprise network monitoring (Suricata, Snort), cloud (GuardDuty, VPC flow logs analytics), and as part of zero-trust monitoring.
- **Legacy/compliance**: PCI-DSS mandates firewalls and (often) IDS at segmentation boundaries.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: no firewall — open everything, protect each host.* Then every service on every host is exposed; one weak app = total compromise. Centralized enforcement at the boundary is cheaper and covers the "known-good" baseline. (Zero trust later *partially* inverts this — but the host/app enforcement it uses *is* a host firewall.)
- *Alternative: block all inbound, allow nothing.* Breaks the business (servers need inbound). The 5-tuple/stateful model is the minimal correct way to express "this service, on this port, for these hosts, only in this direction."
- *Alternative: static ACL only, no state.* Can't distinguish a spoofed "reply" from a real one — the classic blind spot that stateful inspection fixes by tracking the connection table.
- *Alternative: rely on IDS alone.* Detection without action requires a human to react in time (too slow for automated attacks). IPS exists because inline prevention is the only real-time response; but IPS can also cause false-positive outages — so both exist and are tuned differently.
- *Alternative: signature-only detection.* Known attacks are caught, but zero-days and evasions slip through — hence anomaly/behavioral detection (ML, baselines) added on top.

## 5. Intuition
A firewall is the **building's front desk** (access control): "stateful" means the front desk remembers who already signed in (connection table) and lets the pizza delivery in only if someone actually ordered (established connection). A packet filter is the old guard who just checks "are you on the list?" (5-tuple). The WAF is the **mail room that reads every letter** for suspicious content (application inspection). IDS is the **security camera operator** who watches everyone (passive, records, alerts); IPS is the same operator with the authority to **lock the doors** when they see someone acting suspiciously (inline, blocks).

## 6. Real-World Analogy
A **nightclub**. The bouncer (firewall) checks IDs at the door — name, photo, age (5-tuple). A *stateful* bouncer remembers who's inside: when you go to the bar, they recognize you as a guest (established connection) and let you pass without re-IDing; a random stranger claiming to be a guest gets denied. The VIP lounge has a *stricter* bouncer (zone firewall) with an explicit list (ACL). The security team watches the cameras (IDS — detect and report) and can eject rowdy patrons in real time (IPS — prevent). The WAF is the liquor control officer who refuses to serve anyone showing signs of being a known scammer (attack signature).

## 7. Formal Definition
- **Packet filter**: applies ordered ACL rules to each packet's (src IP, dst IP, protocol, src port, dst port); stateless — no connection memory.
- **Stateful firewall**: keeps a connection table via `conntrack` (Linux) / session table; states NEW (SYN), ESTABLISHED, RELATED (ICMP errors, FTP data), INVALID; default drop, allow ESTABLISHED/RELATED + explicit NEW rules.
- **Application firewall / NGFW / WAF**: deep packet inspection of L7 — protocol conformance, signatures, allow-lists (SNI, hostname, URL, user-agent); WAF = HTTP-specific (OWASP rulesets, rate limits, bot management).
- **IDS**: passive monitoring of a copy of traffic (TAP/SPAN); alerts on **signature** (known patterns) or **anomaly** (baseline deviation); **NIDS** (network) vs **HIDS** (host). **IPS**: inline, actively drops/quarantines; false positives cause availability impact.
- **Layered terminology**: perimeter / internal / host firewalls; DMZ; zones; east-west (internal) vs north-south (border) traffic.

## 8. Example
**Linux iptables/nftables stateful rule** — allow SSH and web from anywhere, drop everything else, only in established/related for replies:
```
# NEW inbound: allow 22 and 443
iptables -A INPUT -p tcp --dport 22  -m conntrack --ctstate NEW -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -m conntrack --ctstate NEW -j ACCEPT
# All existing connections may reply
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
# Everything else inbound: drop
iptables -A INPUT -j DROP
```
`conntrack` tables the connections so replies (ESTABLISHED) are allowed without being explicitly enumerated — this is the difference between stateful and a static ACL.

**WAF rule (conceptual)**: `SecRule ARGS "@contains \"' OR '"` → blocks classic SQLi patterns; `SecRule ARGS "@rx <script"` → XSS signature; plus rate limiting and geo/ASN rules. Real WAFs ship with thousands of OWASP CRS rules.

## 9. Internal Working
1. **Packet filter path**: packet → ACL chain (ordered) → first match decides (allow/deny) → default deny. Stateless = per-packet, no memory.
2. **Stateful path (Linux netfilter)**: packet → `conntrack` lookup → if in table (ESTABLISHED) → pass; if NEW (SYN) → check NEW rules; if INVALID (spoofed/no SYN) → drop; new connections get a table entry. This defeats spoofed "reply" packets.
3. **NGFW/WAF path**: L4 pass → TCP reassembly → protocol parse (HTTP/SNI/DNS) → ruleset match (signatures, geo, rate) → allow/deny/redirect (CAPTCHA, block page).
4. **IDS path**: mirror traffic (SPAN/TAP) → stream reassembly → signature match (Suricata/Snort rulesets) + anomaly scoring → alert to SIEM. Never in the data path → zero latency impact, can't block.
5. **IPS path**: inline chain → same detection → drop/reject/quarantine/reset on match; "fail-open" vs "fail-closed" mode choice (availability vs security).
6. **Evasion countermeasures**: fragmentation, IP encoding, TLS inspection/decryption at the gateway (a policy decision), and normalization before matching — modern engines reassemble first.

## 10. Time Complexity / Performance
- **Packet filter**: O(1)-O(rules) per packet; line-rate in hardware (TCAM).
- **Stateful**: O(1) hash on (src,dst,ports) into the connection table; table size = concurrent connections (millions on large firewalls).
- **NGFW/WAF**: O(payload) per session with signature engines; TLS inspection adds decrypt/re-encrypt (2-3× CPU); rate limiting per key.
- **IDS/IPS**: O(bytes) with multi-pattern matchers (Aho-Corasick); Suricata handles ~Gbps per core; 100+ Gbps with hyperscan/ASICs.
- The real budget: state tables + signature engines + TLS decrypt — measured in throughput and sessions/sec, not algorithmic Big-O.

## 11. Advantages
- **Enforcement at scale**: one policy point protects thousands of hosts; line-rate filtering.
- **Defense in depth**: firewall (deny by default) + IDS/IPS (catch the sneaky) + WAF (app attacks) layers independently.
- **Stateful awareness**: kills spoofed-reply attacks, tracks related flows (FTP data, ICMP errors).
- **Granular policy**: per zone, per service, per app, per user (NGFW) — least privilege at the network.
- **Detection value**: IDS/IPS give visibility (what attacks are hitting you) even when they don't block — the logs are threat intel.

## 12. Disadvantages
- **Stateless filter gaps**: no connection context — spoofed replies pass; port-only rules are coarse.
- **Stateful limits**: connection table exhaustion (a DDoS vector in itself); NAT/state issues with asymmetric routing.
- **App-layer blind spots**: encrypted traffic (TLS) hides payloads unless decrypted (the TLS-inspection trade-off); signature engines miss zero-days.
- **IPS false positives**: legitimate traffic dropped = availability incidents (the fail-closed dilemma).
- **Not a silver bullet**: none stop phishing, XSS on allowed endpoints, or insider abuse — they enforce policy, they don't protect the app from its own bugs (that's WAF+code).

## 13. Interview Questions
1. **Q: What's the difference between a packet filter, a stateful firewall, and an application firewall?** A: Packet filter: stateless 5-tuple ACLs. Stateful: tracks connections (conntrack) — allows replies to established connections, blocks spoofed packets. Application/NGFW/WAF: inspects L7 (HTTP, SNI, signatures) for app-aware decisions. Each layer adds awareness at the cost of performance.

2. **Q: Why is a stateful firewall better than a stateless ACL?** A: A stateless ACL allows any packet matching the rule — including a spoofed packet claiming to be a "reply." Stateful tracking remembers that a connection was initiated and only lets replies/related traffic through, defeating spoofed-response and "was it initiated?" problems.

3. **Q: How does Linux's conntrack/iptables stateful model work?** A: `iptables -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT` allows only packets matching an existing connection table entry; NEW (SYN) packets must match explicit allow rules; INVALID (no matching connection) are dropped. `conntrack` table = the session state.

4. **Q: What is the default-deny principle and why is it the firewall baseline?** A: Allow nothing unless explicitly permitted; drop everything else. Default-deny minimizes attack surface — every rule you *don't* write is an exposure you don't have. Classic ACLs are usually default-deny with explicit allows; a default-allow ACL is a checklist, not a firewall.

5. **Q: What is the difference between IDS and IPS?** A: IDS detects passively (mirrored traffic, alerts, no blocking); IPS detects inline and actively drops/blocks. IDS has zero availability impact but requires response; IPS responds instantly but risks false-positive outages.

6. **Q: How do signature-based and anomaly-based detection differ?** A: Signature: matches known attack patterns (Snort/Suricata rules) — accurate for known attacks, blind to zero-days/evasions. Anomaly: builds a baseline and flags deviation — catches novel behavior but noisy (false positives). Modern systems combine both.

7. **Q: TRICKY — Your IPS is dropping legitimate traffic. What do you do?** A: False positives are the IPS's known cost: move to fail-open or alert-only (IDS) mode for that rule, tune signatures (narrow match conditions, context), add allow-lists for known-good flows, and deploy detection in stages (alert → mitigate → block) with rollback.

8. **Q: What is a WAF and what does it protect against?** A: A Web Application Firewall inspects HTTP traffic against OWASP-style rulesets (SQLi/XSS signatures), bot detection, rate limits, geo/ASN rules, and protocol validation — placed in front of web apps. It protects against app-layer attacks that network firewalls can't see (they're "normal" HTTP).

9. **Q: SCENARIO — A web server is publicly exposed on port 443 only. Design the firewall policy.** A: Default-deny on all inbound; allow NEW TCP 443 from anywhere (to the web tier); allow 22 only from admin VPN/management IPs; allow outbound responses (ESTABLISHED,RELATED); put the web tier in a DMZ zone that can reach only the app tier (which can reach only the DB). Segmentation > a single open port.

10. **Q: PRODUCTION — What is east-west vs north-south traffic and why does segmentation matter?** A: North-south = traffic across the border (Internet ↔ DC); east-west = between internal hosts. Perimeter firewalls protect north-south; after a compromise, attackers move *laterally* (east-west), so internal zone firewalls / microsegmentation limit blast radius — the zero-trust idea (Section 05).

11. **Q: What is a DMZ and why do you need one?** A: A network zone that holds publicly-reachable services (web, email) but is isolated from the internal network; if the DMZ host is compromised, the attacker can't directly reach internal hosts — the DMZ is where the firewall's segmentation rules are enforced.

12. **Q: What is TLS inspection and what are its trade-offs?** A: The gateway decrypts, inspects, and re-encrypts TLS traffic to apply IDS/WAF signatures to encrypted content. Benefits: detection of malware-in-TLS, policy control. Costs: privacy concern, key material at the edge (a risk), 2-3× CPU, and MITM-ability (requires distributing a CA to clients).

13. **Q: TRICKY — A packet filter sees a "reply" packet but there's no connection. What should the stateful firewall do?** A: Drop it as INVALID — no SYN was seen, so it can't be a legitimate reply. This is exactly the spoofed-reply attack the stateful design eliminates; a stateless filter would have allowed it if the 5-tuple matched.

14. **Q: What are security groups vs NACLs in AWS (stateful vs stateless)?** A: Security groups are *stateful* (allow inbound X → replies auto-allowed) and evaluated per instance. NACLs are *stateless* ACLs (must allow both directions explicitly). This is a concrete production example of the stateful/stateless distinction.

15. **Q: PRODUCTION — How do you place IDS/IPS in a cloud architecture?** A: Mirrored VPC flow logs (detection — GuardDuty, VPC traffic mirroring for NIDS); inline IPS via gateway instances/NGFW-as-a-service; WAF in front of the ALB; host-based detection (auditd, osquery) on instances. Cloud shifts from "box at the border" to "log + detect everywhere."

16. **Q: What is an HIDS and how does it differ from a NIDS?** A: HIDS runs *on the host* — monitors files, processes, syscalls, logs (auditd, osquery, EDR) and catches attacks NIDS can't (encrypted payloads, local exploits, file tampering). NIDS watches the wire. Together: network visibility + endpoint truth.

17. **Q: SCENARIO — An internal host is beaconing to a known C2 domain. Which controls fire the alarm and what happens?** A: DNS/firewall logs (egress to unknown domain), NIDS signature/anomaly (beaconing pattern), HIDS/EDR (suspicious process). The IPS can block the egress domain; the response is containment (isolate host), investigate, remediate, and add the domain to the blocklist.

18. **Q: What are the pitfalls of "security by default-deny" in production?** A: Breakage of legitimate flows (misconfigured rules → outages), silent failures (dropped traffic looks like a network problem), and the temptation to add permissive rules ("just allow all of X") that erode the policy. Operationally: audit rules, use logging/deny counters, and test changes in staged environments.

## 14. Follow-Up Questions
1. **Q: What is "fail-open" vs "fail-closed" for an IPS/firewall?** A: Fail-open: on a component failure, pass traffic (availability preserved, security lost). Fail-closed: drop traffic (security preserved, availability lost). Choose per control: edge firewalls often fail-open with backup paths; IPS with high false-positive risk may fail-open to avoid outages.

2. **Q: How do you evade an IDS and how are those evasions countered?** A: Fragmentation, encoding, obfuscation, protocol tunneling, slow-loris pacing. Countered by *reassembly-then-match* (normalize first, then run signatures) and protocol decoders — which is why engines like Suricata reassemble streams before inspecting.

3. **Q: What is a honeypot and how does it relate to IDS?** A: A deliberately attractive decoy host/service that has no legitimate users — any traffic to it is by definition suspicious. It feeds the IDS/SIEM with early warning of scanning and exploits (deception as detection).

4. **Q: What is the difference between a proxy firewall and a stateful firewall?** A: A proxy terminates the connection and re-establishes it (application-level mediation — client→proxy→server, full inspection, hides topology); a stateful firewall inspects and forwards within the same connection. Proxies give deeper control (and their own TLS/caching) at higher latency.

## 15. Coding Example
```python
# A tiny stateful firewall model in Python
class Flow:
    def __init__(self, proto, sip, dip, sport, dport):
        self.key = (proto, sip, sport, dip, dport)
        self.state = "NEW"

class StatefulFirewall:
    def __init__(self, allow_new):
        self.flows = {}
        self.allow_new = allow_new      # set of allowed (proto,dport)

    def decide(self, proto, sip, sport, dip, dport):
        if (proto, dip, dport) in self.allow_new and self.flows.get((proto, sip, sport, dip, dport)) is None:
            self.flows[(proto, sip, sport, dip, dport)] = Flow(proto, sip, dip, sport, dport)
            return "ALLOW (NEW)"
        if (proto, dip, dport) in self.allow_new or (proto, dip, sport) == (proto, dport, sport):
            # matching an existing flow key in either direction
            rev = (proto, dip, dport, sip, sport)
            if rev in self.flows or (proto, sip, sport, dip, dport) in self.flows:
                self.flows[rev] = self.flows.get(rev) or Flow(proto, dip, sip, dport, sport)
                return "ALLOW (ESTABLISHED)"
        return "DROP"

fw = StatefulFirewall({("tcp", 443)})
print(fw.decide("tcp", "1.2.3.4", 5000, "10.0.0.1", 443))   # NEW → allow
print(fw.decide("tcp", "10.0.0.1", 443, "1.2.3.4", 5000))    # reply → ESTABLISHED
print(fw.decide("tcp", "5.6.7.8", 6000, "10.0.0.1", 443))    # another NEW → allow
print(fw.decide("tcp", "5.6.7.8", 6000, "10.0.0.1", 22))     # no rule → DROP
```
```bash
# Inspect the real stateful firewall on Linux
sudo iptables -L -n -v --line-numbers | head -20          # filter rules + hit counters
sudo conntrack -L | head -10                              # the connection/state table
sudo iptables -A INPUT -p tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT
sudo iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -j DROP
# or the modern nftables:
sudo nft list ruleset | head -30
# IDS visibility:
sudo journalctl -u fail2ban --since today | tail          # login-ban firewall automation
sudo tcpdump -ni eth0 'tcp[13] & 2 != 0' | head -3        # watch NEW SYN segments (firewall perspective)
```

## 16. Industry Usage
- **Enterprise perimeter**: Check Point, Palo Alto, Cisco ASA/Firepower, Fortinet — the NGFW market.
- **Cloud**: AWS Security Groups (stateful) + NACLs (stateless) + AWS WAF; GCP Cloud Armor + firewall rules; Azure NSG/Firewall — firewalling is now *policy-as-code*.
- **Host hardening**: Linux `nftables`/`iptables`, firewalld, UFW; Windows Defender Firewall — every production host has a default-deny or allow-listed host firewall.
- **Detection**: Suricata/Snort (NIDS/IPS), Zeek (NSM), osquery (HIDS), CrowdStrike/SentinelOne (EDR), AWS GuardDuty, Google Chronicle — the SOC stack.
- **CDN/WAF**: Cloudflare, Fastly, AWS WAF, Imperva — application-layer filtering at the edge for every public web app.
- **Zero trust**: Cloudflare Access/Google BeyondCorp replace "VPN + perimeter" with identity-aware proxies — the next-generation firewall (Section 05).

## 17. References
- Linux `netfilter`/`nftables` docs — https://docs.kernel.org/networking/nf_conntrack-sysctl.html
- Suricata (IDS/IPS) — https://suricata.io/ ; Snort — https://www.snort.org/
- OWASP CRS (Core Rule Set for WAFs) — https://coreruleset.org/
- AWS Security Groups & NACLs docs — https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html
- RFC 4787 (NAT/firewall behavioral requirements) — https://datatracker.ietf.org/doc/html/rfc4787
- Kurose & Ross, *Computer Networking*, 8th ed., §8.6-8.7 (firewalls, IDS).
- NIST SP 800-41 (Guidelines on Firewalls) — https://csrc.nist.gov/pubs/sp/800/41/r1/final

## 18. Cheat Sheet
- Packet filter: 5-tuple ACL, stateless. Stateful: conntrack/connection table (NEW/ESTABLISHED/RELATED/INVALID).
- Default-deny: allow explicit, drop everything else — the firewall baseline.
- NGFW/WAF: L7 inspection (HTTP, SNI, signatures, bots); WAF = HTTP app attacks.
- IDS = passive detect + alert; IPS = inline block; signature + anomaly detection.
- IPS false positives → availability risk; fail-open vs fail-closed.
- DMZ: public services isolated from internal network.
- East-west (lateral) vs north-south (border) → internal segmentation/microsegmentation.
- AWS SG = stateful, NACL = stateless (both must be configured intentionally).
- TLS inspection: decrypt→inspect→re-encrypt; privacy/CPU/MITM trade-offs.
- HIDS (host) + NIDS (wire) together = full visibility.

## 19. Quiz
1. A stateless firewall inspects: a) connection state b) the 5-tuple c) HTTP payload d) TLS certs → **b**
2. ESTABLISHED/RELATED matching requires: a) conntrack b) a WAF c) TLS d) DNS → **a**
3. IDS is: a) inline blocking b) passive detection c) a proxy d) a WAF → **b**
4. IPS differs from IDS by: a) location b) inline prevention c) signatures d) logging → **b**
5. A WAF protects: a) the network layer b) web apps (HTTP) c) DNS d) email → **b**
6. Default-deny means: a) allow all b) drop unless allowed c) log all d) rate-limit → **b**
7. A DMZ hosts: a) internal DBs b) public-facing services c) only admin hosts d) nothing → **b**
8. AWS security groups are: a) stateless b) stateful c) WAFs d) proxies → **b**

**Answers**: 1-b, 2-a, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: Packet filter vs stateful?** → **A:** 5-tuple ACL vs connection-table (conntrack) awareness — stateful blocks spoofed replies.
- **Q: IDS vs IPS?** → **A:** Passive detect+alert vs inline block (availability risk from false positives).
- **Q: What does a WAF see that a firewall can't?** → **A:** HTTP payloads — SQLi/XSS signatures, bots, rate limits.
- **Q: What is default-deny?** → **A:** Allow nothing unless explicitly permitted; the baseline policy.
- **Q: What is a DMZ?** → **A:** Isolated zone for public services so a compromise can't reach internal hosts.
- **Q: AWS SG vs NACL?** → **A:** Stateful (per instance) vs stateless ACL (per subnet, both directions).
- **Q: How does a stateful firewall stop spoofed replies?** → **A:** No SYN → no connection table entry → INVALID → drop.

## 21. Revision
Firewalls enforce policy at boundaries, evolving from stateless 5-tuple ACLs → stateful (conntrack: NEW/ESTABLISHED/RELATED, defeats spoofed replies) → application/NGFW/WAF (L7 HTTP/signatures/bots). IDS detects passively (alerts), IPS blocks inline (drops); both use signature + anomaly detection, and IPS's false positives are its availability cost. Deployment: perimeter, DMZ, zones (east-west segmentation), host (`nftables`/UFW), cloud (SGs stateful, NACLs stateless, WAF). Default-deny is the baseline. Anchor: *firewall = gatekeeper (who/what may pass); IDS/IPS = watchman (see/stop what shouldn't); WAF = mailroom reading letters; layer them because no single control catches everything.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Packet filter vs stateful vs app firewall" | 13-Q1 |
| "Why stateful beats stateless / spoofed replies" | 13-Q2,13 |
| "How does conntrack/iptables work?" | 13-Q3 / 8 |
| "Default-deny principle" | 13-Q4 |
| "IDS vs IPS" | 13-Q5 |
| "Signature vs anomaly detection" | 13-Q6 |
| "IPS dropping legit traffic — fix?" | 13-Q7 |
| "What is a WAF?" | 13-Q8 |
| "Design a firewall policy for a web server" | 13-Q9 |
| "DMZ / east-west segmentation" | 13-Q10,11 |
| "TLS inspection trade-offs" | 13-Q12 |
| "Security groups vs NACLs" | 13-Q14 |
