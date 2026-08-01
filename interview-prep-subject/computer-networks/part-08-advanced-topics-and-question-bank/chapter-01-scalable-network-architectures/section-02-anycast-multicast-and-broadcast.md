# Anycast, Multicast, and Broadcast

> **TL;DR**: Beyond unicast's one-to-one delivery: anycast sends your packet to *one* of many identical servers (the nearest, via routing — DNS, CDN edge, DDoS scrub); multicast delivers to *every interested member* of a group with one copy per link (IPTV, PTP); broadcast delivers to *everyone* on a local link (ARP, DHCP) and never routes.

## 1. Why Does This Exist?
Unicast (one sender → one receiver) is the internet's default, but three other delivery models exist because reality needs them:
- **Anycast**: for resilience and low latency. The same service (DNS resolver, CDN edge, DDoS scrubber) runs in many locations; a *single* IP address represents all of them, and the routing system picks the closest. Without it, every query would cross continents and one failure would take out the entire "one node."
- **Multicast**: for *efficient one-to-many*. Streaming the same video to a million viewers as unicast means a million copies crossing shared links. Multicast lets a packet be sent once and *copied by routers* only where it forks toward members — linear cost, not linear-per-receiver cost. It's the only sane way to do IPTV/live distribution at scale.
- **Broadcast**: for *local, link-scoped discovery*. A host that doesn't know the Ethernet MAC of a peer, or that needs to find a DHCP server, sends a "to everyone on this link" message. It's intentionally bounded to the local link because flooding it across the internet would be catastrophic.
Each model trades semantics (one-of-many, one-to-many, one-to-all) and scope (global/group/local) to match the job.

## 2. How Does It Work?
- **Anycast**: the same IP prefix is *announced* via BGP from multiple sites (e.g., 1.1.1.1 from hundreds of Cloudflare PoPs). Routers compute the best path and forward to the *nearest* instance. The decision is made by the routing protocol at each hop — no application awareness. Delivery = "exactly one instance, the best-reachable one." Uses BGP as the load balancer.
- **Multicast**: a sender addresses packets to a *group address* (224.0.0.0/4 IPv4, ff00::/8 IPv6). Hosts *join* groups via **IGMP** (IPv4) / **MLD** (IPv6) to their local router; routers build a delivery tree using **PIM** (Protocol Independent Multicast: sparse-mode/DM) or **DVMRP**; each router copies the packet only onto interfaces that lead to members. RPF (reverse path forwarding) checks prevent loops. Delivery = "one copy per link, delivered to every current member."
- **Broadcast**: L2 broadcast (FF:FF:FF:FF:FF:FF) floods the frame to every port in the VLAN; L3 limited broadcast (255.255.255.255) is *confined to the local link/subnet* (RFC 919/922) — routers never forward it (they may answer for protocols like DHCP via relay). Delivery = "everyone on this link." IPv6 drops broadcast entirely (replaced by multicast ff02::1 and ff02::2).

## 3. When Is It Used?
- **Anycast**: DNS resolvers (8.8.8.8, 1.1.1.1), DNS root/authoritative servers, CDN edge IPs, DDoS scrubbing centers, some API/load-balancer VIPs, and NTP (pool/anycast). Also RFC 4786 general guidance.
- **Multicast**: IPTV/linear TV, live sports/live-streaming backhaul, PTP (precision time sync) over multicast, financial market-data feeds, software deployment to many hosts, gaming LANs, IPv6 SLAAC/router discovery (link-local multicast), mDNS/Bonjour, and SSDP.
- **Broadcast**: ARP (find a MAC for an IP), DHCP/DHCPv6 (discover a server), NetBIOS/legacy discovery, and IPv4-only local protocols. All confined to the local link/VLAN.

