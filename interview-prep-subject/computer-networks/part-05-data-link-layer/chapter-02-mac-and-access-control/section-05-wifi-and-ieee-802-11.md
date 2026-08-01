# WiFi and IEEE 802.11

> **TL;DR**: IEEE 802.11 (WiFi) is the wireless LAN standard that runs CSMA/CA instead of CSMA/CD, adds frame-level ACK + retransmission because air is lossy, and has evolved from 802.11a/b/g (1–54 Mb/s) through n/ac (multi-MIMO, 600 Mbps–3.5+ Gbps) to ax (WiFi 6, OFDMA) and be (WiFi 7, 46 Gbps) — while never trusting the shared, hidden-terminal-prone radio medium.

## 1. Why Does This Exist?
Wired Ethernet requires a cable; wireless requires a *radio* channel that is shared, half-duplex, lossy, and full of surprises (fading, interference, hidden terminals). WiFi exists to deliver Ethernet-like connectivity without wires: clients and APs share an unlicensed radio band (2.4 GHz, 5 GHz, 6 GHz), and because anyone can transmit at any time, the protocol must *arbitrate the air*. The core problems WiFi solves: (1) **carrier sense** — listen before talking; (2) **collision avoidance** — since a radio can't listen while transmitting (can't do CSMA/CD), it avoids collisions with random backoff + ACKs; (3) **reliability** — the air is lossy (BER 10⁻⁴–10⁻⁶), so unlike Ethernet it ACKs and retransmits every frame at L2; (4) **security** — the air is open, so it needed WEP→WPA→WPA2→WPA3 and 802.1X enterprise auth; (5) **throughput** — spectral efficiency via OFDM, MIMO, channel bonding, and now OFDMA.

## 2. How Does It Work?
An 802.11 frame has a **MAC header** (frame control, duration, 3–4 addresses for AP/STA/BSSID/DA/SA, sequence control), a payload, and a 32-bit FCS (CRC-32). Access uses **DCF (Distributed Coordination Function)**: a station with data senses the channel; if idle for DIFS, it waits a random **backoff** (contention window, 15–1023 slots) and transmits; the AP replies with an **ACK** after SIFS; failure → retransmit with doubled CW. **RTS/CTS** reserves the medium for the **hidden-terminal** problem. The **PCF** (optional polling) and 802.11ax **OFDMA** centralize scheduling. Frames carry data, management (beacons, auth, assoc), and control (RTS/CTS/ACK) traffic. Power-save lets clients sleep and APs buffer frames.

## 3. When Is It Used?
- **Everything wireless for consumers**: home/office/enterprise LANs, hotspots, IoT (802.11ah, 802.15.4-style for low power), Wi-Fi Direct, hotspot offload.
- **Enterprise**: WPA2/WPA3-Enterprise (802.1X/EAP-TLS), band steering, 802.11k/v/r roaming, dual-band/6 GHz (WiFi 6E).
- **IoT/embedded**: 802.11ax low-power features, Wi-Fi HaLow (802.11ah, sub-GHz).
- **Hotspots/tethering/mesh**: 802.11s mesh networking, Wi-Fi EasyMesh.
- **Cellular offload**: carriers offload to carrier-grade WiFi; unlicensed access (LTE-U vs WiFi coexistence debates).
- **Automotive/industrial**: where wired cabling is impractical.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: reuse Ethernet's CSMA/CD.* Physically impossible — a WiFi radio cannot transmit and receive on the same frequency simultaneously (no full duplex on the air), so it can't detect a collision while transmitting. It must *avoid* collisions (CSMA/CA) instead.
- *Alternative: scheduled TDMA/FDMA like cellular.* Centralized scheduling needs a coordinated controller, tight sync, and licensed spectrum; WiFi runs unlicensed and decentralized, so random access + backoff (DCF) was the only practical choice — 802.11ax's OFDMA later *added* scheduler-like efficiency on top of DCF.
- *Alternative: central polling (PCF).* Deterministic but inefficient and rarely implemented; DCF's random access is simpler and robust.
- *Alternative: no L2 retransmission (like Ethernet).* Air BER is 10⁻⁴–10⁻⁶ vs 10⁻¹² for copper; without frame-level ACK/retransmit, TCP would collapse (each loss = RTO). So 802.11 chose to ACK and retransmit at L2 — the opposite of Ethernet's detect-and-drop.
- *Alternative: stay in one band.* Unlicensed 2.4 GHz is crowded (microwave, BT); 5 GHz and 6 GHz add capacity. Not an "approach" but the same bandwidth-shortage logic that pushed wider channels (20→160 MHz).

