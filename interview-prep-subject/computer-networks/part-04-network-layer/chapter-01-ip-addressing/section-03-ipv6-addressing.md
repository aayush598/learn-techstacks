# IPv6 Addressing

> **TL;DR**: IPv6 replaces IPv4's exhausted 32-bit space with **128-bit addresses** (hextet notation, prefix-based like CIDR) — billions of addresses per person, no NAT (end-to-end restored), **SLAAC** for stateless auto-configuration, built-in multicast/anycast, and mandatory security hooks; adoption rides on dual-stack, NAT64/DNS64, and 464XLAT.

## 1. Why Does This Exist?
IPv4 has 2^32 addresses (≈4.3 billion) — and the Internet has more devices than that (phones, IoT, containers, VMs multiply demand per person). Exhaustion (IANA pool: 2011; RIRs: 2019) forced the stopgaps — NAT (breaks end-to-end, inbound, P2P) and CGNAT (ISP-level NAT). **IPv6 exists to restore what IPv4's scarcity took away**: a practically unlimited address space (2^128 ≈ 340 undecillion — ~10^28 per person) so *every device gets a global address* with no NAT, plus the design fixes IPv4 lacked: built-in **SLAAC** (stateless autoconfiguration — no DHCP dependency), **multicast instead of broadcast**, **anycast** built-in, a clean 40-byte header with no checksum (faster routers), **mandatory IPsec hooks**, extension headers for options (no more "hacky" IPv4 options), and **route aggregation** with fixed-size subnets (/64). It's the "finish the job properly" version of the Internet's addressing.

