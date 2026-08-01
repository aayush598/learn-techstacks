# ARP, RARP, and IP Helper Protocols

> **TL;DR**: **ARP** (Address Resolution Protocol) maps an IP address to a MAC address on a local link — "who has 192.168.1.1? Tell 192.168.1.5" — with a cached table, gratuitous announcements, and proxy/spoofing variants; **RARP** (the reverse, MAC→IP, RFC 903) is obsolete but spawned BOOTP→DHCP; together they're the glue between the network and link layers.

## 1. Why Does This Exist?
IP addresses are *logical, routable, hierarchical* — but on a physical LAN, frames are delivered by **MAC addresses** (burned into hardware, flat, link-local). Before any IP packet can cross a link, the sender must know the receiver's MAC: "which NIC on this wire owns 192.168.1.1?" ARP exists because there's no built-in correspondence between the two name spaces — the IP address is assigned (static/DHCP) while the MAC is hardware. Without ARP, every host would need a manually-maintained IP→MAC table (impossible at scale) — so ARP *discovers* the mapping on demand and *caches* it. RARP existed for the reverse question diskless workstations asked at boot: "I know my MAC, what's my IP?" — it's obsolete (replaced by BOOTP/DHCP) but is the ancestor of the dynamic-configuration lineage. These helpers exist because the network and link layers have *different naming systems* and someone has to translate.

## 2. How Does It Work?
- **ARP request (broadcast)**: the sender broadcasts on the link: "Who has 192.168.1.1? Tell 192.168.1.5" — sender MAC, sender IP, target IP, target MAC=0 (unknown), opcode=1.
- **ARP reply (unicast)**: the target responds directly: "192.168.1.1 is 00:11:22:33:44:55" (opcode=2), MAC filled. Everyone on the link *snoops* both directions and caches.
- **Cache**: the mapping is cached (`arp -a`, `ip neigh`) for ~30 s–4 min (entry lifetime); entries are refreshed by use, removed on timeout.
- **Gratuitous ARP (GARP)**: a host announces its own IP→MAC *unsolicited* — on interface up, IP change, or failover (VRRP/keepalive) — so neighbors update their caches immediately.
- **Proxy ARP**: a router answers ARP for a remote network on behalf of a host it can reach ("I know where 192.168.2.10 is") — lets a host think a remote host is on-link (legacy/special cases, RFC 1027).
- **ARP cache poisoning/ARP spoofing**: an attacker answers ARP requests with its own MAC → intercepts traffic (MITM) — the classic LAN attack (mitigated by DHCP snooping/DAI, static entries).
- **RARP (obsolete)**: a booting host broadcasts "I have MAC X, what is my IP?"; a RARP server replies (opcode 3/4). Replaced by BOOTP (which added the IP *assignment* server-side + options) → DHCP (dynamic leases).

## 3. When Is It Used?
- **Every on-link IP delivery**: any time a host sends to a same-subnet IP (or its gateway), ARP resolves the MAC first — it's the *first packet* of every conversation.
- **IPv4 only**: ARP exists for IPv4; IPv6 replaced it with NDP (ICMPv6). This is a frequent interview comparison.
- **Bootstrapping**: a diskless client's *very first* problem is "what's my IP?" — RARP (legacy) → BOOTP (1985) → DHCP (1997) is the lineage that answers it.
- **Failover/VRRP**: virtual IPs move between hosts using gratuitous ARP so the network re-ARP's to the new MAC instantly (HA pairs, LBs).
- **Troubleshooting**: `arp -a`/`ip neigh show` shows the table; "no ARP reply" = host not on the network / MAC wrong / broadcast blocked.
- **Security**: ARP is the classic LAN MITM vector — dynamic ARP inspection, static ARP, and 802.1X guard the cache in enterprise LANs.