## 5. Intuition
WiFi is a **noisy room with a polite etiquette**. Everyone checks that no one else is talking (carrier sense), waits a random extra beat (backoff) so two people don't start at the same time, then speaks (transmit). The listener replies "got it" (ACK); if the speaker doesn't hear "got it," they say it again (retransmit). Some people can't hear each other but both talk to the same listener (hidden terminal) — so the speaker first announces "I'm about to talk, everyone hold on" (RTS/CTS) to reserve the floor. Because everyone shares one radio band, only one conversation happens at a time in a given area — the more polite the waiting, the higher the throughput.

## 6. Real-World Analogy
A **dinner party with a maitre d'**. Guests (stations) wait at the door (DCF); the maitre d' lets one group in at a time (scheduling), and each speaker confirms the listener heard (ACK). If two people begin talking simultaneously, the speaker pauses, waits a random beat, and retries (backoff). When a speaker is too far from a nearby listener to hear them but they share the same audience (hidden terminal), the speaker first calls the maitre d' "I'll be speaking to table 3" (RTS/CTS), so everyone else waits. The party only has one dance floor (the channel) — politeness (backoff) keeps it productive.

## 7. Formal Definition
IEEE 802.11 is a family of L2/L1 standards for wireless LANs operating in ISM bands. **DCF**: stations use CSMA/CA — channel idle for DIFS (34–50 µs) then random backoff in [0, CW], CW ∈ [15, 31, 63, 127, 255, 511, 1023]; a successful unicast data frame is ACKed after SIFS (16–28 µs); unACKed → retransmit with CW doubling. **802.11 frame**: Frame Control (2 B: protocol, type, subtype, ToDS/FromDS, More Frag, Retry, PwrMgt, More Data, WEP, Order), Duration/ID (2 B), 4 address fields (6 B each — DA, SA, BSSID, and transmitter/receiver as needed), Sequence Control (2 B), QoS Control (2 B, 802.11e/n), payload, FCS (4 B CRC-32). **Physical layers**: DSSS/OFDM/OFDMA across bands; **MIMO/beamforming**; modulation up to 4096-QAM (802.11be); channel widths 20–320 MHz; spatial streams 1–16. **Security**: WEP (broken) → WPA (TKIP) → WPA2 (CCMP/AES-CCM) → WPA3 (SAE, GCMP, management-frame protection). **Roaming**: 802.11r fast BSS transition.

## 8. Example
**A single data exchange under DCF with RTS/CTS (numbers for 2.4 GHz, ~11 Mb/s-era but illustrative):**
1. STA senses idle for DIFS (50 µs) → picks backoff, say 4 slots × 20 µs = 80 µs.
2. Sends RTS (20 B) addressed to AP. AP replies CTS after SIFS (10 µs) — reserving the medium for the Duration field (NAV).
3. STA waits SIFS → sends data frame (e.g., 1500-byte payload, ~1 ms at 12 Mb/s).
4. AP waits SIFS → sends ACK (14 B). STA's NAV says the reservation ends; backoff count resumes.
5. If no ACK within ACK timeout, STA doubles CW and retries — up to ~7 retries for data (long retry limit).
Total: ~2–3 ms of airtime for a reliable 1500-byte delivery, versus Ethernet's ~12 µs on wire — WiFi's per-frame overhead is dominated by DIFS+SIFS+backoff+ACK, which is why aggregation (A-MPDU/A-MSDU, 802.11n+) exists.

