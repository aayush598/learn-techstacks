# MAC Addresses and Address Resolution (ARP)

> **TL;DR**: A MAC (Media Access Control) address is a flat, hardware-bound 48-bit identifier burned into a network interface that frames on a LAN are actually delivered to, and ARP (RFC 826) is the protocol that lets a host resolve "what IP is at what MAC?" locally — the glue between the network layer (IP) and the data link layer (Ethernet).

## 1. Why Does This Exist?
An IP address is a *logical, hierarchical* locator that routers use to navigate across the Internet — but routers and switches don't move packets over "the Internet" abstractly; every hop is a physical link where the frame's header must name the *next* machine's interface. Ethernet hardware has no idea what an IP address is; a NIC matches incoming frames by the 48-bit MAC written in silicon. So the question "which MAC do I put in the destination field for IP 10.0.0.5?" must be answered *locally* — that's the address resolution problem. MACs exist because: (1) hardware needs a globally unique, fixed-size, self-contained identifier that needs no lookup (switching is simpler and faster than routing); (2) the L3 address may change (DHCP reassignment, NAT) without touching the physical interface; (3) broadcast delivery (send to everyone on the LAN) needs a reserved L2 address that all NICs accept. ARP exists to bridge these two address spaces on demand, with a cache so it doesn't need to ask every time.

## 2. How Does It Work?
A host needing the MAC for an IP it wants to reach (same subnet) sends an **ARP request**: a broadcast Ethernet frame whose destination MAC is `FF:FF:FF:FF:FF:FF`, containing "who has IP X? tell me at MAC Y." Every NIC accepts broadcasts; only the host configured with IP X replies with an **ARP reply** (a unicast frame) carrying its MAC. The requester inserts the mapping into its **ARP cache** (Linux: `ip neigh`) with a TTL and uses it for subsequent frames. Requests are broadcast, replies are unicast — the classic asymmetry that attackers abuse.

## 3. When Is It Used?
- **Every time you send a packet to a local destination**: before the first frame to a new IP on the same subnet.
- **Router-to-router or host-to-default-gateway**: the next-hop IP must be resolved to a MAC before the Ethernet frame leaves the interface.
- **Proxy ARP** (RFC 1027): a router answers ARP on behalf of hosts behind it, so a remote subnet appears local.
- **Gratuitous ARP (GARP)**: a host announces its IP→MAC mapping without being asked — used on boot, IP-address changes, failover (keepalived/VRRP), and duplicate-address detection.
- **ARP for IPv4 only**: IPv6 replaces it with **NDP (Neighbor Discovery Protocol, RFC 4861)** using ICMPv6 Router/Neighbor Solicitation + Advertisement (multicast, with built-in security extensions — SEND, RFC 3971).

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: embed IP in the hardware address.* Rejected — hardware can't be renumbered; NICs are manufactured before being assigned IPs, and networks must renumber freely (that's what DHCP/NAT exploit).
- *Alternative: broadcast a request every time, no caching.* Rejected — a broadcast per frame is catastrophically expensive; every LAN peer must process each broadcast, so the ARP cache + TTL is essential.
- *Alternative: a central directory service mapping IP→MAC.* Rejected — adds a server, a lookup RTT, and a single point of failure, and it must be consistent with the broadcast domain; ARP's on-link discovery needs no infrastructure.
- *Alternative: put the mapping in DNS.* Rejected — DNS is global and slow; MAC resolution must be instantaneous and local, tied to the physical link. (A reverse "DNS is not ARP" confusion is a classic interview trap.)
- *Alternative: derive the multicast MAC directly for IPv6.* IPv6/NDP *does* avoid asking "who has X?" by using the solicited-node multicast address (derived from the last 24 bits of the target IPv6 address) — this is the improved design IPv6 chose.

## 5. Intuition
ARP is like **knocking on the door of every apartment in a building and asking "does 10.0.0.5 live here?"** Everyone hears the knock (broadcast); only the tenant named 10.0.0.5 answers by giving you their flat number (their MAC). You write it down in your address book (ARP cache) so next time you go straight to their door. A neighbor who moves (IP change) re-knocks; a malicious tenant who answers on behalf of someone else is an **ARP spoofer** who has just redirected your mail (traffic).

## 6. Real-World Analogy
The **phone directory with a memory**: you know someone's name (IP) but need their phone number (MAC) to actually call (transmit the frame). You yell the name out the window (broadcast ARP request); they shout back their number (reply); you memorize it (cache) because you call often. If you yell and a different person answers claiming to be them (ARP spoofing), all your calls get routed to the impostor.

