# Multiplexing and Switching

> **TL;DR**: Multiplexing lets many users share one physical channel by dividing it by frequency (FDM/WDM), time (TDM, with statistical variants for bursts), or code (CDMA); switching connects those users' flows across a network — circuit switching (dedicated path) vs packet switching (statistical multiplexing) being the architectural fork that made the Internet possible.

## 1. Why Does This Exist?
A single fiber can carry tens of Tbps; a single user needs a few Mbps to a few Gbps. Wasting one channel on one user is unthinkable — **multiplexing** exists so many conversations share one expensive medium. Separately, a network with many users needs to *connect* them: **switching** decides how a conversation's data moves through intermediate nodes. These two ideas are the physical+network layer's economics: multiplexing multiplies what a channel carries, switching routes flows through a topology. Circuit switching (telephone) and packet switching (Internet) are the two grand designs, and the entire modern Internet's character — burst-friendly, statistical, cheap, best-effort — follows from the packet-switching choice.

## 2. How Does It Work?
**Multiplexing**:
- **FDM** (frequency division): each user gets a frequency band; all transmit simultaneously; guards keep bands separate. WDM is FDM on a fiber (each wavelength = a user).
- **TDM** (time division): time is sliced into slots; each user transmits only in their slot; synchronized. **Statistical TDM** (STDM): slots are assigned *on demand* to active users — the key improvement that makes packet switching efficient.
- **CDMA** (code division): every user transmits on the *same* frequency at the *same* time, but each multiplies their bits by a unique spreading code; receivers decode by correlating with the known code (3G cellular used this).
- **OFDM/OFDMA**: split a wide channel into many narrow orthogonal subcarriers; 4G/5G/WiFi 6 assign subcarriers per user — modern FDM+time scheduling.

**Switching**:
- **Circuit switching**: a dedicated end-to-end path (physical or TDM slots) is reserved *before* data flows, held for the whole conversation, torn down after — like a phone call. Deterministic but wastes idle capacity.
- **Packet switching**: data is chopped into packets, each forwarded independently by store-and-forward nodes using its destination address (datagram) or a precomputed path (virtual circuit, MPLS); statistical multiplexing means *no reservation* — bursts share links. Simple, robust, efficient for bursty traffic, best-effort.

## 3. When Is It Used?
- **FDM**: radio/TV broadcast bands, cable TV, DOCSIS (downstream), POTS (up/down bands for DSL).
- **WDM/DWDM**: every long-haul/undersea fiber — hundreds of wavelengths on one strand.
- **TDM**: T1/E1 telephony (24/30×64 kbps DS0s), SONET/SDH (STS/STM frames), some industrial buses.
- **CDMA**: 3G (IS-95, WCDMA), GPS (each satellite has a unique code), military spread-spectrum.
- **OFDM/OFDMA**: LTE/5G, WiFi 4/5/6, DVB-T, ADSL — the current ubiquity.
- **Statistical TDM / packet switching**: the entire Internet, Ethernet, IP, MPLS, data centers.
- **Circuit switching**: legacy PSTN, TDM telephony, and where QoS is mandatory (some carrier backhaul, ISDN); classic "packet vs circuit" interview comparisons.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: one circuit per conversation (circuit switching for everything).* Deterministic QoS and no loss, but catastrophic inefficiency for bursty data: a reserved 64 kbps circuit for a Web click that sends 100 ms of data per minute wastes ~99.9%. The phone network is circuit-switched *because voice is constant-bit-rate*; data is bursty, so packet switching + statistical multiplexing wins — that's the core economic argument (Kleinrock's packet switching insight, vs the telephone era).
- *Alternative: pure FDM for everything.* Fixed bands are fine for continuous streams (radio/TV) but a silent user wastes their band; TDM does better for fixed-rate digital; statistical TDM (packets) captures the bursty case.
- *Alternative: CDMA for data everywhere.* CDMA is robust against interference (spread-spectrum gain) but needs tight power control and complex receivers; OFDMA gives better spectral efficiency for broadband — that's why 3G CDMA became 4G/5G OFDMA.
- *Alternative: packet switching with virtual circuits only (like X.25/ATM).* VCs give QoS and ordering but need per-flow state at every node and setup latency; pure datagram IP is stateless per flow (only routing table) — simpler, more robust to failures. MPLS compromises (VC-like labels) where QoS matters, but the Internet core is datagram.

