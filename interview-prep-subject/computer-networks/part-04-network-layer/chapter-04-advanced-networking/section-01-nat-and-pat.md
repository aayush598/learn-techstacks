# NAT and PAT

> **TL;DR**: **NAT** (RFC 1631) rewrites IP addresses in headers at a gateway; **PAT** (port address translation) rewrites both IP *and* port so thousands of private (RFC 1918) hosts share one public IP. The NAT table maps (private IP:port ↔ public IP:port) bidirectionally — it bought IPv4 time, but breaks inbound connections and end-to-end transparency, the very reason IPv6 exists.

## 1. Why Does This Exist?
The IPv4 address space (2^32 ≈ 4.3 billion) ran out long ago — the RIRs exhausted pools in 2011–2020 — yet the Internet serves billions of devices. The Internet runs on **RFC 1918 private addresses** (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16) inside every home, office, and DC. Those are *not* globally routable: a packet with source 192.168.1.5 can't cross the Internet. **NAT** exists to bridge the private world to the public one: a gateway *rewrites* the source IP (and, with **PAT**, the source port) so private hosts appear as one public address. It gives **security-by-obscurity** (hosts aren't directly reachable — no inbound path without a mapping), **flexibility** (change ISPs/IPs without renumbering internal hosts), and — the historical driver — **IP address conservation**: a /29 of public IPs can serve tens of thousands of private devices. It's a stopgap that became permanent infrastructure: essentially *every* enterprise, DC, and home network uses NAT today, and even IPv6 deployments often keep it for transition.

## 2. How Does It Work?
- **Basic NAT (1:1)**: a static mapping private↔public IP; an internal host is translated to a fixed public IP (used for servers needing a stable public identity, or in some IPv4-deficiency ISPs).
- **PAT (NAT overload, N:1)**: thousands of private hosts share *one* public IP. The NAT rewrites **source IP** to the public IP and **source port** to a free high port (e.g., 50000–65535), keeping the entry in the **NAT table**. Return packets are reverse-mapped: (public IP:port) → (original private IP:port).
- **NAT table**: entries (internal IP:port ↔ external IP:port, protocol, timers). Table *size* and *timeout* (UDP ~5 min, TCP per-session) are operational limits — a full table drops new connections.
- **Directionality**: outbound connections *create* mappings → inbound connections *can't* be initiated (no entry → return packet can't be reverse-mapped). This is NAT's defining property and its biggest limitation. Solutions: **static NAT / port forwarding** (DMZ) for servers, **STUN/UPnP/NAT-PMP** for P2P, **hole punching** (both sides send to a rendezvous).
- **Port forwarding / DMZ**: admin configures "public IP:80 → 192.168.1.10:80" so external clients can reach the internal web server.
- **Symmetric vs cone NAT**: **full-cone** (any external can reply once a mapping exists), **restricted-cone** (only the external you spoke to can reply), **port-restricted** (external IP+port), **symmetric** (a *different* mapping per destination — breaks most P2P/STUN tricks). P2P works best with cone NAT.
- **NAT traversal**: STUN (discover your public IP:port via a server) → TURN (relay through a server when direct fails) → ICE (the candidate-pairing algorithm used by WebRTC). This is the standard "how does NAT work for real-time apps?" story.
- **NAT64/NAT-PT (IPv6 transition)**: translate between IPv6 and IPv4 — the transition tools that let IPv6-only clients reach IPv4 servers (DNS64 + NAT64 is the modern form).

## 3. When Is It Used?
- **Home/branch**: every router does PAT by default — the "192.168.1.x → one public IP" pattern everyone lives on.
- **Enterprise egress**: corporate firewalls NAT all internal egress through a pool of public IPs (PAT), with static NAT/port-forward for inbound servers.
- **DC/cloud**: cloud load balancers and internet gateways NAT (AWS Internet Gateway: private VPC → public EIP via 1:1 NAT; Azure/GCP similar). Outbound-only workloads use NAT gateways (PAT).
- **ISP CGNAT (carrier-grade)**: ISPs PAT customers behind shared public IPs (IPv4 exhaustion) — with the operational consequences: no inbound, per-user rate limits, IPv6 push. CGNAT is *why* you can't port-forward on many mobile/cable plans.
- **IPv6 transition**: NAT64 (v6→v4) + DNS64 lets v6-only networks reach the v4 Internet.
- **P2P**: WebRTC (Google Meet, Discord), VoIP, torrents all depend on **STUN/TURN/ICE** to traverse NAT — this is the practical "how does peer-to-peer actually work?" answer.