## 4. Why Wasn't Another Approach Chosen?
- *Anycast vs "unicast + DNS round-robin":* DNS RR can't pick the *nearest* and caches make it stale — anycast lets the *network* choose the closest live node and self-heals when one dies (no DNS change). Chosen wherever "nearest stateless replica" is the goal.
- *Anycast vs "unicast with GSLB":* GSLB (Section 01) is deterministic and region-aware (good for stateful/region decisions); anycast is automatically nearest and absorbs failures. Real systems use GSLB for the region, anycast for the nodes.
- *Multicast vs "N unicast copies":* For one-to-many at scale, unicast is N× bandwidth on shared links; multicast is ~1 copy per unique path — an O(V) saving that makes IPTV/efficient group delivery possible. Its costs (complexity, state, some network operators disable it) are why it lost to CDNs for on-demand video (unicast from caches) — the *edge* replicates instead.
- *Broadcast vs multicast:* Broadcast is dumb (floods everyone, even those who don't care) but zero-setup (no join protocol) — fine for small local discovery (ARP). Multicast requires joins and router state but is selective and routable — chosen when scale/link sharing or routing is needed.
- *IPv6:* broadcast was abolished — all "everyone on link" uses multicast (ff02::1) because multicast is selective and cheaper; this is the modern design.

## 5. Intuition
- **Anycast**: a **chain of identical coffee shops**. You search "coffee" and the map app (routing) always sends you to whichever of the (identical) stores is nearest. If one closes, the map app reroutes you to the next. You never know which store served you — they're interchangeable.
- **Multicast**: a **conference call / megaphone broadcast to a mailing list**. You speak once (one packet); the phone system (routers) copies your voice only to the branches that have a listener. People who hung up don't get the audio. One utterance, N listeners, minimal copies.
- **Broadcast**: a **town crier in the village square** — everyone within earshot (the local link) hears it, and the crier is bound to the square (never routed to the next town). Perfect for "hey, anyone got this MAC?"

## 6. Real-World Analogy
The **highway + freight system**:
- *Anycast* = several identical depots (same address, "Depot 7") in different cities. A trucker (packet) with a package addressed to "Depot 7" simply drives to the nearest depot; dispatchers (routers) pick the depot by proximity, and if the local depot is closed (down), trucks route to the next one automatically. The sender just writes "Depot 7."
- *Multicast* = a single broadcast feed from the studio (sender) where the *rail company* (routers) copies the signal only at junctions that lead to subscriber towns (members), and only down the branches with subscribers — one transmission from the studio, deliveries only where people subscribe.
- *Broadcast* = a loudspeaker announcement in one town's central square that reaches everyone in the square but never travels down the highway to the next town. Anyone who wasn't there misses it.

## 7. Formal Definition
- **Unicast**: 1:1 — one source, one destination address; the internet's default; every standard connection.
- **Anycast** (RFC 4786): a unicast address *and* a service; multiple nodes announce the same prefix; routers forward to the "closest" (best BGP path). Delivery: exactly one receiver, the nearest reachable instance. Addressing: *topologically-aware* (the address doesn't name a specific node, it names "the nearest node offering X").
- **Multicast**: 1:N (group) — a single address (224.0.0.0/4, ff00::/8) names a *group*; members join/leave; routers replicate toward members. Protocols: **IGMPv3** (IPv4 host-router), **MLDv2** (IPv6), **PIM-SM/DM**, **SSM** (source-specific multicast, 232.0.0.0/8), **MBGP/MSDP** for inter-domain. RPF: a multicast packet is accepted only if it arrived on the interface that leads back to the source (loop prevention).
- **Broadcast**: 1:all on a link — L2 `ff:ff:ff:ff:ff:ff` (all ports in the broadcast domain) or L3 `255.255.255.255` (all hosts on the subnet). Routers forward broadcast *to the local subnet only* (they can relay DHCP via helper-address). No join, no state, maximum flooding. IPv6: no broadcast — `ff02::1` (all nodes) multicast.
- **Scope**: anycast = global (routing-driven), multicast = group (routable but gated by membership), broadcast = link-local only.

## 8. Example
**Anycast path (1.1.1.1 from Mumbai):**
```
Client 103.21.x.x → "1.1.1.1" (Cloudflare, advertised from ~300 PoPs worldwide)
Route lookup: BGP best path → nearest Cloudflare PoP (Mumbai/Chennai) 
  → packets reach the LOCAL instance; RTT ~5-30ms.
If Mumbai PoP's route disappears → BGP converges → next-closest PoP (Singapore).
The client never changes its target IP.
```
**Multicast (IPTV channel, 232.1.1.1):**
```
Set-top box: IGMPv3 JOIN 232.1.1.1 → local router adds it to the group's outgoing list
Routers: PIM-SM builds a tree from the source to all members (RP = rendezvous point)
Head-end sends ONE copy of the stream → each router replicates ONLY toward
branches with members → receiver in every subscribed household; unsubscribed
houses get nothing; the shared uplink carries one copy, not N.
```
**Broadcast (ARP on a /24):**
```
Host A wants 192.168.1.5's MAC → ARP broadcast 192.168.1.5 (dest MAC ff:ff:ff:ff:ff:ff)
→ ALL hosts on the /24 receive it; only 192.168.1.5 replies with its MAC (unicast ARP reply).
The broadcast never leaves the subnet — no router forwards it.
```

## 9. Internal Working
1. **Anycast**: BGP advertises the prefix from each site (with the same AS path attributes for the "same service" semantics); routers select the best path (shortest AS path + MED/local-pref). Sites tune advertisements (e.g., AS-prepend to make a site less attractive) to balance load. Anycast sessions are prone to *shift*: if the best path changes, traffic moves; therefore state must not be tied to a single instance.
2. **Multicast join**: IGMPv3/MLDv2 reports establish host membership on the leaf router; PIM-SM uses an RP for sparse-mode trees (shared tree → switchover to source tree after data flows); SSM (source-specific) simplifies to (S,G) tree building without an RP. RPF check: the packet must arrive on the interface used to reach the source, else drop — the loop guard.
3. **Multicast forwarding**: a router keeps (S,G)/(*,G) state per group with an OIF (outgoing interface) list; it copies each received packet once per OIF (hardware replication in modern switches, e.g., via multicast replication in ASICs).
4. **Broadcast**: switches flood L2 broadcast to all ports in the VLAN (a copy to each); L3 broadcast is received by every host on the subnet; protocols like DHCP listen on UDP 67/68 and answer (DHCP also uses relay agents to route the request to a server). Broadcast storms: loops + flooding → hence STP (Part 05) and storm-control.
5. **Failure behavior**: anycast = automatic failover (BGP convergence); multicast = group state times out if members stop reporting (IGMP queries); broadcast = no state, purely flooded.

## 10. Time Complexity / Performance
- **Anycast**: one extra BGP advertisement per site; convergence seconds-minutes (tunable: BFD + fast-reroute); RTT = distance to nearest node (5-60 ms typical). Load is "proximity-based" — a busy nearest node takes the traffic (needs anycast tuning: prepends, or LB-hairpin). No per-packet overhead beyond normal routing.
- **Multicast**: one copy per OIF; replication is hardware offloaded on datacenter/IPTV switches (tens of Gbps per group); control-plane cost is (S,G) state per group per router — a concern at massive group counts (state explosion). RPF adds one lookup. Latency: no per-receiver sender cost — the bottleneck is the tree's slowest path.
- **Broadcast**: cost = N copies of the frame (one per recipient port); constant latency; but every broadcast interrupts every host (a /24 ARP broadcast = 254 receivers), so high broadcast rates cause CPU/packet loss on hosts ("broadcast storm") — keep broadcast domains small (VLAN size), use storm control.

## 11. Advantages
- **Anycast**: automatic failover (no DNS/state changes), low latency (nearest node), DDoS absorption (scrub at the edge), simple client config (one IP).
- **Multicast**: linear cost for one-to-many (one copy per unique link) — the only scalable way to do live broadcast-style delivery; low sender load (send once); supports join/leave dynamically.
- **Broadcast**: zero setup/state (works out of the box), simple, perfect for small local discovery protocols.

## 12. Disadvantages
- **Anycast**: not for stateful services (session loss on route change); load imbalance (nearest ≠ capacity-aware); BGP convergence black-holes; address space is "topological" (can't easily do per-instance accounting); troubleshooting is harder (which instance answered?).
- **Multicast**: complex (IGMP/PIM/RP/SSM, inter-domain MSDP); group state explosion; some operators disable inter-domain multicast; reliability/flow control are absent (UDP-based; needs FEC/redundant streams); NAT/access-control friction.
- **Broadcast**: floods everyone (wasteful, privacy leak); bounded to one link (can't route); storms degrade the whole domain; IPv6 eliminated it (multicast instead).
- **General**: all three are *one-way* delivery models (UDP-family) — no built-in reliability, ordering, or congestion control (except the transport above them).

## 13. Interview Questions
1. **Q: What are the four delivery models and their scope?** A: Unicast (1:1, default), anycast (1:nearest-of-many, global via routing), multicast (1:group, routable with membership), broadcast (1:all on the link, local only). Key axis: how many receivers and whether routers make the choice (anycast) or membership does (multicast).

2. **Q: How does anycast choose the server?** A: The same IP prefix is BGP-announced from multiple sites; each router forwards to the *best path* toward the prefix, so packets converge on the nearest reachable instance. The routing table (not DNS, not the app) picks the node. It's "unicast addressing + routing-based placement."

3. **Q: Why do DNS resolvers use anycast?** A: 8.8.8.8/1.1.1.1 are anycast — (1) low latency (nearest PoP), (2) resilience (PoP failures auto-route around), (3) DDoS absorption (attack spreads across PoPs, each absorbs its share). The resolvers are stateless/cache-replicated, so anycast is safe for them.

4. **Q: Why can't you anycast a stateful app?** A: If routing converges mid-session (link flap, policy change), your connection jumps from node A to node B — B has no TCP/session state, so the connection breaks. Anycast requires *stateless* or replicated-state nodes (resolvers, cache servers, TLS-terminating proxies that can forward). Stateful apps need DNS GSLB + sticky sessions (Section 01).

5. **Q: What is multicast and when is it used?** A: A group-delivery model: one packet sent to a group address is copied by routers only toward members. Used for IPTV/live video, PTP, market data, IPv6 discovery. It turns N× unicast bandwidth into ~one copy per unique path — the only way to do efficient one-to-many.

6. **Q: How do hosts join a multicast group?** A: The host sends an IGMP (IPv4) / MLD (IPv6) membership report to its local router; the router maintains group state and builds the delivery tree (PIM-SM via an RP, or SSM source-specific). Leaves happen via timeouts on periodic IGMP queries.

7. **Q: What is the RPF check in multicast?** A: Reverse Path Forwarding: a multicast packet is accepted only if it arrived on the interface that the router would use to reach the source. This prevents loops in multicast trees (where unicast's hop-by-hop anti-loop doesn't apply). It's the multicast loop guard.

8. **Q: TRICKY — What is the difference between a broadcast and a multicast at L2?** A: L2 broadcast (ff:ff:ff:ff:ff:ff) floods to *every* port in the VLAN — everyone receives it regardless of interest. L2 multicast (01:00:5e:...) is *selective*: it's delivered only to ports that subscribed (IGMP snooping), others aren't disturbed. Both are switch-copied, but multicast is interest-filtered, broadcast is not. That's why IPv6 replaced broadcast with multicast.

9. **Q: Why did IPv6 abolish broadcast?** A: Broadcast floods everyone (waste + privacy + DoS vector) and can't route. IPv6 uses link-local multicast instead: ff02::1 (all nodes), ff02::2 (all routers) — selective, extensible, and leaves room for group-specific scopes. Every "everyone on link" function maps to a multicast group.

10. **Q: PRODUCTION — An IPTV service with 100k concurrent viewers. Why multicast instead of unicast from a CDN?** A: For *live* linear channels, unicast means each of 100k viewers gets a stream across the shared uplink — bandwidth = 100k × stream rate on the last mile/core, and the sender must emit 100k copies. Multicast: one copy per unique link (a shared last-mile carries one copy to a community), sender emits once, and the tree replicates only toward subscribers. Trade-offs: on-demand/VOD stays unicast-from-CDNs (caches replicate content); multicast is for *same-content-same-time* distribution.

11. **Q: What is the difference between PIM-SM and SSM?** A: PIM-SM (sparse mode) is group-based (*,G): joins go to an RP (rendezvous point), then switch to a source tree — works for many-to-many, has RP complexity. SSM (source-specific, 232.0.0.0/8): the receiver specifies the *source* address, building a direct (S,G) tree with no RP — simpler, more scalable, and the standard for IPTV/live. SSM is what modern deployments prefer.

12. **Q: What is a "broadcast storm" and how do you prevent it?** A: A loop in a broadcast domain makes switches flood broadcast endlessly (each loop hop duplicates), saturating links and pegging host CPUs. Prevention: STP/RSTP (Part 05) to break loops, storm-control/broadcast suppression on switchports, VLAN size limits, and careful topology. It's why STP is not optional.

13. **Q: TRICKY — Can anycast and multicast be combined?** A: They address different problems (routing-selects-one vs membership-selects-many) and are orthogonal — an anycast-announced group address isn't standard. But anycast and *unicast* GSLB combine constantly (Section 01: GSLB picks region, anycast picks node); multicast and anycast rarely mix because multicast needs the tree built to members, not "nearest." Keep them separate in answers.

14. **Q: What is IGMP snooping?** A: On an L2 switch, IGMP snooping reads IGMP membership reports to learn *which ports* have members, so multicast frames are only flooded to those ports — not the whole VLAN. Without it, multicast would behave like broadcast (flood to all ports in the VLAN), destroying the selectivity that makes multicast efficient.

15. **Q: SCENARIO — Multicast video works in one VLAN but not across two. Why?** A: (1) No PIM on the router (multicast routing disabled); (2) missing RP (sparse-mode without a rendezvous point); (3) IGMP query is on one subnet only / querier election issue; (4) the router's multicast routing table has no (S,G) state (check `show ip mroute`); (5) firewall/ACL blocking 232.0.0.0/8. Debug: verify joins on the receiver (`show ip igmp groups`), tree on the router, and that the source tree exists.

16. **Q: What is a "limited broadcast" vs "directed broadcast"?** A: Limited = 255.255.255.255, confined to the *local subnet* (never routed, always sent to the local network). Directed = subnet's broadcast (e.g., 192.168.1.255 for 192.168.1.0/24), routable *to* that subnet (though routers disable it by default now, RFC 2644, to stop smurf-style amplification). ARP is an L2 broadcast (ff:ff:ff:ff:ff:ff), neither of the L3 forms.

17. **Q: PRODUCTION — Design low-latency market-data delivery to 5000 trading firms.** A: Multicast over a dedicated low-latency network (SSM, 232.0.0.0/8) with per-firm filtering; PTP (multicast, RFC 8173) for timestamp sync to µs; IGMP snooping + querier per segment; redundant sources (stream A/B) since multicast is UDP (no retransmit) — firms dedup on sequence numbers; unicast for request/response (orders) with TCP/QUIC. This is exactly how exchange feeds (NASDAQ, CME) work.

## 14. Follow-Up Questions
1. **Q: What is the difference between IGMPv3 and IGMPv2?** A: v2 supports group join/leave only (*,G). v3 adds source filtering (INCLUDE/EXCLUDE lists) — needed for SSM (join a specific source, ignore others). IPv6 uses MLDv2 which mirrors IGMPv3 semantics.

2. **Q: What is an RP (rendezvous point)?** A: In PIM-SM, the central meeting point: receivers join the shared tree at the RP, and sources send to the RP; after data flows, routers switch to a direct source tree for efficiency. RP redundancy (anycast-RP/MSDP) is needed for HA.

3. **Q: What is "group state explosion"?** A: Each multicast group requires (S,G) state in every on-tree router; millions of simultaneous live groups (IPTV channels × regions) can exhaust router memory. Mitigations: SSM (fewer states, no RP), forwarding planes that aggregate, and careful group addressing.

4. **Q: How does anycast affect TCP vs UDP?** A: Anycast works fine for stateless UDP (DNS) and for TCP *if* connection state is shared/replicated or sessions are short (and reconnection is cheap). Long-lived TCP over anycast risks mid-flow route shifts breaking connections; UDP + short-lived requests (DNS) are the classic safe cases.

## 15. Coding Example
```python
# Simulate anycast "nearest node" selection and multicast "copy per unique path"
import heapq

def anycast_nearest(sites, client):
    # sites: {prefix_owner: {ip, latency_to_client}}
    return min(sites, key=lambda s: sites[s]["latency"])

sites = {"blr": {"latency": 5}, "sin": {"latency": 30}, "fra": {"latency": 140}, "iad": {"latency": 250}}
print("anycast picks:", anycast_nearest(sites, "mumbai"))          # blr

def multicast_edges(graph, group_members):
    # graph: {router: [neighbor, ...]} ; returns edges carrying the group stream
    import itertools
    members = set(group_members)
    edges = set()
    for a, b in itertools.combinations(members, 2):
        edges.add((a, b))
    return edges
print("multicast copies one per unique member-edge pair:",
      multicast_edges({}, {"house1", "house2", "house3"}))
```
```bash
# Linux real-world multicast/broadcast/anycast ops
ip maddr show                       # multicast group memberships of this host
ip -4 route show table all | grep -i multicast      # multicast route state
# Capture an ARP broadcast (L2 broadcast) and a multicast join:
sudo tcpdump -i eth0 'arp or (udp port 5353)' -c 20        # ARP + mDNS multicast
sudo tcpdump -i eth0 -e 'ether dst ff:ff:ff:ff:ff:ff' -c 5 # only L2 broadcasts
# Confirm anycast reachability of a DNS resolver (which instance?):
mtr -n -r -c 10 1.1.1.1            # RTT path -> nearest Cloudflare PoP
dig +short @1.1.1.1 example.com    # resolver works over anycast
# IPv6 link-local multicast (all nodes on the link):
ping6 -I eth0 ff02::1 -c 2         # everyone on the link answers
```

## 16. Industry Usage
- **Anycast**: Cloudflare/Google/Akamai (resolvers, CDN edge, DDoS scrub), DNS root servers (~1500 instances), NTP (Cloudflare's time.cloudflare.com), modern API edges.
- **Multicast**: IPTV/linear TV (ISPs, broadcasters), market-data feeds (NASDAQ, CME, Reuters), PTP time sync (finance/telecom/5G), datacenter "elephant" data distribution, IPv6 SLAAC (ff02::), mDNS (Bonjour), SSDP.
- **Broadcast**: ARP, DHCP (L2/L3 broadcast + relay), legacy discovery; every IPv4 LAN uses it daily.
- **Cloud**: GCP/AVS now expose multicast-enabled VPCs for market-data workloads; AWS offers multicast via Transit Gateway for on-prem extension.

## 17. References
- RFC 4786 (IP Anycast) — https://datatracker.ietf.org/doc/html/rfc4786
- RFC 1112 (IGMPv1), RFC 3376 (IGMPv3) — https://datatracker.ietf.org/doc/html/rfc3376 ; RFC 4607 (SSM), RFC 7761 (PIM-SM)
- RFC 8173 (PTP over multicast), RFC 919/922 (broadcasting internet datagrams)
- RFC 2644 (directed broadcast handling), RFC 4291 (IPv6 addressing — multicast ff00::/8)
- Kurose & Ross, *Computer Networking*, 8th ed., §4.5 (multicast), §1.3.
- Cloudflare "What is anycast?" — https://www.cloudflare.com/learning/cdn/glossary/anycast-network/

## 18. Cheat Sheet
- Unicast 1:1 | anycast 1:nearest-of-many | multicast 1:group | broadcast 1:all-on-link.
- Anycast = same IP, many BGP announcements; routers pick nearest; stateless-only; auto-failover; DDoS absorb.
- Multicast = group address (224/4, ff00::/8); IGMP/MLD joins; PIM-SM/SSM trees; RPF loop guard; one copy per unique link.
- Broadcast = ff:ff:ff:ff:ff:ff (L2) / 255.255.255.255 (L3 limited) — link-local only, never routed; IPv6 replaced it with ff02:: multicast.
- IGMP snooping = switch learns member ports (else multicast ≈ broadcast flood).
- SSM (232/8) = receiver specifies source, no RP — the modern IPTV model.
- Broadcast storms = loops + flooding → STP + storm control.
- PTP (RFC 8173) uses multicast for µs time sync.

## 19. Quiz
1. Anycast selects the node via: a) DNS b) routing (BGP) c) GeoIP d) health checks → **b**
2. Anycast is safe for: a) stateful TCP sessions b) stateless services c) databases d) websockets → **b**
3. Multicast delivers: a) to all on link b) to all group members c) to the nearest d) one-to-one → **b**
4. Which protocol builds the multicast tree? a) IGMP b) PIM c) BGP d) DHCP → **b**
5. The RPF check prevents: a) loops b) broadcast storms c) DDoS d) fragmentation → **a**
6. IPv6 replaced broadcast with: a) unicast b) multicast c) anycast d) nothing → **b**
7. IGMP snooping: a) routes multicast b) limits multicast to interested ports c) encrypts d) nothing → **b**
8. L3 limited broadcast is: a) routable b) link-local only c) anycast d) group-based → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-a, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: Four delivery models** → **A:** unicast (1:1), anycast (nearest of many), multicast (group), broadcast (all on link).
- **Q: How does anycast pick the server?** → **A:** BGP best-path routing to the nearest of several same-IP nodes.
- **Q: Why not anycast stateful apps?** → **A:** Route convergence breaks in-flight TCP/session state.
- **Q: What is multicast's benefit?** → **A:** One copy per unique link for one-to-many — the IPTV/efficient broadcast model.
- **Q: How do hosts join a group?** → **A:** IGMP/MLD reports to the router; routers build PIM trees.
- **Q: What is the RPF check?** → **A:** Accept only packets arriving on the interface toward the source — loop guard.
- **Q: Why did IPv6 kill broadcast?** → **A:** Wasteful flooding; replaced by link-local multicast (ff02::1/2).