## 2. How Does It Work?
- **128-bit address, 8 hextets (16-bit groups)**: `2001:0db8:85a3:0000:0000:8a2e:0370:7334`. Rules: leading zeros dropped (`0db8` → `db8`), and one run of all-zero groups collapses to `::` once (`2001:db8::8a2e:370:7334`). Full IPv4-embedded form `::ffff:192.168.1.1`.
- **Prefix/length notation (CIDR-style)**: `2001:db8::/32` (the ISP block), `/48` (site), `/64` (subnet), `/128` (host). No classes — pure prefixing.
- **Address types**: **unicast** (one-to-one: global `2001::/16`+ or ULA `fc00::/7` private, link-local `fe80::/10`), **multicast** (`ff00::/8`), **anycast** (the *same* address on many hosts; routers deliver to the nearest — the CDN/anycast trick, first-class in IPv6).
- **No broadcast**: IPv6 uses multicast (`ff02::1` = all nodes on link, `ff02::2` = all routers) — ARP is replaced by **NDP** (Neighbor Discovery Protocol, ICMPv6-based).
- **SLAAC (RFC 4862)**: a host builds its own global address from router advertisements (RA) — prefix + its interface ID (EUI-64 from MAC, or privacy addresses from random). Stateless, no DHCP. **DHCPv6** is optional for extra parameters (DNS, domain).
- **Transition**: **dual-stack** (run both), **NAT64 + DNS64** (v6-only clients reach v4 servers; the DNS returns synthetic `64:ff9b::/96` addresses that NAT64 translates), **464XLAT** (a 1:1 stateless NAT inside a NAT64, used by mobile carriers for apps that are v4-only), tunneling (6in4, GRE, Teredo — deprecated).
- **Header**: fixed 40 bytes (vs IPv4's variable 20-60), no checksum (layers above handle integrity), flow label for QoS; extension headers for hop-by-hop/routing/fragment options.

## 3. When Is It Used?
- **Global Internet (growing)**: ~40-50%+ of Google's traffic is IPv6 (2024); mobile carriers (US/India/China) and CDNs (Cloudflare/Google/Netflix) are v6-default. IPv6 *without* v4 is common on mobile networks.
- **Cloud (the norm)**: AWS/GCP/Azure support VPC IPv6; new DCs run v6 internally (or dual-stack); Kubernetes has dual-stack service support.
- **ISP/consumer**: most broadband now ships dual-stack; some ISPs are v6-only with 464XLAT.
- **IoT & constrained devices**: SLAAC means no DHCP server; global addresses mean direct (NAT-less) reachability — the IoT-per-device model.
- **Corporates**: /48 allocations (2^16 subnets per site); DC address plans; government mandates (US OMB v6-only by 2025).
- **Where v4 won't go**: P2P (no NAT), gaming consoles (no port-forwarding), IPv6-only datacenters, massive VM/container fleets.

## 4. Why Wasn't Another Approach Chosen?
- **Why 128 bits and not 64?** 64 bits would "suffice" numerically but breaks *end-to-end autoconfiguration*: IPv6 derives part of the address from the interface (EUI-64) and reserves fixed subnet bits; 128 bits gives room for hierarchy (ISP /32 → site /48 → subnet /64 → host /64) *and* future assignment without renumbering. 64 bits would force compromises now regretted — 128 is the "never run out, plan deep" choice.
- **Why no NAT in IPv6?** NAT was a scarcity stopgap, not a feature: it broke end-to-end (no inbound without hacks), auditing, P2P, and even the security story (IPsec assumes real addresses). With unlimited space, every host can be globally addressable — the original Internet architecture restored. ULA (fc00::/7) exists for *privacy/lab* internal use but is not the model.
- **Why SLAAC over DHCP?** DHCP is a server dependency (provisioning, failure mode). SLAAC lets a host configure itself purely from a router advertisement — zero server, zero state, instant; a host moving networks reconfigures automatically. It also randomizes addresses for privacy. DHCPv6 exists only where extra parameters are needed.
- **Why multicast instead of broadcast?** Broadcast wastes: every broadcast wakes every host. Multicast is selective — only group members process. IPv6 made it the *only* mechanism (no broadcast address at all), improving scale and efficiency.
- **Why a fixed 40-byte header, no checksum?** IPv4's variable options made routers parse variable-length headers and recompute checksums at every hop (slow). IPv6 moved options to *extension headers* (only the destinations that care process them) and dropped the checksum (Layer 2 + Layer 4 cover integrity) — routers go faster. The "clean rewrite" approach: fix every IPv4 wart in one go.
- **Why not just extend IPv4 (more addresses, same design)?** Addressing is *structural* — classes/CIDR, NAT semantics, options, checksum, broadcast, autoconfig are baked into the packet format and stack. You can't bolt on 128 bits; the protocol needed a fresh, incompatible design — which is exactly why IPv6 is a *new protocol* and transition, not a patch, is the hard part.

## 5. Intuition
IPv4 is a **city that ran out of house numbers** and had to hide three families behind one front door (NAT). IPv6 is the **new city plan**: every building gets its own unique number, forever — so the mail goes directly to each door, no doorman needed. The address itself is hierarchical like the postal system: country (ISP /32) → region (site /48) → street (subnet /64) → house (host /64), and the system is so generous that each street can have 2^64 houses (the entire IPv4 address space fits into one /64 *four billion times*). The clever part: a house *chooses its own house number* from the street prefix (SLAAC) — no need to ask a central office. And the postal service dropped its "broadcast to every house" megaphone in favor of mailing lists (multicast) — only subscribers get the mail.

## 6. Real-World Analogy
**Renumbering a whole country's postal system**: The old system (IPv4) ran out of numbers, so apartment blocks (NAT) crammed 100 families behind one door — great for space, terrible for direct mail (no package deliveries without a concierge, no visiting relatives without special arrangements). The new system (IPv6): every family gets a *permanent global street number* (128-bit address), delivered directly. The number is structured like the phone system: country code (ISP), area (site), exchange (subnet), line (host). New homes **assign their own number** from the street's announced prefix (SLAAC) — the mailman just publishes "this street starts with 2001:db8:1:" and everyone fills in their own suffix. Two-door countries (dual-stack) run both systems side by side; some countries tear out the old system entirely (v6-only). Moving house? The new system's numbers include a moving-friendly model — with privacy addresses, your "from address" changes automatically.

## 7. Formal Definition
IPv6 (RFC 8200) is a 128-bit addressing architecture: eight 16-bit hextets in colon-separated hex (RFC 4291), with leading-zero elision and one `::` collapse. Notation `addr/prefixlen` (0–128). Types: global unicast `2000::/3`; unique local `fc00::/7` (ULA, RFC 4193); link-local `fe80::/10`; multicast `ff00::/8`; unspecified `::`; loopback `::1`; IPv4-mapped `::ffff:0:0/96`; NAT64 well-known prefix `64:ff9b::/96`. Header: fixed 40 bytes (version, traffic class, flow label, payload length, next header, hop limit, src, dst); options via extension headers; no checksum; fragmentation by source only. Addressing mechanisms: SLAAC (RFC 4862) via Router Advertisements (RFC 4861 NDP), optional DHCPv6 (RFC 8415), privacy addresses (RFC 8981). Transition: dual-stack (RFC 4213), NAT64/DNS64 (RFC 6146/6147), 464XLAT (RFC 6877). Subnet standard: /64.

## 8. Example
Address compression and SLAAC:
```
Full:        2001:0db8:0000:0000:0000:0000:0000:00ab
Elide zeros: 2001:db8::ab                      (leading zeros + one :: run)
Link-local:  fe80::1                          (auto on every v6 interface)
IPv4-mapped: ::ffff:192.168.1.5               (v4-in-v6 form)

SLAAC (stateless):
Router Advertisement: "prefix 2001:db8:1::/64, I'm the gateway"
Host picks:          2001:db8:1::aabb:ccdd:eeff:1122   (EUI-64 from MAC)
  (privacy mode instead: random suffix, rotating every N hours)

NDP replacing ARP (ff02::1 = all nodes on the link):
  ping6 ff02::1%eth0        -> every node answers (that's your "arp cache" rebuilt)
  ip -6 neigh show          -> IPv6 neighbor table (was: arp -a)
```
Dual-stack in action: `ip addr show` shows `inet 192.168.1.5/24` *and* `inet6 2001:db8:1::aabb/64`. A dual-stacked host tries v6 first (happy eyeballs, RFC 6555), falls back to v4.

## 9. Internal Working
1. **Header processing**: 40-byte fixed header; routers read (src, dst, hop limit) and forward — no checksum, no option parsing (options live in extension headers, processed only by the destination or listed routers). Faster, simpler silicon.
2. **NDP (Neighbor Discovery)**: replaces ARP + DHCP stateless parts: RS/RA (router solicitation/advertisement) announce prefixes + gateways; NS/NA (neighbor solicitation/advertisement) resolve on-link IP→MAC; DAD (duplicate address detection) before using a new address; unreachability detection. All ICMPv6 — no separate ARP protocol.
3. **SLAAC**: host sends RS → router replies RA (prefix, lifetime, flags) → host combines prefix + interface ID (EUI-64 or random) → DAD → global address active. Privacy extensions (RFC 8981) rotate the suffix so the address can't track the device.
4. **Routing**: routers advertise/learn routes (OSPFv3, BGP4+ — see part-04 ch3) with the same longest-prefix logic over /64s; no NAT (no translation state). Anycast: the *same* /128 announced from many sites → packets go to the nearest (CDN/root-server model).
5. **Multicast**: ff02::1/2 etc. for local; MLD (multicast listener discovery) manages group membership — replacing IPv4's IGMP/broadcast with a leaner model.
6. **Fragmentation**: only the *source* fragments (Path MTU Discovery required); routers *never* fragment (unlike IPv4) — the "fragment at the edge" design.
7. **Transition**: dual-stack (both stacks, DNS A + AAAA), NAT64/DNS64 (v6-only client → synthetic `64:ff9b::` → NAT64 gateway → v4 Internet), 464XLAT (v4 app → v4-to-v6 stateless translation → NAT64 → v4 peer) — the carrier playbook. Tunnels (6in4, GRE) are fallbacks for network owners without native v6.

## 10. Time Complexity
- **Forwarding**: fixed 40-byte header, no checksum/options → fewer operations per packet; lookup same O(prefix) trie/TCAM (wider entries).
- **Address arithmetic**: 128-bit ops (vs 32) — still O(1); IPAM/`ipcalc` handle the width.
- **Table sizes**: aggregation over /48s, /64s — same summarization benefit; the BGP table carries both families.
- **SLAAC/NDP**: O(1) per host (RS/RA exchange) — no server, no lease state; the "config cost" is one round trip to a router.
- **Transition complexity**: dual-stack = 2× state (routes, DNS, firewalls, security groups); NAT64 adds translation state — the operational cost is *deployment*, not algorithm.

## 11. Advantages
- **Unlimited address space**: every device globally addressable — no NAT, no CGNAT, no port-forwarding hacks, true P2P.
- **End-to-end restored**: inbound connections, IP-based auditing/security, and protocols that hate NAT (games, P2P, IoT) work natively.
- **SLAAC**: zero-server autoconfiguration — plug in, get a global address; ideal for IoT/constrained/mobile.
- **Built-in features**: multicast + anycast first-class, NDP (no ARP), privacy addresses (anti-tracking), no broadcast waste.
- **Faster core**: fixed header, no checksum, no router fragmentation — simpler forwarding silicon.
- **Mandatory security hooks**: IPsec designed-in (AH/ESP header); extension headers for secure options.

## 12. Disadvantages
- **Not backward-compatible**: a *new* protocol — dual-stack is a 2× ops burden (routes, DNS A/AAAA, firewalls, tooling) until v4 is retired (still not, decades later).
- **Transition pain**: NAT64/DNS64/464XLAT add complexity and subtle bugs (fragmentation, MTU, some apps fail on synthetic addresses); tunneling (Teredo/6in4) is flaky/deprecated.
- **Tooling/ecosystem lag**: many tools, firewalls, and cloud services added v6 late or incompletely; some networks block v6 (broken "happy-eyeballs" bugs).
- **Memorization/debugging**: 128-bit hex is unwieldy; typos and `::` ambiguity are real; the community needed `ipv6calc` and compressed forms.
- **Security surface newness**: NDP has its own attacks (spoofing RAs, DAD DoS — mitigated by SEND/RFC 3971); v6 firewalls are less mature than v4's NAT-based accidental protection (no NAT = no implicit firewall).
- **Legacy momentum**: the entire installed base (code, configs, ISPs, vendors) is v4 — progress is real but glacial.

## 13. Interview Questions
1. **Q: What is IPv6 and why does it exist?** A: A 128-bit addressing architecture (RFC 8200) replacing exhausted IPv4 — unlimited addresses (no NAT), SLAAC, multicast/anycast, faster headers, and designed-in security.
2. **Q (tricky): How many addresses does IPv6 provide?** A: 2^128 ≈ 340 undecillion — ~10^28 per person. Enough that every device, VM, container, and IoT thing gets a global unicast address with no translation.
3. **Q: How is an IPv6 address written?** A: Eight 16-bit hextets in hex, colon-separated: `2001:db8:85a3::8a2e:370:7334`; leading zeros dropped, one `::` run elided.
4. **Q: What are the IPv6 address types?** A: Global unicast (2000::/3), link-local (fe80::/10, auto on every interface), ULA/private (fc00::/7), multicast (ff00::/8), loopback (::1), unspecified (::), IPv4-mapped (::ffff:a.b.c.d).
5. **Q (FAANG): What is SLAAC and how does it work?** A: Stateless autoconfiguration: a host sends a Router Solicitation; the router advertises the subnet prefix + gateway (RA); the host combines the prefix with its interface ID (EUI-64 or random privacy suffix), runs Duplicate Address Detection, and has a global address — no DHCP server.
6. **Q: Why no NAT in IPv6?** A: NAT was a scarcity stopgap with real costs (no inbound, P2P pain, audit trouble). IPv6's space makes global addressing possible — end-to-end restored. ULA exists for internal/privacy use but isn't the model.
7. **Q: What replaces ARP in IPv6?** A: NDP (Neighbor Discovery Protocol, ICMPv6-based): NS/NA for address resolution, RS/RA for autoconfiguration, DAD for duplicates, and unreachability detection. No separate ARP protocol.
8. **Q (tricky): How is anycast used in IPv6?** A: The *same* address is announced from many locations (routers via BGP); packets go to the *nearest* instance. Built into IPv6; CDNs and root DNS servers use it (IPv4 does it too via BGP trickery — IPv6 makes it first-class).
9. **Q: What are the transition mechanisms?** A: Dual-stack (both protocols), NAT64 + DNS64 (v6-only → synthetic 64:ff9b:: addresses → translation to v4), 464XLAT (v4 apps over v6-only networks, the carrier playbook), and tunnels (6in4, Teredo — legacy/deprecated).
10. **Q (production): A v6-only network can't reach some v4 sites. What's the fix?** A: NAT64 + DNS64: the DNS64 synthesizes a 64:ff9b::/96 address for the v4-only name; the NAT64 gateway maps it to the real v4 destination. Apps that embed IPs (old FTP-style) need 464XLAT instead.
11. **Q: What is a /64 in IPv6?** A: The standard subnet size (2^64 addresses); the *entire IPv4 space fits ~4 billion times in one /64*. Sites get /48 (65,536 subnets), hosts /128. No host-conservation concerns.
12. **Q (tricky): Why is the header fixed at 40 bytes with no checksum?** A: Fixed length = no per-hop option parsing; no checksum = fewer instructions and Layer 2/4 already provide integrity. Options moved to extension headers, processed only where relevant. Result: faster, simpler router silicon.
13. **Q: What is DAD?** A: Duplicate Address Detection — a host sends NS for its *own* tentative address before using it; if anyone answers, the address is taken (rechoose). Prevents the "two hosts, one address" failure that IPv4 tolerated until trouble.
14. **Q (FAANG): What are privacy extensions and why?** A: EUI-64 embeds the MAC → an address is a device fingerprint trackable across networks. RFC 8981 privacy addresses use a *random* suffix that rotates (hours), so you can't be tracked by address. Mobile/OSes enable it by default.
15. **Q: What is the difference between link-local and global IPv6?** A: Link-local (fe80::/10) is auto-generated per interface and valid *only on that link* (NDP, routers, no routing of fe80). Global (2000::/3) is routable Internet-wide. Every v6 interface has both.
16. **Q (production): `ping6 ff02::1%eth0` — what does that do?** A: Multicast to *all nodes on eth0* — every neighbor answers, listing who's on the link (IPv6's replacement for the old "ping broadcast" neighbor discovery). Useful when you don't know addresses on a fresh link.
17. **Q: How does IPv6 handle fragmentation?** A: Only the *source* fragments (PMTU Discovery is required); routers never fragment — the "fragment at the edge" design. IPv4 routers could fragment mid-path (a performance + security mess); IPv6 forbids it.

