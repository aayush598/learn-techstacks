# Secure Channel Protocols and VPN

> **TL;DR**: IPsec and TLS are the two dominant secure-channel protocols — IPsec works at the network layer (protecting all IP traffic for VPNs, RFC 4301/7296), TLS at the transport layer (protecting individual connections); SSH secures remote shell access, and WireGuard is the modern minimal VPN protocol.

## 1. Why Does This Exist?
Applications assume the network is hostile — packets cross untrusted networks (the internet, untrusted LANs, coffee-shop Wi-Fi) where anyone can read, modify, or inject traffic. **Secure channel protocols** exist to provide *confidentiality, integrity, and authentication* for traffic in transit, at whichever layer makes sense. **IPsec** (network layer) protects *all* IP traffic transparently — the whole subnet, no application changes — which is why it powers site-to-site and remote-access VPNs. **TLS** (transport layer) protects individual connections and is the web's workhorse. **SSH** provides authenticated, encrypted remote shells. The design question is *layer*: protect everything (IPsec) vs protect specific flows (TLS), with trade-offs in transparency, granularity, and NAT/firewall friendliness.

## 2. How Does It Work?
**IPsec (RFC 4301, 4303, 7296)**: two protocols — **ESP** (encryption + integrity) and **AH** (integrity only, deprecated in practice). Two modes — **tunnel mode** (encapsulates the whole IP packet, used for VPNs) and **transport mode** (protects payload only). **IKEv2** (RFC 7296) does the key exchange: IKE_SA_INIT (DH key agreement) → IKE_AUTH (mutual authentication via PSK or certificates + SA setup) → then ESP SAs carry data via the IPsec **security association database (SAD)**. **SPD (security policy database)** decides which traffic is protected/how.
**TLS VPN**: OpenVPN/WireGuard-style — TLS for the control channel, derived keys for the tunnel (OpenVPN uses TLS + AEAD data channel).
**SSH (RFC 4253)**: TCP 22; key exchange (curve25519/DH) + host-key authentication (TOFU) + AEAD encryption; the user authenticates via password or public key.
**WireGuard**: single-curve crypto (Curve25519, ChaCha20-Poly1305), each peer has a public/private keypair, UDP-based, keys pre-shared out-of-band — no CA, no IKE; state is static except for rotating keys.

