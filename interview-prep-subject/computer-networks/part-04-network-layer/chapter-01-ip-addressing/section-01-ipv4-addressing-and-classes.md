# IPv4 Addressing and Classes

> **TL;DR**: IPv4 is a 32-bit hierarchical address (4 octets, dotted decimal) that locates a host on the Internet — originally split into **classful** blocks (A/B/C with fixed 8/16/24-bit network parts), now allocated via **CIDR**; private ranges (10/8, 172.16/12, 192.168/16), loopback (127/8), and special-purpose addresses complete the ecosystem, and the 4.3B-address space is exhausted, driving IPv6.

## 1. Why Does This Exist?
A packet needs a **globally unambiguous locator** — if two machines answer to the same address, delivery is ambiguous; if no machine answers, it's unroutable. The network layer's job ("get this datagram to the right host, anywhere in the world") requires an address that is (a) **unique** (no two hosts share it), (b) **hierarchical** (the prefix narrows the destination continent → country → ISP → subnet, so routers don't need per-host tables — they route by *prefix*), and (c) **self-describing enough** for packet forwarding. IPv4's 32-bit address was chosen in 1981 as "enough" (4.3 billion); the *hierarchical* design (network part + host part) is what makes the Internet's routing tables — ~1M routes, not 4B host routes — possible. Addressing exists to convert "deliver this to the right device anywhere" into a scalable, prefix-based forwarding problem.

## 2. How Does It Work?
- **32-bit address, 4 octets**: `11000000 10101000 00000001 00000001` = `192.168.1.1` (dotted decimal). Bits: network portion (left) + host portion (right).
- **Classful addressing (1981)**: fixed boundaries — Class A: first bit 0 → network 8 bits, host 24 bits (16.7M hosts each); Class B: first bits 10 → 16/16 (65,534 hosts); Class C: first bits 110 → 24/8 (254 hosts); Class D: 1110 → multicast; Class E: 1111 → reserved.
- **Private (RFC 1918)**: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 — non-routable on the public Internet, reused inside enterprises (with NAT).
- **Special**: loopback 127.0.0.0/8 (localhost); link-local 169.254.0.0/16 (APIPA); broadcast 255.255.255.255; multicast 224.0.0.0/4; documentation 192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24.
- **CIDR (1993, RFC 4632)**: replaced classful with arbitrary prefix length — `10.0.0.0/8`, `192.168.1.0/24`; allocation and route summarization follow real need.
- **NAT (RFC 3022)**: one public IP multiplexes many private hosts (see part-04 chapter-04) — the pragmatic answer to exhaustion.
- **Exhaustion timeline**: IANA pool exhausted Feb 2011; ARIN exhausted Sep 2015; RIPE exhausted Nov 2019 — new allocations now come from returned/reclaimed space.

## 3. When Is It Used?
- **Every IP packet, always**: source + destination address in the IPv4 header; routers forward by longest-prefix match on the destination.
- **Configuration**: static IP vs DHCP-assigned; `ip addr`/`ipconfig` show the address + mask; interfaces bind addresses.
- **Private networks**: offices, homes, clouds use RFC 1918 + NAT for Internet access — the *dominant* real-world model.
- **Diagnostics**: ping/traceroute need a valid address; `whois`/RDAP lookup ownership; routing tables (`ip route`) are prefix tables.
- **Access control**: security groups/firewalls allow/deny by IP+port; geo-blocking by address ranges.
- **Address planning**: subnet allocation per department/VPC/pod; IPAM tools track usage; exhaustion → IPv6 or renumbering.

## 4. Why Wasn't Another Approach Chosen?
- **Why 32 bits?** In 1981, a 32-bit field ("4 billion" = "more than enough") was a reasonable engineering bet on the then ~200-host Internet. The *real* design goal wasn't raw size — it was **hierarchy** (prefix routing) and **simplicity** (fixed-size field, easy arithmetic). 64/128 bits were considered and rejected as wasteful then; hindsight says the bet was wrong, which is exactly why IPv6 went to 128 bits.
- **Why hierarchical (network+host) instead of flat?** Flat addressing (every host unique, no structure) means routers must know *every host* — millions × 4B = impossible tables. Hierarchy lets a router forward by a *prefix* ("anything in 8.0.0.0/8 → that direction") and *aggregate* routes. This is the single most important design decision in networking.
- **Why classful then CIDR?** Classful was simple (boundary implied by the first bits) but wasteful: a Class C (254 hosts) for a 20-host department, a Class B (65K hosts) for a 2K-host company. CIDR's *arbitrary* prefix (RFC 4632) lets you allocate exactly what you need and *summarize* routes hierarchically — it's classful with the rigidity removed.
- **Why not MAC-address-only?** MACs are flat, burned into hardware, and *not hierarchical* — they can't be aggregated, so no router could scale. IP's hierarchical locator is what routing needs; ARP bridges the two (IP → MAC on a link).
- **Why private + NAT instead of just IPv6?** IPv6 is the "right" answer but requires renumbering, new routing, and IPv6-aware apps everywhere — slow. RFC 1918 + NAT was a *deployable* stopgap that kept IPv4 viable for decades (at the cost of end-to-end transparency).

## 5. Intuition
An IP address is a **street address with a zip code hierarchy**: `192.168.1.5` is "zip 192.168.1 (the subnet), house 5 (the host)". The postal system routes *by zip* — a letter to "192.168.1.anything" goes to the same regional hub, which then delivers to the specific house. That's prefix routing: routers read the *zip* (network bits) to decide the direction, and only the last hop reads the *house number*. The classful system was like fixed-size zips (some zips absurdly large — a Class A "zip" could cover a country); CIDR is flexible zips (a /24 is a town, a /8 a continent-scale block). Private addresses are "internal mail that must not leave the building" (NAT is the doorman who rewrites the return address when it goes outside).

## 6. Real-World Analogy
**A worldwide postal system with street numbers + zip codes**: Every building has a unique address (the host), and the zip code (network prefix) routes it: mail to "10001 New York" is sorted at a national hub, forwarded to the NYC facility, then the street deliverer reads the street number (host bits). The old classful system forced every town into one of three *rigid* zip sizes — tiny towns forced into giant zones (waste), big cities squeezed into small ones. CIDR allows *any-size* zones, so allocation matches reality and routes can be aggregated ("anything starting 8.x → this hub"). Private address blocks are *internal* postal codes used only inside a building — the doorman (NAT) writes a public return address on anything leaving. And the whole system's address book (4.3 billion numbers) has run out — hence the new system (IPv6) with an essentially infinite address book.

## 7. Formal Definition
IPv4 (RFC 791) is a 32-bit address space written as four octets in dotted decimal (e.g., 192.168.1.1). Classful addressing (RFC 791): Class A = first bit 0, 8-bit network / 24-bit host (1.0.0.0–127.0.0.0); Class B = 10, 16/16 (128.0.0.0–191.255.0.0); Class C = 110, 24/8 (192.0.0.0–223.255.255.0); Class D = 1110 (multicast 224.0.0.0–239.255.255.255); Class E = 1111 (reserved 240.0.0.0+). CIDR (RFC 4632): an address plus prefix length `a.b.c.d/n`, where the first n bits are the network and the rest the host; allocation is arbitrary-prefix. Private (RFC 1918): 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. Loopback 127.0.0.0/8; link-local 169.254.0.0/16; limited broadcast 255.255.255.255. IANA pool exhausted Feb 2011; RIR pools by 2019.

## 8. Example
```
Address:     192.168.1.5        = 11000000.10101000.00000001.00000101
Mask /24:    255.255.255.0      = 11111111.11111111.11111111.00000000
Network:     192.168.1.0        (host bits zeroed)  -> the subnet
First host:  192.168.1.1        (usually the gateway / router)
Last host:   192.168.1.254
Broadcast:   192.168.1.255      (all host bits one)
Hosts:       2^8 − 2 = 254      (network + broadcast not assignable)

Classful (pre-CIDR) view of the same number:
  192 → first bits "110" → Class C → network = 192.168.1, host = 5.
  A Class C block = exactly 254 usable hosts, no smaller, no larger.
```
The `ip addr` output on a typical Linux box:
```
$ ip addr show eth0
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> ...
    inet 192.168.1.5/24 brd 192.168.1.255 scope global eth0
```
`/24` is the modern way to say "the old Class C" — the same number of hosts, but expressed as a CIDR prefix instead of a class boundary.

## 9. Internal Working
1. **Hierarchical forwarding**: a router's table is a list of prefixes (`10.0.0.0/8 → eth0`, `0.0.0.0/0 → default`). On a packet, it does **longest-prefix match** — the most specific matching prefix wins. This is O(prefix bits) via a Patricia trie — not a per-host lookup.
2. **Local subnet determination**: a host ANDs its mask with destination → if the result equals its own network, it's on-link (ARP for the destination MAC); else → the gateway. The mask *is* the local/remote decision logic.
3. **ARP (on-link)**: to send within a subnet, the host resolves IP → MAC via ARP (see part-04 ch2).
4. **DHCP (configuration)**: on boot, a host broadcasts DHCP Discover → gets a lease (IP, mask, gateway, DNS) from the server — so "addressing" in practice is often *dynamic* (see part-02 DHCP section).
5. **NAT (public/private)**: private hosts send with private src; the gateway rewrites src to its public IP + a port mapping; the return packet is translated back (see part-04 ch4). The address on the wire is *not* the host's real one.
6. **Special handling**: loopback (127/8) never leaves the host; link-local (169.254/16) auto-configures when no DHCP; broadcast (255.255.255.255) floods the local link; multicast uses group membership (IGMP) not unicast routing.
7. **Renumbering**: because IP is a *locator*, changing networks means changing addresses (DHCP/renewal, NAT re-mapping) — the address-is-location model is why mobility was hard and IPv6's address independence (multiple addresses per host) helps.

## 10. Time Complexity
- **Forwarding lookup**: O(prefix length) worst case (trie walk) — effectively O(1) per packet in hardware (TCAM) at line rate. This is why "how many bits to look up" is a design lever: /24 lookup is 24 bits, trivial.
- **Table size**: classful = ~100K routes in the 90s; CIDR + aggregation keeps the global table ~1M routes (2024) *despite* billions of hosts — the whole reason hierarchy matters. Flat addressing would be 4B routes (impossible).
- **Address math**: subnetting = O(1) bitwise ops per computation.
- **Exhaustion**: 2^32 = 4,294,967,296 theoretical; ~usable less (multicast/reserved). The *scarcity* cost is operational (NAT, IPv6 migration), not computational.

## 11. Advantages
- **Simple, universal, mature**: 32-bit field, dotted-decimal, universally implemented; the entire industry's tooling assumes it.
- **Hierarchical = scalable**: prefix routing + aggregation keeps tables manageable at Internet scale — the design *is* the scalability.
- **Private/NAT ecosystem**: RFC 1918 + NAT gives unlimited internal addressing behind one public IP — practical, cheap, and works today.
- **Huge ecosystem**: subnetting, DHCP, NAT, firewalling, CDN anycast — all IPv4-native and battle-tested.
- **Learnable**: the /24 math, class history, and special ranges are a compact, well-documented body of knowledge (a common interview topic precisely because it's foundational).

## 12. Disadvantages
- **Exhausted**: no new public blocks; new services ride NAT or reclaimed space — a structural scarcity with real operational cost.
- **NAT breaks end-to-end**: inbound connections need port-forwarding; P2P needs hole punching; IP-based security/auditing is complicated by translated addresses; carrier-grade NAT (CGNAT, 100.64/10) degrades the experience further.
- **Classful legacy confusion**: "Class B/C" terminology persists and muddles CIDR discussions; old hosts/documents assume classes.
- **No built-in security**: IPv4 has no authentication/encryption (IPsec is an add-on); header options are weak; spoofing is trivial without egress filtering.
- **Renumbering pain**: locator semantics make mobility and multihoming awkward (connections die on IP change — see QUIC migration for the modern fix).
- **Waste**: broadcast/multicast/reserved blocks and /8 misallocations (the historic 7/8s) further reduce usable space.

## 13. Interview Questions
1. **Q: What is an IPv4 address and how is it structured?** A: A 32-bit number in four octets (dotted decimal, e.g., 192.168.1.1), split into a network prefix (routable) and a host part (local delivery).
2. **Q (tricky): Classful vs CIDR?** A: Classful (RFC 791) fixed the network boundary by the first bits — A=8, B=16, C=24 bits — wasting blocks (a 20-host company burning a 254-host Class C). CIDR (RFC 4632) uses an explicit prefix length (/n) for arbitrary boundaries — allocate exactly, summarize exactly. The Internet's table runs on CIDR + aggregation.
3. **Q: What are the private ranges?** A: RFC 1918: 10.0.0.0/8 (one Class A), 172.16.0.0/12 (16 Class Bs), 192.168.0.0/16 (256 Class Cs). Non-routable on the public Internet — reused behind NAT.
4. **Q: What is loopback?** A: 127.0.0.0/8 — the host addresses *itself* (127.0.0.1 = localhost); traffic never leaves the machine. Used for testing local services.
5. **Q (FAANG): Why is the address space exhausted when 2^32 ≈ 4.3 billion?** A: Because addresses are allocated hierarchically and wastefully: /8s handed out in blocks, multicast/reserved space set aside, NAT didn't exist when 16.7M-host Class As were granted to single orgs. Real usable space ≪ 4.3B, and IoT/mobile multiplied demand. IANA exhausted Feb 2011; RIRs by 2019.
6. **Q: What is a subnet mask and what does it do?** A: A 32-bit value whose 1-bits mark the network portion (e.g., 255.255.255.0 = /24). It lets a host/rout decide on-link vs gateway: `(dst & mask) == (my_net & mask)` → local.
7. **Q: What are the special addresses?** A: Loopback 127/8; link-local 169.254/16 (APIPA); limited broadcast 255.255.255.255; directed broadcast (all host bits 1); multicast 224.0.0.0/4; documentation 192.0.2/24, 198.51.100/24, 203.0.113/24; 0.0.0.0 (default/unassigned).
8. **Q (production): A host has 169.254.x.x. What does that mean?** A: Link-local (APIPA) — it failed to get a DHCP lease and auto-assigned itself; the DHCP server/network is the problem (cable, server down, no relay). A classic "why am I offline?" fingerprint.
9. **Q: What is the difference between public and private IP?** A: Public = globally routable (allocated by RIRs, used on the Internet); private (RFC 1918) = reused internally, never on the Internet — separated by NAT at the edge.
10. **Q (tricky): Can two devices on different private networks use the same IP?** A: Yes — 192.168.1.5 exists in millions of homes because they're *separate* broadcast domains, each hidden behind its own NAT. Uniqueness is required *within* a routing domain, not globally for privates.
11. **Q: What is a broadcast address?** A: 255.255.255.255 (limited, local link) or the all-host-bits-one address of a subnet (directed, e.g., 192.168.1.255 for /24) — delivers to every host on the network. DHCP/ARP rely on it.
12. **Q (FAANG): How does longest-prefix matching work?** A: Among all routes whose prefix matches the destination, forward via the *longest* (most specific) match — e.g., 10.0.0.0/8 and 10.1.0.0/16 both match 10.1.2.3; the /16 wins. Implemented with tries/TCAM for O(1)-ish lookups. This specificity-first rule is why aggregation + default routes coexist.
13. **Q: Why is 10.0.0.0/8 "a Class A private"?** A: Historically 10 was a Class A network (8-bit network); RFC 1918 reserved that entire /8 for private use — 16.7M internal hosts on a private "one network." The class terminology survives but the *usage* is CIDR.
14. **Q: What are multicast addresses?** A: 224.0.0.0–239.255.255.255 (Class D) — group-based delivery: senders transmit to a group address, only group members receive (IGMP manages membership). Used for streaming, discovery protocols (mDNS 224.0.0.251, NTP, routing protocols).
15. **Q (production): What is IPv4 exhaustion doing to real deployments?** A: New orgs get /24s at best (or none) → carrier-grade NAT (CGNAT 100.64/10), IPv6-only data centers + NAT64, address brokering/transfers, and heavy RFC 1918 reuse behind LBs — every cloud VPC is private-subnet + NAT by default.
16. **Q: What is the role of the mask in routing?** A: It defines *which bits matter* for the route: the mask in a route table entry (e.g., `192.168.1.0/24 via 192.168.1.1`) tells the router the entry's scope — the match is over masked bits only.
17. **Q (tricky): Why does the network address have all-zero host bits?** A: Because the network address *names the subnet itself* — it's the identifier used in routing tables, not an assignable host. All-zero host bits = "this network"; all-one = "everyone on this network" (broadcast). The −2 rule (hosts = 2^n − 2) follows.

## 14. Follow-Up Questions
1. **Q: What is CGNAT and why does it exist?** A: Carrier-grade NAT (RFC 6598, 100.64.0.0/10) — ISPs NAT many subscribers behind shared public IPs because IPv4 is gone. It's NAT at ISP scale: breaks P2P/gaming, complicates home port-forwarding, and is a *worse* version of the problem IPv6 solves properly.
2. **Q: What is APIPA / link-local and when does it trigger?** A: When DHCP fails, Windows/Linux auto-assign 169.254.x.x (link-local) so the host can still talk *on-link* — a diagnostic signal, not a working Internet connection. It's the same mechanism IPv6 uses properly (SLAAC, fe80::).
3. **Q (tricky): Why does an interface have multiple addresses (IPv4 + IPv6 + multiple IPs)?** A: Multiple addresses per interface are legal (address *families* + aliases): IPv6 coexists with IPv4 (dual-stack), plus link-local (fe80::), global IPv6, and secondary IPv4s (VIPs). "One IP per NIC" is a simplification — modern hosts hold a *set*.
4. **Q: How does DNS interact with addressing?** A: DNS maps names → addresses (A records for IPv4, AAAA for IPv6). On exhaustion/DNS64 (NAT64), names resolve to synthetic addresses that NAT64 translates — the *address choice* (v4 vs v6) is increasingly made at DNS resolution time.
5. **Q (FAANG): "Design an addressing plan for a company with 3,000 hosts across 5 sites."** A: Use private RFC 1918 (e.g., 10.0.0.0/16), carve per-site /19 or /20 subnets (each ~8K/4K hosts), per-VLAN /24s, reserve a /24 per site for network/infra, and one public /24 for egress NAT + servers; document ranges in IPAM. The interview tests subnet math + CIDR + hierarchy, not memorized answers.

## 15. Coding Example
```python
# IPv4 subnetting math — the questions interviewers actually ask
def subnet_info(prefix: str):
    addr_str, plen_str = prefix.split("/")
    plen = int(plen_str)
    addr = int.from_bytes([int(x) for x in addr_str.split(".")], "big")
    mask = (0xFFFFFFFF << (32 - plen)) & 0xFFFFFFFF
    net = addr & mask
    bcast = net | (~mask & 0xFFFFFFFF)
    def s(x):  # 32-bit int -> dotted quad
        return ".".join(str((x >> (8 * i)) & 0xFF) for i in (3, 2, 1, 0))
    hosts = (1 << (32 - plen)) - 2
    return dict(network=s(net), broadcast=s(bcast), mask=s(mask),
                prefix=f"/{plen}", usable_hosts=hosts,
                first_host=s(net + 1), last_host=s(bcast - 1))

print(subnet_info("192.168.1.0/24"))
print(subnet_info("10.0.0.0/28"))
# {'network': '192.168.1.0', 'broadcast': '192.168.1.255', ... 'usable_hosts': 254}
```
```bash
# The real-world addressing toolkit
$ ip addr show eth0                       # address + mask (192.168.1.5/24)
$ ip route show                           # longest-prefix table
#   192.168.1.0/24 dev eth0 proto kernel   <- on-link subnet
#   default via 192.168.1.1 dev eth0       <- gateway
$ ping -c 1 127.0.0.1                      # loopback
$ whois 8.8.8.8 | grep -i -E 'range|netname'   # ownership / allocation
$ ip neigh show                            # ARP cache: IP -> MAC on-link
```

## 16. Industry Usage
- **Cloud VPCs (AWS/Azure/GCP)**: every cloud network is private RFC 1918 CIDR planning — "VPC = 10.0.0.0/16, subnets /24 per AZ" is the standard blueprint; NAT gateways, security groups, and ALBs all key on the address/mask.
- **Enterprise IPAM (Infoblox, NetBox, phpIPAM)**: address planning, DNS+DHCP+IPAM integration, and IPv6 rollout tracking are core IT ops.
- **ISPs & carriers**: public prefix allocation, CGNAT (100.64/10), BGP announcements of customer prefixes, and IPv6 dual-stack deployment — exhaustion is *their* daily problem.
- **CDNs/anycast**: services announce the *same* IP from many locations (anycast) so clients route to the nearest; address planning + BGP are the platform.
- **Security**: firewalls/security groups filter by source/destination IP; egress filtering (BCP 38) blocks spoofed *source* addresses; geo-fencing and DDoS mitigation operate on address ranges.
- **The transition**: "IPv6-only data center + NAT64/DNS64" and dual-stack are now standard cloud/gov guidance — addressing strategy is a live deployment concern.

## 17. References
- RFC 791 — Internet Protocol: https://www.rfc-editor.org/rfc/rfc791
- RFC 1918 — Address Allocation for Private Internets: https://www.rfc-editor.org/rfc/rfc1918
- RFC 4632 — CIDR (classless inter-domain routing): https://www.rfc-editor.org/rfc/rfc4632
- RFC 6890 — Special-Purpose IP Address Registries: https://www.rfc-editor.org/rfc/rfc6890
- RFC 6598 — Shared Address Space (CGNAT): https://www.rfc-editor.org/rfc/rfc6598
- Kurose & Ross, *Computer Networking*, Ch. 4 §4.3 (IPv4 datagrams/addressing).
- IANA IPv4 address space registry: https://www.iana.org/assignments/ipv4-address-space

## 18. Cheat Sheet
- IPv4 = 32-bit, 4 octets, dotted decimal; network bits + host bits (mask).
- Classful: A /8, B /16, C /24 (by first bits). CIDR: arbitrary /n (RFC 4632).
- Private (RFC 1918): 10/8, 172.16/12, 192.168/16.
- Special: 127/8 loopback; 169.254/16 link-local; 255.255.255.255 broadcast; 224/4 multicast; 0.0.0.0 default.
- Hosts per prefix = 2^(32−n) − 2 (minus network + broadcast).
- Longest-prefix match wins; default route = 0.0.0.0/0.
- Exhaustion: IANA Feb 2011, RIRs by 2019 → NAT, CGNAT (100.64/10), IPv6.
- NAT: private hosts share one public IP; breaks end-to-end/inbound/P2P.
- `ip addr`, `ip route`, `ip neigh`, `whois` for the real view.

## 19. Quiz
1. IPv4 address size: a) 16 b) 32 c) 48 d) 128 → **b**
2. Class C network prefix bits: a) 8 b) 16 c) 24 d) 32 → **c**
3. Private range 192.168.0.0/16 is historically: a) Class A b) Class B c) Class C d) Class D → **c**
4. Loopback block: a) 10/8 b) 127/8 c) 169.254/16 d) 224/4 → **b**
5. Hosts in a /26: a) 62 b) 62? c) 64 d) 62 → **a** (2^6 − 2 = 62)
6. Longest-prefix match: a) /8 wins b) /24 wins c) first route d) default → **b**
7. IANA pool exhausted: a) 2011 b) 2015 c) 2019 d) 2023 → **a**
8. CGNAT range: a) 10/8 b) 100.64/10 c) 172.16/12 d) 192.0.2/24 → **b**
9. A host with 169.254.x.x likely: a) DHCP failed b) offline c) public d) multicast → **a**
10. Class D is: a) unicast b) multicast c) broadcast d) reserved → **b**