## 4. Why Wasn't Another Approach Chosen?
- **Why discovery (broadcast ask) instead of a centralized registry?** A directory server would be another dependency, another SPOF, and needs every host to *know* it before ARP. On-demand broadcast discovery works with zero configuration — hosts learn as needed and cache. (That's also why it's insecure: no authentication.)
- **Why broadcast the request but unicast the reply?** The question is "who?" — unknown target → broadcast. The answer is specific → unicast (the requester's MAC is in the request). Everyone snoops to build caches (free knowledge).
- **Why cache?** Resolving per packet would flood the link with ARP broadcasts; caching makes ARP O(1) after the first resolution. The trade: stale entries (handled by timeouts + GARP refresh).
- **Why not use MAC as the address (flat addressing)?** MACs aren't hierarchical → routers can't aggregate → no scalable routing. IP (hierarchical) routes; ARP *bridges* the last-hop gap. "IP for the world, MAC for the wire."
- **Why RARP failed / BOOTP-DHCP won?** RARP required a per-MAC server entry and only delivered an IP (no mask/gateway/DNS). BOOTP added *options* (server-provided config) and DHCP added *leases* (dynamic). The lineage shows the need: IP config, not just an address.
- **Why proxy ARP instead of proper routing?** Proxy ARP lets a host that *thinks* a target is on-link still reach it via a router — a compatibility hack for old hosts/network designs; real routing is preferred (proxy ARP is a legacy/edge feature).

## 5. Intuition
ARP is **looking up a phone number in a building directory by calling out loud**: You stand in the office and shout, "Who is person 192.168.1.1? Please call extension 192.168.1.5" (broadcast request). The right person replies, "I'm 192.168.1.1, I'm at desk 00:11:22:33:44:55" (unicast reply). You write it in your notebook (cache) so you don't have to shout again; everyone who overheard also jots it down. When someone changes desks (IP change), they announce it publicly (gratuitous ARP) so everyone updates their notebooks. The malicious version: a stranger shouts "I'm 192.168.1.1!" first, and you write *their* desk number — now all your mail goes to them (ARP spoofing). And RARP is the reverse: a new employee who knows their desk number but not their badge (IP) asks "who can tell me my badge number?" — the ancestor of "ask the HR server to configure me" (DHCP).

## 6. Real-World Analogy
**A college dorm with room numbers (IPs) and student IDs (MACs)**: To deliver a letter to "Room 214," you first ask "Who's in Room 214?" at the front desk — they check their roster (ARP reply) and give you the student's mailbox number (MAC). You keep a small list of known Room→Mailbox pairs (ARP cache) so you don't re-ask every time. When a student moves, they tell the front desk and the roster updates (gratuitous ARP). The campus network's *routers* (postal sorting centers) only care about building numbers (IP prefixes); only the *last-mile* mail carrier (link layer) needs the mailbox numbers (MACs) — ARP is the front-desk lookup that bridges the two. RARP is a student who forgot their room number asking "I'm student #4821 — what room am I in?" — replaced by the modern system where the front desk just *assigns* you a room on arrival (DHCP).

## 7. Formal Definition
ARP (RFC 826) resolves a target IPv4 address to a link-layer (MAC) address on a broadcast-capable link. Messages (28-byte Ethernet/IPv4 format): hardware type (1=Ethernet), protocol type (0x0800=IPv4), HLEN/PLEN (6/4), opcode (1=request, 2=reply), sender HA/IP, target HA/IP. Request: broadcast, target HA = 0; reply: unicast to requester, target HA filled. Both parties (and snoopers) update their caches. Gratuitous ARP: request/reply with sender IP = target IP, announcing an address (RFC 5227 details address-conflict detection). Proxy ARP (RFC 1027): a router replies for a target it can route to. RARP (RFC 903) resolved MAC→IP at boot (opcodes 3/4) — obsolete; superseded by BOOTP (RFC 951) → DHCP (RFC 2131). IPv6 equivalent: NDP/ICMPv6 (RFC 4861).

## 8. Example
The classic exchange (tcpdump of the very first ping):
```
Host A (192.168.1.5, MAC AA:AA:AA:AA:AA:AA)
Host B (192.168.1.20, MAC BB:BB:BB:BB:BB:BB)

1. A -> broadcast:  ARP, Request who-has 192.168.1.20 tell 192.168.1.5,
                     length 46    (opcode 1, target MAC = 00:00:00:00:00:00)
2. B -> A:           ARP, Reply 192.168.1.20 is-at BB:BB:BB:BB:BB:BB,
                     length 46    (opcode 2, unicast back)
3. A -> B:           ICMP echo request (now A knows the MAC and sends the packet)
4. B -> A:           ICMP echo reply
```
Everyone who heard step 1 *also* learns B's MAC (and A's), so subsequent ARPs are cache hits. On `ip neigh show`, you'll see `192.168.1.20 dev eth0 lladdr bb:bb:bb:bb:bb:bb REACHABLE` — the resolved cache entry. First ping: ~1 RTT extra (the ARP exchange); every later packet: no ARP at all.