## 21. Revision
Anycast: same IP from many sites; BGP routes to nearest; stateless-only; auto-failover; DDoS scrub. Multicast: group addresses (224/4, ff00::/8); IGMP/MLD joins; PIM-SM/SSM trees; RPF loop guard; one copy per link — the efficient one-to-many model (IPTV, PTP, market data). Broadcast: ff:ff:ff:ff:ff:ff / 255.255.255.255, link-local only, no join/state, storm-prone (STP + storm control); IPv6 replaced it with multicast. Key contrasts: anycast = routing picks one (stateless, "nearest"); multicast = membership picks many (stateful trees, "members"); broadcast = everyone on the link, zero selectivity. Anchors: *anycast = same-IP nearest via BGP, stateless-only; multicast = one copy per unique path to members (IGMP/PIM/SSM, RPF); broadcast = local-link flood, never routed, IPv6's ff02::1.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "The four delivery models" | 13-Q1 |
| "How does anycast choose a server?" | 13-Q2 |
| "Why anycast DNS resolvers?" | 13-Q3 |
| "Why not anycast stateful apps?" | 13-Q4 |
| "What is multicast and when used?" | 13-Q5 |
| "How do hosts join a group?" | 13-Q6 |
| "What is the RPF check?" | 13-Q7 |
| "L2 broadcast vs multicast" | 13-Q8 |
| "Why did IPv6 abolish broadcast?" | 13-Q9 |
| "Multicast vs unicast CDN for live" | 13-Q10 |
| "PIM-SM vs SSM" | 13-Q11 |
| "Broadcast storms" | 13-Q12 |
| "What is IGMP snooping?" | 13-Q14 |
| "Multicast not crossing VLANs — debug" | 13-Q15 |
| "Design market-data delivery" | 13-Q17 |