## 9. Internal Working
1. **Carrier sense**: two mechanisms — physical (PHY energy detect) and virtual (NAV — stations read Duration in overheard frames and stay quiet until it expires). Hidden terminals are handled by RTS/CTS establishing a NAV that even non-hearing stations respect.
2. **Backoff state machine**: contention window grows 15→31→…→1023 on each failed attempt; success resets CW to 15. This is exponential backoff for airtime — the same idea as CSMA/CD's, applied to *avoidance*.
3. **ACK/retransmit**: unicast data must be ACKed (SIFS apart); no ACK → retry with Retry bit set. Broadcast/multicast are NOT ACKed (no single ACK possible) → less reliable.
4. **Fragmentation**: long frames can be fragmented (above a threshold) so a collision costs less to retransmit.
5. **Aggregation (n/ac/ax)**: A-MSDU (multiple MSDUs in one frame) + A-MPDU (multiple MPDUs in one PPDU) with **block-ACK** — one ACK per burst (Selective Repeat semantics, Section 02).
6. **OFDMA (ax)**: the AP schedules multiple stations on subcarriers simultaneously (multi-user) — mixing TDMA-like scheduling into the random-access DCF, boosting efficiency under many clients.
7. **Power save (PSM)**: client sets PwrMgt bit, AP buffers frames and announces them in beacons' TIM; client wakes and requests delivery (PS-Poll) — the client can sleep most of the time.
8. **Roaming**: STA scans (active: probe requests; passive: beacon listening), authenticates + associates to the new AP, re-runs 4-way handshake (or fast handover 802.11r).

## 10. Time Complexity / Performance Math
- **Access delay**: expected backoff ≈ CW/2 × slot_time (9 µs in 5 GHz, 20 µs in 2.4 GHz legacy) — O(CW) where CW doubles exponentially on collisions.
- **Throughput ceilings** (link rate, not real-world): 802.11b 11, g 54, n up to 600 (4×4 40 MHz), ac up to ~3.5 Gbps (8 streams), ax up to ~9.6 Gbps (OFDMA, 160 MHz), be up to ~46 Gbps (16 streams, 320 MHz). Real-world ≈ 40–60% of link rate after overhead (DIFS/SIFS/backoff/ACK/fragmentation).
- **Effective single-station efficiency** ≈ payload_airtime / total_airtime; aggregation lifts it from ~50% to ~85%+.
- **Scaling**: with N active stations sharing one channel, per-station share ≈ 1/N of channel time (random access fairness) — that's why multi-AP + 6 GHz + OFDMA matter in dense venues.

## 11. Advantages
- **No cabling** — instant, flexible deployment, mobile clients, ad-hoc/mesh options.
- **Unlicensed bands** — no spectrum license required (2.4/5/6 GHz).
- **Vendor interoperability** — Wi-Fi Alliance certification ensures cross-vendor operation.
- **Reliable enough**: L2 ACK/retransmit gives near-wire-like reliability to upper layers despite a lossy medium.
- **Continuously improving**: data rate ~×1000 since 1997; 6 GHz + OFDMA + MU-MIMO solve density.
- **Decentralized**: DCF needs no controller — any two devices can talk (Wi-Fi Direct, ad-hoc, mesh).

## 12. Disadvantages
- **Shared, half-duplex medium**: one conversation at a time per channel; throughput divides among active clients.
- **Unpredictable**: interference, walls, fading, multi-path → throughput/latency vary wildly; no hard QoS.
- **Security exposure**: air is open — needs WPA2/WPA3 + 802.1X; WEP/early WPA are broken; evil-twin/rogue APs.
- **Hidden/exposed terminals**: still cause collisions despite RTS/CTS; RTS/CTS itself costs airtime.
- **Power**: radios consume energy (mitigated by PSM, but clients with heavy traffic drain batteries).
- **Management overhead**: beacons, probes, association, key exchange consume airtime and complexity.

## 13. Interview Questions
1. **Q: Why does WiFi use CSMA/CA instead of CSMA/CD?** A: A radio can't transmit and receive on the same frequency simultaneously, so it cannot detect a collision while transmitting. It must *avoid* collisions by sensing the channel and adding a random backoff before transmitting, then confirm delivery with an ACK.