## 9. Internal Working
1. **Trigger**: before sending an IP packet, the host checks `dst` against its own prefix/mask → on-link? → look up the MAC in the ARP cache (`ip neigh`). Miss → queue the packet, send an ARP request.
2. **Broadcast delivery**: the request goes to ff:ff:ff:ff:ff:ff on the link; every host's NIC accepts it and the IP layer checks "is target IP mine?" → only the target replies (others update their cache with the requester's info — "snooping").
3. **Reply + cache update**: the target caches the requester (sender fields), sends a unicast reply; the requester caches the target; the queued packet is now sent. Cache entries have lifetimes (~30 s–4 min, refreshed on use; Linux `gc_staletime`/`base_reachable_time`); expired entries are dropped, requiring re-ARP.
4. **Gratuitous ARP**: sent on interface up / IP assignment / failover — neighbors update their caches (and detect duplicate IPs via RFC 5227 address-conflict detection: a reply to a GARP = "that IP is already in use").
5. **Proxy ARP**: a router with an interface in A's subnet answers for a host in B's subnet — A adds the target to its cache *with the router's MAC*, so it frames the packet to the router without knowing a default gateway exists. (Enabled selectively; off by default in modern hosts.)
6. **Security**: ARP has no authentication → poisoning: an attacker replies with its MAC for the gateway → traffic flows through it (MITM). Defenses: static ARP entries, Dynamic ARP Inspection (DAI, switches validate against DHCP snooping tables), 802.1X port auth.
7. **Failure modes**: no reply → "ARP resolution timed out" (packet dropped, ARP retried with backoff); wrong MAC in cache → wrong delivery (GARP fixes on re-announce); ARP cache overflow → DoS on some stacks.

## 10. Time Complexity
- **Resolution cost**: one broadcast + one unicast ≈ 1 RTT (sub-ms on LAN) *per new neighbor*; cached thereafter → O(1) lookup.
- **Cache**: small (a few hundred entries typical), O(1) hash per lookup; memory trivial.
- **Traffic**: one request per neighbor per cache-life — negligible on a healthy LAN; gratuitous ARP storms happen on failovers/boot floods (rate-limitable).
- **Security cost**: poisoning is *cheap* (one reply) — the asymmetry that makes LAN MITM so easy and defense (DAI/static) necessary.
- **Failure detection**: missing ARP = a "no route to host"-ish failure; ARP retry/backoff adds latency to the first packet of a dead-neighbor conversation.

## 11. Advantages
- **Zero configuration**: on-demand discovery — no server, no manual tables, works on any broadcast link.
- **Fast**: cached lookups are O(1); the 1-RTT cost is paid once per neighbor.
- **Self-healing**: caches expire, gratuitous ARP propagates changes, and address-conflict detection (RFC 5227) surfaces duplicate IPs.
- **Simple**: one message type, tiny payload, trivially implemented — 40 years of reliability.
- **Foundation**: enables IP-over-Ethernet (and wireless) transparently; every conversation's first hop.