## 20. Flashcards
- **Q: IPv4 size/format?** → **A:** 32-bit, 4 octets, dotted decimal.
- **Q: Classful boundaries?** → **A:** A=8, B=16, C=24 network bits.
- **Q: Private ranges?** → **A:** 10/8, 172.16/12, 192.168/16.
- **Q: Loopback?** → **A:** 127/8 = the host itself.
- **Q: Usable hosts formula?** → **A:** 2^(32−n) − 2.
- **Q: Longest-prefix match?** → **A:** most specific prefix wins.
- **Q: Exhaustion timeline?** → **A:** IANA 2011, RIRs 2019.
- **Q: CGNAT?** → **A:** 100.64/10 ISP-level NAT (RFC 6598).

## 21. Revision
IPv4 = 32-bit hierarchical locator (network + host). Classful fixed A/B/C boundaries wasted space; CIDR (RFC 4632) uses arbitrary /n prefixes + aggregation → scalable tables via longest-prefix match. Private RFC 1918 ranges behind NAT, loopback 127/8, link-local 169.254/16, broadcast, multicast 224/4. Exhausted (2011/2019) → NAT/CGNAT (100.64/10) → IPv6. Hosts = 2^(32−n) − 2. Debug with ip addr/route/neigh, whois.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Classful vs CIDR?" | 2 How It Works / 13 Q&A |
| "Private ranges / special addresses?" | 13 Q&A / 7 Formal Definition |
| "Why is IPv4 exhausted?" | 13 Q&A / 12 Disadvantages |
| "What is a subnet mask?" | 13 Q&A / 9 Internal Working |
| "Longest-prefix matching?" | 13 Q&A / 10 Time Complexity |
| "What is CGNAT / APIPA?" | 14 Follow-Up / 13 Q&A |
| "Design an addressing plan." | 13 Q&A / 15 Coding |
| "How do clouds do VPC addressing?" | 16 Industry Usage |
