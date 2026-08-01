# Subnetting and CIDR

> **TL;DR**: Subnetting carves an IP block into smaller, routable networks using a subnet mask; **CIDR** (RFC 4632) expresses any block as a prefix length (`192.168.1.0/28`) so you allocate exactly the hosts you need. The math — masks, network/broadcast ranges, host counts, VLSM, aggregation — is the most numerically-intensive interview topic in networking.

## 1. Why Does This Exist?
A single flat IP block (say, 10.0.0.0/8 with 16.7 million hosts on "one network") is useless: a broadcast there reaches every host; routing can't isolate traffic; a loop or failure affects everything; and you can't delegate. **Subnetting** exists to (a) **contain broadcast/ARP scope** (only hosts in the same subnet hear each other's broadcasts), (b) **create routing boundaries** (subnets are routable units — different subnets need a router, giving security/ACL granularity), (c) **delegate control** (give each department/VPC/pod its own block), and (d) **use address space efficiently** (a /24 for 20 hosts is wasteful; a /27 fits). **CIDR** exists because classful boundaries were too rigid — arbitrary prefix lengths let you both *right-size* allocations and *aggregate* routes (advertise 10.1.0.0/16 instead of 256 × /24 routes), keeping the Internet's routing table small. Subnetting + CIDR = "exact-sizing + summarizing" — the two halves of scalable addressing.

## 2. How Does It Work?
- **Subnet mask**: a 32-bit value with `1`-bits over the network portion. `192.168.1.0/24` = mask `255.255.255.0` (24 ones). The mask *defines* the subnet boundary.
- **Network address**: address AND mask (host bits = 0) — names the subnet.
- **Broadcast**: address OR NOT mask (host bits = 1) — delivers to all hosts in the subnet.
- **Usable hosts**: `2^(32−prefix) − 2` (subtract network + broadcast). /24 → 254; /30 → 2 (point-to-point); /31 → 0 (RFC 3021 allows /31 for P2P, no broadcast).
- **Prefix ↔ mask**: /n = n ones. /24 = 255.255.255.0, /28 = 255.255.255.240 (last octet 11110000 = 240), /16 = 255.255.0.0.
- **Subnet enumeration**: given a block and a target prefix, subnets increment by `2^(32−target)`. 192.168.1.0/24 → four /26s (0, 64, 128, 192) — each with 62 hosts.
- **VLSM (Variable Length Subnet Masking)**: different subnets of one block can have different sizes (/27 for a 20-host team, /30 for a link) — the pre-CIDR "one size" rule is gone.
- **Aggregation (route summarization)**: adjacent smaller prefixes merge into one: 10.1.0.0/24 + 10.1.1.0/24 + 10.1.2.0/24 + 10.1.3.0/24 = 10.1.0.0/22 (they share a 22-bit prefix).
- **Supernetting/CIDR blocks**: an ISP hands a customer 203.0.113.0/24; the customer subnets it internally and the ISP advertises the /24 (not the subnets).

## 3. When Is It Used?
- **Every network design**: home router (192.168.1.0/24), office VLANs, cloud VPCs (10.0.0.0/16 split into per-AZ /24s), data-center racks (each rack a /24).
- **The DHCP pool**: a subnet's usable range is exactly what DHCP hands out; you need the math to size pools.
- **Routing tables**: `ip route` shows prefix/mask entries; longest-prefix match resolves overlaps.
- **ACLs/security groups**: "allow 10.0.1.0/24" — the CIDR is the security boundary syntax.
- **Interview whitespace problems**: "split 192.168.0.0/24 into 4 subnets; how many hosts each?" — pure prefix arithmetic.
- **Route aggregation in BGP**: ISPs advertise summarized prefixes; VPC peering summaries; cloud route tables.
- **IPAM/planning tools**: NetBox/phpIPAM auto-compute ranges from a prefix plan.

## 4. Why Wasn't Another Approach Chosen?
- **Why masks/prefixes instead of fixed-size classes?** Classes gave only three sizes (254/65K/16.7M hosts) — absurd granularity. A mask is *just data* (a 32-bit field) so any boundary is expressible — the router compares mask bits, no special-casing by first bits. Masks generalized classes; CIDR finished the job.
- **Why prefix length (`/n`) notation instead of dotted mask everywhere?** `/24` is unambiguous and compact; `255.255.255.0` is only needed at configuration layers. The notation *is* the count of network bits — one number, no confusion.
- **Why VLSM instead of one subnet size?** Real networks mix point-to-point links (/30 or /31), small teams (/28), and big subnets (/16). Fixed-size subnetting wastes the small blocks. VLSM is "right-size each subnet" — required for efficiency on scarce IPv4.
- **Why aggregate routes instead of advertising every subnet?** Route count = table size = memory + lookup cost + convergence time. Summarization collapses N routes into one — the trick that keeps the global BGP table ~1M instead of billions of host routes. Cost: a summarized route can only be *contiguous* and share a prefix.
- **Why −2 for network+broadcast?** The all-zeros host bits *name the subnet* (used in routing tables) and all-ones is the broadcast address (needed for local delivery) — neither is a usable host. RFC 3021 waives this for /31 (P2P) where both addresses are used.

## 5. Intuition
An IP block is like a **street grid you can re-zone**: a /24 is a neighborhood with 256 house numbers. Subnetting is *cutting the block into smaller neighborhoods* — a /26 is a street of 64 houses. The mask is the **boundary marker** (how many leading digits name the street vs the house). You count "houses" as `2^(remaining digits) − 2` because the first number (all zeros) is reserved to *name* the street and the last (all ones) is the "everyone on the street" broadcast. CIDR is just saying the boundary with a slash-number instead of a dotted mask. Aggregation is **merging adjacent streets back into one zip code** for the postal system's route book — fewer entries, but the streets must actually be adjacent (share a prefix). Every subnetting problem is this zoning arithmetic: pick the street size that fits, cut, and compute each street's name, range, and broadcast.

## 6. Real-World Analogy
**A hotel with numbered wings and floors**: The full address is "Wing 1, Floor 3, Room 7." The *wing* is the big prefix (10.0), the *floor* the middle (subnet — 10.0.3), the *room* the host (10.0.3.7). The mask is the hotel's convention for "how many of these digits are wing+floor vs room" — some buildings have 2-digit rooms (smaller mask → more rooms per floor), others 1-digit (bigger mask → fewer rooms, more floors). Cutting a wing into floors = subnetting; the floor's first room is reserved to *label the floor* (network) and the last to broadcast to everyone on the floor. The bell desk (router) needs only the *floor* to route a letter — it doesn't memorize rooms. When the hotel merges two adjacent wings into one corridor (route aggregation), the bell desk updates one entry instead of two — but only if the wings are truly adjacent. Every interview subnet problem is just "how many floors/rooms fit, and what are their labels?"

## 7. Formal Definition
Subnetting divides an IP network into smaller networks (subnets) by extending the network prefix beyond its natural boundary: a subnet mask (or prefix length /n) marks the network bits; the network address = address AND mask; broadcast = network OR (NOT mask); usable hosts = 2^(32−n) − 2. CIDR (RFC 4632) represents any block as `address/n` (n = prefix bits, 0–32), enabling variable-length subnetting (VLSM) and route aggregation/supernetting (adjoining prefixes merged: 10.1.0.0/24..10.1.3.0/24 → 10.1.0.0/22). Longest-prefix match governs forwarding among overlapping prefixes. RFC 3021 permits /31 point-to-point links (both addresses usable). IPv6 uses the same prefix concept (RFC 4291): /64 subnets, /48 site allocations, /128 host.

## 8. Example
The classic split:
```
Given: 192.168.1.0/24  (mask 255.255.255.0, 254 usable)
Split into 4 equal subnets → each a /26 (mask 255.255.255.192 = 11000000):

Subnet   Network        First host     Last host      Broadcast    Hosts
1       192.168.1.0     192.168.1.1    192.168.1.62   192.168.1.63   62
2       192.168.1.64    192.168.1.65   192.168.1.126  192.168.1.127  62
3       192.168.1.128   192.168.1.129  192.168.1.190  192.168.1.191  62
4       192.168.1.192   192.168.1.193  192.168.1.254  192.168.1.255  62

Why /26? We need 4 subnets → 2 extra bits (2^2 = 4) → /24 + 2 = /26.
Increment: 2^(32−26) = 64 per subnet. Hosts each: 2^6 − 2 = 62.
```
Aggregation (the reverse):
```
Advertise 10.1.0.0/24 + 10.1.1.0/24 + 10.1.2.0/24 + 10.1.3.0/24
  → all share the top 22 bits (000000 | 00000010 00000000 = 10.1.000000)
  → summarize as 10.1.0.0/22  (4 × /24 = one /22)
```
These two directions — *split* (subnet) and *merge* (aggregate) — are the entire skill.

## 9. Internal Working
1. **Masks in config**: an interface's `ip addr add 192.168.1.5/24` stores the address *and* the mask; the kernel derives the on-link network (192.168.1.0/24) and adds it to the route table automatically.
2. **On-link vs gateway decision**: for a destination, `dest & mask == iface_net`? → ARP for the MAC on-link; else → forward to the gateway (the router). One AND per packet.
3. **Router forwarding**: the FIB is prefix-based; longest-prefix match via trie/TCAM. Overlapping routes resolve to the most specific — this *is* how subnets of a block can each route differently.
4. **DHCP scoping**: a DHCP server has a *pool* scoped to a subnet (range + mask + gateway); it leases within the usable range and never assigns network/broadcast.
5. **VLSM practical**: plan big-first (large subnets first, then smaller) so leftover space stays contiguous; e.g., carve 10.0.0.0/24 into /25 + two /26s + a /30 without fragmentation.
6. **Aggregation in BGP**: an ISP announces a summarized customer prefix (/22) rather than subnets; on the Internet, providers summarize their own blocks the same way — table growth is *fought* by aggregation.
7. **IPv6 parallel**: subnets are /64 (2^64 hosts!); sites get /48; hosts /128. The concept is identical — prefix, network address, and (no broadcast! IPv6 has multicast all-nodes ff02::1 instead).

## 10. Time Complexity
- **Forwarding**: O(1)-ish per packet (trie walk ≈ prefix bits; TCAM = constant). The *mask* is an O(1) AND per lookup.
- **Route table size**: directly the reason for aggregation — 1M global routes (2024) vs the 4B+ host routes that flat addressing would demand. Each summarized prefix *divides* table memory.
- **Subnet math**: O(1) per subnet; planning = enumerate subnets (O(subnet count)).
- **Convergence**: smaller aggregates = fewer routes to flood/withdraw in BGP = faster convergence. This is why "summarize your routes" is standard practice.
- **IPv6**: prefix math is identical but with 128-bit widths — same O(1), trivially more bits to walk (still TCAM-able with wider entries).

## 11. Advantages
- **Isolation**: broadcasts/ARP contained per subnet; failures, loops, and traffic don't cross boundaries without a router.
- **Security granularity**: ACLs/security groups reference subnets — "deny 10.0.1.0/24" is the unit of policy.
- **Efficiency**: VLSM right-sizes every allocation (no wasted /24 for a 10-host team); the scarce IPv4 space is used sparingly.
- **Scalability**: aggregation keeps routing tables small — the Internet's tables *are* the aggregation story.
- **Delegate-able**: hand each team/VPC/pod its own /xx and they manage internally — organization mirrors addressing.
- **Simple math**: prefix arithmetic is deterministic and toolable (any calculator/IPAM does it).

## 12. Disadvantages
- **Complexity/errors**: hand-computed masks → misconfigurations (overlapping subnets, broadcast/non-usable ranges, wrong gateway) are a classic source of "why can't host A reach host B."
- **IPv4 scarcity pressure**: efficient subnetting matters so much precisely because space is scarce — you plan at /24 granularity and re-justify.
- **Aggregation limits**: summarized routes must be contiguous and aligned — non-contiguous subnets *can't* be summarized (an operational constraint).
- **Over-subnetting**: too many tiny subnets → more routes, more NAT/ACL rules, more admin burden — the opposite of the benefit.
- **Legacy confusion**: classful terminology, "network vs subnet" mixing, and the −2 rule trip up newcomers; masks vs prefix notational drift in tools.

## 13. Interview Questions
1. **Q: What is a subnet?** A: A logical subdivision of an IP network, defined by extending the prefix (mask); it's a routing/broadcast/security boundary. Hosts in the same subnet reach each other directly (ARP); others need a router.
2. **Q (tricky): What is a subnet mask and what does it do?** A: A 32-bit value marking the network bits (ones) vs host bits (zeros). It enables the on-link/gateway decision (`dest & mask`) and defines the network/broadcast/usable range.
3. **Q: How many hosts in a /28? A /30? A /31?** A: /28 → 2^4 − 2 = 14; /30 → 2^2 − 2 = 2; /31 → 2^1 − 2 = 0, but RFC 3021 allows both addresses for point-to-point links.
4. **Q: Split 192.168.1.0/24 into 4 subnets.** A: Each /26 (24+2 bits). Increment 64: .0–.63, .64–.127, .128–.191, .192–.255; 62 usable hosts each; network = first, broadcast = last.
5. **Q (FAANG): Why is CIDR better than classful addressing?** A: Classful fixed the boundary (A/B/C), wasting space and forcing huge allocations. CIDR (RFC 4632) allows any prefix → exact-size allocations (VLSM) and route aggregation (supernetting) → the Internet's routing table stays manageable.
6. **Q: What is VLSM and why do we need it?** A: Variable-length subnet masking — different subnets of a block can have different sizes (a /30 for a P2P link, a /27 for a team). Without it, one size fits all → wasted addresses.
7. **Q: What is route aggregation / summarization?** A: Merging contiguous prefixes that share a longer prefix into one route: 10.1.0.0/24–10.1.3.0/24 → 10.1.0.0/22. Fewer routes, smaller tables, faster convergence.
8. **Q (tricky): Can you aggregate 10.1.0.0/24 and 10.1.2.0/24?** A: No — they're not contiguous under one prefix (10.1.1.0/24 sits between them); the shared prefix that covers both would also cover 10.1.1.0/24 (i.e., /23 = 10.1.0.0–10.1.1.255, not both). Aggregation requires *adjacency*.
9. **Q: What is the network address and why can't hosts use it?** A: The address with all host bits zero — it *names* the subnet (used in routing/DHCP config). Assigning it to a host would collide with the subnet's identifier.
10. **Q (production): Two hosts on 192.168.1.5/24 and 192.168.1.70/24 but can't ping. What's wrong?** A: Same subnet → should be on-link (ARP works). The typical break: different *masks* (one thinks /25, the other /24 → different on-link views), a gateway in the way, or a firewall/ACL. Verify masks match and the subnet math agrees.
11. **Q: What is the broadcast address?** A: All host bits one (e.g., 192.168.1.255 for /24) — delivers to every host in the subnet (used by DHCP, ARP, discovery). 255.255.255.255 is the *limited* broadcast (local link only).
12. **Q (FAANG): How does longest-prefix matching interact with subnets?** A: Overlapping prefixes (a /24 containing /26s) are resolved by specificity: a packet for 192.168.1.5 matches both 192.168.1.0/24 and 192.168.1.0/26 → the /26 (longest) wins. This is how a subnet's route overrides its parent.
13. **Q: What's a /30 good for?** A: Point-to-point links between routers (2 usable addresses — one per side; the classic "link subnet"). /31 (RFC 3021) is the modern alternative using both addresses.
14. **Q (tricky): Why is 255.255.255.0 the same as /24?** A: Both encode "24 leading ones then 8 zeros" — the mask is the dotted form, /24 the shorthand. The prefix is the count of network bits; the mask is its spelling.
15. **Q: How many /26s fit in a /24? How many /27s?** A: Each /26 = 2× the size of a /27; a /24 = 4 × /26 = 8 × /27. General rule: each extra prefix bit doubles the subnet count and halves the host count.
16. **Q (production): You're assigned 203.0.113.0/24 and need subnets for 3 VLANs of ~60 hosts and 2 point-to-point links. Plan it.** A: 4 × /26 (62 hosts each) covers the VLANs with one spare; 2 × /30 for the links (or /31s). Layout: VLANs at .0, .64, .128, spare .192; links at .240 and .244 (/30s) — VLSM in one /24.
17. **Q: What is the difference between a network and a subnet?** A: A network is any prefix block; a subnet is a network *derived* from a larger block (extended prefix). Functionally identical — the terms differ by direction (parent vs child).

## 14. Follow-Up Questions
1. **Q: How does subnetting interact with DHCP?** A: A DHCP scope must map to exactly one subnet (range + mask + gateway + DNS). Wrong scope → host gets an address in a different subnet → no connectivity (the "DHCP gave me the wrong network" classic).
2. **Q: What is CIDR aggregation in BGP specifically?** A: An ISP or cloud advertises a summarized prefix (e.g., 10.1.0.0/22 or the provider's whole /16) instead of each /24; peers receive fewer routes → smaller tables + faster convergence. "Summarize at every boundary" is the rule.
3. **Q (tricky): What happens if two subnets overlap?** A: Routing ambiguity: longest-prefix match picks the more specific, but the *other* block's hosts become unroutable-or-misrouted; DHCP conflicts; ARP storms. Overlap is a top misconfiguration cause — IPAM tools exist to prevent it.
4. **Q: How does IPv6 subnetting differ?** A: Same prefix concept, but /64 subnets are the norm (2^64 hosts — no broadcast, multicast all-nodes instead), sites get /48, hosts /128. The "planning" is about *prefix delegation* and hierarchy, not conserving hosts (no scarcity).
5. **Q (FAANG): "Design a subnet plan for 1,000 hosts in 8 locations with 4 VLANs each."** A: Reserve 10.0.0.0/16: per-location /19 (8 × /19 = 8K hosts each — overkill, so use /20 ≈ 4K); per-VLAN /24 within; /30s for site links; aggregate at the core (site /20s). Interview scores the *hierarchy + math + summary*, not a single right answer.

## 15. Coding Example
```python
# CIDR math, implemented — hosts, ranges, splits, aggregation
def hosts(n): return 2 ** (32 - n) - 2

def split(prefix, parts):
    addr_s, plen = prefix.split("/"); plen = int(plen)
    base = int.from_bytes([int(x) for x in addr_s.split(".")], "big")
    bits = (32 - plen).bit_length() - 1          # bits to borrow for `parts` (power of 2)
    new_plen = plen + bits
    step = 2 ** (32 - new_plen)
    return [f"{to_dotted(base + i * step)}/{new_plen}" for i in range(2 ** bits)]

def to_dotted(v): return ".".join(str((v >> (8 * i)) & 0xFF) for i in (3, 2, 1, 0))

print(hosts(26))            # 62
print(split("192.168.1.0/24", 4))   # 4 x /26 subnets
print(split("10.0.0.0/16", 256))    # 256 x /24

def aggregate(prefixes):              # merge contiguous /24s -> /22 if aligned
    nets = [int.from_bytes([int(x) for x in p.split("/")[0].split(".")], "big")
            for p in prefixes]
    lo = min(nets); hi = max(nets)
    for plen in range(24, 15, -1):
        if lo % (2 ** (32 - plen)) == 0 and (hi - lo) == (2 ** (32 - plen)) - 1:
            return f"{to_dotted(lo)}/{plen}"
    return None
print(aggregate(["10.1.0.0/24", "10.1.1.0/24", "10.1.2.0/24", "10.1.3.0/24"]))  # 10.1.0.0/22
```
```bash
# The real toolkit
$ ip addr add 192.168.50.7/25 dev eth0        # config an interface with mask
$ ip route | grep 192.168.50                    # on-link route auto-added: 192.168.50.0/25
$ sipcalc 192.168.1.0/24                        # full subnet math (net/bcast/hosts)
$ ipcalc 10.0.0.0/16 | grep -A4 Subnets        # split visualizer
```

## 16. Industry Usage
- **Cloud VPC design (AWS/GCP/Azure)**: "VPC 10.0.0.0/16, a /24 per AZ, a /27 per service tier" — subnetting is the *skeleton* of cloud architecture; route tables, NACLs, and security groups all key on CIDR blocks.
- **Enterprise/DC networking**: VLAN-per-/24, rack subnets, core aggregation — standard IPAM (NetBox/Infoblox) plans; link /30s/31s between switches/routers.
- **ISP & carrier**: public prefix allocation (/24s to customers), summarization before advertising to BGP peers, and CGNAT 100.64/10 planning — aggregation is how ISPs keep the global table bounded.
- **Security**: CIDR is the ACL/security-group syntax ("allow 10.0.0.0/8 from VPC"), WAF/geo rules, and egress filtering operate on prefix ranges.
- **Kubernetes/containers**: pod CIDR and service CIDR are explicit /16 or /12 ranges; CNI allocates per-node /24s — networking-at-scale is literally a subnet-planning exercise.
- **IPv6 planning**: /48 per site, /64 per subnet, no NAT — the same discipline, no scarcity.

## 17. References
- RFC 4632 — CIDR: https://www.rfc-editor.org/rfc/rfc4632
- RFC 3021 — Using 31-bit prefixes on IPv4 P2P links: https://www.rfc-editor.org/rfc/rfc3021
- RFC 4291 — IPv6 Addressing Architecture (prefix model): https://www.rfc-editor.org/rfc/rfc4291
- RFC 1918 — private ranges (used by subnet plans): https://www.rfc-editor.org/rfc/rfc1918
- Kurose & Ross, *Computer Networking*, Ch. 4 §4.3 (subnetting/CIDR).
- Linux tools: `ipcalc`, `sipcalc`, `ip`, `iproute2`.

## 18. Cheat Sheet
- Prefix /n = n network bits; mask = n ones then zeros (255.255.255.0 = /24).
- Hosts = 2^(32−n) − 2 (network + broadcast reserved); /31 P2P excepted (RFC 3021).
- Network = addr AND mask; broadcast = network OR NOT mask.
- Split: extra bits double subnet count, halve hosts. /24 = 4 × /26 = 8 × /27 = 16 × /28.
- Step between subnets = 2^(32−new_prefix).
- Aggregate: merge contiguous aligned prefixes sharing a longer prefix (4 × /24 = /22).
- Longest-prefix match wins for overlapping routes.
- VLSM = different sizes per subnet (plan big → small to avoid fragmentation).
- Typical: /30-31 P2P links, /26-27 teams, /24 standard subnet, /16 site, /8 private.
- ipcalc/sipcalc/`ip` for the math; IPAM tools for planning.

## 19. Quiz
1. /24 mask: a) 255.255.0.0 b) 255.255.255.0 c) 255.255.255.240 d) 255.0.0.0 → **b**
2. Hosts in a /27: a) 32 b) 30 c) 62 d) 14 → **b**
3. Broadcast of 192.168.1.0/26: a) .63 b) .64 c) .255 d) .32 → **a**
4. /24 into 4 subnets → each: a) /25 b) /26 c) /27 d) /28 → **b**
5. Network address is used to: a) assign a host b) name the subnet c) broadcast d) gateway → **b**
6. Aggregate 10.1.0.0/24 + 10.1.1.0/24: a) /23 b) /22 c) /25 d) /24 → **a**
7. Can't aggregate 10.1.0.0/24 + 10.1.2.0/24 because: a) not aligned b) not contiguous c) too big d) IPv6 → **b**
8. /30 usable hosts: a) 0 b) 2 c) 6 d) 14 → **b**
9. RFC 3021 enables: a) /31 P2P b) /0 c) IPv6 d) NAT → **a**
10. Longest-prefix match: overlapping /24 and /26 → a) /24 b) /26 c) both d) default → **b**