## 4. Why Wasn't Another Approach Chosen?
- **Why not just give everyone public IPs?** Because IPv4 ran out (RIR exhaustion 2011–2020); the space is physically consumed. NAT is the stopgap that let the Internet keep growing with the *existing* address space. The "real" fix is **IPv6** (RFC 8200) — 2^128 addresses, end-to-end restored — but adoption is slow, so NAT persists.
- **Why PAT and not just basic NAT?** Basic NAT needs *one public IP per private host* — that's the entire problem. PAT multiplexes thousands of hosts onto one IP by using the 16-bit port space as an extra discriminator → orders-of-magnitude address conservation. It's the only way one /32 serves a city (CGNAT).
- **Why not use the port field differently / no header rewrite?** Without NAT, private addresses can't route (RFC 1918 blocks aren't in the global table); you *must* rewrite at a boundary. PAT is the minimal change that works with existing applications — a giant pragmatic hack over redesigning the Internet.
- **Why does IPv6 not need NAT?** End-to-end addressing returns: every host gets a routable global address, no header rewriting, no inbound-blocking, true transparency. NAT was the *workaround* for scarcity; IPv6 removes the scarcity, so the workaround dies. (Networks still choose NAT for filtering/security in some designs, but it's optional — and that choice is a policy, not a necessity.)

## 5. Intuition
Think of a **company reception desk** in an office building (the NAT gateway). Every employee (private host) has a *desk number* (private IP) but the building has only *one* street address (public IP). To call out, the receptionist (NAT) takes your name, calls back with the building's number, and assigns you a temporary "line number" (source port). Everyone shares the one street number, and the receptionist's *notebook* (NAT table) records "employee A ↔ line 50001." When a call comes in for line 50001, the receptionist routes it to employee A. If someone calls the building *cold* asking for an employee by name, the receptionist has no notebook entry → the call is refused (no inbound). Employees all think they have the street address (NAT's transparency) — but they don't, and they can't receive cold calls. Big problem: employee A tries to call two different outside companies *at the same time* — the receptionist gives each a different line (PAT), and this works only if the receptionist is good at note-taking. And some employees use their own secret direct-dial numbers (STUN discovery) to make the receptionist's job easier — that's NAT traversal.

## 6. Real-World Analogy
**The apartment-building mailroom**: A building (the NAT) with one street address serves hundreds of apartments (private IPs). Outgoing mail is re-labeled with the building's address plus a unit number (the port) — the postal service only ever sees the building's single address (PAT). The mailroom clerk's log (NAT table) maps each outgoing letter to its apartment so return mail can be delivered (reverse mapping). Return mail addressed *only* to the building ("The Smiths, 123 Main St") can't be delivered — there's no apartment on the label (no inbound without a mapping) — which is why services you *want* to reach must publish a specific mailbox: "send to 123 Main St, Apt 5, Port 80" (port forwarding). And the day the city gives every apartment its own address (IPv6), the mailroom becomes optional. Meanwhile, apps that *must* receive unsolicited traffic (gaming, video calls) run a protocol to ask the mailroom to open a specific path (STUN/UPnP), or route through a courier service (TURN relay) when the mailroom won't cooperate — that's exactly how NAT traversal works in the real world.

## 7. Formal Definition
NAT (RFC 1631) is a gateway function that modifies network-layer (IP) and, in PAT, transport-layer (TCP/UDP port) fields in passing packets, maintaining a stateful **NAT mapping table** `(internal IP, internal port, external IP, external port, protocol, timeout)` to translate return traffic. **Basic NAT**: 1:1 address rewrite. **PAT (overload)**: N:1 — one external address shared, distinguished by external port. **NAT behaviors**: full-cone, address-restricted cone, port-restricted cone, symmetric (RFC 4787/5382 classify). Translation is *stateless at the IP level for basic NAT, stateful for PAT*. Inbound connections fail without a pre-existing mapping; traversal uses STUN (RFC 5389), TURN (RFC 5766), ICE (RFC 8445). IPv6 transition: NAT64 (RFC 6146) + DNS64 (RFC 6147) translate v6↔v4.

## 8. Example
A private host reaches the Internet (the canonical PAT walk):
```
Private host:  192.168.1.5 : 51000   →  8.8.8.8 : 53   (UDP DNS query)
NAT gateway (public IP 203.0.113.7):
  rewrite source  →  203.0.113.7 : 56001
  add table entry:  (192.168.1.5:51000  ↔  203.0.113.7:56001, UDP, TTL 300s)
On the wire:      203.0.113.7 : 56001  →  8.8.8.8 : 53

Reply arrives:   8.8.8.8 : 53  →  203.0.113.7 : 56001
NAT looks up port 56001 → entry found → rewrite dest:
                 8.8.8.8 : 53  →  192.168.1.5 : 51000   ✓ delivered
```
If *no* entry existed for :56001, the packet is dropped (inbound block). Note the table lookup is on the **external port** — that's the discriminator that lets 10,000 private hosts share one IP.

## 9. Internal Working
1. **Forwarding path**: every outbound packet traverses the NAT; if no mapping exists, it creates one (source IP → public, source port → allocated external port), records the entry with a protocol-specific timeout, and rewrites checksums (IP checksum + TCP/UDP checksum, since the pseudo-header changes).
2. **Return path**: reverse lookup on (dest IP, dest port) → rewrite dest to internal (IP, port) → deliver. Lookup *miss* → drop (with optional logging — the "NAT drops inbound" behavior).
3. **Table management**: entries expire on timers (UDP ~2–5 min, TCP until FIN/RST or timeout, ICMP short); a full table (many cheap NAT gateways hold only thousands) drops *new* connections — the "NAT table exhaustion" outage mode.
4. **Special cases**: FTP (passive data channel needs a *second* connection — FTP ALG inspects and creates mappings for data ports), SIP/H.323 (media ports), DNS (embedded addresses in responses), and fragmented packets (first fragment carries the ports → fragmented traffic can break PAT). ALGs (application-level gateways) inspect protocols to make NAT work with them — a huge source of firewall/NAT quirks.
5. **Deterministic NAT (CGNAT)**: ISPs use deterministic algorithms so the same internal IP always maps to the same external IP+port range — keeps logs manageable and enables per-customer limits (RFC 7596).
6. **Hairpin NAT**: two private hosts talking to each other's *public* address must be hairpinned back through the NAT (loopback) — the "NAT hairpin/reflexive" feature some home routers lack (why LAN-to-LAN via your public IP fails on cheap routers).
7. **Traversal mechanics**: STUN (query a server: "what's my public IP:port?" → returns the mapping) → ICE (collect candidates, pair local+server-reflexive+relay, connectivity-check via STUN) → TURN (relay through a server when symmetric NAT or firewalls block direct) — WebRTC's full stack.

## 10. Time Complexity
- **NAT lookup**: O(1) — hash on (external IP, external port, protocol). Every packet = one lookup; it's a *hardware-fast* data-plane operation on modern gateways (a small, hot hash table).
- **Table size**: the practical limit — consumer gateways hold ~thousands of entries; carrier-grade NATs hold *millions*. A full table = dropped connections, so table size and timeout *directly* bound connection capacity. This is NAT's real complexity constraint (it's the state, not the math).
- **PAT port space**: 2^16 ≈ 65,535 ports × number of public IPs = total concurrent outbound sessions (e.g., 1 IP ≈ 65K sessions — a real CGNAT/enterprise limit for many-to-one).
- **ALG processing**: O(protocol payload scan) for FTP/SIP — a per-session cost that makes ALGs a scaling bottleneck.
- **Impact**: unlike pure routing (O(1), stateless), NAT is *stateful* and *per-packet* — the price paid for address conservation. CGNAT scale requires distributed state and huge tables.

## 11. Advantages
- **Address conservation**: thousands of hosts per public IP (PAT/CGNAT) — the *reason* the IPv4 Internet kept growing past exhaustion.
- **Immediate security**: internal hosts are unaddressable from outside (no inbound mapping) → automatic inbound filtering, hide your internal topology.
- **Flexibility**: renumber internal networks / change ISP without touching public addressing; overlaps are tolerable behind a NAT.
- **Simple deployment**: works with unmodified client apps (mostly), zero client config — the reason it spread everywhere.
- **Protocol breadth**: one mechanism serves web, DNS, VoIP, games (with ALG/traversal help).

## 12. Disadvantages
- **Breaks end-to-end**: no true transparency; inbound services need port-forwarding/static NAT; some protocols (SIP/FTP) require ALG fiddling.
- **Breaks P2P**: symmetric NAT blocks direct connections → STUN/TURN/ICE overhead and relays (extra latency, cost — the WebRTC tax).
- **Stateful cost**: NAT tables must be sized, timed, and engineered; table exhaustion and timeout issues are real production failures; CGNAT per-user logging adds ops burden.
- **Head-of-line for apps**: some apps embed IPs in payloads (FTP/SIP) → ALG bugs, breakage, IPv6 is cleaner.
- **Complicates security & audit**: source IP is *not* the host (NAT masks identity — abused for abuse/anonymity); logs tie CGNAT user↔IP mappings.
- **Latency/changes**: hairpin NAT, keepalive overhead, and ALG processing add edge cases and operational complexity that pure routing doesn't have.

## 13. Interview Questions
1. **Q: What is NAT and why does it exist?** A: Network Address Translation — rewriting IP addresses at a gateway so private (RFC 1918) hosts share public IPs; it exists because IPv4 ran out and it conserves addresses (plus gives security and flexibility).
2. **Q (tricky): NAT vs PAT?** A: NAT (basic) = 1:1 IP rewrite (a private host gets a fixed public IP). PAT (NAT overload) = N:1 — many private hosts share one public IP, distinguished by *source port*; the NAT table holds IP+port mappings.
3. **Q: Walk through a PAT flow.** A: Outbound: rewrite source (IP → public, port → allocated high port), log mapping in the NAT table, fix checksums. Return: lookup the external port → reverse-map → deliver to the private host. No entry → drop.
4. **Q (FAANG): Why can't an external host initiate a connection through NAT?** A: No NAT table entry for an inbound packet → no mapping to reverse → dropped. NAT only translates traffic matching an *existing* mapping, which outbound connections create; inbound has no path unless port-forwarding/static NAT is configured.
5. **Q: What is port forwarding and the DMZ?** A: A manual static NAT rule: "public IP:port → internal IP:port" so external clients reach an internal server; DMZ = forward all unmapped ports to one host (a blunt, insecure option).
6. **Q (tricky): Cone vs symmetric NAT?** A: Cone NAT: once a mapping exists, external hosts can reach it (full-cone: anyone; address-restricted: only IPs you talked to; port-restricted: only IP:port you talked to). Symmetric: a *new* mapping per destination — P2P/direct connections generally fail → need TURN relay.
7. **Q: How does NAT traversal work?** A: STUN (learn your public IP:port from a server), TURN (relay when direct fails), ICE (pair candidates + connectivity checks). This is how WebRTC/VoIP/P2P works through NAT.
8. **Q (FAANG): What is CGNAT and its tradeoffs?** A: Carrier-grade NAT: ISPs PAT customers behind shared public IPs (IPv4 exhaustion). Pros: serves millions with few IPs. Cons: no inbound, port restrictions, per-user logging, breaks some apps, IPv6 push.
9. **Q: Does IPv6 need NAT?** A: No — IPv6's address space makes end-to-end addressing possible (no scarcity → no rewrite). NAT persists in some designs for security/filtering, but it's a policy choice, not a requirement.
10. **Q (tricky): Why does FTP break behind NAT?** A: Passive-mode FTP uses a *second* data connection on a dynamically negotiated port — the IP:port is embedded in the control payload. NAT must inspect and create a mapping for it (FTP ALG); without ALG, the data connection fails.
11. **Q: What is a NAT table and why does it matter operationally?** A: The stateful mapping (internal IP:port ↔ external IP:port, protocol, timeout). Size/timeout bound concurrency; exhaustion drops new connections (a classic outage); timeout tuning affects app keepalives.
12. **Q: What is hairpin NAT?** A: Two private hosts reaching each other's *public* address → traffic must be hairpinned back through the NAT; some cheap routers don't support it (LAN-to-LAN via public IP fails).
13. **Q (FAANG): "Your API serves 50K clients behind CGNAT. Any concerns?"** A: IP-based rate-limiting/auth-by-IP breaks (all CGNAT users share IPs); connection-count limits per public IP; long-lived connections need keepalives; you need *session/port* awareness, not raw IP identity — a real production concern with NAT at scale.
14. **Q: NAT64 — what is it?** A: IPv6→IPv4 translation (with DNS64 synthesizing A records) so v6-only clients reach v4-only servers — the practical IPv6 transition tool.
15. **Q (tricky): Fragmentation and PAT?** A: The first fragment carries the TCP/UDP header (ports); subsequent fragments don't. PAT must handle fragments specially (or drop them) — a real-world NAT gotcha for large UDP/ICMP traffic.

## 14. Follow-Up Questions
1. **Q: What are the RFC 1918 private ranges?** A: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 — never routed on the public Internet, always behind a NAT/edge.
2. **Q: What happens to the TCP/UDP checksum with NAT?** A: The checksum covers the pseudo-header (src/dst IP + ports), so NAT *must* recompute it after rewriting — a mandatory per-packet cost.
3. **Q (production): Diagnose "external can't reach my port-forwarded server."** A: Check: (1) the rule's internal IP is current (DHCP changed it!), (2) the WAN IP isn't behind CGNAT (your router's WAN IP is private → you can't forward — an ISP-level block), (3) the internal firewall allows it, (4) hairpin vs external testing (test from outside, not from inside the LAN).
4. **Q: Why is NAT considered a security feature?** A: It drops all inbound by default (stateful inspection) and hides internal IPs/topology — but it's *not* a firewall (no rule/state-based filtering policy); treat it as defense-in-depth, not a substitute.
5. **Q (tricky): UDP timeouts and keepalives behind NAT.** A: NAT entries for UDP expire (~2–5 min); apps must send keepalives to hold the mapping — the reason VoIP/gaming/WebRTC send regular STUN-binding refreshes. Mis-tuned timeouts = "connections drop randomly" bugs.
6. **Q: How does a stateful firewall differ from NAT?** A: NAT rewrites addresses (translation); a firewall filters by state/policy (allow/deny). They often live in the same box but are different functions — you can NAT without filtering and filter without NAT.

## 15. Coding Example
```python
import random
import hashlib

class NatTable:
    """A minimal PAT/NAT table (production ones are hash maps + timers)."""
    def __init__(self):
        self.mappings = {}          # (ext_ip, ext_port, proto) -> (priv_ip, priv_port)
        self._next_port = 50000
        self._used = set()

    def outbound(self, priv_ip, priv_port, proto):
        key = (priv_ip, priv_port, proto)
        for (ext_ip, ext_port, p), v in self.mappings.items():
            if v == key:
                return (ext_ip, ext_port)
        # allocate a free external port (PAT)
        while self._next_port in self._used:
            self._next_port += 1
        ext = ("203.0.113.7", self._next_port)
        self._used.add(self._next_port)
        self._next_port += 1
        self.mappings[(ext[0], ext[1], proto)] = key
        return ext

    def inbound(self, ext_ip, ext_port, proto):
        return self.mappings.get((ext_ip, ext_port, proto))

nat = NatTable()
ext = nat.outbound("192.168.1.5", 51000, "udp")
print("on the wire:", ext[0] + ":" + str(ext[1]))          # 203.0.113.7:50000
print("return path:", nat.inbound(ext[0], ext[1], "udp"))  # ('192.168.1.5', 51000)
```
```bash
# NAT in action
$ tcpdump -ni eth0 'udp port 53'              # watch DNS go out (private src)
$ tcpdump -ni eth0 'host 203.0.113.7'         # the public face (NATed src)
# Linux NAT (the machinery that runs most of the Internet's NATing):
$ iptables -t nat -L -n -v                     # view PAT mappings
$ iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE   # PAT for a subnet
$ iptables -t nat -A PREROUTING -d 203.0.113.7 -p tcp --dport 80 \
    -j DNAT --to-destination 192.168.1.10:80  # port forwarding
$ conntrack -L | head                          # the real NAT table
```

## 16. Industry Usage
- **Every home/branch router**: default PAT — the fabric of IPv4 reality; most users are behind at least one NAT.
- **ISPs/CGNAT**: carriers PAT customers (IPv4 exhaustion) with dedicated NAT appliance/software (Carrier-Grade NAT, RFC 6888); per-user mapping, logging for law enforcement, IPv6 transition parallel.
- **Cloud (AWS/Azure/GCP)**: NAT gateways for outbound-only workloads (PAT over one/two public IPs per AZ), 1:1 NAT for instances (AWS EIP + Internet Gateway), CGNAT-style pools for public services.
- **Enterprise egress & security**: firewalls (Palo Alto/Fortinet) do NAT + stateful filtering + VPN termination in one box — the standard edge.
- **P2P/real-time (WebRTC)**: STUN/TURN/ICE servers at scale (Google, Cloudflare TURN, Twilio) traverse NAT for Meet/Discord/Slack calls — a multi-billion-user dependency on NAT traversal.
- **IPv6 transition**: NAT64/DNS64 in mobile ISPs (large v6-only deployments reach v4 services), and 464XLAT (AT&T mobile) — NAT's final act as a *transition* tool.

## 17. References
- RFC 1631 — NAT: https://www.rfc-editor.org/rfc/rfc1631
- RFC 1918 — Private address space: https://www.rfc-editor.org/rfc/rfc1918
- RFC 4787 / RFC 5382 — NAT behavioral requirements (cone/symmetric, TCP): https://www.rfc-editor.org/rfc/rfc4787
- RFC 5389 — STUN: https://www.rfc-editor.org/rfc/rfc5389
- RFC 5766 — TURN: https://www.rfc-editor.org/rfc/rfc5766
- RFC 8445 — ICE: https://www.rfc-editor.org/rfc/rfc8445
- RFC 6146/6147 — NAT64/DNS64: https://www.rfc-editor.org/rfc/rfc6146
- RFC 6888 — CGNAT requirements: https://www.rfc-editor.org/rfc/rfc6888
- RFC 8200 — IPv6: https://www.rfc-editor.org/rfc/rfc8200
- Kurose & Ross, *Computer Networking*, Ch. 4 §4.3 (NAT).

## 18. Cheat Sheet
- RFC 1918: 10/8, 172.16/12, 192.168/16 — never globally routed.
- NAT = rewrite IP; PAT = rewrite IP + port (N:1, the standard).
- NAT table: (priv IP:port ↔ pub IP:port, proto, timeout); O(1) lookup; size = capacity.
- Outbound creates mapping → inbound without mapping = drop (NAT blocks inbound).
- Port forwarding / static NAT / DMZ = inbound access to servers.
- Cone (full/address/port-restricted) vs symmetric NAT — symmetric breaks P2P.
- Traversal: STUN (discover) → ICE (pair) → TURN (relay) — WebRTC's stack.
- CGNAT = ISP-level PAT; per-user logs, no inbound, connection limits.
- FTP/SIP need ALGs (second data channel, embedded IPs). Fragments break PAT.
- Hairpin = LAN→own public IP (needs NAT loopback). Timeouts → keepalives needed.
- IPv6 → no NAT needed (end-to-end); NAT64/DNS64 = v6↔v4 transition.
- Linux: iptables MASQUERADE / DNAT; conntrack shows the table.

## 19. Quiz
1. PAT lets: a) 1:1 IP map b) many hosts share one public IP c) no IPs d) IPv6 → **b**
2. RFC 1918 private range: a) 192.168.0.0/16 b) 8.8.8.0/8 c) 0.0.0.0/0 d) 203.0.113.0/24 → **a**
3. Inbound connection through PAT: a) always works b) fails w/o mapping c) faster d) needs no table → **b**
4. NAT traversal "discover my public IP:port" = a) TURN b) STUN c) DNS d) ICMP → **b**
5. Relay through a server when direct fails = a) STUN b) TURN c) ICE d) DNS → **b**
6. Symmetric NAT: a) one mapping per dest b) cone c) no NAT d) IPv6 → **a**
7. FTP needs NAT: a) ALG b) no mapping c) TURN d) DHCP → **a**
8. CGNAT: a) ISP-level PAT b) IPv6 c) DNS d) BGP → **a**
9. NAT checksum must be: a) ignored b) recomputed c) zeroed d) cached → **b**
10. IPv6 removes the need for NAT because: a) port space b) address scarcity gone c) faster d) security → **b**