## 12. Disadvantages
- **Insecure by design**: no authentication → spoofing/poisoning → MITM, hijacking, DoS. This is the #1 LAN attack and requires extra machinery (DAI, 802.1X, static entries) to defend.
- **Broadcast-dependent**: only works on broadcast-capable links (Ethernet/WiFi); point-to-point links use other methods; broadcast storms from misconfigured hosts degrade the LAN.
- **Scalability limit**: on huge flat L2 networks, ARP traffic + caches grow (one reason for segmentation/subnets; IPv6's NDP adds options but shares the concern).
- **Stale cache issues**: expired/incorrect entries cause wrong delivery until refreshed; "no ARP" failures are hard to distinguish from "host down."
- **Per-protocol duplication**: IPv4 needs ARP, IPv6 NDP, IPX its own — the helper is *layer-specific* (no unified resolution).
- **RARP's lesson**: reverse resolution (MAC→IP) requires server-side state and failed to scale — the lineage (BOOTP/DHCP) had to solve the real problem (config delivery), not just addresses.

## 13. Interview Questions
1. **Q: What is ARP?** A: Address Resolution Protocol (RFC 826) — resolves an IPv4 address to a MAC address on the local link: broadcast "who has IP X?" → the owner unicasts "IP X is MAC Y"; both cache it.
2. **Q (tricky): When does ARP happen?** A: Only when sending *within the same subnet* (on-link). For remote destinations, the packet goes to the gateway, so ARP resolves the *gateway's* MAC, not the destination's. ARP resolves the *next hop's* MAC every time.
3. **Q: Why do we need ARP if hosts have IPs?** A: IP is hierarchical and routable; the link layer delivers frames by flat hardware MACs. There's no built-in IP↔MAC mapping, so ARP discovers it on demand — the translation between the two naming systems.
4. **Q (FAANG): How does ARP affect the gateway case?** A: A host sends to a remote subnet via its default gateway: the frame is addressed to the *gateway's MAC* (resolved by ARP) with the destination's IP inside. The router then ARPs for the next hop. ARP always resolves "the next MAC on the path," not the final IP's MAC.
5. **Q: What is gratuitous ARP?** A: An unsolicited announcement of one's own IP→MAC (request where sender IP = target IP) — sent on interface up, IP change, or failover so neighbors update caches instantly and duplicate IPs are detected (RFC 5227).
6. **Q: What is proxy ARP?** A: A router answers an ARP request on behalf of a host it can reach — making the remote host *appear on-link* to the requester. Legacy/edge feature (RFC 1027); replaced by proper default-gateway routing.
7. **Q (tricky): What is ARP spoofing and why does it work?** A: An attacker sends an unsolicited (or competitive) ARP reply claiming the gateway's IP with *its* MAC → hosts cache the wrong MAC → traffic is forwarded to the attacker (MITM). Works because ARP has no authentication; defenses: DAI (switch), static ARP, 802.1X.
8. **Q: What is the difference between ARP and RARP?** A: ARP: IP→MAC (any host, on demand, still used). RARP (RFC 903): MAC→IP (diskless boot, needed a per-MAC server). RARP is obsolete — BOOTP then DHCP replaced it with full config delivery.
9. **Q (production): `ping` fails but the neighbor is up. What's the first check?** A: ARP: `ip neigh show`/`arp -a` — is the entry there? Is it the right MAC? Is it STALE/FAILED? A missing/failed ARP entry (wrong subnet mask, wrong MAC, broadcast blocked, host firewall dropping ARP) explains "no route to host" even when ping isn't blocked.
10. **Q: What does `ip neigh` show?** A: The kernel's ARP/neighbor table: each neighbor's IP, MAC, interface, and state (INCOMPLETE, REACHABLE, STALE, FAILED, PERMANENT) — the live resolution cache.
11. **Q (tricky): What happens if an ARP request gets no reply?** A: The sender retries (exponential backoff), then fails the send ("no ARP answer / host is down"). Causes: host off, wrong IP, MAC filter, firewall dropping ARP, or a L2 isolation (port security, VLAN mismatch).
12. **Q: What is the ARP cache lifetime?** A: Kernel-tunable (`gc_staletime`, `base_reachable_time_ms`), typically 30 s–4 min; entries refresh on use and drop on expiry, requiring a fresh ARP. Failover/HA uses GARP to refresh everyone instantly.
13. **Q (FAANG): How is ARP different in IPv6?** A: IPv6 has no ARP — NDP (ICMPv6, RFC 4861) does neighbor discovery with NS/NA (multicast, not broadcast), plus router discovery (RS/RA), DAD, and reachability tracking — a superset replacing ARP and DHCP's stateless part.
14. **Q: What is Dynamic ARP Inspection?** A: A switch feature that validates every ARP message against the DHCP snooping table (or ACLs) — bogus/spoofed ARP replies are dropped — the standard enterprise defense against ARP poisoning.
15. **Q (production): A failover cluster takes 2 minutes to recover. Why?** A: Likely ARP cache timeouts: the virtual IP's MAC changed but neighbors still hold the old mapping until expiry. Fix: GARP on failover (so caches refresh immediately) and shorter cache lifetimes on LANs.
16. **Q: What is an ARP "cache flooding" attack?** A: An attacker floods the cache with bogus entries until it overflows → legitimate entries evicted (or on some stacks, the cache stops learning) → DoS by cache exhaustion. Mitigate by rate-limiting ARP and using static entries for critical hosts.
17. **Q (tricky): Can ARP work across routers?** A: No — ARP is strictly link-local (requests are broadcasts, replies don't cross routers). Each link does its own resolution; routers ARP for their own next hops. This is why proxy ARP was needed to "bridge" the illusion.

## 14. Follow-Up Questions
1. **Q: What's the difference between ARP and the DHCP lease?** A: DHCP assigns the *IP configuration* (address, mask, gateway, DNS) with a lease — how a host gets its identity. ARP resolves an *already-known* IP to a MAC for delivery — how a frame finds its target. DHCP gives you the IP; ARP finds the NIC.
2. **Q: How does NDP improve on ARP (beyond not being broadcast)?** A: NDP (ICMPv6) uses multicast (solicited-node) instead of broadcast (less wakeup), integrates router discovery (RS/RA — DHCP-less autoconfiguration), DAD, and reachability detection (neighbor unreachability tracking) into one protocol — a full "neighbor + router + config" stack vs ARP's single lookup.
3. **Q (tricky): How does gratuitous ARP cause address-conflict detection?** A: A host sends a GARP for its tentative address; if *anyone* replies, another host already owns that IP → the newcomer must choose a different address (RFC 5227). This "announce then check for a response" is how duplicate-IP detection works with zero server.
4. **Q: What is the BOOTP→DHCP lineage and why did it win over RARP?** A: RARP only gave an IP (per-MAC server table). BOOTP (RFC 951) delivered *config* (IP, mask, gateway, DNS) via broadcast/UDP to a central server. DHCP (RFC 2131) added *leases* (dynamic allocation + renewal) and option extensibility — modern dynamic configuration descends from this.
5. **Q (FAANG): "Why does my laptop get a working IP but no traffic flows after connecting to a new Wi-Fi?"** A: Classic ARP/neighbor problem: the new network's subnet/gateway changed; the stale ARP cache holds the *old* gateway's MAC (or the new gateway's ARP never succeeded). Fix: flush the cache (`ip neigh flush all`), verify the gateway's MAC with `ip neigh`, check the router's own ARP/table, and confirm the L2 (broadcast, VLAN) allows ARP. The symptom pattern (IP fine, no route) is almost always ARP-layer.

## 15. Coding Example
```python
# A minimal ARP request/reply over raw sockets (educational)
import socket, struct

def build_arp(opcode, sha, sip, tha, tip):
    # Ethernet frame: dst=ff:ff:ff:ff:ff:ff, src, ethertype=0x0806
    eth = b'\xff' * 6 + bytes.fromhex(sha.replace(':', '')) + b'\x08\x06'
    arp = struct.pack(">HHBBH", 1, 0x0800, 6, 4, opcode)
    arp += bytes.fromhex(sha.replace(':', '')) + socket.inet_aton(sip)
    arp += bytes.fromhex(tha.replace(':', '')) + socket.inet_aton(tip)
    return eth + arp

# Who-has 192.168.1.1? (broadcast)
req = build_arp(1, "aa:aa:aa:aa:aa:aa", "192.168.1.5",
                   "00:00:00:00:00:00", "192.168.1.1")
s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0806))
s.bind(("eth0", 0))
s.send(req)                       # the broadcast
reply = s.recv(2048)              # the unicast answer (requires root)
```
```bash
# The real toolkit
$ ip neigh show                       # ARP/neighbor table with states
#   192.168.1.1 dev eth0 lladdr 00:11:22:33:44:55 REACHABLE
$ arp -a                              # classic view
$ sudo tcpdump -i eth0 arp -nn        # watch requests/replies live
#   ARP, Request who-has 192.168.1.1 tell 192.168.1.5, length 46
#   ARP, Reply 192.168.1.1 is-at 00:11:22:33:44:55, length 46
$ sudo ip neigh flush all             # clear the cache (debugging trick)
$ cat /proc/net/arp                   # kernel table as text
```

## 16. Industry Usage
- **Every LAN/Ethernet/WiFi**: ARP is the invisible first packet of every conversation — home routers, enterprise switches, cloud VPCs (where the hypervisor's virtual switch does ARP/NDP for the VM's MAC) all depend on it.
- **Cloud virtual networks**: AWS/GCP/Azure VPCs implement ARP/NDP in their virtual switch; "IP reached, no MAC resolution" appears as "unreachable" in cloud diagnostics — the same ARP layer, virtualized.
- **HA/failover (VRRP, keepalived, LBs)**: gratuitous ARP is *the* mechanism that moves a virtual IP between nodes in seconds — L4 load balancers and database HA pairs live on it.
- **Enterprise security**: Dynamic ARP Inspection (DAI) + DHCP snooping on switches, static ARP for critical hosts, and 802.1X port auth — the defense stack against ARP poisoning.
- **Troubleshooting everywhere**: `arp -a`/`ip neigh` state (STALE/FAILED) is the first stop for "can't reach neighbor" — NOC and support playbooks start with it.
- **The RARP/BOOTP/DHCP lineage**: every dynamic IP (DHCP) in the world descends from RARP's question — the "helper protocols" family is the foundation of automatic configuration.

## 17. References
- RFC 826 — ARP: https://www.rfc-editor.org/rfc/rfc826
- RFC 5227 — IPv4 Address Conflict Detection (gratuitous ARP): https://www.rfc-editor.org/rfc/rfc5227
- RFC 903 — RARP: https://www.rfc-editor.org/rfc/rfc903
- RFC 951 — BOOTP: https://www.rfc-editor.org/rfc/rfc951
- RFC 2131 — DHCP: https://www.rfc-editor.org/rfc/rfc2131
- RFC 1027 — Proxy ARP: https://www.rfc-editor.org/rfc/rfc1027
- RFC 4861 — NDP (IPv6 replacement): https://www.rfc-editor.org/rfc/rfc4861
- Kurose & Ross, *Computer Networking*, Ch. 5 §5.4 (ARP).

## 18. Cheat Sheet
- ARP: IP→MAC on a broadcast link; request (broadcast) → reply (unicast); both sides + snoopers cache.
- Fields: htype=1, ptype=0x0800, HLEN/PLEN, opcode 1=req/2=rep, sender+target HA/IP (28 B).
- Cache: ~30 s–4 min (`ip neigh`); GARP refreshes instantly; RFC 5227 detects duplicates.
- Gateway case: ARP resolves the *gateway's* MAC, not the destination's.
- Gratuitous ARP: unsolicited announce (failover, IP change).
- Proxy ARP: router answers for a remote host (legacy).
- Spoofing/poisoning: unauthenticated replies → MITM; defend with DAI + static ARP + 802.1X.
- RARP (MAC→IP) obsolete → BOOTP → DHCP.
- IPv6: NDP (NS/NA multicast, RS/RA, DAD) replaces ARP.
- No ARP reply → retry → "host is down"; check `ip neigh` states.

## 19. Quiz
1. ARP resolves: a) MAC→IP b) IP→MAC c) name→IP d) IP→route → **b**
2. ARP request goes: a) unicast b) broadcast c) multicast d) anycast → **b**
3. ARP reply goes: a) broadcast b) unicast c) multicast d) no reply → **b**
4. For a remote destination, ARP resolves the: a) destination MAC b) gateway MAC c) DNS d) router IP → **b**
5. Gratuitous ARP is used for: a) discovery b) announcing IP→MAC / failover c) routing d) DNS → **b**
6. RARP does: a) IP→MAC b) MAC→IP c) name→IP d) route→IP → **b**
7. RARP was replaced by: a) ARP b) BOOTP/DHCP c) NDP d) ICMP → **b**
8. IPv6's ARP replacement: a) IGMP b) NDP c) DHCPv6 d) RARP → **b**
9. ARP spoofing is mitigated by: a) ip_forward b) DAI + static ARP c) TTL d) MSS → **b**
10. Proxy ARP: a) router answers for remote host b) switch caches c) GARP d) RARP → **a**