## 20. Flashcards
- **Q: Hosts per prefix?** → **A:** 2^(32−n) − 2.
- **Q: Split rule?** → **A:** +1 bit = 2× subnets, ½ hosts.
- **Q: Network vs broadcast?** → **A:** all-host-bits 0 = network (subnet name); all 1 = broadcast.
- **Q: Aggregation?** → **A:** merge contiguous aligned prefixes (4×/24 = /22).
- **Q: VLSM?** → **A:** variable subnet sizes per allocation.
- **Q: Longest-prefix?** → **A:** most specific route wins.
- **Q: /31?** → **A:** P2P link, both addresses usable (RFC 3021).
- **Q: Default route?** → **A:** 0.0.0.0/0 — the least-specific catch-all.

## 21. Revision
Subnetting = splitting a prefix using masks: hosts = 2^(32−n) − 2 (network all-0 = subnet name, broadcast all-1); subnets step by 2^(32−new_n); VLSM right-sizes each. CIDR (RFC 4632) generalizes classes → arbitrary /n, exact allocation, and aggregation (merge contiguous aligned prefixes → fewer routes). Longest-prefix match resolves overlap. Plan big→small; /30-31 for links, /24 standard, /16 site, /10 private blocks. Use ipcalc/`ip`, IPAM for planning; overlap and mask mismatch are top misconfig bugs.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a subnet/mask?" | 2 How It Works / 7 Formal Definition |
| "Host count for /28, /30?" | 13 Q&A / 8 Example |
| "Split a /24 into 4." | 13 Q&A / 15 Coding |
| "Why CIDR over classful?" | 13 Q&A / 4 Why Not Another Approach |
| "VLSM?" | 13 Q&A / 6 Real-World Analogy |
| "Route aggregation?" | 13 Q&A / 9 Internal Working |
| "Can you aggregate these /24s?" | 13 Q&A / 10 Time Complexity |
| "Design a subnet plan for X hosts/sites." | 13 Q&A / 16 Industry Usage |
| "Why can't hosts ping when same /24?" | 13 Q&A / 14 Follow-Up |