## 20. Flashcards
- **Q: NAT vs PAT?** → **A:** 1:1 IP rewrite vs N:1 (IP+port) sharing one public IP.
- **Q: Why NAT?** → **A:** IPv4 exhaustion → conserve addresses; + security, flexibility.
- **Q: Why no inbound?** → **A:** no table mapping → return can't be reverse-translated.
- **Q: Cone vs symmetric?** → **A:** cone = reusable mapping; symmetric = per-dest → breaks P2P.
- **Q: Traversal stack?** → **A:** STUN → ICE → TURN (relay).
- **Q: CGNAT?** → **A:** ISP PAT; no inbound, per-user logs, IPv6 transition driver.
- **Q: IPv6 + NAT?** → **A:** not needed (end-to-end restored); NAT64/DNS64 for transition.

## 21. Revision
NAT (RFC 1631) exists because IPv4 ran out: private RFC 1918 hosts must be rewritten at the edge. PAT = many hosts → one public IP via source-port translation, with a stateful NAT table (O(1) lookup, bounded by size/timeout). Outbound creates mappings; inbound without one is dropped (NAT's defining security + its biggest limitation) → port-forwarding for servers, STUN/TURN/ICE for P2P. Cone (works) vs symmetric NAT (breaks P2P). CGNAT = ISP PAT at scale (logs, limits, no inbound). FTP/SIP need ALGs; fragments break PAT; hairpin needs loopback. IPv6 removes the scarcity so NAT is optional; NAT64/DNS64 transition tools bridge v6↔v4. Practical tools: iptables MASQUERADE/DNAT, conntrack, tcpdump.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is NAT / why does it exist?" | 2 How It Works / 7 Formal Definition |
| "NAT vs PAT?" | 13 Q&A / 7 Formal Definition |
| "Why can't external hosts connect in?" | 13 Q&A / 5 Intuition |
| "Cone vs symmetric NAT?" | 13 Q&A / 5 Intuition |
| "How does NAT traversal work?" | 13 Q&A / 9 Internal Working |
| "What is CGNAT?" | 13 Q&A / 16 Industry Usage |
| "Does IPv6 need NAT?" | 13 Q&A / 4 Why Not Another Approach |
| "FTP behind NAT / ALGs?" | 13 Q&A / 9 Internal Working |
| "NAT table / exhaustion / keepalives?" | 13 Q&A / 10 Time Complexity |
| "Port-forwarding troubleshooting?" | 13 Q&A / 14 Follow-Up |
