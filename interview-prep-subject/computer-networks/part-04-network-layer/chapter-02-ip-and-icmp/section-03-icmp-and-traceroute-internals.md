# ICMP and Traceroute Internals

> **TL;DR**: **ICMP** (Internet Control Message Protocol) is IP's control/error channel — echo (ping), destination-unreachable, time-exceeded, redirect, and parameter-problem messages that report network conditions to the source; **traceroute** exploits the TTL field to force each router to send ICMP time-exceeded and reconstruct the path hop by hop.

## 1. Why Does This Exist?
IP is *stateless and silent*: a packet that can't be delivered, is too big, has expired (TTL), or hits a blackhole produces **no error by itself** — the sender would wait forever. ICMP exists so the network can *tell the source what happened*: "destination unreachable (host/network/protocol/port)", "fragment needed (MTU too small)", "time exceeded (TTL reached 0)", "redirect (use this better route)", "parameter problem (malformed header)". It's the *control plane's mouth* — not a transport for user data (that's TCP/UDP) but a low-bandwidth status/notification channel between IP implementations. It also powers the diagnostic tools *everyone* uses: **ping** (echo request/reply — "are you there? how long does a round trip take?") and **traceroute** (deliberately expire TTLs to map the path). ICMP exists because a self-correcting network needs *feedback*, and the feedback must be separate from the data plane to be trustworthy and minimal.