2. **Q: What are the components of the 802.11 DCF access method?** A: Carrier sense (physical + NAV virtual), DIFS idle wait, random exponential backoff in [0, CW] with CW 15→1023, transmit, SIFS, wait for ACK, retry on no-ACK with doubled CW. RTS/CTS reserves the medium for hidden terminals.

3. **Q: What is the hidden terminal problem and how does RTS/CTS help?** A: A and C both associate to AP B but can't hear each other; both transmit simultaneously → collision at B. RTS (from A) + CTS (from B) set a NAV on all stations within B's range (including C), so C stays silent during A's data — reducing collisions at B. (Not perfect: exposed-terminal cases remain.)

4. **Q: How does 802.11 achieve reliability at L2?** A: Every unicast data frame is ACKed after SIFS; no ACK → the frame is retransmitted with the Retry bit set and a doubled contention window, up to the retry limit. This is why TCP over WiFi sees few random losses — L2 retransmits absorb air errors.

5. **Q: What is the difference between DCF and PCF?** A: DCF is distributed random access (CSMA/CA) — every station competes. PCF is centralized polling by the AP (contention-free period) — deterministic but rarely implemented. 802.11ax's OFDMA brings a scheduler into DCF for multi-user efficiency.

6. **Q: TRICKY — Why are broadcast/multicast frames not ACKed in WiFi?** A: Because there's no single recipient to ACK, and asking everyone would cause ACK collisions. So broadcasts/multicasts are sent at a lower (more robust) rate and are less reliable — a hidden cost of WiFi that ARP and mDNS suffer. This is also why multicast-heavy apps use unicast relaying.

7. **Q: What is the NAV and how does virtual carrier sense work?** A: Every station reads the Duration field in overheard frames (RTS/CTS/data) and sets a Network Allocation Vector — a countdown timer during which it defers. This lets a station that can't physically hear the transmitter still avoid the medium (solving hidden-terminal part). Real energy detection is physical carrier sense; NAV is virtual.

8. **Q: PRODUCTION — Users report slow WiFi. What are the top causes you investigate?** A: (1) Channel congestion (check neighboring APs, channel width, DFS); (2) too many clients on one AP/one channel; (3) coverage/fading (signal strength, antenna, walls); (4) legacy clients (b/g devices drag the whole BSS to slow rates, "protection" overhead); (5) interference (microwave/Bluetooth at 2.4 GHz); (6) hidden terminals; (7) poor roaming (sticky clients). Fix: band-steer to 5/6 GHz, channel planning, fast roaming, and 802.11ax/be upgrades.

9. **Q: How does a WiFi client discover and join a network?** A: Scanning (passive: listen for beacons; active: probe request/response) → authentication (open or 802.1X) → association (assoc request/response) → 802.1X/EAP + 4-way handshake for keys (WPA2/3) → data. Roaming repeats scan+auth+assoc at the new AP (fast version: 802.11r).

10. **Q: What is the 4-way handshake and why does it exist?** A: In WPA2/WPA3-PSK, both sides derive a PMK from the passphrase; the 4-way handshake (AP→STA nonce, STA→AP nonce + MIC, AP confirms, STA confirms) proves both know the PMK without exposing it and derives fresh per-session PTK keys. It prevents passphrase exposure over the air and provides key freshness.

11. **Q: SCENARIO — You see high retry counts on one AP. What could it mean?** A: Retries mean frames weren't ACKed → hidden terminals, interference, too many clients, low signal (retrying at high rates), or power-save clients missing frames. Check `iw dev wlan0 station dump` retry counters, channel noise, and client signal; consider RTS/CTS threshold, lower rates, or more APs.

12. **Q: TRICKY — What is the "protection mechanism" (RTS/CTS with legacy rates)?** A: When 802.11g/n/ac devices coexist with 802.11b clients, the AP announces a "protection" mode: 802.11g/n/ac stations must use CTS-to-self or RTS/CTS frames sent at 802.11b-compatible rates, so b-only devices can decode them and defer — otherwise b clients would transmit during n transmissions. Costs throughput.