## 14. Follow-Up Questions
1. **Q: What is happy-eyeballs and why?** A: RFC 6555/8305 — when a host has both A and AAAA, it tries both (v6 first, v4 in parallel after ~250 ms) and uses whichever connects; it avoids the "v6 broken but advertised" outage. Every modern OS/browser implements it.
2. **Q: How do you deploy IPv6 in a cloud VPC?** A: Enable VPC dual-stack (v4 subnet + v6 /56 per subnet), assign /64s, update security groups/NACLs for both families, DNS AAAA records, and test happy-eyeballs + NAT64 for any v4-only dependencies. Many clouds default v4-only; IPv6 is an explicit enable.
3. **Q (tricky): Why does the NAT64 well-known prefix 64:ff9b::/96 exist?** A: DNS64 needs a *deterministic* way to synthesize an address that maps to a v4 destination; 64:ff9b:: + the 32-bit v4 address gives NAT64 an unambiguous "this is really a v4 host" marker — no state, no ambiguity. (RFC 6052 specifies the whole embedding.)
4. **Q: What is 464XLAT in plain terms?** A: Mobile carriers run v6-only networks; most apps are still v4. 464XLAT = a stateless CLAT inside the phone (v4 app → v6 packet) + a NAT64 gateway (v6 → v4 Internet). The phone "speaks v4 to the app, v6 to the network." That's how "no v4 at all" works today for consumers.
5. **Q (FAANG): "Your API must support clients on v6-only mobile networks. What breaks and what do you fix?"** A: Breaks: v4 literals in app code/URLs, security-group/allowlists that are v4-only, geo/rate-limit keyed on v4, some SDKs resolving only A. Fixes: AAAA records + dual-stack listeners, DNS64-compatible behavior, NAT64-aware allowlists (64:ff9b range), and IPv6 test coverage. The "IPv6-only readiness" checklist is a real production skill.