## 2. How Does It Work?
- **ICMP messages**: header (type, code, checksum) + a portion of the offending packet (IP header + 8 bytes) so the source can identify it. Carried *inside* IP (protocol 1) — ICMP is IP's payload, not a separate layer-3 protocol.
- **Main types**:
  - **Echo request/reply (8/0)**: the ping pair.
  - **Destination unreachable (3)**: codes — 0 network unreachable, 1 host unreachable, 2 protocol unreachable, 3 port unreachable, 4 fragmentation needed (with MTU), 13 administratively prohibited.
  - **Time exceeded (11)**: 0 TTL expired in transit (traceroute's breadcrumb), 1 fragment reassembly timeout.
  - **Redirect (5)**: "don't send via me; go direct / via a better router."
  - **Parameter problem (12)**: header malformed.
  - **Source quench (4)**: obsolete congestion notification.
- **Ping**: sends echo requests (with ID/seq), the peer replies; computes RTT, loss, and TTL → "is it up, how fast, how many hops."
- **Traceroute**: sends UDP probes to high ports (or ICMP echoes) with TTL=1,2,3,... — each router at the TTL boundary drops the probe and returns ICMP time-exceeded (with its address); when the destination replies (port unreachable — nothing listens on the high port) or an echo reply comes, the path is complete. ICMP-based (Linux default) or UDP-based (traceroute) or TCP-based (mtr's variant).
- **Error-reporting rules**: ICMP errors are generated *for ordinary datagrams only* (not for ICMP errors, fragments, broadcast, multicast) — to avoid error storms.
- **Security**: ICMP is rate-limited and often partially filtered (ping allowed, unreachable/redirect dropped) — both as DoS protection and as "stealth" hardening.

## 3. When Is It Used?
- **Ping — reachability + latency**: the universal liveness check; `ping -c 5 host` reports loss + RTT (min/avg/max/mdev) + TTL (hop distance hint).
- **Traceroute / mtr — path mapping**: find where packets go, where they stall, and which hop is slow; `mtr` runs it continuously (traceroute + ping).
- **MTU discovery**: "fragmentation needed" (code 4) with the new MTU — the mechanism behind path-MTU discovery (RFC 1191).
- **Router redirects**: a host learns a better route from the router ("don't go through me — the target is on your own link").
- **Protocol/port testing**: ICMP port-unreachable tells you "this host is up but nothing listens on that port" (how port scanners + traceroute's final hop work).
- **Error diagnosis**: `netstat -s`/`ip -s` counters of ICMP errors; "destination unreachable" in traceroute output.
- **Tunnels/overlays**: ICMP is often the *canary* (ping the tunnel end) and sometimes rides inside tunnels (gre/ICMP tunnels for covert channels — a security topic).

## 4. Why Wasn't Another Approach Chosen?
- **Why a separate protocol instead of TCP/UDP messages?** Errors must be reportable by *any* device on the path (routers — which have no TCP/UDP state) and must not depend on the *very transport that failed* (a TCP error message about a failed TCP flow can't rely on TCP). A minimal, IP-embedded control channel (protocol 1) is available to every IP implementation and independent of the data flow.
- **Why only report errors to the *source*?** IP is stateless end-to-end; the source is the only party that can act (retry, fragment, choose another route). On-path devices just report; the sender decides.
- **Why include a copy of the offending packet?** The source must match the error to the specific flow (src/dst/ports) to react correctly — the embedded header+8 bytes is exactly enough for the transport to identify the connection (ports live in the first 8 bytes of TCP/UDP).
- **Why rate-limit and restrict?** ICMP is *forged-able* (no auth) and cheap to generate — unlimited ICMP is a classic DoS amplifier. Restricting error generation (no errors for broadcast/ICMP-error/multicast) and rate-limiting are defensive necessities, not protocol purity.
- **Why traceroute uses TTL instead of asking routers directly?** Routers won't answer "where are you going next?" (no such query). TTL expiry is *mandatory* (RFC 791) and ICMP time-exceeded is *mandatory* — traceroute piggybacks on two guarantees the protocol already provides. Clever, zero new protocol, works on every path.

## 5. Intuition
ICMP is the **post office's returned-mail slips**: when a letter can't be delivered, the post office doesn't silently swallow it — it sends you a slip (unreachable, wrong address, weight too heavy, expired in transit), and you decide what to do. ICMP is exactly that: routers and hosts tell the *sender* what happened to a specific packet. **Ping** is mailing a "return receipt requested" postcard: the other side just stamps it and sends it back, so you learn "they got it, and it took this long." **Traceroute** is sending letters addressed to the *same place* with successively smaller postage so each letter dies at a further sorting office — and each sorting office's "dead letter" slip (time-exceeded) tells you its location, letting you reconstruct the whole route. The slips themselves are never the cargo — they're the *status* messages that let the sender adapt.

## 6. Real-World Analogy
**A courier's "delivery exception" notifications**: ICMP is the courier network's automated status messages to the *sender*, not to the recipient: "undeliverable — no such address" (host unreachable), "no building at this address" (network unreachable), "recipient not taking packages at this office" (port unreachable), "package too heavy for this road — truck won't fit" (fragmentation needed + MTU), "package expired in the sorting loop" (TTL exceeded), "use a different drop-off — there's a closer depot" (redirect). **Ping** is the courier's *proof-of-delivery postcard* you send to check "are you reachable, and how fast?" **Traceroute** is sending postcards with 1, 2, 3, ... stops of postage: the card dies at each successive sorting hub, and each hub's "expired" notice reveals its location — so you map the entire truck route, hop by hop. No hub ever carries your actual goods on this exercise; it's pure status signaling.

## 7. Formal Definition
ICMP (RFC 792; updated by RFC 4884) is the Internet Control Message Protocol, carried in IP (protocol 1). Message format: Type (8), Code (8), Checksum (16), then type-specific fields (e.g., unused, pointer) and, for error messages, a copy of the invoking datagram's IP header + first 8 bytes. Types: 0 echo reply, 3 destination unreachable (codes: 0 net, 1 host, 2 protocol, 3 port, 4 frag-needed+MTU, 13 admin-prohibited), 4 source quench (obsolete), 5 redirect, 8 echo request, 11 time exceeded (0 TTL expired, 1 reassembly timeout), 12 parameter problem. Ping (RFC 2151 tools) sends echo request/reply with identifier+sequence. Traceroute (RFC 2151) sends probes with increasing TTL (UDP high ports, ICMP echo, or TCP SYN) and reconstructs the path from ICMP time-exceeded and final destination-unreachable/echo replies. ICMPv6 (RFC 4443) adds NDP (RFC 4861) messages (NS/NA, RS/RA) and packet-too-big for PMTUD.

## 8. Example
A ping and its ICMP exchange:
```
$ ping -c 3 8.8.8.8
PING 8.8.8.8 (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: icmp_seq=0 ttl=116 time=8.5 ms     <- echo reply, ttl shows hops
64 bytes from 8.8.8.8: icmp_seq=1 ttl=116 time=8.2 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=116 time=8.4 ms     <- 0% loss, ~8 ms RTT
```
Traceroute (Linux, UDP probes):
```
$ traceroute -n 8.8.8.8
 1  192.168.1.1    1.2 ms   (home router — TTL=1 died here, ICMP time-exceeded)
 2  10.0.0.1       3.1 ms
 3  172.16.0.1     5.0 ms   (ISP edge — each hop = one TTL increment)
 ...
11  8.8.8.8        8.6 ms   (final: ICMP port-unreachable — nothing on UDP high port)
```
The tcpdump view: probe with TTL=1 → ICMP `time exceeded in-transit` from 192.168.1.1; TTL=2 → time-exceeded from 10.0.0.1; ... TTL=11 → `destination port unreachable` from 8.8.8.8 (the *destination* replies, not a router). The path IS the sequence of time-exceeded sources.

## 9. Internal Working
1. **Ping path**: host sends ICMP echo request (type 8, id+seq) → destination's stack validates checksum → replies echo reply (type 0) → sender times the round trip. RTT = reply time − send time; loss = unanswered/total; the reply's TTL (and your start TTL) lets you estimate hops (128−116=12 hops for Windows-sourced 8.8.8.8... in the example the *reply's* ttl 116 came from a sender that started 128).
2. **Error generation**: a router that can't forward generates an ICMP error: builds the message, includes the original IP header + 8 payload bytes (enough for TCP/UDP ports), sends to the *source address*. Errors aren't generated for error-messages, fragments (except first), broadcast, or multicast (RFC 1812 rules).
3. **Time-exceeded on TTL=0**: when a router decrements TTL to 0, it discards the packet and (rate-limited) sends ICMP time-exceeded (11/0) to the source — *this is the traceroute trigger*.
4. **Fragment-needed**: a router that can't forward a DF packet sends ICMP 3/4 with its MTU in the message — the sender (RFC 1191 PMTUD) caches the path MTU and shrinks segments; TCP MSS is clamped accordingly.
5. **Redirect**: a router that forwards a packet *out the same interface it came in* sends ICMP redirect (5) — "the destination is reachable directly / via a better router"; the host updates its routing table. (Modern hosts often disable redirect acceptance — a spoof/DoS vector.)
6. **Traceroute mechanics**: for TTL=1..N: send probe (UDP to a high port by default, or ICMP echo, or TCP SYN — Linux `traceroute -I`, `mtr`). Each on-path router's time-exceeded reveals a hop. The destination replies with port-unreachable (UDP), echo reply (ICMP), or SYN-ACK/RST (TCP) — ending the trace. `mtr` repeats probes to show per-hop loss/latency over time.
7. **ICMP in the kernel**: net/ipv4/icmp.c handles generation (rate-limited, type-filtered) and reception; counters in `/proc/net/snmp` (Icmp:) and `netstat -s` track both.

## 10. Time Complexity
- **Ping**: O(1) per packet — trivial CPU; the *measurement* is timing, not compute.
- **Traceroute**: O(hops) probes (typically ≤30 × 3 packets) — a handful of packets per path; each hop costs 1 RTT worth of waiting (3 probes × RTT per hop in the naive case, `-N` parallelizes).
- **ICMP error generation**: O(1) per error, but *rate-limited* — Linux default `icmp_ratelimit` (1000/s) and the "no errors for broadcast/multicast" rules bound the cost (a reflected error storm is a real DoS otherwise).
- **PMTUD convergence**: one frag-needed per MTU decrease — O(path MTU changes) until the working size is found; cached per-destination with TTLs.
- **Security cost**: ICMP-based discovery tools (ping sweeps, traceroute) are cheap — which is why network admins monitor/limit ICMP visibility.

## 11. Advantages
- **Universal diagnostics**: ping and traceroute work on *every* IP network, zero configuration — the first tools any engineer reaches for.
- **Actionable errors**: unreachable/frag-needed/time-exceeded give the source exactly what it needs to react (retry, fragment smaller, drop).
- **Path discovery**: traceroute's TTL trick maps the Internet's topology with no router cooperation — an extraordinary diagnostic for zero new protocol.
- **Minimal + safe**: small messages, rate-limited, restricted generation — designed to not amplify.
- **Foundation for other machinery**: PMTUD, router redirects, ECN (via IP header CE marking, echo through ICMP-less flows), and IPv6 NDP all build on the ICMP family.

## 12. Disadvantages
- **No authentication**: ICMP is trivially forged — spoofed unreachable/time-exceeded can be used to disrupt (kill TCP flows, confuse PMTUD); spoofed echo floods are a DDoS vector (smurf: forged source → broadcast echo → amplified replies).
- **Easily filtered**: many networks drop ICMP (or parts) for security/stealth — breaking PMTUD, making *diagnostics* fail (ping blocked ≠ host down), and sometimes causing "blackhole" bugs.
- **Blackhole risk**: if "frag-needed" is dropped by a firewall, PMTUD silently fails → large packets vanish (the classic MTU blackhole) while small ones pass.
- **Traceroute limits**: asymmetric routing means the return path differs (each hop's time-exceeded travels back over a *different* route); NATs and strict firewalls hide hops (`*`); path changes mid-trace confuse interpretation.
- **Amplification/abuse**: broadcast ping (smurf), ICMP tunnels (covert channels), and error-based DoS are the dark side — hence rate limits and filtering.
- **Noisy by nature**: transient errors (queues full, one path down) produce visible ICMP noise that ops must learn to read correctly.

## 13. Interview Questions
1. **Q: What is ICMP and what is it used for?** A: The Internet Control Message Protocol (RFC 792) — IP's control/error channel: echo (ping), destination-unreachable, time-exceeded, redirect, fragment-needed. It reports network conditions to the *source*, not user data transport.
2. **Q (tricky): Why isn't ICMP a "transport protocol"?** A: It doesn't carry application data or provide ports/reliability — it's a *control* protocol carried inside IP (protocol 1), generated by routers and hosts to report errors/status to the sender. It's the network layer's mouth, not a data pipe.
3. **Q: What are the main ICMP message types?** A: 0 echo reply, 8 echo request (ping); 3 destination unreachable (0 net, 1 host, 2 protocol, 3 port, 4 frag-needed, 13 admin-prohibited); 5 redirect; 11 time exceeded (0 TTL expired, 1 reassembly timeout); 12 parameter problem.
4. **Q (FAANG): How does traceroute work?** A: Sends probes with TTL=1,2,3,...; the router that decrements a probe's TTL to 0 discards it and sends ICMP time-exceeded (revealing its address); the final hop (destination) replies with port-unreachable/echo-reply/SYN-ACK. Each TTL maps one hop — the path is reconstructed from the time-exceeded sources.
5. **Q: How does ping work?** A: Sends ICMP echo request (type 8, id+seq); the peer replies echo reply (type 0); the sender times the RTT and counts loss. TTL in the reply hints at hop distance.
6. **Q (tricky): How does ICMP enable path MTU discovery?** A: When a DF packet exceeds an MTU, the router drops it and sends ICMP type 3 code 4 ("fragmentation needed") *with its MTU*. The sender caches the smaller path MTU and shrinks segments — the basis of RFC 1191 PMTUD and TCP MSS clamping.
7. **Q: What is the difference between destination-unreachable codes?** A: Network (0) — can't reach the subnet; host (1) — can't reach the host; protocol (2) — no handler; port (3) — no process listening (this is what port scanners see); fragmentation needed (4); admin-prohibited (13) — filtered by a firewall.
8. **Q (production): ping fails but the host is up and TCP works. Why?** A: ICMP is filtered — many networks drop echo (or all ICMP) for security/stealth. Ping is a *probe*, not a contract: "no reply" means "ICMP blocked or host down" — check TCP (curl/`nc`) to disambiguate.
9. **Q: What is an ICMP redirect and why is it risky?** A: A router tells a host "the target is reachable directly / via a better router" (type 5). Hosts applying it can be *tricked* into sending traffic to an attacker — most modern stacks disable redirect acceptance by default (it's a known spoofing vector).
10. **Q (tricky): Why does traceroute show `* * *` at some hops?** A: Those routers don't send time-exceeded (filtered ICMP, rate-limited, or load-balanced) — the hop is *invisible*, not necessarily broken. Also: asymmetric return paths mean the reply travels a different route; NAT/private hops may hide.
11. **Q: What happens when a router receives a packet with TTL=1 destined elsewhere?** A: It decrements to 0 and discards it, sending ICMP time-exceeded (11/0) to the source — which is exactly the signal traceroute harvests. If it's the *destination*, the packet is delivered normally (TTL isn't checked on arrival).
12. **Q (FAANG): How would you measure loss and latency to a specific hop without traceroute?** A: `mtr` (continuous traceroute + ping per hop); or craft ICMP/TCP probes at a fixed TTL (source-address the specific hop's time-exceeded). For path *health*, mtr's per-hop loss over time is the standard tool.
13. **Q: What is the smurf attack?** A: An attacker sends ICMP echo requests with a *spoofed source* (the victim) to a broadcast address → every host replies to the victim → amplified reflection flood. Fixes: no broadcast ping, ingress filtering (BCP 38), ICMP rate limits.
14. **Q (production): Large transfers stall but small packets work. Diagnose?** A: Classic MTU blackhole: the "fragmentation needed" ICMP is being dropped by a firewall, so PMTUD fails silently — large packets (DF set) vanish. Fix: allow ICMP frag-needed, clamp MSS on the router/VPN, or lower MTU — the ICMP message *is* the diagnostic.
15. **Q: What is ICMPv6 and how does it differ?** A: ICMPv6 (RFC 4443) is *required* in IPv6 (no ICMPv4 option) and carries the neighbor-discovery (NS/NA/RS/RA), packet-too-big (PMTUD), and echo messages — a superset; IPv6 routing/autoconfiguration depends on it.
16. **Q (tricky): Why does the ICMP error include a copy of the original packet?** A: So the source's transport can identify which flow failed — the IP header + 8 bytes contains the TCP/UDP ports — and react (retry, resize, re-route). Without it, "something failed" would be unusable.
17. **Q: What are ICMP tunnels?** A: Covert channels that wrap arbitrary data in ICMP echo (ping) payloads to bypass firewalls that allow ICMP — a security concern; detection looks for abnormally large/frequent echo payloads.

## 14. Follow-Up Questions
1. **Q: What is the difference between `ping` and `mtr`?** A: Ping = one-end RTT/loss; mtr = continuous per-hop loss + latency (traceroute + ping combined over time) — the better operational tool for finding *where* a path degrades. Interview-wise: "use mtr to localize the lossy hop."
2. **Q: How does ICMP interact with TCP for error detection?** A: TCP learns a flow failed via (a) ICMP (unreachable → connection refused / reset-like) or (b) silence → RTO. ICMP *accelerates* failure detection (immediate, exact) — e.g., port-unreachable is how `connect()` to a closed port fails fast. But ICMP is advisory; TCP must still be robust to its loss.
3. **Q (tricky): Why is "ping allowed but unreachable filtered" harmful?** A: It breaks PMTUD (frag-needed is an unreachable-type message): ping passes (small packets), large transfers stall — the "ping works but transfers don't" mystery. Correct policy: allow frag-needed + time-exceeded, filter only the risky types (redirect, and limit echo).
4. **Q: What is a "traceroute anomaly" and how do you read it?** A: Common patterns: `* * *` (filtered/rate-limited hop), late hops with high RTT (a NAT/PE router not reporting — RTT jumps at the real edge), RTT *decreasing* (asymmetric return path), and repeated `!H`/`!N` (host/network unreachable from a specific hop — a routing blackhole). Reading traceroute is a whole ops skill.
5. **Q (FAANG): "Your path MTU discovery is broken and packets are disappearing. Walk me through the fix."** A: Verify ICMP frag-needed isn't filtered (check firewalls/security groups allow ICMP type 3/4); confirm DF is set (default); test with `ping -M do -s <size>` to find the true MTU; then clamp MSS on the gateway/VPN (`iptables -t mangle -A FORWARD -p tcp --tcp-flags SYN,RST SYN -j TCPMSS --clamp-mss-to-pmtu`) or lower the interface MTU. The diagnosis starts and ends with ICMP.

## 15. Coding Example
```python
# A raw ICMP echo request + reply (the essence of ping) — needs root
import socket, struct, time, os

def checksum(data):
    if len(data) % 2:
        data += b"\x00"
    s = sum(struct.unpack(">%dH" % (len(data) // 2), data))
    s = (s >> 16) + (s & 0xFFFF); s += s >> 16
    return (~s) & 0xFFFF

def ping(dst, timeout=2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.settimeout(timeout)
    ident, seq = os.getpid() & 0xFFFF, 1
    payload = b"ping" * 4
    header = struct.pack(">BBHHH", 8, 0, 0, ident, seq)   # type=8 echo request
    pkt = header + payload
    pkt = pkt[:2] + struct.pack(">H", checksum(pkt)) + pkt[4:]
    t0 = time.time()
    sock.sendto(pkt, (dst, 0))
    try:
        reply, addr = sock.recvfrom(1024)
        rtt = (time.time() - t0) * 1000
        print(f"{addr[0]}: icmp_seq={seq} time={rtt:.2f} ms")
    except socket.timeout:
        print("no reply")

ping("8.8.8.8")
```
```bash
# The operational toolkit
$ ping -c 5 8.8.8.8                            # RTT + loss + TTL
$ traceroute -n 8.8.8.8                        # UDP probes, numeric hops
$ traceroute -I -n 8.8.8.8                     # ICMP-echo probes
$ mtr -n 8.8.8.8                               # continuous per-hop loss/latency
$ sudo tcpdump -i eth0 icmp -nn -v | head      # watch echo + time-exceeded live
$ cat /proc/net/snmp | grep '^Icmp'            # kernel ICMP counters (errors!)
```

## 16. Industry Usage
- **NOC/SRE diagnostics**: ping + traceroute + mtr are the *first* tools in every outage playbook; ICMP counters (`/proc/net/snmp` Icmp:) feed alerting (ICMP unreachable storms, time-exceeded floods = routing problems).
- **Cloud networking (AWS/Azure/GCP)**: "ICMP reachability" checks (load balancer health pings), VPC reachability analyzers, and support's "run mtr" default; security groups/NACLs must allow ICMP for healthy checks (and *selectively* filter frag-needed-safe PMTUD).
- **CDNs/anycast/ISP**: traceroute is how ISPs and CDNs debug peering (where does traffic enter/exit? which peer is congested?); RTT maps from ping probes feed geo-routing.
- **Security**: ICMP-based recon (ping sweeps, traceroute topology mapping) is the first phase of attacks; defenses rate-limit/filter ICMP, watch smurf/reflectors, and use ICMP for DDoS *detection* (unexpected ICMP floods = attack signal).
- **Network equipment**: routers generate/consume ICMP constantly (TTL decrement → time-exceeded, frag-needed, redirects); ICMP inspection is a firewall/WAF feature; PMTUD is mandatory on TCP stacks.
- **Research/measurement**: ping/traceroute power Internet measurement platforms (RIPE Atlas, CAIDA) — the world's network health data is largely ICMP-derived.

## 17. References
- RFC 792 — ICMP: https://www.rfc-editor.org/rfc/rfc792
- RFC 4443 — ICMPv6: https://www.rfc-editor.org/rfc/rfc4443
- RFC 1191 — Path MTU Discovery (frag-needed): https://www.rfc-editor.org/rfc/rfc1191
- RFC 1812 — Router Requirements (ICMP generation rules): https://www.rfc-editor.org/rfc/rfc1812
- RFC 2151 — Internet tools (ping, traceroute): https://www.rfc-editor.org/rfc/rfc2151
- Kurose & Ross, *Computer Networking*, Ch. 4 §4.3.6 (ICMP).
- Linux man: `ping(8)`, `traceroute(8)`, `mtr(8)`.

## 18. Cheat Sheet
- ICMP: type/code/checksum + copy of original header+8B; carried in IP (proto 1).
- Types: 8 echo req, 0 echo reply (ping); 3 unreachable (0 net, 1 host, 2 proto, 3 port, 4 frag-needed+MTU, 13 admin-prohibited); 5 redirect; 11 time-exceeded (0 TTL, 1 reassembly); 12 param-problem.
- Errors only for ordinary datagrams (not errors/fragments/broadcast/multicast), rate-limited.
- Ping: echo req/reply → RTT, loss, TTL→hops. Blocked ≠ down.
- Traceroute: TTL=1,2,3... probes → time-exceeded per hop → port-unreachable/echo at destination.
- mtr: traceroute + continuous ping per hop.
- PMTUD: frag-needed (3/4) with MTU → shrink segments; dropping it = MTU blackhole (large packets die, small pass).
- Redirect (5): "use a better route" — spoofable; modern hosts reject by default.
- ICMPv6: required; NDP (NS/NA, RS/RA), packet-too-big.
- `* * *` = hidden/filtered hop; asymmetric return paths confuse traceroute.

## 19. Quiz
1. ICMP is carried: a) directly on L2 b) inside IP (proto 1) c) over UDP d) over TCP → **b**
2. Ping uses ICMP types: a) 0/8 b) 3/11 c) 5/12 d) 1/2 → **a**
3. Traceroute relies on which ICMP type: a) echo reply b) time-exceeded (11) c) redirect d) unreachable only → **b**
4. "Fragmentation needed" is type: a) 3 code 4 b) 11 code 0 c) 5 d) 8 → **a**
5. Port-unreachable signals: a) host down b) nothing listening c) network down d) TTL → **b**
6. Ping blocked means: a) host is down b) ICMP may be filtered c) always broken d) route gone → **b**
7. `* * *` in traceroute means: a) hop is broken b) hop filtered/rate-limited c) loop d) dest → **b**
8. MTU blackhole cause: a) too much MTU b) frag-needed ICMP dropped c) TTL d) redirect → **b**
9. ICMP redirect is risky because: a) slow b) spoofable → traffic hijack c) heavy d) obsolete → **b**
10. ICMPv6 is: a) optional b) required and carries NDP c) removed d) over TCP → **b**