13. **Q: How does MIMO and beamforming improve WiFi?** A: MIMO uses multiple antennas/spatial streams to send independent data in parallel (spatial multiplexing) or to improve reliability (diversity); beamforming shapes the signal toward the client (explicit/implicit), boosting SNR and range. 802.11n added up to 4 streams; ac/ax up to 8; be up to 16.

14. **Q: PRODUCTION — WiFi 6 (802.11ax) claims better efficiency, not just speed. Why?** A: OFDMA lets the AP schedule multiple clients on subcarrier groups simultaneously (instead of one client hogging the whole channel); MU-MIMO handles multiple clients on the same time; TWT (Target Wake Time) schedules client sleep — all reduce contention and overhead under many clients, which is why ax shines in dense venues, not just on link rate.

15. **Q: What is WPA3's SAE and why is it better than WPA2-PSK?** A: SAE (Simultaneous Authentication of Equals) uses a Dragonfly-based key exchange instead of PSK-to-PMK derivation: it's resistant to offline dictionary attacks (an attacker can't crack the passphrase from a captured handshake), provides forward secrecy, and prevents deauth-type downgrade attacks. WPA3 also adds GCMP (192-bit) and protected management frames (PMF).

16. **Q: TRICKY — Your phone shows "full bars" but throughput is terrible. Why?** A: Signal strength (RSSI) ≠ data rate: if the channel is congested, interfered, or half-duplex with many clients, even a strong signal yields low throughput. Also "bars" don't reflect contention, SNR vs interference, or which band/width you're on. Check the *actual* link rate and channel utilization.

17. **Q: What is the difference between infrastructure, ad-hoc, and mesh modes?** A: Infrastructure: clients talk via an AP (most deployments; BSSID = AP MAC). Ad-hoc (IBSS): peers talk directly without an AP. Mesh (802.11s): APs form a multi-hop wireless backhaul with routing; clients attach to any mesh AP. Mesh trades throughput for coverage without cabling.

18. **Q: SCENARIO — Two 802.11n devices, one 802.11b device, same AP. How does the b device affect the others?** A: The AP enables protection (CTS-to-self/RTS-CTS at b rates), and the b device's slow rate and long preamble occupy more airtime per bit — so the fast devices' effective throughput drops dramatically. This is the classic "one legacy client kills the BSS" problem; the fix is isolating legacy devices on a separate AP/band.

## 14. Follow-Up Questions
1. **Q: What is the relationship between slot time and DIFS/SIFS?** A: SIFS < DIFS ≤ slot time matters: SIFS is used by ACKs so they get priority over new data (ACKs aren't backed off); DIFS (data start) > SIFS ensures control frames win the medium. The ordering SIFS < DIFS is what makes ACKs reliable.

2. **Q: Why does WiFi retransmit but Ethernet doesn't?** A: Air BER (10⁻⁴–10⁻⁶) vs copper (10⁻¹²): on wire, drops are rare enough to leave to TCP; over the air, without L2 ACK/retransmit, TCP's RTO would wreak havoc on a lossy link. WiFi trades the simplicity of detect-and-drop for the reliability the medium demands.

3. **Q: How do 802.11k/v/r improve roaming?** A: k (neighbor reports), v (BSS transition management — AP tells the client a better AP), r (fast BSS transition — fast reauthentication/key handover). Together they cut roaming blackouts from seconds to <100 ms for voice/video.

4. **Q: What's the "DCF vs PCF vs EDCA" hierarchy?** A: DCF = baseline random access; PCF = (rare) central polling; EDCA (802.11e) = prioritized DCF with four access categories (voice/video/best-effort/background) with different CW ranges — QoS without full centralization.

## 15. Coding Example
```python
import random, struct, time

CW_MIN, CW_MAX, SLOT = 15, 1023, 9  # µs slot at 5 GHz

def csma_ca_send(data: bytes, sifs=16, difs=34, ack_timeout=100) -> int:
    """Simulated DCF transmit: returns airtime µs (or retries if no ACK)."""
    cw = CW_MIN
    airtime = 0
    for attempt in range(7):            # long retry limit
        backoff = random.randint(0, cw) * SLOT
        airtime += difs + backoff + len(data) * 8 // 12 * 8 + sifs + 14 * 8 // 12 * 8
        if random.random() < 0.9:        # 90% ACK success
            return airtime
        cw = min(cw * 2 + 1, CW_MAX)     # exponential backoff
    return None                          # frame dropped after retries

def estimate_throughput(rate_mbps=600, payload=1500, overhead_us=200) -> float:
    """Real-world WiFi throughput ≈ link rate minus MAC/CSMA overhead."""
    frame_us = (payload + 40) * 8 / (rate_mbps * 1e-3)
    return (payload * 8) / (frame_us + overhead_us) / 1e3   # Mbps

print(f"single-frame airtime: {csma_ca_send(b'x'*1500)} µs")
print(f"802.11ac ~{estimate_throughput(600):.0f} Mbps real-world at 600 Mb/s link")
```
```bash
# Practical WiFi inspection on Linux
iw dev wlan0 link                              # BSSID, freq, signal, tx bitrate
iw dev wlan0 station dump                      # rx/tx packets, retries, signal
iw dev wlan0 info                              # interface type (managed/AP/mesh)
sudo tcpdump -i wlan0 -n 'wlan type mgt subtype beacon'   # beacon sniffing
sudo tcpdump -i wlan0 -n -e                     # 802.11 frames with MACs/FCS
nmcli dev wifi list                             # scan results (channels, signal)
iwlist wlan0 channel                            # channel availability/DFS
```

## 16. Industry Usage
- **Every consumer device**: phones, laptops, TVs, IoT (802.11 a/b/g/n/ac/ax/be); Wi-Fi Alliance certification.
- **Enterprise**: Cisco/Meraki/Aruba/Extreme APs, WPA3-Enterprise (802.1X/EAP-TLS), 6 GHz (WiFi 6E/7), zero-touch deployment, AI-driven RF optimization.
- **Cloud-managed**: cloud AP controllers (Cisco Meraki, Aruba Central, Mist AI) centralize config/analytics.
- **Roaming/security**: 802.11r/k/v, rogue-AP detection, WIDS/WIPS (Part 07).
- **IoT**: 802.11ah (HaLow) sub-GHz for sensors; Wi-Fi Aware (proximity); Matter/Thread + WiFi.
- **Cellular offload & unlicensed**: LTE-LAA/WiFi coexistence research; carrier WiFi hotspots.

## 17. References
- IEEE Std 802.11-2020 (all amendments) — https://standards.ieee.org/ieee/802.11/7028/
- IEEE 802.11ax (WiFi 6) / 802.11be (WiFi 7) — https://www.ieee802.org/11/
- Kurose & Ross, *Computer Networking*, 8th ed., §6.3.3/§6.4 (Wireless LANs, WiFi).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §4.3 (Wireless LANs).
- Matthew Gast, *802.11 Wireless Networks: The Definitive Guide*, O'Reilly.
- Wi-Fi Alliance — https://www.wi-fi.org/

## 18. Cheat Sheet
- WiFi = IEEE 802.11; uses CSMA/CA (can't listen while transmitting) + ACK + L2 retransmit.
- DCF: DIFS + backoff [0,CW], CW 15→1023; SIFS < DIFS so ACKs win; RTS/CTS for hidden terminals.
- Frame: FC(2)+Duration(2)+Addr(4×6)+Seq(2)+QoS(2)+payload+FCS(4 CRC-32); up to 4 addresses (DA/SA/BSSID/TA/RA).
- NAV = virtual carrier sense via Duration field; physical = energy detect.
- Unicast ACKed, broadcast/multicast NOT ACKed.
- Speeds: b 11, g 54, n 600 (4×4), ac ~3.5G (8×8), ax ~9.6G (OFDMA), be ~46G.
- Real-world throughput ≈ 40–60% of link rate (MAC overhead + contention).
- Security: WEP(broken)→WPA→WPA2(CCMP)→WPA3(SAE/PMF); 4-way handshake; 802.1X enterprise.
- Protection mechanism: legacy clients force CTS/RTS at slow rates (bottleneck).
- Power save: PSM/TIM, client sleeps, AP buffers; TWT in ax.

## 19. Quiz
1. WiFi uses which MAC protocol? a) CSMA/CD b) CSMA/CA c) TDMA d) token → **b**
2. Why not CSMA/CD? a) too slow b) can't transmit and receive simultaneously c) too few users d) uses fiber → **b**
3. The ACK is sent after: a) DIFS b) SIFS c) backoff d) NAV → **b**
4. Contention window starts at: a) 15 b) 31 c) 63 d) 1023 → **a**
5. Broadcast frames in WiFi are: a) ACKed b) not ACKed c) retransmitted d) fragmented → **b**
6. NAV provides: a) physical carrier sense b) virtual carrier sense c) encryption d) power save → **b**
7. WPA3 uses which key exchange? a) PSK only b) SAE c) TKIP d) WEP → **b**
8. Which standard adds OFDMA? a) 802.11n b) 802.11ac c) 802.11ax d) 802.11g → **c**