## 7. Formal Definition
A MAC (EUI-48) address is a 48-bit globally unique identifier assigned to a network interface, formatted as 6 octets (e.g., `AC:DE:48:01:23:45`); bit 0 of octet 1 is the Individual/Group (I/G) bit (0 = unicast, 1 = multicast), bit 1 is the Universally/Locally (U/L) bit (0 = globally unique/OUI-assigned, 1 = locally administered), and the first 3 octets are the OUI assigned to the manufacturer (IEEE Registration Authority). **ARP** (Address Resolution Protocol, RFC 826) is a link-layer protocol that maps a target protocol (IP) address to the hardware (MAC) address of the interface owning it within the local network; request/reply packets have a fixed 28-byte body (32 for Ethernet+IPv4 with padding) and run directly over Ethernet EtherType `0x0806`.

## 8. Example
Host A `10.0.0.1` (MAC `AC:DE:48:00:00:01`) wants to send an IP packet to host B `10.0.0.2`. 
1. A checks its ARP cache (`ip neigh show`) — miss.
2. A builds an ARP request: hardware type 1 (Ethernet), protocol type 0x0800 (IPv4), HLEN 6, PLEN 4, opcode 1 (request), sender IP `0A 00 00 01`, sender MAC `AC DE 48 00 00 01`, target IP `0A 00 00 02`, target MAC `00 00 00 00 00 00`.
3. The frame is sent with dest MAC `FF:FF:FF:FF:FF:FF`, EtherType `0x0806`. B's NIC sees broadcast, OS matches target IP → replies with opcode 2 (reply), sender = B, target = A, unicast.
4. A inserts `10.0.0.2 → AC:DE:48:00:00:02` into its cache (TTL ~ minutes, configurable via `gc_staletime`).
5. Now A's IP packet to B travels in an Ethernet frame with dest MAC = B's MAC. ARP was only needed once.

## 9. Internal Working
1. **Cache design**: per-interface neighbor table (`struct neigh` in Linux, `ip neigh`); entries are REACHABLE → STALE → DELAY → PROBE → FAILED, driven by GC timers; on use of a STALE entry, Linux re-resolves.
2. **Same-subnet test**: before ARP, the host ANDs dest IP with its netmask; if the dest is not local, ARP resolves the *gateway's* IP, not the dest's (the frame goes to the router).
3. **Request broadcast / reply unicast**: only the target answers; gratuitous ARP can be sent to announce/check.
4. **GARP conflicts**: on receiving a GARP for an IP the host already owns, hosts raise a duplicate-address warning (RFC 5227 DAD); keepalived/VRRP rely on GARP to migrate VIPs to the new active node, and switches re-learn the MAC from the GARP's source address.
5. **ARP in hardware**: the NIC does NOT process ARP — the kernel does; only the destination-address match (unicast/broadcast/multicast filtering) happens in silicon.
6. **Linux artifacts**: `arp_ignore`/`arp_announce` sysctls control reply policy (e.g., only reply if the request targets an address owned by the receiving interface); `neigh.default.gc_thresh*` bounds cache size.

