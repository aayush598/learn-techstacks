# Bandwidth, Throughput, and Latency

> **TL;DR**: Bandwidth is a channel's theoretical capacity (Hz or max bps), throughput is what a workload actually achieves, and latency is the time data takes to travel — four components (transmission, propagation, queueing, processing) — and the two are linked by the bandwidth-delay product, the amount of "data in flight" a pipe can hold.

## 1. Why Does This Exist?
Every network decision — "is 100 Gbps enough?", "why is my app slow?", "can I serve this many users?" — reduces to two numbers: *how much can the pipe carry* (bandwidth/capacity) and *how long does it take* (latency). But these get conflated constantly: people say "bandwidth is slow" when they mean latency, or expect a bigger pipe to fix a propagation-delay problem (it can't). This section exists to give precise, quantitative definitions and the models that connect them: throughput as the achieved rate, latency as the sum of four components, and the bandwidth-delay product as the pipe's "content." Every FAANG systems-design answer (load balancing, caches, streaming, DB replication) depends on getting these right.

## 2. How Does It Work?
**Bandwidth** (capacity, C) = the theoretical maximum bit rate the channel supports (bps), itself derived from Nyquist/Shannon (Sections 01-02): C = B·log₂(1+SNR). **Throughput** (R) = the achieved rate for a specific flow, which can be lower due to overhead, congestion, protocol inefficiency, or small windows (R ≤ C). **Goodput** = throughput minus protocol overhead (retransmissions, headers). **Latency** = total delay = **transmission** (L/R — pushing the bits onto the wire) + **propagation** (d/v — bits already on the wire, at ~2/3 c) + **queueing** (waiting in buffers) + **processing** (lookups). The **bandwidth-delay product** (BDP) = C × RTT — the bits in flight in a full pipe; a window smaller than BDP underutilizes (Part 05's flow-control section) and TCP must be window-sized ≥ BDP.

## 3. When Is It Used?
- **Capacity planning**: sizing links (WAN, DC fabric) from workload bandwidth; oversubscription ratios.
- **Performance debugging**: "slow" apps — is it latency (propagation/queueing) or bandwidth (throughput)? Tools: `ping`, `traceroute`, `iperf3`, `ss -tin`, `iftop`.
- **TCP tuning**: window size ≥ BDP for high-BDP links (1000+ km, 100 Gbps); the reason `rwnd`/`cwnd` matter.
- **Streaming/gaming/voice**: latency-sensitive (each ms matters), bandwidth moderate — QoS design targets queueing delay.
- **Data transfer**: bandwidth-bound (large files) vs latency-bound (small messages, RPCs) — the model that decides caching vs CDN vs replication strategy.
- **BGP/metrics**: OSPF/EIGRP metrics encode delay/bandwidth — the same concepts in routing.

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: treat "speed" as one number.* The entire point of splitting bandwidth vs latency is that they're *independent*: doubling bandwidth doesn't reduce propagation (light speed is fixed); shortening distance doesn't increase throughput. Conflating them misleads design (buying a bigger pipe for an RPC-latency problem fails).
- *Alternative: only measure theoretical capacity.* Capacity (Shannon/Nyquist) is the *ceiling*; real systems sit below it (headers, retransmissions, congestion, protocol overhead), so you need *throughput* and *goodput* as achieved measures.
- *Alternative: model latency as single "delay."* Then you can't explain why a 1-byte ping across a 3000-mile link takes ~25 ms (propagation) nor why a full pipe adds queueing delay. The four-component split is what makes latency *debuggable*.
- *Alternative: ignore BDP.* Then you can't explain why a TCP window of 64 KB underutilizes a 10 Gbps × 100 ms pipe (BDP = 125 MB) — the bandwidth-delay product is the missing link between capacity and achievable throughput.

## 5. Intuition
Bandwidth is the **width of a highway**; latency is the **distance between cities**. A wider highway carries more cars per second (throughput), but it doesn't make the drive shorter. If the cities are 3000 km apart, even a 1000-lane highway takes 10+ ms just to drive the distance (propagation). "How many cars are on the highway at once" = bandwidth × travel time = **bandwidth-delay product**. If the traffic light (TCP window) only lets 10 cars enter before you have to stop, a 1000-lane highway is pointless — you need a window as wide as the highway times the travel time (BDP).

## 6. Real-World Analogy
Think of **a water pipeline delivering oil to a refinery 1000 km away**. Bandwidth = pipe diameter (liters/sec capacity). Throughput = what you actually deliver (may be less if the pump is weak, or the refinery is slow to accept). Latency = the time the *first* drop takes to arrive (1000 km of pipe at whatever flow speed) — almost entirely distance, not diameter. The pipe's *content* (all the oil already in transit) = diameter × travel time = BDP. If your order-in system (window) only fills a tiny amount before waiting for confirmation, the big pipe sits empty.

## 7. Formal Definition
- **Bandwidth / capacity**: C (bps) = max bit rate the channel can carry; Shannon C = B·log₂(1+SNR); Nyquist caps symbol rate. Distinguish from *spectral bandwidth* (Hz).
- **Throughput**: R = achieved bit rate of a flow over time; instantaneous or average; R ≤ min(C, bottleneck link, window/RTT).
- **Goodput**: application-level bits/sec = throughput minus retransmissions/headers.
- **Latency / delay**: T = T_trans + T_prop + T_queue + T_proc, where T_trans = L/R (bits÷rate), T_prop = d/v (distance÷speed, ~0.66c in fiber/copper, c in vacuum), T_queue = buffer wait, T_proc = node processing. **RTT** ≈ 2× one-way latency.
- **Bandwidth-delay product**: BDP = C × RTT (bits) — the amount of in-flight data in a fully utilized pipe; the minimum window (bits) for full utilization.

## 8. Example
A **100 Mbps link over 5000 km fiber** (v = 2×10⁸ m/s in fiber):
- T_trans for a 1 MB file: 8×10⁶ / 10⁸ = **80 ms**.
- T_prop: 5×10⁶ / 2×10⁸ = **25 ms** one-way → RTT ≈ **50 ms**.
- One-way latency = 80 ms (trans) + 25 ms (prop) + queueing + processing ≈ **~105 ms + queue**.
- BDP = 100 Mbps × 0.05 s = **5×10⁶ bits = 625 KB** — a TCP window must be ≥ 625 KB to saturate the pipe; the default 64 KB window gives only ~64 KB/625 KB = **10% utilization** (unless window scaling).
- If you double bandwidth to 200 Mbps, propagation stays 25 ms (nothing changes for latency); throughput only doubles if the window ≥ BDP (=1.25 MB now).

## 9. Internal Working
1. **Transmission delay** grows linearly with packet size (L/R) — the "time to shove bits out."
2. **Propagation delay** is distance-bound (d/v) — can't be improved by hardware; this is why GEO satellites add 240-280 ms RTT and why CDNs cache *near* users.
3. **Queueing delay** appears under load: arrival rate > service rate → buffers grow → delay and (if full) loss; bufferbloat = too-deep buffers → huge queueing delay; Active Queue Management (AQM, CoDel) bounds it.
4. **Processing delay**: forwarding lookups, FCS checks — small but real per hop; TSO/GRO and hardware offloads shrink it.
5. **Throughput ceiling**: R ≤ min over the path of (bottleneck link C, receiver window/RTT). The "narrowest link" and the "window" jointly cap throughput — the formula every TCP tuning problem uses.
6. **Measuring**: `iperf3` measures throughput directly; `ping` RTT measures propagation+queueing (minus trans for tiny packets); `traceroute` exposes per-hop latency; `ss -tin` shows cwnd/rwnd/RTT estimates.

## 10. Time Complexity / Performance Math
- Throughput = min(bottleneck C, window/RTT); for a single flow on an otherwise idle path: R ≈ min(C, W/RTT).
- Latency = L/R + d/v + T_q + T_proc (per hop); end-to-end = Σ hops.
- BDP = C × RTT — the sizing formula: window (bits) = BDP; if W < BDP, utilization = W/BDP.
- Transfer time of a file of size S over RTT τ with window W: ≈ τ + S/min(C, W/τ) (roughly, ignoring ramp).
- "1-byte vs 1-GB question": small messages are latency-dominated; large files are bandwidth-dominated — the boundary is ~BDP bytes.

## 11. Advantages
- **Precise vocabulary** separates "slow network" causes (bandwidth vs latency) — the difference between buying fiber and adding caching.
- **Debuggable**: each delay component maps to a fix (bigger pipe, shorter path/edge placement, better buffers/AQM, faster hardware/offloads).
- **Quantitative design**: BDP sizes TCP windows; throughput formula sizes links and CDNs; latency model sizes geographic replication.
- **Universal**: applies to every layer — L1 (medium), L4 (TCP window), L7 (app RPC).
- **Simple, testable**: `iperf3`, `ping`, `traceroute` validate the model instantly.

## 12. Disadvantages
- **Models hide details**: queueing is stochastic (bursts vary); real throughput is dynamic (congestion, reordering).
- **Unit confusion is common**: bits vs bytes, Mbps vs MB/s, dB — the traps that cost interview marks.
- **BDP formula assumes clean pipe**: with loss, TCP's effective throughput is capped by the loss-rate formula (~MSS / (RTT·√p)) — bandwidth alone isn't the ceiling.
- **Latency components interact**: queueing depends on throughput; you can't always decompose cleanly.
- **Hard to measure precisely**: `ping` shows RTT not one-way; clocks skew; jitter adds noise.

## 13. Interview Questions
1. **Q: What's the difference between bandwidth, throughput, and goodput?** A: Bandwidth = theoretical max capacity (Shannon). Throughput = achieved bit rate (≤ bandwidth, affected by congestion/protocol). Goodput = application-useful rate (throughput minus headers/retransmissions). Bandwidth is the ceiling; throughput is reality; goodput is what the app feels.

2. **Q: What are the four components of latency?** A: Transmission (L/R — pushing bits out), propagation (d/v — bits on the wire, ~0.66c in fiber), queueing (buffer wait under load), processing (lookup/forward). Total one-way latency = sum; RTT ≈ 2×.

3. **Q: Compute the latency of a 1 MB file over a 100 Mbps, 5000 km fiber link.** A: Transmission = 8e6/1e8 = 80 ms; propagation = 5e6/2e8 = 25 ms one-way (RTT 50 ms); total ≈ 105 ms + queueing + processing. The key insight: propagation (25 ms) is *distance*, unchanged by bandwidth.

4. **Q: Why can't you fix latency by adding bandwidth?** A: Propagation is distance-bound (d/v — light speed in the medium). Doubling bandwidth only shrinks transmission delay (L/R), not propagation. On short RTTs, transmission dominates; on long RTTs, propagation dominates — and adding bandwidth helps only the former.

5. **Q: What is the bandwidth-delay product and why does it matter for TCP?** A: BDP = C × RTT — the bits a full pipe holds in flight. TCP's window (cwnd × rwnd) must be ≥ BDP to saturate; a smaller window underutilizes. Example: 10 Gbps × 100 ms = 125 MB → a 64 KB window uses <0.05% of the pipe.

6. **Q: A 1 Gbps, 200 ms RTT link: what TCP window (bytes) is needed for full utilization?** A: BDP = 1e9 × 0.2 = 2e8 bits = **25 MB**. With 64 KB segments/window scaling, the effective window = min(rwnd, cwnd); you need ≥ 25 MB via window scaling and a big rwnd.

7. **Q: TRICKY — A 1-byte RPC takes 50 ms but the link is 100 Gbps. Is it bandwidth-bound or latency-bound?** A: Latency-bound — 1 byte has ~0 transmission time; the 50 ms is mostly propagation + RTT (plus queueing). No bandwidth increase helps. This is why microservices optimize *round trips*, not pipes.

8. **Q: SCENARIO — Users in NYC and SF complain about slow transfers from a server in London. What do you measure?** A: RTT (ping — expect ~70-80 ms transatlantic), throughput (iperf3), and per-hop delay (traceroute). If RTT is high and throughput is below expected, check BDP window sizing, then consider CDN/edge or closer replica. The fix depends on *which* component dominates.

9. **Q: What is bufferbloat and how does it affect latency?** A: Deep buffers absorb bursts but introduce huge queueing delay under sustained load — latency spikes to seconds while throughput looks fine. Fixed with AQM (CoDel/fq_codel, BBR) that keeps queues short. It's a *queueing-delay* pathology.

10. **Q: PRODUCTION — `iperf3` shows 9 Gbps but your app gets 3 Gbps. Where did the difference go?** A: Throughput ≠ goodput: protocol overhead (headers, ACKs), retransmissions, per-connection limits, TLS overhead, small message sizes (underutilizing window), or server CPU/disk. iperf3 measures raw TCP; your app measures application semantics — the delta is the layers in between.

11. **Q: What is the throughput formula for TCP over a lossy link?** A: For a single flow: R ≈ 1.22·MSS / (RTT·√p) (Mathis formula) — throughput falls as 1/√(loss rate). Loss, not just bandwidth, caps TCP — the reason high-BDP lossy links need TCP variants (CUBIC/BBR).

12. **Q: What is the relationship between RTT and achievable throughput?** A: Throughput ≤ window/RTT (and ≤ bandwidth). Halving RTT doubles achievable throughput at the same window; that's why CDNs place servers *geographically near* users (shorter RTT) and why congestion avoidance grows the window toward BDP.

13. **Q: TRICKY — Two links: 1 Gbps/10 ms and 100 Mbps/1 ms. Which has the higher BDP?** A: BDP₁ = 1e9 × 0.01 = 10 Mb; BDP₂ = 1e8 × 0.001 = 0.1 Mb. The fast-long link has 100× the in-flight capacity — its window must be 100× bigger even though RTT is higher. BDP, not RTT alone, sizes windows.

14. **Q: What's the difference between throughput and goodput in the context of retransmissions?** A: Throughput = all bits across the link (including retransmitted ones); goodput = unique application bits. A 50% retransmission rate gives goodput = half the throughput — TCP SACK/selective repeat (Part 05) directly improves goodput.

15. **Q: SCENARIO — A satellite link (250 ms RTT) at 1 Mbps streaming video. What's the fundamental limit?** A: Propagation alone is 250 ms one-way → 500 ms RTT; BDP = 1e6 × 0.5 = 62.5 KB. The pipe is small *in bits*; the problem is latency (interactive apps die) and window sizing for throughput. FEC (Part 05) beats retransmission on such links.

16. **Q: What is the "slow start" effect on throughput of a new TCP flow?** A: cwnd grows 1 → 2 → 4 → ... each RTT (exponential), so throughput ramps toward BDP/RTT. For a big BDP, ramp-up takes many RTTs — that's why short flows never reach line rate and why BBR/slower-start variants exist.

17. **Q: What is jitter and which component of latency creates it?** A: Jitter = variance in delay, caused almost entirely by *queueing* (variable buffer wait under changing load). Transmission/propagation/processing are nearly constant. Voice/video care about jitter (smooth playback) → QoS/jitter buffers.

18. **Q: PRODUCTION — You must choose: cache at the edge (cut RTT 50→5 ms) or upgrade the WAN (10→40 Gbps). Which for a chat app vs a video store?** A: Chat = latency-bound (many tiny messages) → edge/caching wins. Video store = bandwidth-bound (large files) → WAN upgrade wins. This is exactly the latency-vs-bandwidth analysis; the answer is "it depends on message size and RTT dominance."

## 14. Follow-Up Questions
1. **Q: Why is propagation speed in fiber ~2/3 c and not c?** A: The refractive index n ≈ 1.5 slows light: v = c/n ≈ 2×10⁸ m/s. Copper is similar (~0.6-0.7c) due to dielectric. In vacuum (satellite) it's c — which is why satellite RTTs are ~500 ms.

2. **Q: How do you estimate throughput from a packet capture?** A: Sum payload bytes over the capture window (goodput), or all bytes including headers (throughput); `tshark -qz io,stat` and `iperf3` report both; retransmission counts (`tcp.analysis.retransmission`) explain the gap.

3. **Q: What is the difference between RTT and one-way latency?** A: RTT = send→ack (≈ 2× one-way + server processing); one-way = source→destination. Clock asymmetry makes one-way measurement hard (needs NTP/PTP sync); RTT needs no sync.

4. **Q: How does BDP relate to memory/CPU costs?** A: A window = BDP means the sender holds BDP bytes in buffers and does BDP/RTT-ish processing; 100 Gbps × 100 ms = 1.25 GB of buffered data per flow — a real cost that motivates BBR and offloads.

## 15. Coding Example
```python
import math

C = 299792458.0

def prop_delay(distance_km, medium="fiber", v_factor=None):
    v = v_factor or {"fiber": 0.66, "copper": 0.6, "vacuum": 1.0, "fiber-0.66": 0.66}[medium]
    return (distance_km * 1000) / (v * C)

def trans_delay(bits, rate_bps):
    return bits / rate_bps

def bdp(rate_bps, rtt_s):
    return rate_bps * rtt_s

def tcp_throughput_lossy(mss_bytes, rtt_s, loss_p):
    return 1.22 * mss_bytes * 8 / (rtt_s * math.sqrt(loss_p))

link = dict(rate=100e6, km=5000)
tt = trans_delay(8e6, link["rate"])
tp = prop_delay(link["km"])
print(f"trans={tt*1e3:.1f}ms prop={tp*1e3:.1f}ms one-way={1000*(tt+tp):.1f}ms")
print(f"BDP(100Mbps,50ms) = {bdp(100e6,0.05)/8/1024:.1f} KB")
print(f"TCP @1Gbps,80ms,0.1% loss = {tcp_throughput_lossy(1500,0.08,1e-3)/1e6:.1f} Mbps")
```
```python
# Latency vs bandwidth: which dominates for a given message size?
def dominant_component(size_bytes, rate_bps, rtt_s):
    trans = size_bytes * 8 / rate_bps
    return "latency(RTT)" if trans < rtt_s * 0.5 else "bandwidth(trans)"
for sz in [100, 100_000, 100_000_000]:
    print(f"{sz} B -> {dominant_component(sz, 1e9, 0.08)}")
```
```bash
# Measure the real numbers
ping -c 10 <host>                       # RTT distribution (min/avg/max, jitter)
iperf3 -c <host> -t 10                  # raw TCP throughput (server: iperf3 -s)
iperf3 -c <host> -u -b 100M -t 10       # UDP throughput (loss reveals queueing)
traceroute -n <host>                    # per-hop propagation+queueing
ss -tin | head -5                       # cwnd/rwnd/RTT/retrans per connection
cat /proc/net/tcp | head                # kernel TCP state
ip route show | head -3                 # rtt/2 estimate per destination
```

## 16. Industry Usage
- **Cloud/CDN**: CDNs exist to shrink *latency* (propagation) by caching at the edge; WAN upgrades address *bandwidth*. The distinction is the core of edge-computing economics.
- **Data centers**: BDP sizing for 100-400G links (window scaling, DCTCP/BBR); lossless Ethernet (PFC) keeps queueing loss near zero; latency-critical AI training uses RDMA/RoCE to cut processing+queueing.
- **TCP stack (Linux)**: CUBIC (default), BBR (Google, YouTube) — designed around BDP and queueing; `net.ipv4.tcp_wmem/rmem` sized to BDP.
- **Streaming/real-time**: WebRTC, cloud gaming, voice — jitter buffers, QoS, and edge placement all combat queueing+propagation.
- **Observability**: Datadog/New Relic/SignalFx split latency into network/application; `iperf3`-based WAN tests are standard for "is it the WAN?" questions.
- **Global load balancing (Part 08)**: anycast/geo-DNS pick the *lowest-latency* replica — the production application of the propagation model.

## 17. References
- Kurose & Ross, *Computer Networking*, 8th ed., §1.4-1.5 (Delay, Throughput, Latency).
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §2.2 (Bandwidth and Latency).
- Mathis et al., "The Macroscopic Behavior of the TCP Congestion Avoidance Algorithm," CCR 1997 (throughput vs loss).
- RFC 3649 (HighSpeed TCP — BDP motivation) — https://datatracker.ietf.org/doc/html/rfc3649
- RFC 7323 (TCP Window Scaling — BDP enablement) — https://datatracker.ietf.org/doc/html/rfc7323
- `iperf3` documentation — https://iperf.fr/ ; `ss(8)` man page — https://man7.org/linux/man-pages/man8/ss.8.html

## 18. Cheat Sheet
- Bandwidth = capacity (Shannon/Nyquist); throughput ≤ bandwidth; goodput = app-useful rate.
- Latency = T_trans (L/R) + T_prop (d/v, ~0.66c fiber) + T_queue + T_proc.
- RTT ≈ 2 × one-way latency.
- Propagation is distance-bound: can't fix with bandwidth. 1000 km fiber ≈ 7.6 ms one-way.
- BDP = C × RTT (bits) — data in flight; TCP window must be ≥ BDP.
- 10 Gbps × 100 ms → BDP = 125 MB; default 64 KB window = <0.05% utilization.
- Throughput ≤ min(bottleneck C, window/RTT).
- TCP over loss: R ≈ 1.22·MSS/(RTT·√p) (Mathis).
- Small messages = latency-bound; large files = bandwidth-bound (boundary ≈ BDP).
- Bufferbloat = queueing delay from deep buffers; fix with AQM/BBR.
- Tools: `ping` (RTT), `iperf3` (throughput), `traceroute` (per-hop), `ss -tin` (TCP).

## 19. Quiz
1. Propagation delay over 1000 km fiber ≈: a) 5 ms b) 7.6 ms c) 0.5 ms d) 33 ms → **b**
2. A 1 MB file over 100 Mbps: transmission time ≈: a) 8 ms b) 80 ms c) 8 µs d) 1 s → **b**
3. BDP for 1 Gbps, 100 ms: a) 12.5 MB b) 125 MB c) 1.25 MB d) 1.25 GB → **a**
4. Which can't be reduced by more bandwidth? a) transmission b) propagation c) queueing d) processing → **b**
5. Throughput is bounded by: a) bandwidth only b) min(bottleneck, window/RTT) c) RTT only d) packet size → **b**
6. Bufferbloat adds mostly: a) propagation b) transmission c) queueing delay d) processing → **c**
7. TCP throughput scales with loss as: a) 1/p b) 1/√p c) √p d) p → **b**
8. A 10 Gbps link, 50 ms RTT — window for full utilization: a) 62.5 KB b) 62.5 MB c) 6.25 MB d) 625 KB → **b**