## 15. Coding Example
```python
# IPv6 in Python — the modern parts (SLAAC is OS-level; here we parse/address)
import ipaddress, socket

# Address handling
ip = ipaddress.IPv6Address("2001:0db8:0000:0000:0000:0000:0000:00ab")
print(ip.compressed)          # '2001:db8::ab'
print(ip.version)             # 6
net = ipaddress.IPv6Network("2001:db8:1::/64")
print(list(net.hosts())[:2], len(list(net.hosts())))   # 2^64 - 1 ... huge!
print(ipaddress.IPv6Address("::ffff:192.168.1.5").ipv4_mapped)  # 192.168.1.5

# A real v6 client (DNS + connect, happy-eyeballs style is OS-level)
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
try:
    s.connect(("2001:db8::1", 80))          # requires a real v6 peer
except OSError as e:
    print("no v6 path:", e)

# Multicast ping to all-nodes on the local link (like ARP discovery)
import subprocess
print(subprocess.run(["ping6", "-c", "2", "ff02::1%eth0"],
                     capture_output=True, text=True).stdout)
```
```bash
# The IPv6 toolkit
$ ip addr show eth0 | grep inet6     # fe80::.../64  +  global 2001:db8::/64
$ ip -6 route show                   # ::/0 via fe80::1, 2001:db8::/64 dev eth0
$ ip -6 neigh show                   # NDP table (was: arp -a)
$ ping6 -c 2 2001:db8::1             # or: ping -6
$ dig AAAA example.com               # v6 records
$ curl -6 -sv https://ipv6.google.com -o /dev/null 2>&1 | grep -i 'ipv6'
```