## 5. Intuition
Multiplexing is **lanes on a highway**: FDM paints separate lanes (each user a different frequency lane), TDM makes everyone use one lane but only during their assigned time window, CDMA lets everyone drive on the same lane at once but in cars painted with unique patterns (the receiver filters for their pattern), and statistical TDM is a smart toll booth that lets you on whenever you show up with data (no reserved time). Switching is **how the highway system connects cities**: circuit switching = you rent the *entire* highway between two cities for your trip (empty when you're not driving), packet switching = everyone shares the highways, each car (packet) picks its own route and merges in (traffic jams possible, but the roads are never empty).

## 6. Real-World Analogy
A **post office with sorting rooms (packet switching)** vs **a private chauffeur (circuit switching)**. In the post office, your letter (packet) is routed room by room (hop by hop), other letters interleave freely (statistical multiplexing), and if one room is busy your letter waits or takes another path (no reservation, robust). The chauffeur reserves the whole street network for your trip — perfect timing, but the roads are empty when you're not moving and a closed road is a disaster. The Internet chose the post office because data comes in bursts; the phone network keeps the chauffeur because a call is a continuous stream.

## 7. Formal Definition
**Multiplexing**: combining multiple independent signals onto one shared channel. **FDM** divides the spectrum into disjoint bands with guard bands (bandwidth per user = W/N). **WDM** is FDM at optical frequencies (each lambda a channel). **TDM** divides time into frames of N slots, each user assigned a slot (bit rate per user = link_rate/N); **statistical TDM** assigns slots dynamically to active users, achieving multiplexing gain M (effective users > N). **CDMA**: user *i* multiplies each bit by a code cᵢ of length L (chip rate); codes are orthogonal (cᵢ·cⱼ = 0); receiver correlates r(t)·cᵢ to recover user *i*'s bits; processing gain = L.

**Switching**: **circuit** — a path with reserved resources (e.g., 64 kbps TDM slots) is established end-to-end before transmission; **packet (datagram)** — packets are self-contained and routed independently by destination address (store-and-forward); **virtual circuit (packet with connection)** — a label-switched path is set up once (X.25, Frame Relay, ATM, MPLS), then packets carry only the label. **Store-and-forward** delay at each node = L/R (transmission) + processing + queueing.

## 8. Example
**FDM/TDM allocation on a 100 Mbps link, 4 users:**
- FDM: each user gets a dedicated 25 Mbps band (100/4) — always available but wasted if idle.
- TDM: each user transmits in their 1/4 time slot at 100 Mbps instantaneous → same average 25 Mbps; a user with nothing to send still holds their slot (wasted).
- Statistical TDM: if users are active 10% of the time, the link can *statistically* serve ~10 users of the same rate because collisions are rare (multiplexing gain). Expected concurrent load with 10 users × 10% = 1.0 → rarely oversubscribed.

**Circuit vs packet, worked:**
- Circuit: 64 kbps voice circuit held for a 3-minute call → 11.5 MB of reserved capacity for 11.5 MB of data.
- Packet: a Web page transfer of 200 KB over a 1 Gbps link with 50 ms RTT: store-and-forward + queueing; total transfer time ≈ RTT + file_size/bandwidth + propagation ≈ 50 ms + 1.6 ms + prop — vastly less than reserving a circuit.

## 9. Internal Working
1. **FDM hardware**: each transmitter is assigned a carrier (band); a frequency-division *multiplexer* combines; the demultiplexer filters by band (band-pass filters); guard bands prevent adjacent-channel interference.
2. **TDM hardware**: a frame clock slices time; each slot carries one user's bits; the demux picks bits by slot number — needs slot/frame synchronization.
3. **Statistical TDM / packet switch**: each packet has a header (dest address); the switch does output-port queueing (FIFO, WFQ, etc.); packets from many sources interleave; queues overflow → drops → TCP reacts (Part 03). This is "shared, on-demand, lossy, fair-ish."
4. **CDMA**: transmitter multiplies bits by the spreading code (BPSK on the chip sequence); receiver multiplies the combined signal by the *same* code and integrates over the bit period — orthogonal codes cancel other users' energy (interference from others ≈ 0).
5. **OFDMA**: the IFFT/FFT maps data onto orthogonal subcarriers; the base station schedules subcarriers per user per slot — combining FDM's orthogonality with TDM-style scheduling (4G/5G).
6. **Circuit setup**: signaling (SS7/ISDN) reserves slots at each switch along the path; data flows without per-packet decisions; teardown releases slots.

## 10. Time Complexity / Performance
- **FDM**: capacity/user = W/N, latency = propagation (no queueing); simple but fixed.
- **TDM**: capacity/user = R/N; slot overhead; deterministic latency ≤ one frame.
- **Statistical TDM**: capacity = R × (active users' demand), with *multiplexing gain*; latency includes queueing (unbounded under load); loss under overload.
- **Packet switching delay** = transmission (L/R per hop) + propagation (d/v) + queueing + processing. Number of hops × per-hop delay — the "why store-and-forward costs" math.
- **Circuit switching**: setup time + propagation; no queueing (deterministic) but capacity is *reserved* (wasted when idle).
- CDMA: chip-rate processing (L× bit rate), fine for 3G-era rates.

## 11. Advantages
- **Multiplexing (all)**: one medium serves many users — the core economics of every network.
- **Statistical TDM/packet**: *work-conserving* — idle users consume nothing; active users can borrow spare capacity (vs FDM/TDM's fixed waste); robust, stateless, cheap.
- **Circuit**: guaranteed bandwidth, no queueing loss, bounded latency, natural for CBR (voice/video).
- **CDMA**: robust to interference and jamming (spread-spectrum), soft capacity, works with no frequency planning.
- **WDM**: hundreds of lambdas on existing fiber = massive capacity without new cable.
- **OFDMA**: near-optimal spectral efficiency + flexible scheduling + robustness to multipath.

## 12. Disadvantages
- **FDM**: fixed allocation wastes idle bands; guard bands waste spectrum.
- **TDM**: idle slots wasted; synchronization complexity.
- **Statistical TDM**: congestion → queueing delay, loss, unfairness (needs TCP/congestion control).
- **Circuit**: setup latency, resource waste on bursty traffic, single point of failure per circuit.
- **CDMA**: power-control fragility (near-far problem), complex receivers, lower spectral efficiency than OFDMA at high rates.
- **Packet switching (datagram)**: no QoS guarantee, out-of-order possible, per-packet overhead.

## 13. Interview Questions
1. **Q: What is multiplexing and why is it necessary?** A: Combining many users' signals onto one shared channel — because channels (fiber, cable, spectrum) cost far more than the traffic of any single user. Without it, every conversation would need a dedicated physical medium.

2. **Q: Explain FDM vs TDM vs statistical TDM.** A: FDM divides frequency into fixed bands (each user a band, simultaneous). TDM divides time into slots (each user a slot, sequential). Statistical TDM assigns slots *on demand* only to active users — the efficiency win that enables packet switching.

3. **Q: What is WDM and why is it important for fiber?** A: Wavelength Division Multiplexing — many wavelengths (colors) on one fiber (FDM at optical frequencies). DWDM packs 80-160 channels × 400G → tens of Tbps on a single strand without pulling more fiber.

4. **Q: What is CDMA and how does it separate users?** A: All users share the same frequency/time but each multiplies their bits by a unique orthogonal code; the receiver correlates the combined signal with the target code — other users' codes integrate to ~0. Used in 3G and GPS; robust to interference.

5. **Q: TRICKY — A 4-user link at 100 Mbps: FDM vs TDM, what's each user's guaranteed rate, and what's the total?** A: Both give each user a guaranteed 25 Mbps average (FDM = 25 Mbps band always; TDM = full 100 Mbps in 1/4 of the slots), total 100 Mbps. The difference is behavior under *idle* users: FDM/TDM waste, statistical TDM lets active users use the whole 100 Mbps.

6. **Q: Why is the Internet packet-switched and not circuit-switched?** A: Data is *bursty* — reserving a circuit for a bursty flow wastes most of it (a page view uses milliseconds per second). Packet switching + statistical multiplexing shares links on demand, is work-conserving, robust (no single circuit to fail), and cheap. Voice was the circuit-switch justification (constant rate).

7. **Q: What are the components of packet-switching delay?** A: Transmission (L/R per hop), propagation (distance/speed of light), queueing (at output buffers), and processing (lookup, forwarding). Store-and-forward means each hop adds L/R before forwarding — the reason multi-hop paths add latency.

8. **Q: PRODUCTION — When would you still choose circuit switching today?** A: Where QoS is non-negotiable and traffic is constant-rate: legacy TDM voice (T1/E1), some carrier backhaul, and real-time control with hard latency bounds. Also conceptually in "guaranteed-resource" reservations (e.g., some optical lightpaths, and 5G's "network slicing" borrows the idea).

9. **Q: SCENARIO — A shared 1 Gbps link has 100 users each needing 10 Mbps at 10% duty cycle. Can you provision it?** A: Yes — statistical multiplexing: expected concurrent demand = 100 × 10% × 10 Mbps = 100 Mbps, far under 1 Gbps. The *multiplexing gain* lets you oversubscribe (like cloud compute). Risk: correlated bursts (flash crowds) still overload — which is why oversubscription ratios are carefully chosen.

10. **Q: What is OFDM/OFDMA and why did 4G/5G/WiFi adopt it?** A: A wide channel split into many narrow orthogonal subcarriers (IFFT-modulated); each carries a low-rate stream, making the signal robust to frequency-selective fading and multipath. OFDMA additionally *schedules* subcarriers per user per slot — flexible, efficient, near-Shannon (with FEC).

11. **Q: TRICKY — Why is the "multiplexing gain" not free?** A: Because statistical sharing means sometimes *everyone* is active (correlated load) → queueing delay and packet loss. The gain is a probabilistic expectation, not a guarantee — hence congestion control (TCP) and admission control in QoS designs.

12. **Q: What is a virtual circuit (packet switching with connection)?** A: A path with labels is set up once (signaling), then packets carry only a short label (no full destination lookup per packet) — X.25, Frame Relay, ATM, and MPLS. It gets circuit-like ordering/QoS with packet efficiency; the Internet core is datagram IP but MPLS lives inside ISP backbones.

13. **Q: What is store-and-forward and how does it differ from cut-through?** A: Store-and-forward: receive the whole packet, check FCS, then forward (error isolation, adds L/R per hop). Cut-through: forward as soon as the destination header is read (µs latency, no FCS check). Switches default to store-and-forward; cut-through suits latency-critical DC fabrics.

14. **Q: SCENARIO — Voice over a packet network keeps jittering. Which multiplexing property is the culprit?** A: Queueing delay varies with load (statistical multiplexing) — jitter. Circuit/TDM has fixed slots → no jitter. Solutions: QoS prioritization (DiffServ/EF), jitter buffers at the receiver, and dedicated codec bandwidth — but the *statistical* nature is the root cause.

15. **Q: What's the difference between FDM and OFDM's use of frequency?** A: FDM uses non-overlapping bands *with guard bands* (waste). OFDM uses overlapping orthogonal subcarriers (side-lobe nulls align) — no guard bands → far better spectral efficiency. The orthogonality comes from the FFT structure.

16. **Q: PRODUCTION — A DC fabric is "oversubscribed 4:1" at the spine. Is that a mistake?** A: No — it's statistical multiplexing by design: leaf-to-spine is 4:1 because real workloads are bursty and rarely all-saturate simultaneously. Problems arise only when correlated traffic (all-to-all, big ML jobs) exceeds the ratio — which is why GPU clusters get 1:1 fabrics.

17. **Q: TRICKY — Can packet switching provide the same QoS as circuit switching?** A: Not with datagram alone — no reservation means no guarantee; QoS needs virtual circuits/MPLS, admission control, or scheduling (DiffServ/IntServ) layered on. This is exactly why carriers use MPLS for VPN QoS inside a datagram Internet.

18. **Q: What is T1/E1 and how is it an example of TDM?** A: A T1 = 24 × 64 kbps DS0 voice channels in time slots + framing bit = 1.544 Mbps; E1 = 32 slots (30 usable) = 2.048 Mbps. Each call occupies a recurring time slot — pure TDM, the telephone multiplexing standard for decades.

## 14. Follow-Up Questions
1. **Q: What is the difference between FDM guard bands and OFDM's approach?** A: FDM needs guard bands (wasted spectrum) because filters aren't perfect; OFDM's subcarriers are mathematically orthogonal (sidelobe nulls), so they can touch without interference — the spectral-efficiency win.

2. **Q: How does MPLS combine circuit and packet ideas?** A: It sets up label-switched paths (circuit-like, with QoS/bandwidth options) but forwards with labels on shared links (packet-like, statistical). It's the industry's pragmatic compromise: datagram IP on the edges, labeled paths in the core.

3. **Q: What is the "near-far problem" in CDMA?** A: A near transmitter's high power swamps a far transmitter's weak signal at the receiver (power control must equalize received powers). This is why CDMA needed tight power control and why OFDMA (frequency separation) replaced it for broadband.

4. **Q: What is statistical multiplexing in plain terms?** A: Sharing a channel on-demand so that the *sum of average* demands, not the *sum of peak* demands, needs to fit — enabling oversubscription with high probability.

## 15. Coding Example
```python
import random

def tdm_allocate(users=4, slots=8, link_mbps=100):
    """TDM: each user gets link/N slots → guaranteed rate."""
    return {f"u{i}": link_mbps // users for i in range(users)}

def statistical_tdm_load(n_users, duty_cycle, rate_mbps, link_mbps):
    """Expected concurrent load under statistical multiplexing."""
    return n_users * duty_cycle * rate_mbps / link_mbps

def packet_switch_delay(hop_count, packet_bits, rate_bps, prop_s, proc=1e-6):
    """Store-and-forward end-to-end delay for n hops."""
    trans = packet_bits / rate_bps
    return hop_count * (trans + proc) + hop_count * prop_s

print("TDM:", tdm_allocate())
print(f"statistical load (100 users,10%,10Mbps,1G link): {statistical_tdm_load(100,0.1,10e6,1e9):.2f}")
print(f"10 hops, 1500B, 1Gbps, 1ms prop: {packet_switch_delay(10, 12000, 1e9, 1e-3)*1e3:.3f} ms")
```
```python
# Simple CDMA-style correlation (orthogonal codes)
codes = {0: [1,1,1,1], 1: [1,-1,-1,1]}   # length-4 orthogonal codes
def cdma_encode(bits, code):
    return [b * c for b in bits for c in code]
def cdma_decode(signal, code):
    out = []
    for i in range(0, len(signal), len(code)):
        chip = sum(signal[i+j] * code[j] for j in range(len(code)))
        out.append(1 if chip > 0 else 0)
    return out
sig = cdma_encode([1,0,1], codes[0]) + cdma_encode([0,1,0], codes[1])
print("decoded u0 from mixed signal:", cdma_decode(sig, codes[0]))  # [1,0,1]
```
```bash
# Observe multiplexing/switching in production
ss -tin | head -5                                    # per-flow queueing / congestion state
ip -s link show eth0 | grep -E "dropped|overruns"    # queue overflow (loss) evidence
tc -s qdisc show dev eth0                            # active scheduler (FIFO/WFQ/etc.)
# MPLS/VLAN 'labels' in Linux:
ip link add name mpls0 type dummy
ip -details link show | grep -i mpls
# OFDM/multiplexing visible on WiFi:
iw dev wlan0 info | grep channel
```

## 16. Industry Usage
- **Long-haul**: DWDM (80-160 lambdas/fiber) with ROADMs — FDM/WDM everywhere.
- **Access**: DOCSIS (FDM downstream + TDM/statistical upstream), GPON (TDM/WDM), DSL (FDM bands).
- **Cellular**: 4G/5G OFDMA + TDD/FDD scheduling; CDMA was 3G (IS-95/WCDMA); 5G slicing = circuit-like guarantees on packet radio.
- **Core ISP**: MPLS label switching + statistical sharing; RSVP-TE for reserved bandwidth.
- **Data centers**: packet switching with oversubscribed spines (4:1 typical), lossless Ethernet (PFC) for storage/ML; VXLAN overlays.
- **Telephony**: TDM T1/E1/SONET legacy; the PSTN is circuit-switched — why "phone" and "Internet" are different designs.

## 17. References
- Kurose & Ross, *Computer Networking*, 8th ed., §1.3 (Circuit vs Packet), §1.3.2 (multiplexing).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §2.3/2.4 (multiplexing), §3.5 (packet vs circuit).
- Kleinrock, "The Early Days of the ARPANET" — packet switching history.
- ITU-T G.707 (SONET/SDH/TDM) — https://www.itu.int/rec/T-REC-G.707
- 3GPP TS 36.211 / 38.211 (OFDMA physical layer) — https://www.3gpp.org/
- Stallings, *Data and Computer Communications*, Ch. 8 (Multiplexing).

## 18. Cheat Sheet
- FDM = fixed frequency bands (with guard bands); WDM = FDM on fiber (lambdas).
- TDM = fixed time slots; statistical TDM = on-demand slots (packet switching).
- CDMA = orthogonal codes, same freq/time; processing gain = code length; near-far problem.
- OFDMA = orthogonal subcarriers + per-user scheduling (4G/5G/WiFi 6).
- Circuit = reserved path (deterministic, wasteful for bursts); Packet = statistical sharing (efficient, lossy).
- Packet delay = transmission + propagation + queueing + processing (per hop).
- Multiplexing gain → oversubscription (DC spines 4:1; risk = correlated load).
- MPLS = virtual-circuit labels in a packet network.
- Store-and-forward adds L/R per hop; cut-through skips FCS.
- Voice = circuit (TDM 64k DS0); data = packet (Internet).

## 19. Quiz
1. FDM divides a channel by: a) time b) frequency c) code d) voltage → **b**
2. WDM is FDM at: a) radio b) optical wavelengths c) time d) code → **b**
3. Statistical TDM differs from TDM by: a) fixed slots b) on-demand slots c) frequencies d) codes → **b**
4. 4 users on 100 Mbps TDM → each gets: a) 100 b) 50 c) 25 d) 10 Mbps → **c**
5. The Internet is: a) circuit-switched b) packet-switched c) CDMA d) TDM-only → **b**
6. Packet-switching delay components include: a) setup b) queueing c) reservation d) paging → **b**
7. CDMA separates users via: a) time b) frequency c) orthogonal codes d) slots → **c**
8. Which replaced CDMA in 4G/5G? a) FDM b) TDM c) OFDMA d) WDM → **c**