## 10. Time Complexity
- **Cache hit**: O(1) — hash lookup on the target IP.
- **Cache miss**: 1 broadcast + 1 unicast exchange, costing O(1) LAN-wide processing (each peer must inspect the broadcast — that's the "broadcast cost" of ARP) plus the RTT of the request/reply (~100 µs–1 ms on LAN).
- **Table growth**: O(n) memory for n neighbors, bounded by `gc_thresh3` (default 1024 per interface in Linux).
- **Attack cost**: an ARP flood (poisoning) is cheap for the attacker — one crafted packet per victim — but expensive for the victim (cache churn, MITM exposure).

## 11. Advantages
- **Zero configuration**: works with no server, no admin, no infrastructure — plug a NIC in, ARP just works.
- **On-link correctness**: the mapping is discovered exactly where it matters (the local segment), immune to stale global directories.
- **Cache efficiency**: repeated traffic to the same neighbor costs nothing after the first resolution.
- **Simple and robust**: 28-byte packet, no connection state, survives reboots (re-resolved on demand).
- **Hardware agnostic**: the format supports any link layer (Ethernet, FDDI, ATM) and any network protocol (IPv4, IPv6 via NDP) by design (HLEN/PLEN fields).

## 12. Disadvantages
- **No authentication**: ARP has no notion of identity — any host may answer for any IP → **ARP spoofing/poisoning** is a classic MITM (that's why DHCP snooping + Dynamic ARP Inspection + static ARP exist).
- **Stateless and cache-oriented**: caches go stale; a host that changes MACs (failover) needs GARP to correct everyone.
- **Broadcast cost**: every request is a LAN-wide broadcast; at scale, ARP storms and cache sizes grow with LAN size (mitigated by switching + VLANs + neighbor limits).
- **Flat, unrouteable**: MAC addresses carry no topology information; you cannot route by MAC, only switch — which is why every cross-network packet needs ARP at every hop.
- **Privacy**: the MAC is globally unique and visible in every frame → tracking; WiFi uses MAC randomization (802.11ax and OS-level) to mitigate.

## 13. Interview Questions
1. **Q: What is the difference between ARP and DNS?** A: ARP resolves *local* L3→L2 (IP→MAC) on the same link, using broadcasts, for immediate frame delivery; DNS resolves *global* names→IP through a hierarchical, cached, distributed database. DNS knows nothing about hardware addresses; ARP knows nothing about names.

2. **Q: How big is a MAC address and what are its fields?** A: 48 bits = 6 octets. Octet 1 bit 0 = I/G (0 unicast, 1 multicast), bit 1 = U/L (0 globally unique, 1 locally administered); first 3 octets = OUI (IEEE-assigned manufacturer). Example `AC:DE:48:01:23:45`: OUI `AC:DE:48`.

3. **Q: Walk me through an ARP request/reply.** A: Host sends a broadcast frame (dest `FF:FF:FF:FF:FF:FF`, EtherType `0x0806`) with opcode 1, sender IP/MAC, target IP, and target MAC = 0. The target replies unicast (opcode 2) with its MAC. Requester caches the mapping. Ethernet/IPv4 ARP body = 28 bytes (2+2+1+1+2 + 6+4 + 6+4).

4. **Q: What is a gratuitous ARP and when is it used?** A: An ARP request sent by a host *for its own IP*, unsolicited — to announce a new IP/MAC (boot), announce a moved IP (keepalived/VRRP failover so switches re-learn the MAC), and to detect duplicates (RFC 5227). Receivers update their caches; the source MAC also refreshes switch MAC tables.

5. **Q: What is ARP spoofing and how do you defend against it?** A: An attacker on the same LAN answers ARP requests for a victim's IP with the attacker's MAC, so frames meant for the victim go to the attacker (MITM, session hijack). Defenses: Dynamic ARP Inspection (DAI) at the switch with DHCP snooping, static ARP entries, arpwatch-style anomaly detection, and encrypted transport (TLS) so the MITM can't read the payload.

6. **Q: When does a host resolve the gateway's MAC instead of the destination's?** A: When the destination IP is *not* on the same subnet — the host ANDs dest IP with its netmask; on mismatch it ARPs for the default gateway's IP and sends the frame to the gateway. This is the "next hop" rule.

7. **Q: TRICKY — Your ARP request goes unanswered even though the target host is up. List causes.** A: The target may be on a *different subnet* (you'd need the gateway); the target's interface may drop the request (firewall/`arp_ignore=1` policy on multi-homed hosts); the switch blocked the broadcast (broadcast storm control, port isolation); VLAN mismatch; or the target is down/unplugged. Also check the request used the correct VLAN/interface (`ip neigh`, `tcpdump -e`).

8. **Q: PRODUCTION — Why does the ARP cache go STALE and how does Linux handle it?** A: Because MACs can change (NIC replacement, failover). Linux marks entries STALE after `base_reachable_time` (default 30 s), then on use transitions to DELAY→PROBE and re-ARP's if the neighbor doesn't respond. Sysctls: `gc_staletime`, `base_reachable_time_ms`, `gc_thresh1/2/3`.

9. **Q: SCENARIO — You see "arp_cache: neighbor table overflow" in dmesg. What's happening and what do you do?** A: The neighbor cache (`gc_thresh3`, default 1024/interface) filled — usually a big LAN, an ARP flood, or a misconfigured proxy. Fixes: raise `gc_thresh*`, ensure `arp_ignore`/`arp_announce` are sane, segment the LAN (VLANs), or find the flooding host.

10. **Q: How does IPv6 replace ARP?** A: NDP (RFC 4861) over ICMPv6: Neighbor Solicitation goes to the *solicited-node multicast* address (derived from the target's last 24 bits) instead of a broadcast; Neighbor Advertisement is the reply. Router Solicitation/Advertisement handle default-gateway discovery (no DHCP required), and SEND (RFC 3971) adds cryptographic verification — fixing ARP's lack of authentication.

11. **Q: What is proxy ARP and when would you use it?** A: A router answers ARP requests *for hosts it can route to*, claiming the target IP with its own MAC (RFC 1027). Used for simple transparent routing, e.g., two subnets on one interface, or when a host has a wrong netmask and shouldn't be fixed (legacy). It also underpins some load-balancing/bonding tricks.

12. **Q: TRICKY — Two hosts on the same cable with the same MAC but different IPs. What happens?** A: The switch/NIC sees duplicate source MACs and flips the MAC table entry back and forth — frames destined to that MAC alternate unpredictably; ARP cache entries for both IPs map to the same MAC, so traffic is misdelivered. This is a config error (MAC cloning) and also how MAC-based load-balancing tricks break.

13. **Q: Can a switch be ARP-spoofed, or only hosts?** A: Hosts are the victims; but the *switch's MAC learning* can be abused — an attacker can flood the switch with fake source MACs to fill the MAC table (MAC flooding → switch floods unknown frames like a hub → traffic sniffing). DAI + MAC table limits defend.

14. **Q: What fields does an ARP packet carry?** A: Hardware type (1=Ethernet), protocol type (0x0800=IPv4), HLEN (6), PLEN (4), opcode (1=request, 2=reply), sender hardware addr, sender protocol addr, target hardware addr, target protocol addr. For Ethernet+IPv4 the body is 28 bytes, padded to 46 minimum payload for the 64-byte minimum Ethernet frame.

15. **Q: PRODUCTION — Why does a failover (keepalived VIP move) need gratuitous ARP?** A: Every host's ARP cache still points the VIP at the old node's MAC, and switches' MAC tables still map that MAC to the old port. The new active node sends GARP (its MAC for the VIP), so caches update and the switch re-learns the port — otherwise traffic keeps going to the dead node until TTLs expire.

16. **Q: SCENARIO — `tcpdump` shows ARP requests repeating every few seconds for the same IP with no replies. Diagnose.** A: A host can't reach a neighbor that doesn't exist or is blocked — retransmits continue (default 3 tries then FAILED). Check: is the target powered? Same broadcast domain? Is the request's sender IP one this interface owns (could be a stale multi-homed config)? Verify the target's firewall isn't dropping broadcasts and its `arp_ignore` is 0.

17. **Q: What's the difference between the ARP cache and the forwarding/switching table?** A: The ARP cache (host) maps IP→MAC for hosts *I* talk to. The switch MAC table maps MAC→port for all hosts seen on any port (used to forward frames). A host also maintains an IP route table; the switch never routes. These are three different tables.

18. **Q: Why does the destination MAC change at every hop while the IP stays the same?** A: MACs are hop-by-hop (next physical interface) — the frame is rebuilt at each router with the next hop's MAC as destination and the outgoing interface's MAC as source. IP is end-to-end and unchanged until NAT. This is the "MAC changes, IP stays" rule that underlies all routing.

## 14. Follow-Up Questions
1. **Q: What happens to an ARP cache entry when the NIC's MAC is changed (`ip link set eth0 address ...`)?** A: The kernel purges/resolves entries for that interface; neighbors' caches still hold the old MAC until they GARP or time out — so changing a MAC without GARP causes outages.

2. **Q: What is "ARP flux" on Linux?** A: With multiple interfaces on the same subnet and `arp_announce`/`arp_ignore` defaults, a host may reply with different source MACs/IPs depending on which interface the request arrived on — confusing peers and breaking routing. Fixed by tuning `arp_announce=2` etc.

3. **Q: What is the solicited-node multicast address derivation in IPv6?** A: `FF02::1:FFXX:XXXX`, where XX:XXXX = the *last 24 bits* of the target IPv6 address — so at most 2²⁴ neighbors share one solicited-node group, making NDP far cheaper than ARP's broadcast.

4. **Q: Why can't you use a MAC address to route across the Internet?** A: MACs are flat (no hierarchy), globally scattered, and have no aggregation — a router can't summarize "all MACs starting with AA" as a network. Routing needs hierarchical, aggregatable addresses (IP prefixes), which is why L2 is hop-local.

## 15. Coding Example
```python
import struct

def build_arp_request(sender_ip: str, sender_mac: str, target_ip: str) -> bytes:
    """Ethernet+IPv4 ARP request (RFC 826), as a raw frame (no preamble/FCS)."""
    s_ip = bytes(map(int, sender_ip.split(".")))
    t_ip = bytes(map(int, target_ip.split(".")))
    s_mac = bytes.fromhex(sender_mac.replace(":", ""))
    # 14-byte Ethernet header: dest=FFFF.., src, EtherType=0x0806
    eth = b"\xff" * 6 + s_mac + struct.pack("!H", 0x0806)
    arp = struct.pack("!HHBBH", 1, 0x0800, 6, 4, 1)  # hw=eth, proto=IPv4, op=1
    arp += s_mac + s_ip + b"\x00" * 6 + t_ip          # sender + target
    frame = eth + arp + b"\x00" * (46 - len(arp))     # pad to 46-byte payload
    return frame

def parse_arp(frame: bytes) -> dict:
    eth = frame[:14]
    arp = frame[14:42]
    htype, ptype, hlen, plen, op = struct.unpack("!HHBBH", arp[:8])
    shw, sip = arp[8:14], arp[14:18]
    thw, tip = arp[18:24], arp[24:28]
    return {"opcode": op, "sender_mac": shw.hex(":"), "sender_ip": ".".join(map(str, sip)),
            "target_ip": ".".join(map(str, tip))}

frame = build_arp_request("10.0.0.1", "ac:de:48:00:00:01", "10.0.0.2")
print(parse_arp(frame))
```
```bash
# Practical ARP/neighbor debugging on Linux
ip neigh show                          # ARP cache (state REACHABLE/STALE/PROBE...)
ip neigh del 10.0.0.2 dev eth0         # force re-resolution
ip -s neigh                            # cache stats
sysctl net.ipv4.neigh.default.gc_thresh3   # cache size cap (default 1024)
tcpdump -i eth0 -nn -e 'arp'           # watch ARP on the wire
sudo arpwatch -i eth0                  # log new/changed IP-MAC pairs (spoof detection)
```
```bash
# NDP for IPv6
ip -6 neigh show
tcpdump -i eth0 -nn 'icmp6 && ip6[40] == 135'   # Neighbor Solicitation
```

## 16. Industry Usage
- **Every LAN frame ever sent**: ARP resolves the gateway; Ethernet switches learn from it; DHCP hands IPs that ARP then maps.
- **HA/failover**: keepalived, VRRP (RFC 3768), Linux bond/lacp, and cloud VIPs all use gratuitous ARP to move a floating IP to the new active node.
- **Cloud/DC fabric**: VPC overlays (VXLAN) decouple tenant MAC/IP from the fabric, so ARP/NDP run inside the tenant VRF while the physical network maps to its own addresses; smart NICs (SmartNIC/DPU) offload ARP/NDP handling and MAC learning.
- **Security products**: Dynamic ARP Inspection (DAI), DHCP snooping, port-security, and arpwatch-class tools are standard switch/access-layer controls in every enterprise.
- **Linux networking**: the entire neighbor subsystem (`net/ipv4/neighbour.c`, `arp.c`), `ip neigh`, `arp_ignore/announce`, and `CONFIG_IP_PNP` for boot-time ARP; DPDK/XDP users can intercept ARP at line rate.

## 17. References
- RFC 826 (An Ethernet Address Resolution Protocol) — https://datatracker.ietf.org/doc/html/rfc826
- RFC 5227 (IPv4 Address Conflict Detection) — https://datatracker.ietf.org/doc/html/rfc5227
- RFC 1027 (Using ARP to Implement Transparent Subnet Gateways) — https://datatracker.ietf.org/doc/html/rfc1027
- RFC 4861 (Neighbor Discovery for IPv6) — https://datatracker.ietf.org/doc/html/rfc4861
- IEEE 802-2014 (MAC address structure, OUI) — https://standards.ieee.org/ieee/802/6906/
- Kurose & Ross, *Computer Networking*, 8th ed., §6.4.1 (ARP).
- Linux kernel docs: `Documentation/networking/ip-sysctl.rst` (neighbor sysctls) — https://docs.kernel.org/networking/ip-sysctl.html

## 18. Cheat Sheet
- MAC = 48-bit, 12 hex digits, flat/unrouteable, first 3 bytes OUI.
- I/G bit = LSB of first byte (0 unicast, 1 multicast); U/L bit = bit 1 (0 global, 1 local).
- Broadcast MAC = `FF:FF:FF:FF:FF:FF`; IPv4 multicast `01:00:5E:...`; IPv6 `33:33:...`.
- ARP: request = broadcast, reply = unicast; EtherType `0x0806`; opcode 1/2.
- ARP body (Ethernet+IPv4): 28 bytes = htype(2) ptype(2) hlen(1) plen(1) op(2) + sender MAC(6)+IP(4) + target MAC(6)+IP(4).
- Resolve the *gateway* when dest is off-subnet; cache with TTL (`ip neigh`).
- GARP: announce/dup-detect/failover (keepalived); RFC 5227 DAD.
- Attacks: ARP spoofing/poisoning (MITM); defenses DAI, DHCP snooping, static ARP.
- IPv6 replaces ARP with NDP (RFC 4861) via ICMPv6 + solicited-node multicast.
- MAC changes per hop; IP stays constant end-to-end.

## 19. Quiz
1. MAC address length: a) 32-bit b) 48-bit c) 64-bit d) 128-bit → **b**
2. The broadcast MAC address is: a) `00:00:00:00:00:00` b) `FF:FF:FF:FF:FF:FF` c) `AA:AA:AA:AA:AA:AA` d) `FF::` → **b**
3. ARP request is sent as: a) unicast b) multicast c) broadcast d) anycast → **c**
4. ARP maps: a) name→IP b) IP→MAC c) MAC→port d) IP→port → **b**
5. The ARP opcode for a reply is: a) 1 b) 2 c) 3 d) 0 → **b**
6. The EtherType for ARP is: a) `0x0800` b) `0x0806` c) `0x8100` d) `0x86DD` → **b**
7. Which replaces ARP in IPv6? a) DHCPv6 b) NDP c) IGMP d) DNS → **b**
8. The first 3 bytes of a globally-unique MAC identify: a) the user b) the manufacturer (OUI) c) the subnet d) the switch port → **b**