## 16. Industry Usage
- **Mobile carriers (the v6 engine)**: US/India/China networks run large-scale IPv6 (v6-only + 464XLAT); "no IPv4 at all" is now the *mobile* mainstream in several markets — Google reports 40-50%+ v6.
- **CDNs & big web (Cloudflare, Google, Netflix, Akamai)**: dual-stack + v6-default edge; Cloudflare's v6 traffic is a large share of the web; anycast over v6 for DNS roots (one of the 13 root servers is reachable only via v6-anycast designs).
- **Cloud & DCs (AWS/GCP/Azure)**: VPC IPv6, dual-stack ELB/NLB, EKS dual-stack clusters; new hyperscale DCs plan v6-internal.
- **Government & mandates**: US OMB IPv6-only-by-2025 guidance; EU and APAC mandates; procurement requires v6 — compliance is an industry driver.
- **IoT & consumer**: SLAAC-based smart devices (cameras, sensors) reachable directly; Matter/Thread use IPv6/6LoWPAN (v6 over low-power radio).
- **Academia/research**: RFC work, v6 measurement (Google/Akamai v6 stats), and future-proofing — the protocol's design discussions are *the* live transport-architecture conversation.

## 17. References
- RFC 8200 — IPv6 Protocol Specification: https://www.rfc-editor.org/rfc/rfc8200
- RFC 4291 — IPv6 Addressing Architecture: https://www.rfc-editor.org/rfc/rfc4291
- RFC 4862 — IPv6 Stateless Address Autoconfiguration (SLAAC): https://www.rfc-editor.org/rfc/rfc4862
- RFC 4861 — Neighbor Discovery (NDP): https://www.rfc-editor.org/rfc/rfc4861
- RFC 6146/6147 — NAT64 / DNS64: https://www.rfc-editor.org/rfc/rfc6146
- RFC 6877 — 464XLAT: https://www.rfc-editor.org/rfc/rfc6877
- RFC 8981 — Privacy Extensions: https://www.rfc-editor.org/rfc/rfc8981
- RFC 8305 — Happy Eyeballs v2: https://www.rfc-editor.org/rfc/rfc8305
- Kurose & Ross, *Computer Networking*, Ch. 4 §4.3.4 (IPv6).

