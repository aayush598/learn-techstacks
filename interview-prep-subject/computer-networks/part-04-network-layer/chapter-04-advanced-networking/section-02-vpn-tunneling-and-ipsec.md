# VPN, Tunneling, and IPsec

> **TL;DR**: A **VPN** makes a private, encrypted network over the public Internet by **tunneling** — wrapping private packets inside outer IP headers (GRE/IPsec/WireGuard/TLS). **IPsec** (RFC 6071) secures IP via AH/ESP, IKE key exchange, and transport/tunnel modes. The tradeoff: real privacy and access control, at the cost of overhead, latency, and edge complexity — the "extend your network to anywhere" technology.

## 1. Why Does This Exist?
The Internet is untrusted: anyone between you and a server can sniff, tamper, or hijack. Businesses need remote workers, branch offices, and clouds to behave like *one* private network — securely, anywhere. **VPNs** exist to give a **private, authenticated, encrypted, integrity-protected channel** over a *public, hostile* network. IPsec specifically exists because the original IP has *no security*: headers and payload travel in cleartext, any device can spoof a source address, and there's no per-packet authentication. The Internet Protocol Security architecture (RFC 4301/4309/6071) retrofits confidentiality, integrity, and authentication onto IP itself — at the IP layer (protecting *everything* above it, TCP/UDP/apps) — whereas TLS protects only one application connection at a time. IPsec was designed in the 1990s as the Internet's security layer, used for site-to-site tunnels, remote access, and now cloud-to-VPC connectivity. The core motivations: **confidentiality** (don't let the ISP see your traffic), **integrity** (detect tampering), **authenticity** (know the peer is who you think), **anti-replay** (reject replayed packets), and **privacy** (hide your internal topology).

## 2. How Does It Work?
- **Tunneling**: a VPN wraps a private packet (the *payload*, e.g., 192.168.1.10 → 10.0.0.5) inside an outer header (the *tunnel*), sending it across the Internet to a VPN gateway that decapsulates. The private packet *as a whole* is encrypted/authenticated. Tunnel mode = whole IP packet inside; transport mode = only the payload (used for host-to-host).
- **IPsec components**:
  - **ESP** (Encapsulating Security Payload, RFC 4303): provides confidentiality + integrity + anti-replay. Header + encrypted payload + padding + ICV (integrity check value).
  - **AH** (Authentication Header, RFC 4302): integrity + authentication *without* encryption (rarely used now).
  - **IKEv2** (RFC 7296): the key exchange/negotiation protocol (UDP/500 & 4500) — authenticates peers (PSK or certs), negotiates algorithms, derives session keys.
  - **SAs** (Security Associations): the agreement (peer, SPI, algorithms, keys) that both sides install to encrypt/decrypt — the "session object" of IPsec.
- **IKE phases**: Phase 1 (IKE SA — authenticate + secure the negotiation channel via DH key exchange), Phase 2 (IPsec SA — the actual tunnel keys). IKEv2 collapsed this into IKE_INIT + IKE_AUTH + CHILD_SA.
- **Modes**: **transport** (end-to-end, protects TCP/UDP payload, used host-to-host/ESP-for-apps) vs **tunnel** (gateway-to-gateway, encapsulates the whole IP packet — the classic site-to-site VPN).
- **Key exchange**: **IKEv2** (IPsec's own, UDP/500), or pure **WireGuard**'s Noise-protocol handshake; pre-shared keys, certificates, or EAP.
- **TLS VPNs (OpenVPN, SSL VPNs, Cloudflare Tunnel, Tailscale?)**: wrap private packets in TLS over TCP/443 (or UDP/QUIC) — firewall-friendly (443 is always open), NAT-friendly (one TCP/QUIC connection, not a protocol), and per-user authenticate. **WireGuard**: a minimalist modern protocol (UDP, Noise IK handshake, ChaCha20-Poly1305, no state machine, kernel-embedded) that replaced IPsec/OpenVPN for many (Tailscale, Mullvad, Cloudflare WARP).
- **Split vs full tunnel**: split = only some traffic (e.g., corp subnet) goes through the VPN, the rest direct (faster, but leaks info/risks); full = all traffic through (privacy, but latency + bottleneck).

## 3. When Is It Used?
- **Site-to-site (branch↔HQ / DC↔cloud)**: IPsec tunnels between gateways (or WireGuard/OpenVPN) — branch offices reach HQ resources as if local; hybrid cloud connects VPC ↔ on-prem.
- **Remote access (employee↔corp)**: VPN clients (IPsec IKEv2, OpenVPN, WireGuard, AnyConnect/SSL VPN) — the work-from-anywhere backbone.
- **Cloud & hybrid (AWS/GCP/Azure)**: VPN Gateways (site-to-site IPsec, static/BGP routing) for private, encrypted VPC↔on-prem links — the standard hybrid-cloud control path (alongside Direct Connect).
- **Consumer privacy (VPN services: Mullvad, Express, Proton)**: full-tunnel WireGuard/OpenVPN — hide traffic from ISP, unblock geo-restrictions (with the caveat: trust moves from ISP to VPN).
- **Zero-trust mesh (Tailscale, NetBird, ZeroTier)**: WireGuard-based overlay meshes — every device gets an encrypted tunnel to every other, with centralized identity (a 2020s-era VPN).
- **Protecting legacy/insecure protocols (NFS, RDP, telnet, SCADA)**: tunnel them over IPsec so they don't fly in cleartext.
- **IPv6 transition**: IP-in-IP / GRE tunneling (6in4, 6to4, GRE) carries v6 over v4 before native v6 arrives.

## 4. Why Wasn't Another Approach Chosen?
- **Why IP-layer, not app-layer (TLS)?** TLS protects a single TCP connection (and needs app cooperation). IPsec protects *everything* at the IP layer transparently — any app, any protocol (TCP/UDP/ICMP), no app changes. TLS is per-session; IPsec is per-packet network-wide. You need both (TLS in apps, IPsec at the network edge) — they're complementary, not competing.
- **Why not just encrypt at L2 (802.1X/MACsec)?** MACsec protects one link (the physical hop). VPNs must cross *many* untrusted hops; encryption must apply end-to-end across the tunnel, so it happens at L3 (IPsec) or higher, not at the link.
- **Why not a custom protocol for every VPN?** Because interop and standards matter: IPsec (RFC) is the vendor-neutral standard — Cisco, AWS, Fortinet, SonicWall all speak it. Proprietary (PPTP, L2TP-only) had security holes (PPTP/MSCHAPv2 broken) or no interop. The winner is *standards-based, peer-reviewed crypto*.
- **Why IPsec, not just OpenVPN/WireGuard everywhere?** IPsec's ubiquity + native (kernel) performance + site-to-site interop made it the enterprise/cloud default; WireGuard wins on simplicity/speed for remote/mesh; OpenVPN wins on firewall-friendliness (TCP/443) and legacy compat. The industry uses *all*: IPsec for gateway interop, WireGuard for modern overlay, TLS-VPN for remote access through strict firewalls.
- **Why DH/ECDH for keys, not static pre-shared keys?** PSKs are weak to offline brute-force and replay; Diffie-Hellman (forward secrecy) makes compromise of one key not expose past traffic (perfect forward secrecy, PFS) — IKEv2/WireGuard give PFS by design.

## 5. Intuition
A VPN is a **private armored tunnel between two checkpoints**. You stand inside your building (HQ) and load packages (packets) onto a truck marked "VAULT" (the tunnel). The truck drives across the public highway (the Internet) where anyone could look — but every package is sealed in an unbreakable box (encryption), signed by the sender (authentication), and numbered (anti-replay). Anyone who looks at the truck only sees "a sealed vault moving HQ→Branch" — the destination address written on the *truck* (the outer header) is public, but the *contents* (the private packets inside, with your real internal addresses) are invisible. At the other checkpoint, the guard (the VPN gateway) verifies the truck's credentials (IKE — "are you really from HQ?"), unpacks the sealed boxes, and hands the private packets to the branch office, which sees them as arriving from HQ's internal network — as if they were local. The truck can even travel with *some* packages direct (split tunnel) and *all* sealed (full tunnel). And in modern designs (WireGuard), the "truck" is a lean motorcycle that can reach every address directly in a mesh — same idea, less ceremony.

## 6. Real-World Analogy
**The diplomatic courier pouch**: A country's embassy (your branch) needs to send documents to the foreign ministry (HQ) across hostile territory (the Internet). Both use *diplomatic couriers* (VPN gateways) with a *sealed diplomatic pouch* (the tunnel): the outer envelope shows only "Ministry ↔ Embassy" (the public IPs), the contents are classified and sealed (encrypted), stamped with a courier's signature (authenticated), and serial-numbered against duplicates (anti-replay). Before the first pouch is sent, both sides exchange *cipher credentials* through a secure channel (IKE: "here's my certificate / shared secret, let's agree on the cipher") — if they can't prove identity, no pouch moves. The pouch is the *only* way documents cross, so the embassy routes *all* official mail through it (full tunnel) or just sensitive mail (split tunnel), depending on policy. Newer couriers (WireGuard) skip the heavy credential ceremony — a single modern cipher and a handshake — yet deliver the same sealed-pouch service faster and more reliably. And a poorly-sealed pouch (PPTP) is why couriers now use only reviewed seals (modern crypto).

## 7. Formal Definition
A **VPN** extends a private network over a public one via tunneling + cryptography. **IPsec** (RFC 4301–4309, 6071): AH (RFC 4302, integrity/no-encrypt), ESP (RFC 4303, confidentiality + integrity + anti-replay), IKEv2 (RFC 7296, key exchange over UDP 500/4500, ECDH for PFS, PSK/cert/EAP auth). **SAs**: (SPI, peer, algorithms, keys, lifetimes) installed per direction. **Modes**: transport (payload-only, host-to-host) vs tunnel (whole IP packet, gateway-to-gateway). **WireGuard** (no RFC, formalized as a protocol): UDP, Noise-IK handshake, ChaCha20-Poly1305 + Curve25519, per-peer public keys, kernel-native. **TLS VPNs**: private traffic inside TLS/443 or QUIC (OpenVPN, SSL VPNs). **GRE** (RFC 2784): stateless IP-in-IP encapsulation (no crypto — usually paired with IPsec). **Tunnels** vs **overlays**: a tunnel is one protected path; a mesh overlay (Tailscale) auto-creates tunnels between all endpoints.

## 8. Example
A site-to-site IPsec tunnel (the canonical walk):
```
Branch host 192.168.1.10 → HQ server 10.0.0.5

1. Branch host sends:        src 192.168.1.10 → dst 10.0.0.5   (private, clear)
2. Branch VPN gateway: encrypts the whole IP packet with the IPsec SA,
   wraps it in a NEW IP header:
       src <branch-gw-public> → dst <hq-gw-public>, ESP header,
       encrypted(original packet), ICV.
3. Across the Internet: only public IPs are visible; payload is encrypted ESP.
4. HQ gateway: verifies ICV + anti-replay, decrypts, extracts the ORIGINAL packet,
   forwards 192.168.1.10 → 10.0.0.5 inside HQ.
5. Reply reverses the same path.
```
The *encapsulation* is the essence: the private packet is a sealed passenger inside a public envelope (tunnel mode). Only gateways know the private addresses; the Internet only sees the two tunnel endpoints.

## 9. Internal Working
1. **IKEv2 negotiation**: IKE_INIT (peer sends SA proposals + its DH public key; keys derived via ECDH → forward secrecy), IKE_AUTH (mutual auth via PSK/certs, installs the IKE SA), CREATE_CHILD_SA (negotiates the ESP/AH SA + IPsec keys + SPIs). Total: ~4 messages, sub-second.
2. **SA installation**: both peers store (SPI, encryption algo (AES-GCM), integrity algo, DH keys, lifetimes, sequence numbers). The **SPI** in each ESP packet tells the receiver which SA/keys to use — stateless steering for the decrypt path.
3. **Per-packet (ESP tunnel)**: receive private packet → encapsulate (private IP in ESP payload) → encrypt + compute ICV → prepend new outer IP header (public endpoints) + ESP header (SPI, seq#) → send. Decrypt path: SPI lookup → verify anti-replay (seq window) → verify ICV → decrypt → strip outer header → forward private packet.
4. **NAT traversal**: ESP is protocol 50 (no ports) — NAT can't map it. NAT-T (RFC 3948) wraps ESP in **UDP/4500** (encapsulation), adds keepalives, and uses IKE's negotiated NAT detection — the reason IPsec works behind NAT today.
5. **Key/session maintenance**: SAs rekey on lifetime (bytes or time — PFS re-DH); DPD (dead-peer detection) probes liveness; failures tear down and re-negotiate.
6. **Routing/policy**: VPN policy defines which traffic enters the tunnel (source/dest/subnet); split-tunnel routes only specific subnets; the tunnel interface (e.g., `ipsec0`, `wg0`) becomes a normal route in the table.
7. **WireGuard internals**: each peer = one public key + allowed-IPs; handshake (Noise IK) → symmetric session keys (session ID); packets: type (handshake/data), receiver index (the SPI-equivalent), counter (anti-replay), then ChaCha20-Poly1305 ciphertext. No negotiation, no config — one cipher, one handshake. Kernel module → near-native speed.
8. **Failure/failover**: tunnel down (keepalive/DPD timeout) → route removed → traffic fails over to secondary tunnel or direct (for split-tunnel) → re-establish on link recovery.

## 10. Time Complexity
- **Handshake (IKEv2/WireGuard)**: O(1) messages (4 for IKEv2, 3 for WireGuard) — sub-second for reconnection; DH math dominates (~ms on modern CPUs, ECDH is fast; RSA cert verify is heavier). New sessions are cheap.
- **Per-packet**: O(packet size) — encryption (AES-GCM is hardware-accelerated on modern NICs/CPUs → near line rate), plus a small constant for ICV + encapsulation. Overhead: ~50–60 bytes of ESP/outer-header per packet (IPsec), ~32–60 bytes (WireGuard) — the "MTU tax" VPNs pay (tunnel MTU must shrink or fragment/DSCP handle it).
- **Throughput**: AES-NI/AVX + kernel WireGuard → 1–10+ Gbps easily; IPsec in hardware NICs → line rate. The bottleneck is rarely crypto on modern hardware — it's encapsulation + lookups.
- **State**: O(peers) — one SA set per peer; mesh VPNs O(N²) sessions (Tailscale centralizes + direct-connects to keep it O(N)-ish per device).
- **Operational**: rekeying is scheduled (lifetimes), not event-driven — no convergence cost; the cost is *bounded* and predictable vs routing protocols.

## 11. Advantages
- **Security**: confidentiality, integrity, authentication, anti-replay, and (with PFS) no retro-decryption — the whole package.
- **Transparency**: IPsec sits at L3 — apps/protocols need zero changes; it protects any traffic (TCP/UDP/ICMP).
- **Reachability/access**: private networks reachable from anywhere; hybrid cloud VPC↔on-prem works; remote workers get corp access.
- **Privacy**: hide internal topology + traffic from the ISP (the consumer-VPN pitch).
- **Standards + interop**: IPsec is vendor-neutral (Cisco↔AWS↔Fortinet); WireGuard is simple + kernel-fast; TLS-VPNs pass any firewall (443).
- **Overlays**: mesh VPNs (Tailscale) give zero-config private networking at scale.

## 12. Disadvantages
- **Overhead/latency**: encryption + encapsulation add per-packet overhead (~50–60 bytes) and CPU; tunneled MTU/fragmentation issues are classic VPN bugs (PMTU blackholes).
- **Complexity (IPsec)**: IKE phases, SAs, NAT-T, DPD, rekeying, cert management — a real operational burden; misconfig = silent tunnels that "work" but leak or drop.
- **Not a firewall**: a VPN authenticates the *tunnel*, not the user's endpoint necessarily; compromised laptops inside the tunnel are still a risk (hence ZTNA).
- **Trust shift (consumer VPNs)**: the VPN provider now sees all your traffic — privacy is transferred, not created.
- **Performance cost at scale**: crypto + encapsulation add CPU; sub-optimal paths (routing all through a gateway) add latency for split vs full tunnel.
- **Interop headaches**: NAT traversal, MTU mismatch, asymmetric MTUs, and vendor quirks still cause real-world VPN pain (the classic "works in office, fails on hotel wifi" saga).

## 13. Interview Questions
1. **Q: What is a VPN and how does it work?** A: A private network over the public Internet: tunnels (encapsulate private packets in outer headers) + encryption/auth (IPsec/WireGuard/TLS) so only endpoints can read the traffic. Clients connect to a gateway that decapsulates and forwards.
2. **Q (tricky): IPsec transport vs tunnel mode?** A: Transport protects only the *payload* (original IP header stays) — host-to-host (e.g., ESP between two servers). Tunnel encapsulates the *whole* IP packet in a new header — gateway-to-gateway (site-to-site), the classic VPN. Tunnel hides internal addressing; transport doesn't.
3. **Q: ESP vs AH?** A: ESP = confidentiality + integrity + anti-replay (encrypts payload). AH = integrity/auth *without* encryption (header visible). ESP is the standard; AH is legacy (its coverage of mutable IP header fields caused NAT problems).
4. **Q (FAANG): What is IKE and what are its phases?** A: IKEv2 = the key-exchange/negotiation protocol (UDP 500/4500). IKE_INIT (propose ciphers + DH → derive keys, forward secrecy), IKE_AUTH (mutual auth, install IKE SA), CREATE_CHILD_SA (derive the IPsec/ESP SA + keys). ~4 messages; the "handshake" of IPsec.
5. **Q: What is an SA?** A: Security Association: the per-direction session state — SPI, peer, algorithms, keys, lifetimes — that both peers install; the ESP SPI in each packet tells the receiver which SA to use.
6. **Q: Why doesn't IPsec work through NAT, and how is it fixed?** A: ESP is protocol 50 (no ports) — NAT can't build a port mapping. Fix: NAT-Traversal (RFC 3948) wraps ESP in UDP/4500 + keepalives + NAT detection during IKE. Without NAT-T, IPsec dies behind CGNAT/home routers.
7. **Q (tricky): What is perfect forward secrecy and why do VPNs use it?** A: PFS: session keys are derived per-handshake (ECDH) so compromising a long-term key can't decrypt *past* traffic. Old VPNs (static PSKs) failed this; IKEv2/WireGuard get it by default.
8. **Q: Why does MTU matter for VPNs?** A: Encapsulation adds bytes → the tunnel's effective MTU is smaller than the link's. If path MTU isn't adjusted, large packets exceed the tunnel → fragmentation or PMTU blackhole (packets silently dropped) — the classic "VPN works for small traffic, breaks for big files" bug. Fix: lower tunnel MTU + MSS clamping.
9. **Q (FAANG): IPsec vs WireGuard vs OpenVPN — compare.** A: IPsec = standard, enterprise/cloud interop, but complex (IKE/SA/NAT-T). WireGuard = modern, simple (one cipher/handshake), kernel-native speed, minimal attack surface — great for remote/mesh. OpenVPN/TLS = firewall-friendly (443), mature, per-user auth, but userspace + TLS overhead. Choose by interop need, deployment simplicity, and threat model.
10. **Q: What is split vs full tunnel?** A: Split: only specific subnets (corp) go through the VPN; the rest go direct (fast, low bandwidth, but can leak traffic/requests). Full: all traffic through (privacy, control, but more latency + a single point).
11. **Q (tricky): What is a GRE tunnel and when would you use it?** A: GRE (RFC 2784) = stateless IP-in-IP encapsulation — simple, no crypto, carries multicast, any protocol. Use it *under* IPsec (GRE-over-IPsec for multicast/multiple protocols) or for IPv6-over-IPv4 transition; never alone for security.
12. **Q: How do remote-access VPN clients differ from site-to-site?** A: Site-to-site: two gateways, tunnel mode, always-on, no client software (branch↔HQ/cloud). Remote access: one endpoint is a *client* (laptop/phone) with software, transport/on-demand tunnels, per-user auth (IKEv2 cert, TLS, EAP).
13. **Q (FAANG): "Your corp just moved to a mesh VPN (Tailscale/WireGuard). Why?"** A: Traditional hub-and-spoke VPNs route all remote traffic through HQ (latency + bottleneck) and need gateway scale. A mesh/overlay gives direct, encrypted tunnels between every device with centralized identity + ACLs — lower latency, no hub, simpler ops, and zero-trust-style per-device policy. (The 2020s evolution.)
14. **Q: What does a VPN protect against, and not protect against?** A: Protects: eavesdropping, tampering, source spoofing, replay, MITM on the wire. Doesn't protect: endpoint compromise (a rooted laptop inside the tunnel), insider threats, DNS leaks (misconfig), and — for consumer VPNs — the provider itself.
15. **Q (tricky): DNS leaks and VPNs?** A: If only some traffic is tunneled (split tunnel) or the VPN gateway's DNS config is wrong, DNS queries can still go to the ISP's resolver — leaking your lookups. Fix: force DNS through the tunnel, use the VPN's resolver, and disable leak-prone split tunneling.

## 14. Follow-Up Questions
1. **Q: What is a "VPN gateway" architecturally?** A: The edge device that terminates tunnels: decrypts/decapsulates, applies policy (which internal host), and forwards. In clouds, it's a managed service (AWS VPN Gateway); in enterprise, a firewall/NGFW box (Palo Alto/Fortinet); in mesh, it's software on every device.
2. **Q: How does a zero-trust network access (ZTNA) approach differ from a traditional VPN?** A: VPN = "trust the tunnel, everyone inside is trusted" (network-level). ZTNA = per-session, per-user, per-device identity + policy at the *service* level (never trust the network, verify every request). VPN gets you in the building; ZTNA lets you into only the specific rooms you're authorized for.
3. **Q (production): Your site-to-site IPsec tunnel flaps every 10 minutes. Diagnose?** A: Check (1) DPD/liveness mismatches (one side's idle timeout kills the session), (2) NAT-T detection (CGNAT at either end → UDP/4500 keepalives), (3) rekey lifetime misconfiguration (asymmetric lifetimes → both rekey at different times → one fails), (4) routing asymmetry / asymmetric MTU, (5) certificate expiry on one side. `show crypto ikev2 sa` + packet capture (UDP/500, 4500) is the drill.
4. **Q: Is IPsec UDP or TCP?** A: Neither at the data plane — ESP is protocol 50 (IP-layer), AH is protocol 51. IKE (control) runs UDP/500 & 4500. That's why it breaks on NAT and why NAT-T wraps it in UDP/4500.
5. **Q: What is 6in4 / 6to4 / GRE for IPv6 transition?** A: IP-in-IP tunneling protocols that carry IPv6 packets inside IPv4 headers (and vice versa) — the mechanical side of "tunneling" without VPN security, used until native IPv6 is ubiquitous.

## 15. Coding Example
```python
# A conceptual encrypted-tunnel data path (what IPsec/WireGuard do per packet)
import hashlib

def tunnel(inner_packet: bytes, outer_src: str, outer_dst: str) -> bytes:
    """Encapsulate + integrity-protect a private packet in an outer header."""
    icv = hashlib.sha256(b"session-key|" + inner_packet).digest()[:16]
    return (f"{outer_src} -> {outer_dst} | ESP | ".encode()
            + icv + b"|encrypted(" + inner_packet + b")")

def detunnel(wrapped: bytes, session_key: str) -> bytes:
    _, _, payload = wrapped.partition(b"encrypted(")
    inner = payload.rstrip(b")")
    if not hashlib.sha256(b"session-key|" + inner).digest()[:16] in wrapped:
        raise ValueError("integrity check failed (tampered)")
    return inner

inner = b"SRC 192.168.1.10 -> DST 10.0.0.5 payload"
wire = tunnel(inner, "203.0.113.1", "198.51.100.2")
print(wire[:60], "...")          # public envelope, encrypted payload
print(detunnel(wire, "x").decode())   # original private packet recovered
```
```bash
# The real VPN toolbox
$ tcpdump -ni eth0 'udp port 4500' -v          # ESP-over-NAT-T traffic (visible outer)
$ tcpdump -ni eth0 'proto 50' -v               # raw ESP
$ wg show                                    # WireGuard peers / handshakes / bytes
$ ipsec statusall | head                      # strongSwan/IKEv2 SA state
$ ping -M do -s 1400 10.0.0.5                 # MTU test through the tunnel
# Debug IPsec on Linux:
$ ip xfrm state; ip xfrm policy                # SAs + policies (the real tunnel state)
$ journalctl -u strongswan -f                  # IKE logs
```

## 16. Industry Usage
- **Hybrid cloud (the biggest driver)**: AWS VPN Gateway, Azure VPN Gateway, GCP Cloud VPN — site-to-site IPsec (static or BGP) connecting every enterprise VPC to on-prem; Direct Connect is the physical upgrade, VPN is the control-plane alternative.
- **Remote workforce**: AnyConnect/GlobalProtect (SSL-VPN), IKEv2 clients, WireGuard — every company's WFH backbone post-2020.
- **Enterprise site-to-site**: branch→HQ IPsec/GRE tunnels on NGFWs (Palo Alto, Fortinet, Cisco) — the standard WAN extension.
- **Consumer privacy (Mullvad, ExpressVPN, ProtonVPN, Nord)**: WireGuard/OpenVPN full-tunnel — billions in revenue on the "privacy from your ISP" pitch.
- **Zero-trust mesh (Tailscale, NetBird, ZeroTier, Cloudflare Tunnel)**: WireGuard-based overlays replacing hub-and-spoke VPNs — the modern "connect everything securely" layer.
- **IPv6 transition**: GRE/6in4 tunnels and IPsec are standard in carrier and enterprise transition plans.
- **Compliance (SOC2/HIPAA/GDPR)**: encrypted links are an audit requirement — VPNs are the mechanism for "data in transit protected."

## 17. References
- RFC 6071 — IPsec roadmap: https://www.rfc-editor.org/rfc/rfc6071
- RFC 4301 — IPsec security architecture: https://www.rfc-editor.org/rfc/rfc4301
- RFC 4303 — ESP: https://www.rfc-editor.org/rfc/rfc4303
- RFC 4302 — AH: https://www.rfc-editor.org/rfc/rfc4302
- RFC 7296 — IKEv2: https://www.rfc-editor.org/rfc/rfc7296
- RFC 3948 — IPsec NAT-T: https://www.rfc-editor.org/rfc/rfc3948
- RFC 2784 — GRE: https://www.rfc-editor.org/rfc/rfc2784
- WireGuard: https://www.wireguard.com/ and https://www.wireguard.com/protocol/
- Kurose & Ross, *Computer Networking*, Ch. 8 §8.4 (IPsec).

## 18. Cheat Sheet
- VPN = encrypted tunnel over the public Internet. Tunnel mode = whole IP packet inside; transport = payload only.
- IPsec: ESP (crypto+integrity+anti-replay, protocol 50), AH (auth only, 51), IKEv2 (UDP 500/4500, 4-msg handshake, ECDH PFS).
- SA = (SPI, peer, algos, keys, lifetime); SPI routes decrypt. NAT-T wraps ESP in UDP/4500.
- Modes: site-to-site (gateway↔gateway, tunnel) vs remote access (client, per-user auth).
- WireGuard: UDP, Noise handshake, ChaCha20-Poly1305 + Curve25519, kernel-native, one cipher.
- OpenVPN/TLS-VPN: inside TLS/443 — firewall-friendly.
- Split tunnel = only some subnets tunneled; full = all. DNS leak = resolver outside the tunnel.
- Overheads: ~50–60 B/packet; MTU shrink → PMTU blackholes → clamp MSS/lower MTU.
- GRE = stateless encapsulation (no crypto) — pair with IPsec or use for v6 transition.
- ZTNA/mesh (Tailscale) = per-identity, per-service access replacing hub-and-spoke.
- Debug: `wg show`, `ip xfrm state`, tcpdump 'proto 50' / 'udp 4500', `ping -M do`.

## 19. Quiz
1. ESP provides: a) integrity only b) confidentiality + integrity c) nothing d) DNS → **b**
2. IPsec tunnel mode: a) protects payload only b) wraps whole IP packet c) no crypto d) UDP only → **b**
3. IKEv2 runs over: a) TCP/443 b) UDP 500/4500 c) ICMP d) protocol 50 → **b**
4. NAT-T wraps ESP in: a) TCP/179 b) UDP/4500 c) GRE d) TLS → **b**
5. PFS comes from: a) static PSK b) ECDH per-handshake c) longer keys d) certs → **b**
6. Which protocol is crypto-free encapsulation? a) ESP b) GRE c) IKE d) AH → **b**
7. WireGuard uses: a) AES-CBC b) ChaCha20-Poly1305 c) DES d) MD5 → **b**
8. Split tunnel: a) all traffic b) only some subnets c) no encryption d) IPv6 → **b**
9. MTU blackhole is caused by: a) too-large packets past the tunnel MTU b) DNS c) BGP d) QoS → **a**
10. ESP is IP protocol number: a) 17 b) 50 c) 6 d) 1 → **b**