## 3. When Is It Used?
- **Site-to-site VPNs**: HQ ↔ branch/cloud (GCP/AWS VPN gateways), Azure VPN; IPsec tunnel mode, often over UDP/4500 (NAT-T).
- **Remote-access VPNs**: employees to corp — IPsec IKEv2, WireGuard, OpenVPN, corporate TLS portals.
- **TLS as a channel**: HTTPS everywhere (Section 03), but also mTLS for service-to-service, TLS-inside-TLS for inspection bypass (ShadowSocks/V2Ray-style).
- **SSH**: remote administration, `scp`/`rsync`, git-over-SSH, port forwarding, SSH tunnels (poor-man's VPN), jump hosts.
- **Cloud interconnects**: GCP Cloud VPN, AWS VPN → on-prem, using IKEv2 + BGP for routing.
- **Zero-trust**: Cloudflare Access, Tailscale (WireGuard-based mesh VPN).

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: application-level crypto only (HTTPS everywhere).* Doesn't cover UDP, ICMP, legacy apps, or whole subnets; IPsec was chosen where transparency and blanket protection matter — no app changes.
- *Alternative: IPsec for everything.* IPsec breaks with NAT (hence NAT-Traversal UDP/4500), has complex IKE, and is heavy for per-connection web traffic — TLS won for the web due to browser integration and 443 friendliness.
- *Alternative: proprietary VPNs (PPTP).* PPTP's MPPE crypto is broken and actively weak — superseded by IPsec/WireGuard/OpenVPN.
- *Alternative: IKEv1.* Complex, multi-negotiation, timing attacks; IKEv2 simplified to two messages, added mobility (MOBIKE), EAP auth.
- *Alternative: WireGuard vs IPsec.* WireGuard's "cryptokey routing" (keys ARE the identity) is drastically simpler and auditable; IPsec's advantage is standards/compliance (IPsec is mandated in many security frameworks). Both coexist.
- *Alternative: SSH as a VPN.* Great for tunnels/jump hosts but not for whole-subnet routing with dynamic keying — WireGuard/Tailscale fill that niche.

## 5. Intuition
Think of a **tunnel through a wall of cameras**. IPsec wraps your entire letter (IP packet) in a sealed armored envelope (ESP tunnel mode) and routes it through a locked pipe between two post offices (VPN gateways); anyone watching the wall sees only the envelope's source/destination (the gateways), not the contents or the true final address. TLS is a sealed envelope for a *single letter* per connection — the post office chain (browsers) was standardized on it. SSH is a private courier who authenticates his host identity every time and lets you pass notes (port-forward) through a one-way mirror. WireGuard is the modern equivalent: two couriers who know each other's keys by heart (static keys), no notary needed — but anyone can be dropped in (mesh).

## 6. Real-World Analogy
A **high-security shipping route between two warehouses** (site-to-site VPN). Both warehouses have guards who authenticate each other with shared secrets (IKE PSK or certificates). Every crate sent between them is sealed, stamped with an integrity tag (ESP), and the *outer* label only shows "warehouse A → warehouse B" (tunnel mode encapsulation) — hiding the true destination of the crate inside. The route keys are re-established on a schedule (IKE rekey/SA lifetime). For remote workers (remote-access VPN), each worker's laptop becomes a mini-warehouse that joins the protected route, with the corporate gateway validating its identity. SSH is more like a personal messenger: you meet the courier, verify his badge (host key), then exchange sealed notes that only you two can read — and you can ask him to carry extra items (port-forwarding) through the secure corridor.

## 7. Formal Definition
- **IPsec** (RFC 4301): Security Architecture; **ESP** (RFC 4303): encrypt-then-auth (confidentiality + integrity); **AH** (RFC 4302): integrity only, no confidentiality. **IKEv2** (RFC 7296): UDP 500/4500; IKE_SA_INIT (DH) → IKE_AUTH (auth via PSK/EAP/certs) → CHILD_SA (ESP). **SPD** picks policy; **SAD** stores negotiated SAs with SPI, keys, algorithms.
- **Modes**: transport (payload only, host-to-host) vs tunnel (entire packet encapsulated, VPN).
- **NAT-T**: UDP 4500 encapsulation with non-ESP marker to survive NAT.
- **WireGuard** (protocol proposal): uses X25519, ChaCha20-Poly1305, BLAKE2s, HKDF; each interface has a static private key; peers identified by public key = cryptokey routing; handshake every 2 minutes (rotating symmetric keys).
- **SSH** (RFC 4251-4253): transport (TCP 22), user auth (password, publickey, keyboard-interactive), connection (channels/multiplexing, port forwarding, SFTP).
- **TLS VPN** (OpenVPN): control channel = TLS (certs/auth), data channel = separate AEAD keyed by TLS-derived material.

## 8. Example
**IPsec site-to-site setup (conceptual negotiation flow):**
```
1. SPD says "traffic from 10.1.0.0/16 → 10.2.0.0/16 must go via VPN, ESP"
2. IKEv2 (UDP 500):
   IKE_SA_INIT:   both send DH pubkeys + nonces (agreement)
   IKE_AUTH:      mutual auth (PSK/cert), establish CHILD_SA (ESP parameters)
3. Data: IP packet (src 10.1.0.5, dst 10.2.0.7) is
   wrapped as ESP payload, encrypted+auth'd, then
   new outer packet (src gateway1, dst gateway2, proto ESP) sent
4. Receiver looks up SPI in SAD, decrypts, strips outer, routes inner packet.
```
**WireGuard minimal config (two peers):**
```ini
# wg0.conf (peer A)
[Interface]
PrivateKey = A_PRIVATE_BASE64
Address = 10.9.0.1/24

[Peer]
PublicKey = B_PUBLIC_BASE64
AllowedIPs = 10.9.0.2/32, 0.0.0.0/0   # cryptokey routing
Endpoint = b.example.com:51820
```
Peer B mirrors with A's public key and `AllowedIPs = 10.9.0.1/32`. That's the whole protocol config — no IKE, no CAs.

## 9. Internal Working
1. **SPD lookup**: for each outbound packet, find the policy (protect / bypass / discard) and the SA to use; the packet's tuple selects from SAD via SPI.
2. **IKEv2 phases**: IKE_SA_INIT uses DH (e.g., 3072-bit MODP or P-256) + nonces → IKE keys; IKE_AUTH authenticates identities (PSK or certs, optionally EAP) and creates the first CHILD_SA; further CHILD_SAs carry traffic. SAs have limited lifetimes (bytes/time) forcing rekey.
3. **ESP processing**: payload = original IP packet (tunnel) or transport data; ESP header (SPI, seq) → encrypt → add ICV (e.g., HMAC-SHA256 or AEAD GCM); the result is wrapped in a UDP 4500 datagram under NAT-T.
4. **Anti-replay**: per-SA sequence-number window (RFC 4303) rejects replayed packets.
5. **WireGuard**: timer-driven handshake every 2 min; each message keyed from the previous (session keys rotate); peers validate the source MAC address only if allowed.
6. **SSH**: after transport setup, the client authenticates via `publickey` (sign a challenge with the private key) or password inside the encrypted channel; then multiplexes channels (terminal, port-forward, exec) over one encrypted stream.
7. **TLS VPN (OpenVPN)**: TLS handshake authenticates; then the data channel uses the derived key material for AEAD on IP packets encapsulated in UDP/TCP.

## 10. Time Complexity / Performance
- **Setup cost**: IKEv2 ≈ 2-4 messages + DH (sub-ms); WireGuard handshake ≈ 1 round trip every 2 min; SSH ≈ 1-2 RTTs.
- **Per-packet cost**: ESP adds one encrypt+MAC; with AES-GCM that's near line-rate on CPUs with AES-NI (10s of Gbps). UDP encapsulation adds ~50-80 bytes overhead.
- **VPN throughput**: IPsec with AES-GCM typically achieves wire-speed on modern NICs; WireGuard is lightweight (fewer state machines, less rekey chatter).
- **Latency**: one extra hop/gateway and ~50-80B/packet overhead; MTU/MSS adjustments (reduce to ~1300-1400) matter to avoid fragmentation.
- **Scaling**: SPD/SAD are per-SA; millions of short flows can be expensive with per-flow SAs — IKEv2 CHILD_SA reuse and traffic selectors (subnet-level) amortize this.

## 11. Advantages
- **IPsec**: transparent (protects all IP incl. UDP/ICMP, no app changes), standards-based (interop: Cisco/OpenSwan/AWS/GCP), tunnel + transport modes, strong auth options (certs, EAP), AH for integrity-only needs.
- **WireGuard**: minimal ~4k lines (auditable), fast, modern crypto, simple config, great for mesh (Tailscale).
- **SSH**: ubiquitous, secure default host-key trust, multiplexed channels, port forwarding = general-purpose secure tunneling.
- **TLS VPN**: traverses NAT/firewalls via 443 (indistinguishable from HTTPS), browser-integrated, certificate-based auth.
- **General**: ESP + AEAD gives confidentiality+integrity in one primitive; anti-replay windows; rekeying limits key exposure; SAs provide per-peer isolation.

## 12. Disadvantages
- **IPsec**: complex IKE; NAT traversal (UDP 4500) is a special case; MTU/fragmentation issues; debugging SPD/SAD is painful; AH fails behind NAT (IP checksum covered).
- **WireGuard**: no built-in key exchange (keys must be distributed out-of-band); no dynamic routing/built-in auth delegation; limited to its fixed crypto (no algorithm agility — a compliance concern for some).
- **SSH**: TOFU host-key trust is weak on first connect; password auth is brute-forceable (disable it); managing keys at scale is hard.
- **TLS VPN**: doesn't protect non-TCP by default; OpenVPN TCP mode can look like HTTPS but is detectible; performance overhead in userspace.
- **General**: endpoint compromise kills the tunnel's security; VPN ≠ endpoint security; misconfig (overly broad `AllowedIPs`/SPD) leaks traffic or routes everything (kill-switch needed).

## 13. Interview Questions
1. **Q: What are the two IPsec protocols and the two modes?** A: ESP (encrypt+auth) and AH (auth only). Modes: transport (host-to-host, payload only) and tunnel (entire packet encapsulated, used for VPNs). ESP tunnel mode is the VPN workhorse; AH is rare (breaks behind NAT).

2. **Q: Walk through IKEv2.** A: Two phases: IKE_SA_INIT — DH key agreement + nonces (UDP 500); IKE_AUTH — mutual authentication (PSK, certs, or EAP) and establishment of the first CHILD_SA carrying ESP. Subsequent CHILD_SAs protect traffic; SAs rekey periodically.

3. **Q: How does IPsec survive NAT?** A: NAT breaks IPsec because NAT rewrites IP addresses and AH/ESP integrity covers them. Solution: NAT-T — ESP packets are wrapped in UDP datagrams on port 4500, with a non-ESP marker; UDP NAT mapping preserves the tunnel.

4. **Q: What is the difference between transport and tunnel mode?** A: Transport protects only the payload (original headers intact, used host-to-host within a trusted boundary). Tunnel wraps the *entire* original IP packet inside a new packet addressed to the gateways — hiding the true destination and enabling subnet-to-subnet VPNs.

5. **Q: What is WireGuard and how is it different from IPsec?** A: A minimal modern VPN: Curve25519, ChaCha20-Poly1305, static per-peer keypairs = identity (cryptokey routing), UDP-based, ~4k lines, fast, easy to audit. IPsec is more complex (IKE, SA negotiation) but standards-based and required by many compliance frameworks. No built-in key distribution in WireGuard.

6. **Q: What is the difference between IPsec and TLS?** A: Layer and scope. IPsec (L3) protects all IP traffic transparently with no app changes — ideal for VPNs and site-to-site. TLS (L4) protects individual connections with browser/cert integration — ideal for HTTPS and app-specific security. IPsec is heavy/complex; TLS is lighter and 443-friendly.

7. **Q: TRICKY — What is an "SA" and what does it contain?** A: A Security Association is the one-way negotiated agreement: SPI, source/dest addresses, IPsec protocol (ESP/AH), mode, keys, algorithm, and lifetime. IPsec is essentially "match traffic to SAs in the SAD based on the SPD." The SPI in each ESP header tells the receiver which SA (and thus which key) to use.

8. **Q: What is a VPN "kill switch"?** A: If the tunnel drops, the client must block all traffic rather than leak it onto the public network in plaintext — a routing/SPD fail-closed behavior. Especially critical with split-tunnel or full-tunnel remote-access VPNs (protects a laptop's traffic from leaking over Wi-Fi).

9. **Q: What is SSH port forwarding / how do SSH tunnels work?** A: SSH multiplexes multiple channels over one encrypted TCP connection. Local forwarding: `ssh -L localhost:8080:internal:80 host` — connections to localhost:8080 are tunneled to internal:80. Remote (`-R`) and dynamic (`-D`, SOCKS proxy) variants exist. This is a general-purpose secure tunnel — a "poor man's VPN."

10. **Q: PRODUCTION — A site-to-site IPsec tunnel drops repeatedly at the same time each day. What to check?** A: (1) SA lifetime/rekey misconfig — if rekey overlaps NAT-T, tunnels flap; (2) MTU/fragmentation — check DF-bit drops and set tunnel MTU/MSS; (3) dead-peer detection (DPD) timers vs idle timeout; (4) IKE negotiation failures — check phase-1/2 proposals, pre-shared key mismatch, and BGP hold timers after the tunnel. Capture with `tcpdump -i any port 500 or 4500` and check SPD/SAD state (`ip xfrm state`, `strongswan statusall`).

11. **Q: What is the difference between full-tunnel and split-tunnel VPN?** A: Full-tunnel routes *all* client traffic through the VPN (maximum control, higher latency/bandwidth cost); split-tunnel routes only corporate-destination traffic through the tunnel (faster for general browsing, but risks leaking non-routed traffic and allows dual-homed access — a security consideration for zero-trust).

12. **Q: TRICKY — Can you run TLS inside TLS? What's the security implication?** A: Yes — "TLS-in-TLS" (used by some circumvention/proxies): an outer TLS connection to a proxy, inner TLS to the real site. Security is layered (double encryption), but the extra framing and timing can be detected/fingerprinted, and nested encryption doesn't add security beyond the outer layer if both terminate at the same trust boundary.

13. **Q: What does the SSH host key protect against and what is TOFU?** A: The host key authenticates the *server* during the handshake (it signs the key exchange). TOFU = trust-on-first-use: the client stores the key and warns if it changes later. Risk: an attacker on the very first connection can MITM (no out-of-band trust). Real SSH deployments verify fingerprints out-of-band or use SSHFP DNS records.

14. **Q: What is MOBIKE?** A: IKEv2 mobility/multihoming extension — lets an IPsec session survive IP-address changes (laptop roaming, Wi-Fi↔cellular) without re-establishing the tunnel, by rekeying the IKE_SA with the new address. Built into IKEv2 rather than IKEv1.

15. **Q: SCENARIO — A remote worker can reach the VPN but can't browse the internet through it. Why?** A: (1) SPD/policy routes corp traffic but the split-tunnel default route is missing; (2) NAT isn't applied on the gateway for VPN-sourced traffic; (3) DNS is only passed for internal domains; (4) firewall at HQ blocks return traffic; (5) MTU/MSS too large for the tunnel. Debug by pinging the gateway, checking routing (`ip route`), and testing DNS resolution.

16. **Q: What is a "tunnel" in VPN terminology and what does it hide?** A: A tunnel encapsulates one packet inside another (e.g., IP inside ESP inside outer IP). It hides the *inner* packet's true source/destination from intermediaries — on-path observers see only the gateways. "Tunneling" ≠ "encryption" (GRE tunnels are plaintext); VPNs combine encapsulation + encryption + integrity.

17. **Q: PRODUCTION — Design remote-access VPN for 10,000 employees with zero-trust.** A: (1) Use a modern protocol (WireGuard-based like Tailscale, or IKEv2) with short-lived device identity; (2) integrate SSO/EAP-TLS and MFA at authentication; (3) default-deny policies — only allow specific apps/IPs (not full-tunnel trust); (4) device posture checks (managed, patched); (5) split-tunnel with DNS filtering + kill switch; (6) gateway HA, per-user auditing, and continuous revalidation. The trend is "VPN → zero-trust network access (ZTNA)": identity-based, per-app, deny-by-default.

## 14. Follow-Up Questions
1. **Q: What is the difference between AH and ESP?** A: AH (RFC 4302) authenticates the IP header + payload (integrity + anti-replay, no encryption) and fails behind NAT (checksum covers mutable fields). ESP (RFC 4303) encrypts and authenticates the payload (and in tunnel mode the inner header); with AEAD (GCM) it does both in one pass. ESP is the practical choice.

2. **Q: What is "SPI" and why does every ESP packet have one?** A: The Security Parameter Index — an ID in the ESP header that identifies which SA (and key/algorithm) the receiver should use to process the packet. Stateless lookup by (SPI, dest addr) → SAD entry.

3. **Q: What are "DPD" and "NAT keepalives"?** A: DPD (Dead Peer Detection): periodic IKE messages to detect a dead peer so the SA can be re-established. NAT keepalives: small periodic UDP packets on 4500 to keep NAT mappings from expiring during idle periods — both are common VPN "keep it alive" mechanisms.

4. **Q: What is the WireGuard "cryptokey routing"?** A: The routing decision is made *by public key*: an interface only accepts packets from peers it has keys for, and `AllowedIPs` on each peer defines what source ranges that peer may claim — identity, routing, and policy in one model. This eliminates separate SPD/SAD/Auth layers.

## 15. Coding Example
```bash
# Inspect / debug an existing IPsec or WireGuard setup
ip xfrm state                    # current SAs (SPI, algorithms, keys in use)
ip xfrm policy                   # SPD rules (what traffic is protected how)
ip addr show wg0                 # WireGuard interface addressing
wg show                          # handshake time, transfer, peers (last-handshake = tunnel health)
sudo tcpdump -i any 'udp port 500 or udp port 4500'    # IKE/NAT-T traffic
sudo tcpdump -i wg0 -c 5         # decrypted side of a WireGuard tunnel
```
```bash
# Spin up a quick WireGuard pair in a lab (as root)
modprobe wireguard
# A:
ip link add wg0 type wireguard; wg set wg0 listen-port 51820 private-key <A.key>
ip addr add 10.9.0.1/24 dev wg0
wg set wg0 peer <B_PUB> allowed-ips 10.9.0.2/32 endpoint B_IP:51820
ip link set wg0 up
# B: mirror, then
ping 10.9.0.1            # traffic flows through the encrypted tunnel
```
```bash
# SSH tunneling & secure file transfer (production everyday)
ssh -J bastion user@internal        # jump host
ssh -L 9000:db.internal:5432 user@bastion   # tunnel DB port
ssh -D 1080 user@relay              # SOCKS proxy through relay
scp -o Ciphers=chacha20-poly1305@openssh.com file user@host:/tmp/  # AEAD cipher
```
```python
# Verify a tunnel's crypto end-to-end conceptually (integrity tagging)
import hmac, hashlib

def esp_encrypt(key, plaintext_ip_packet, spi, seq):
    icv = hmac.new(key, plaintext_ip_packet, hashlib.sha256).digest()  # integrity
    return f"SPI={spi} SEQ={seq} PAYLOAD=<{len(plaintext_ip_packet)}B ciphertext> ICV={icv.hex()[:12]}"
print(esp_encrypt(b"k"*32, b"inner-ip-packet", 0x1A2B3C, 7))
```

## 16. Industry Usage
- **Cloud**: AWS VPN (IPsec IKEv2 + BGP), GCP Cloud VPN/Interconnect, Azure VPN Gateway — standard site-to-site.
- **Remote access**: Tailscale (WireGuard mesh), Cloudflare WARP/Zero Trust, corporate OpenVPN/IPsec portals, Cisco AnyConnect.
- **SSH**: the universal admin/Git/SFTP channel — `ssh -J`, bastion hosts, `scp`, GitHub SSH keys.
- **Censorship/circumvention**: TLS-in-TLS proxying (ShadowSocks, V2Ray) — layering TLS for plausibility and obfuscation.
- **ZTNA trend**: moving from "network-level VPN" to identity-based access (BeyondCorp, Zero Trust) — though WireGuard-based overlays still provide the encrypted fabric.

## 17. References
- RFC 4301 (IPsec Security Architecture) — https://datatracker.ietf.org/doc/html/rfc4301
- RFC 4303 (ESP) — https://datatracker.ietf.org/doc/html/rfc4303 ; RFC 4302 (AH)
- RFC 7296 (IKEv2) — https://datatracker.ietf.org/doc/html/rfc7296
- RFC 4555 (IKEv2 Mobility/MOBIKE)
- WireGuard whitepaper & protocol — https://www.wireguard.com/protocol/
- RFC 4251/4253 (SSH architecture / transport) — https://datatracker.ietf.org/doc/html/rfc4253
- Kurose & Ross, *Computer Networking*, 8th ed., §8.4 (secure channels), §8.9 (VPNs).
- OpenVPN reference — https://openvpn.net/community-resources/reference-manual-for-openvpn-2-6/

## 18. Cheat Sheet
- IPsec = L3, transparent, protects all IP; ESP = encrypt+auth; AH = auth only.
- Modes: transport (payload) vs tunnel (whole packet) — VPN = tunnel.
- IKEv2 (UDP 500/4500): IKE_SA_INIT (DH) → IKE_AUTH (auth + CHILD_SA). SA = SPI+keys+algo+lifetime.
- NAT-T: ESP wrapped in UDP 4500 + keepalives.
- WireGuard: Curve25519 + ChaCha20-Poly1305 + BLAKE2s, static keys = identity, cryptokey routing, handshake every 2 min.
- SSH: TOFU host keys, publickey auth, multiplexed channels, `-L/-R/-D` tunnels.
- TLS VPN: control = TLS, data = AEAD; runs on 443 (looks like HTTPS).
- Full-tunnel (route all) vs split-tunnel (route corp only) — kill switch for fail-closed.
- Debug: `ip xfrm state/policy`, `wg show`, `tcpdump port 500 or 4500`, `ip route`.

## 19. Quiz
1. Which IPsec protocol does both encryption and integrity? a) AH b) ESP c) IKE d) SPD → **b**
2. IPsec tunnel mode: a) protects payload only b) encapsulates the whole IP packet c) no encryption d) port 443 → **b**
3. IKEv2 authenticates during: a) IKE_SA_INIT b) IKE_AUTH c) ESP d) AH → **b**
4. NAT-T uses which port? a) 500 b) 4500 c) 443 d) 22 → **b**
5. WireGuard uses which identity model? a) certificates b) public keys c) PSK only d) CA → **b**
6. SSH host key trust model: a) CA b) TOFU c) OCSP d) pinned → **b**
7. The SPI tells the receiver: a) the route b) which SA/key to use c) the MTU d) the cipher suite → **b**
8. Split-tunnel means: a) route all traffic b) route only corp destinations c) no encryption d) UDP → **b**