**Answers**: 1-b, 2-b, 3-c, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: What is ARP?** → **A:** RFC 826: resolves local IP→MAC via broadcast request + unicast reply, cached in the neighbor table.
- **Q: MAC size and structure?** → **A:** 48 bits; I/G bit, U/L bit, OUI (first 3 octets), NIC-assigned last 3 octets.
- **Q: Broadcast MAC?** → **A:** `FF:FF:FF:FF:FF:FF`, accepted by all NICs.
- **Q: What is gratuitous ARP used for?** → **A:** Announcement, duplicate detection (RFC 5227), failover/VIP moves.
- **Q: How does IPv6 resolve neighbors?** → **A:** NDP over ICMPv6 using solicited-node multicast; no broadcasts, supports SEND auth.
- **Q: Why is ARP insecure?** → **A:** No authentication — anyone can answer → spoofing/MITM; defended by DAI/static ARP.
- **Q: Who does ARP resolve when the dest is off-subnet?** → **A:** The default gateway's MAC — frames always go hop-by-hop.

## 21. Revision
A MAC address is the flat, 48-bit, hardware-bound identifier a frame's destination field carries on a single LAN; ARP (RFC 826) is how a host learns the MAC for a local IP — a broadcast request, a unicast reply, cached in `ip neigh` with TTLs. Key facts: MAC = 12 hex digits, first 3 bytes OUI, I/G bit = LSB of byte 1, broadcast = all FF; ARP EtherType `0x0806`, opcode 1 request/2 reply, 28-byte body; when the destination is off-subnet you ARP the *gateway*; MAC changes at every hop, IP doesn't. Gratuitous ARP powers failover (keepalived) and duplicate detection; ARP spoofing is the classic L2 MITM (defend with DAI/DHCP snooping/static entries); IPv6 abolishes ARP in favor of NDP over ICMPv6 with solicited-node multicast and optional SEND authentication. Anchor: *ARP = "who has this IP?" knocked on every LAN door; DNS = global name→IP; never confuse the two.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "ARP vs DNS?" | 1 / 13-Q1 |
| "Describe a MAC address" | 7 / 13-Q2 |
| "Walk through an ARP exchange" | 8 / 13-Q3 |
| "What is gratuitous ARP?" | 13-Q4 / 3 |
| "How does ARP spoofing work and how do you defend?" | 13-Q5 / 12 |
| "When do you ARP the gateway?" | 13-Q6 |
| "ARP cache overflow — diagnose" | 13-Q9 |
| "How does IPv6 replace ARP?" | 13-Q10 |
| "Why does MAC change per hop but IP stays?" | 13-Q18 |
| "What is proxy ARP?" | 13-Q11 |