## 20. Flashcards
- **Q: What does ARP do?** → **A:** resolves IP→MAC on a broadcast link.
- **Q: Request/reply?** → **A:** request broadcast, reply unicast; both cache.
- **Q: Gateway case?** → **A:** ARP resolves the next-hop gateway's MAC.
- **Q: Gratuitous ARP?** → **A:** unsolicited announce (failover, IP change, dup detection).
- **Q: ARP spoofing?** → **A:** unauthenticated replies → MITM; defend with DAI/static.
- **Q: RARP?** → **A:** MAC→IP, obsolete → BOOTP → DHCP.
- **Q: IPv6 version?** → **A:** NDP (NS/NA, RS/RA, DAD) via ICMPv6.
- **Q: No ARP reply means?** → **A:** host off/wrong MAC/firewall; "host is down".

## 21. Revision
ARP resolves IP→MAC on broadcast links (request broadcast → reply unicast → cache ~30 s–4 min). For remote traffic, it resolves the *gateway's* MAC. Gratuitous ARP announces/refreshes (failover, dup detection RFC 5227); proxy ARP is legacy. ARP is unauthenticated → spoofing/MITM → defend with DAI/static/802.1X. RARP (MAC→IP) obsolete → BOOTP → DHCP. IPv6: NDP (NS/NA, RS/RA, DAD) via ICMPv6 replaces ARP. Debug with `ip neigh` (states), tcpdump arp; flush cache to fix stale mappings.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is ARP / why needed?" | 2 How It Works / 7 Formal Definition |
| "When does ARP run / gateway case?" | 13 Q&A / 8 Example |
| "Gratuitous ARP?" | 13 Q&A / 9 Internal Working |
| "ARP spoofing + defenses?" | 13 Q&A / 12 Disadvantages |
| "RARP / BOOTP / DHCP lineage?" | 13 Q&A / 14 Follow-Up |
| "ARP vs NDP (IPv6)?" | 13 Q&A / 16 Industry Usage |
| "No route to host — ARP check?" | 13 Q&A / 15 Coding |
| "Failover recovery — why slow?" | 13 Q&A / 14 Follow-Up |