**Answers**: 1-b, 2-b, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: IPsec vs TLS layer/scope** → **A:** IPsec = L3 all-IP transparent (VPN); TLS = L4 per-connection (web).
- **Q: ESP vs AH** → **A:** ESP = encrypt+auth; AH = auth only, breaks behind NAT.
- **Q: IKEv2 two phases** → **A:** IKE_SA_INIT (DH) → IKE_AUTH (auth + CHILD_SA).
- **Q: How does IPsec survive NAT?** → **A:** NAT-T: UDP 4500 encapsulation + keepalives.
- **Q: What is a SA?** → **A:** One-way negotiated bundle: SPI, keys, algorithm, lifetime.
- **Q: WireGuard crypto stack** → **A:** Curve25519, ChaCha20-Poly1305, BLAKE2s, static-key identity, handshake every 2 min.
- **Q: SSH tunnels** → **A:** Multiplexed channels; `-L` local, `-R` remote, `-D` SOCKS.

## 21. Revision
Secure channels exist because networks are hostile. **IPsec** (RFC 4301/4303/7296) protects all IP transparently: ESP tunnel mode encapsulates the whole packet, IKEv2 negotiates (DH → auth → CHILD_SA), SAs in the SAD carry keys/SPI, SPD selects policy, and NAT-T wraps ESP in UDP/4500. **WireGuard** is the minimal modern VPN: static Curve25519 keys = identity, cryptokey routing replaces SPD/SAD, ChaCha20-Poly1305. **SSH** (RFC 4253): TOFU host keys + publickey auth + multiplexed channels/port-forwarding. **TLS VPNs** put the control channel in TLS on 443 for firewall-friendliness. Key trade-offs: transparency (IPsec) vs granularity (TLS); complexity (IKE) vs minimalism (WireGuard); whole-subnet vs per-connection. Anchors: *IPsec = transparent L3 blanket protection, tunnel wraps whole packet, NAT-T=UDP/4500; WireGuard = keys-as-identity, ~4k lines; SSH = TOFU + channels; VPN choice = compliance/interop (IPsec) vs simplicity/perf (WireGuard).*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "IPsec protocols and modes" | 13-Q1 |
| "Walk IKEv2" | 13-Q2 / 9 |
| "How does IPsec survive NAT?" | 13-Q3 |
| "Transport vs tunnel mode" | 13-Q4 |
| "WireGuard vs IPsec" | 13-Q5 |
| "IPsec vs TLS" | 13-Q6 |
| "What is an SA/SPI?" | 13-Q7 |
| "SSH port forwarding/tunnels" | 13-Q9 |
| "Full vs split tunnel" | 13-Q11 |
| "SSH TOFU/host keys" | 13-Q13 |
| "Tunnel flapping postmortem" | 13-Q10 |
| "Design zero-trust remote access" | 13-Q17 |
| "What is a VPN tunnel (hides what)?" | 13-Q16 |