## 18. Cheat Sheet
- 128-bit, 8 hextets, colon hex; `::` collapses one zero-run; leading zeros dropped.
- Types: global 2000::/3, link-local fe80::/10, ULA fc00::/7, multicast ff00::/8, ::1 loopback, :: unspecified, ::ffff:a.b.c.d v4-mapped, 64:ff9b::/96 NAT64.
- Prefixes: /32 ISP, /48 site, /64 subnet (standard), /128 host.
- SLAAC: RS/RA → prefix + interface ID (EUI-64 or random privacy) → DAD → global addr. No DHCP needed.
- NDP replaces ARP (NS/NA, RS/RA, DAD); no broadcast — multicast ff02::1 (all nodes), ff02::2 (routers).
- No NAT, no checksum, no router fragmentation, 40-byte fixed header, extension headers.
- Transition: dual-stack, NAT64/DNS64, 464XLAT (v6-only + v4 apps), tunnels (legacy).
- Happy eyeballs: try v6, fall back to v4 in 250 ms.
- ip addr/-6 route/-6 neigh, ping6, dig AAAA.

## 19. Quiz
1. IPv6 address size: a) 32 b) 64 c) 128 d) 256 → **c**
2. `2001:db8::ab` is the compressed form of: a) 8 full hextets with one zero-run b) 4 hextets c) 16 hextets d) none → **a**
3. Link-local prefix: a) 2000::/3 b) fe80::/10 c) fc00::/7 d) ff00::/8 → **b**
4. Standard IPv6 subnet: a) /24 b) /32 c) /64 d) /128 → **c**
5. SLAAC requires: a) DHCP server b) router advertisement c) DNS d) NAT → **b**
6. ARP replacement in IPv6: a) DHCPv6 b) NDP c) IGMP d) RARP → **b**
7. IPv6 loopback: a) 0.0.0.0 b) ::1 c) 127/8 d) fe80::1 → **b**
8. No NAT in IPv6 because: a) too slow b) unlimited space restores end-to-end c) banned d) unneeded for security → **b**
9. NAT64 prefix: a) 64:ff9b::/96 b) fe80::/10 c) fc00::/7 d) 2000::/3 → **a**
10. Happy Eyeballs: a) v4 only b) try v6, fall back v4 c) v6 only d) tunnels → **b**