## 20. Flashcards
- **Q: What is a VPN?** → **A:** private network over the Internet via encryption + tunneling.
- **Q: Transport vs tunnel mode?** → **A:** payload-only (host-host) vs whole-packet encapsulation (gateways).
- **Q: ESP vs AH?** → **A:** ESP encrypts+authenticates; AH authenticates only (legacy).
- **Q: What is IKEv2?** → **A:** IPsec's 4-message key-exchange handshake (UDP 500/4500, PFS).
- **Q: What is an SA?** → **A:** per-direction session (SPI, keys, algos) installed by both peers.
- **Q: Why NAT-T?** → **A:** ESP (proto 50) has no ports → wrap in UDP/4500 to survive NAT.
- **Q: WireGuard?** → **A:** modern UDP VPN, Noise handshake, ChaCha20, kernel-fast, one cipher.
- **Q: GRE?** → **A:** stateless IP-in-IP, no crypto — pair with IPsec / v6 transition.
- **Q: MTU/PMTU blackhole?** → **A:** encapsulation shrinks MTU; oversized packets dropped → clamp MSS.
- **Q: ZTNA vs VPN?** → **A:** VPN trusts the network; ZTNA verifies every request per identity.

## 21. Revision
VPN = private network over the public Internet via tunneling + crypto. IPsec = the standard (ESP: confidentiality+integrity+anti-replay, protocol 50; AH: auth only; IKEv2: 4-msg handshake over UDP 500/4500, ECDH→PFS; SAs per direction; transport vs tunnel modes). ESP has no ports → NAT-T wraps in UDP/4500. WireGuard = modern UDP VPN (Noise IK, ChaCha20-Poly1305, Curve25519, kernel-native, one cipher). TLS-VPNs (OpenVPN) ride 443. GRE = stateless encapsulation (no crypto). Split vs full tunnel; DNS leaks. Overheads ~50–60 B/packet → MTU shrink/PMTU blackholes → clamp MSS. Used: hybrid cloud (AWS/Azure/GCP VPN gateways), remote work, enterprise site-to-site, consumer privacy, zero-trust meshes (Tailscale), v6 transition. Debug: `wg show`, `ip xfrm state`, tcpdump `proto 50`/`udp 4500`, `ping -M do`.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a VPN and how does it work?" | 2 How It Works / 5 Intuition |
| "IPsec transport vs tunnel mode?" | 13 Q&A / 7 Formal Definition |
| "What is IKE / IKEv2 phases?" | 13 Q&A / 9 Internal Working |
| "What is an SA / SPI?" | 13 Q&A / 9 Internal Working |
| "Why doesn't IPsec work through NAT / NAT-T?" | 13 Q&A / 9 Internal Working |
| "IPsec vs WireGuard vs OpenVPN?" | 13 Q&A / 4 Why Not Another Approach |
| "What is PFS?" | 13 Q&A / 4 Why Not Another Approach |
| "MTU/PMTU blackhole through VPNs?" | 13 Q&A / 8 Example |
| "Split vs full tunnel / DNS leaks?" | 13 Q&A / 10 Time Complexity |
| "VPN in hybrid cloud / mesh (Tailscale)?" | 13 Q&A / 16 Industry Usage |