**Answers**: 1-b, 2-b, 3-a, 4-b, 5-b, 6-c, 7-b, 8-b.

## 20. Flashcards
- **Q: Bandwidth vs throughput vs goodput?** → **A:** Capacity (ceiling) vs achieved rate vs app-useful rate.
- **Q: Four latency components?** → **A:** Transmission (L/R), propagation (d/v), queueing, processing.
- **Q: Why can't bandwidth fix latency?** → **A:** Propagation is distance-bound (light speed in media) — independent of bandwidth.
- **Q: What is BDP and why does TCP care?** → **A:** C×RTT, the in-flight data; window < BDP underutilizes (64 KB vs 125 MB example).
- **Q: Throughput ceiling formula?** → **A:** min(bottleneck bandwidth, window/RTT).
- **Q: What is bufferbloat?** → **A:** Deep buffers → huge queueing delay under load; AQM/BBR fix it.
- **Q: Small message vs large file — what dominates?** → **A:** Latency for small, bandwidth for large (boundary ≈ BDP).

## 21. Revision
Bandwidth = theoretical capacity; throughput = achieved; goodput = app-useful. Latency = transmission (L/R) + propagation (d/v, ~0.66c in fiber → 7.6 ms per 1000 km) + queueing (bufferbloat risk) + processing. Propagation is distance-bound and immune to bandwidth — the source of the "can't buy latency" truth. The bandwidth-delay product (C×RTT) is the in-flight capacity: 10 Gbps×100 ms = 125 MB, so a 64 KB TCP window is worthless without scaling; throughput ≤ min(bottleneck C, window/RTT) and over lossy links ≈ 1.22·MSS/(RTT·√p). Small messages are latency-bound, large files bandwidth-bound. Tools: `ping` (RTT), `iperf3` (throughput), `traceroute` (per-hop), `ss -tin` (cwnd/rwnd). Anchor: *bandwidth = pipe width, latency = distance, BDP = water in the pipe.*

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Bandwidth vs throughput vs goodput" | 13-Q1 / 7 |
| "Four components of latency" | 13-Q2 |
| "Compute latency of a transfer" | 8 / 13-Q3 |
| "Why can't bandwidth fix latency?" | 13-Q4 |
| "What is BDP / size the TCP window" | 13-Q5,6,13 |
| "Small RPC slow on a fast link — why?" | 13-Q7 |
| "TCP throughput vs loss rate" | 13-Q11 |
| "Bufferbloat / queueing delay" | 13-Q9 |
| "iPerf vs app throughput gap" | 13-Q10 |
| "Edge cache vs WAN upgrade — which?" | 13-Q18 |