## 20. Flashcards
- **Q: IPv6 size?** → **A:** 128-bit, 8 hextets, hex-colon, `::` collapse.
- **Q: Address types?** → **A:** global 2000::/3, link-local fe80::/10, ULA fc00::/7, multicast ff00::/8.
- **Q: SLAAC?** → **A:** RS/RA → prefix + interface ID → DAD → global addr; no DHCP.
- **Q: NDP?** → **A:** replaces ARP (NS/NA, RS/RA, DAD, no broadcast).
- **Q: No NAT why?** → **A:** 2^128 addresses restore end-to-end.
- **Q: Transition?** → **A:** dual-stack, NAT64/DNS64, 464XLAT.
- **Q: Privacy extensions?** → **A:** random rotating suffix — anti-tracking.
- **Q: Happy Eyeballs?** → **A:** v6 first, v4 fallback after 250 ms.

## 21. Revision
IPv6 (RFC 8200) = 128-bit, 8 hextets, `::` compression; global 2000::/3, link-local fe80::/10, ULA fc00::/7, multicast ff00::/8, ::1 loopback; /64 standard subnet, /48 site. SLAAC (RS/RA + interface ID + DAD) = no DHCP; NDP replaces ARP (no broadcast). No NAT (end-to-end), 40-byte fixed header (no checksum/options; extension headers), source-only fragmentation, anycast first-class. Transition: dual-stack, NAT64/DNS64 (64:ff9b::/96), 464XLAT. Privacy extensions (RFC 8981) rotate suffixes; happy eyeballs (RFC 8305) handles broken v6. Adoption: mobile/carriers v6-only, CDNs/cloud dual-stack.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is IPv6 / why needed?" | 2 How It Works / 7 Formal Definition |
| "How is it written / types?" | 13 Q&A / 8 Example |
| "What is SLAAC?" | 13 Q&A / 9 Internal Working |
| "What replaces ARP?" | 13 Q&A / 9 Internal Working |
| "Why no NAT in IPv6?" | 13 Q&A / 4 Why Not Another Approach |
| "Transition mechanisms?" | 13 Q&A / 10 Time Complexity |
| "v6-only can't reach v4 sites?" | 13 Q&A / 14 Follow-Up |
| "Privacy extensions / happy eyeballs?" | 13 Q&A / 15 Coding |
| "How do carriers deploy IPv6?" | 16 Industry Usage |