**Answers**: 1-b, 2-b, 3-b, 4-c, 5-b, 6-b, 7-c, 8-c.

## 20. Flashcards
- **Q: Why multiplex?** → **A:** One expensive channel serves many users; per-user demand is far below channel capacity.
- **Q: FDM vs TDM vs STDM?** → **A:** FDM = frequency bands; TDM = fixed time slots; STDM = on-demand slots (packets).
- **Q: What is DWDM?** → **A:** 80-160 wavelengths on one fiber → tens of Tbps.
- **Q: How does CDMA separate users?** → **A:** Orthogonal spreading codes; correlate to decode; near-far problem via power control.
- **Q: Circuit vs packet switching?** → **A:** Circuit reserves a path (deterministic, wasteful for bursts); packet statistically shares (efficient, lossy).
- **Q: What composes packet delay?** → **A:** Transmission + propagation + queueing + processing, per hop (store-and-forward).
- **Q: Why can DC spines be oversubscribed?** → **A:** Statistical multiplexing — average, not peak, demand fits; risk is correlated bursts.

## 21. Revision
Multiplexing shares one channel: FDM (fixed frequency bands + guard bands), WDM (FDM on fiber → tens of Tbps), TDM (fixed time slots), statistical TDM (on-demand slots → packet switching), CDMA (orthogonal codes, 3G/GPS), OFDMA (orthogonal subcarriers + scheduling, 4G/5G/WiFi 6). Switching connects flows: circuit switching reserves a dedicated path (deterministic QoS, wasteful for bursts — phone), packet switching statistically shares (efficient, lossy, robust — Internet). Packet delay = transmission (L/R) + propagation + queueing + processing per hop; store-and-forward adds L/R each hop. Multiplexing gain enables oversubscription (DC spines 4:1) but correlated load overflows queues — the reason TCP congestion control exists. MPLS puts virtual-circuit labels in the packet core. Anchor: *multiplexing = lanes on one highway; switching = how cities connect — and data's burstiness chose statistical sharing.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is multiplexing and why?" | 13-Q1 / 1 |
| "FDM vs TDM vs statistical TDM" | 13-Q2 |
| "What is WDM/DWDM?" | 13-Q3 |
| "How does CDMA separate users?" | 13-Q4 |
| "Guaranteed rates under FDM/TDM" | 13-Q5 / 8 |
| "Why packet-switched and not circuit?" | 13-Q6 / 4 |
| "Components of packet-switch delay" | 13-Q7 |
| "When is circuit switching still right?" | 13-Q8 |
| "Oversubscription / statistical gain" | 13-Q9,16 |
| "OFDMA vs FDM / why 4G-5G adopted it" | 13-Q10,15 |
| "What is a virtual circuit / MPLS?" | 13-Q12 / 14-Q2 |