**Answers**: 1-b, 2-b, 3-b, 4-a, 5-b, 6-b, 7-b, 8-c.

## 20. Flashcards
- **Q: Why CSMA/CA and not CSMA/CD?** → **A:** Radios can't transmit and receive at once, so they can't detect collisions; they avoid them with backoff and confirm with ACKs.
- **Q: How does WiFi guarantee delivery?** → **A:** Unicast ACK after SIFS + retransmission with exponential backoff (up to retry limit).
- **Q: What is the hidden terminal problem?** → **A:** Two transmitters can't hear each other but collide at the common AP; RTS/CTS + NAV mitigates.
- **Q: What does NAV do?** → **A:** Virtual carrier sense: stations defer for the Duration in overheard frames.
- **Q: Security evolution?** → **A:** WEP→WPA→WPA2(CCMP/AES)→WPA3(SAE, PMF); 4-way handshake derives session keys.
- **Q: What is 802.11ax's key efficiency feature?** → **A:** OFDMA — the AP schedules multiple clients on subcarriers at once + MU-MIMO + TWT.
- **Q: Real-world vs link rate?** → **A:** 40–60% of link rate due to DIFS/SIFS/backoff/ACK/aggregation overhead.

## 21. Revision
WiFi (IEEE 802.11) is Ethernet's wireless cousin: it can't do CSMA/CD (a radio can't listen while transmitting), so it uses CSMA/CA — sense idle, wait DIFS + random backoff (CW 15→1023), transmit, get ACK after SIFS, retry with doubled CW on failure; RTS/CTS and the NAV handle hidden terminals; broadcast is never ACKed. Because air is lossy, it ACKs and retransmits at L2 (unlike Ethernet). The frame has up to 4 addresses (DA/SA/BSSID/TA/RA), a QoS control field, and a CRC-32 FCS. Speeds grew 11 Mb/s → 46 Gbps (b→be) via OFDM, MIMO, wider channels, aggregation (A-MPDU + block-ACK = Selective Repeat semantics), and OFDMA (ax) for density. Security went WEP→WPA→WPA2→WPA3 (SAE, PMF, 802.1X). Anchor: *WiFi = "politely avoid collisions then confirm with ACK"; Ethernet = "assume clean wire, detect and drop."*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why CSMA/CA not CSMA/CD?" | 4 / 13-Q1 |
| "How does DCF work?" | 7 / 13-Q2 |
| "Hidden terminal + RTS/CTS?" | 13-Q3 / 5 |
| "How does WiFi provide reliability?" | 13-Q4 / 2 |
| "Why aren't broadcasts ACKed?" | 13-Q6 |
| "What is the NAV?" | 13-Q7 |
| "Slow WiFi — top causes?" | 13-Q8 |
| "How does the 4-way handshake work?" | 13-Q10 |
| "What is 802.11ax/OFDMA efficiency?" | 13-Q14 |
| "One legacy client slows everyone — why?" | 13-Q18 |