## 20. Flashcards
- **Q: What is ICMP?** → **A:** IP's control/error channel (echo, unreachable, time-exceeded, redirect).
- **Q: Ping?** → **A:** echo req/reply → RTT, loss, TTL. Blocked ≠ down.
- **Q: Traceroute?** → **A:** TTL=1,2,3... → time-exceeded per hop → path map.
- **Q: Frag-needed (3/4)?** → **A:** MTU too small → PMTUD shrinks; dropping it = blackhole.
- **Q: Port-unreachable?** → **A:** nothing listening (how scanners/traceroute end).
- **Q: Why error includes packet copy?** → **A:** so the source identifies the flow (ports).
- **Q: Redirect?** → **A:** "use better route" — spoofable, rejected by default.
- **Q: ICMPv6?** → **A:** required; NDP + packet-too-big.

## 21. Revision
ICMP (RFC 792, proto 1) is IP's control/error channel: echo 8/0 (ping), unreachable 3 (net 0, host 1, proto 2, port 3, frag-needed 4+MTU, admin 13), redirect 5, time-exceeded 11 (TTL), param-problem 12. Errors carry the original header+8B for flow identification; generation is rate-limited and restricted. Traceroute: TTL probes → time-exceeded hops → final unreachable/echo. PMTUD runs on frag-needed; dropping it = MTU blackhole. Ping blocked ≠ host down. `* * *` = hidden hop; asymmetric paths confuse. ICMPv6 (required) carries NDP. Tools: ping, traceroute, mtr, tcpdump.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is ICMP / its purpose?" | 2 How It Works / 7 Formal Definition |
| "How does traceroute work?" | 13 Q&A / 9 Internal Working |
| "How does ping work?" | 13 Q&A / 8 Example |
| "Path MTU discovery / frag-needed?" | 13 Q&A / 12 Disadvantages |
| "Ping blocked but host up?" | 13 Q&A / 15 Coding |
| "What is a redirect / risk?" | 13 Q&A / 14 Follow-Up |
| "`* * *` / asymmetric paths?" | 13 Q&A / 16 Industry Usage |
| "Smurf / ICMP abuse?" | 13 Q&A / 13 Interview Q&A |
| "MTU blackhole diagnosis?" | 13 Q&A / 17 References |
