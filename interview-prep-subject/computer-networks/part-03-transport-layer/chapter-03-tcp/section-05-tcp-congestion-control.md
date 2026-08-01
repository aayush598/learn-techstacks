# TCP Congestion Control

> **TL;DR**: Congestion control is the sender's self-imposed throttle that keeps TCP from overloading the **network** (vs flow control's receiver-side throttle). It manages a sender-side **cwnd** via **slow start** (exponential ramp to ssthresh), **congestion avoidance** (linear AIMD), and **fast recovery** (halve on loss) — with Reno/NewReno/CUBIC/BBR as the algorithm generations that made modern line-rate, fair, and stable.

## 1. Why Does This Exist?
The Internet has no central traffic coordinator — millions of senders share bottleneck links (a router queue here, a radio tower there), and none of them knows the network's capacity. If everyone sent at full blast, router buffers would overflow, packets drop, and the network collapses into *congestion collapse* (the 1986 Internet meltdown that birthed the field). TCP congestion control exists to make each sender **probe** the network's available capacity, **adapt** to it, and **share it fairly** — without any signaling from the routers (until ECN). It's a distributed, end-to-end algorithm: observe loss or delay → infer congestion → back off. Without it, the Internet would thrash at a tiny fraction of capacity. It's also the single most consequential "system design" in networking — the algorithms that get asked about in FAANG interviews *are* the algorithm of the Internet.

## 2. How Does It Work?
- **cwnd (congestion window)**: sender-side byte budget (unacked bytes allowed), *separate* from rwnd. Effective send window = `min(rwnd, cwnd)`. Doubling cwnd doubles throughput — hence "window is speed."
- **Slow start**: begin at cwnd ≈ 1-10 segments (or IW=10, RFC 6928). Each ACK adds 1 MSS → cwnd **doubles per RTT** (exponential). Until ssthresh (~initial 64 KB or set by loss).
- **Congestion avoidance (AIMD)**: after ssthresh, add ~1 MSS per RTT (**linear** growth, additive increase) to probe gently.
- **On loss (Reno/NewReno)**: a timeout → cwnd = 1 (restart slow start), ssthresh = cwnd/2; 3 duplicate ACKs → **fast retransmit** + **fast recovery** → cwnd = ssthresh = cwnd/2 (multiplicative decrease). The classic "additive increase, multiplicative decrease" (AIMD) sawtooth.
- **CUBIC**: after a loss, grow cwnd with a cubic function of time — aggressive ramp on fast links, gentle near the known target, and delay-independent (wins on long fat pipes; default in Linux since 2.6.19).
- **BBR**: model *bandwidth × RTT* directly (estimates bottleneck bandwidth and RTT from pacing probes) instead of reacting to loss — targets the full BDP, keeps queues low, avoids bufferbloat, and works on lossy/cellular links.
- **TCP-friendly**: a non-TCP flow that doesn't back off would starve TCP; RFC 5681-style AIMD keeps flows *fair* (each gets ~1/n of the bottleneck).

## 3. When Is It Used?
- **Every TCP connection, always**: cwnd ramps on every new connection (that's why the first ~1 MB of a download is "slow" — slow start).
- **High-BDP WANs**: CUBIC/BBR are the difference between 200 Mbps and 8 Gbps on 100 ms links — default kernels pick per-connection algorithms.
- **Lossy/cellular/mobile**: BBR's loss-tolerance makes it shine (random loss isn't misread as congestion); CUBIC still used where loss-based AIMD is fine.
- **Datacenters**: DCTCP/DCQCN use ECN for microsecond-scale congestion signals — the "congestion control" of the modern fabric.
- **Bufferbloat**: AQM (fq_codel, cake) + BBR/CAKE combats router-buffer latency inflation — a congestion-control-adjacent war fought in home routers and CDNs.
- **Debugging throughput**: `ss -tin` shows `cwnd`, `ssthresh`, `pacing_rate`, `rtt` — the visible outputs of the algorithm.

## 4. Why Wasn't Another Approach Chosen?
- **Why not reserve bandwidth (like ATM's CBR)?** Requires network support/state and unused reservation (expensive). The Internet chose *stateless, end-to-end* adaptation: the network just drops/marks, senders adapt. Zero signaling, maximal robustness, trivial deployment — that's why it won.
- **Why not explicit per-flow signaling?** ECN exists (mark instead of drop) and is supported, but *drop-based* probing works on legacy routers with no changes — the algorithm had to work on 1988's hardware. ECN is a graceful upgrade, not a requirement.
- **Why multiplicative decrease (halve) instead of gentle ramp?** Because a congested network must be relieved *quickly*; cutting in half is aggressive enough to unclog the bottleneck in one RTT. Gentle decrease would prolong congestion.
- **Why additive increase?** To probe for the real capacity: add 1 MSS/RTT, so you approach the ceiling without overshooting; and AIMD is *provably fair* across flows sharing a link (each converges to equal share).
- **Why exponential slow start?** Because the sender starts with *no* knowledge of the path — exponential is the fastest safe way to discover the ceiling (reach ~1/2 capacity in log(capacity) RTTs). Once ssthresh is known, switch to linear.
- **Why react to loss at all (vs delay)?** Loss is a *hard, universal* signal available everywhere (TCP RTO/dup ACKs). Delay signals (Vegas, BBR) are richer but need RTT noise-tolerant inference. Loss-based won on deployability; BBR adds the delay dimension *on top*.

## 5. Intuition
Picture **a flock of birds exploring an unknown feeding ground** — each bird is a connection. They start cautiously (a few birds — slow start) but when food is plentiful (no loss) they double the flock *every minute* (exponential). When they see a few birds collide with a window pane (a dropped packet), they cut the flock *in half* instantly (multiplicative decrease) and then grow it slowly and carefully, one bird per minute (additive increase), forever saw-toothing around the true capacity. CUBIC is the flock that, after a collision, *remembers* the pane's location and rushes back to just below it quickly, then eases in gently. BBR is the flock that stops counting collisions entirely and instead *watches how long food takes to arrive* — measuring the true speed of the wind and the distance — so it flies at exactly the sustainable speed with no window crashes. All of them share one goal: use the whole field, never break the glass.

## 6. Real-World Analogy
**A highway on-ramp with no traffic lights**: Drivers (senders) can't see the highway's capacity, only the consequences. If too many enter, the highway gridlocks (buffers fill → drops). The TCP rule: start by sending a *few* cars, and if the highway keeps absorbing them, *double* the number each second until you sense trouble (a car you sent never arrived / an echo of "too many" comes back). Then **halve** the flow instantly and creep back up one car per second — forever saw-toothing around the highway's true capacity. Rivals who "just gun it" (non-AIMD flows) eventually jam everyone, so the fair rule is enforced by everyone backing off together — that's how 1M flows share one bottleneck without talking to each other. CUBIC/BBR are the drivers who learned the highway's *max sustainable speed* by feel (BBR) instead of always crashing into the limit (Reno).

## 7. Formal Definition
TCP congestion control (RFC 5681; CUBIC: RFC 9438; BBR: draft-cardwell-cc-bbr) is the sender-side algorithm governing `cwnd` (congestion window, in MSS/bytes). States: **Slow Start** — cwnd += MSS per ACK (doubles per RTT) until ssthresh or loss; **Congestion Avoidance** — cwnd += MSS²/cwnd per ACK (≈1 MSS/RTT); on **loss event**: timeout → cwnd = 1 MSS, ssthresh = max(2×MSS, cwnd/2); 3 duplicate ACKs → fast retransmit, fast recovery, cwnd = ssthresh = cwnd/2. Effective window = min(cwnd, rwnd). Fairness: N AIMD flows converge to ~equal bottleneck share; efficiency: each flow fills its BDP share. CUBIC uses a cubic window-growth function in time since last loss; BBR estimates bottleneck bandwidth (max_filtered pacing rate) and min-RTT and paces at the BDP without relying on loss.

## 8. Example
AIMD sawtooth on a 100 Mbps link, RTT 20 ms, MSS 1460 (numbers):
```
1. IW=10 segments → cwnd=14.6 KB
2. Slow start: 14.6 → 29.2 → 58.4 → 116.8 KB (2× per RTT)
   After ~4 RTTs, cwnd ≈ 1 MB, ssthresh=512 KB exceeded → congestion avoidance
3. AIMD: +1 MSS/RTT → 512 KB + 1.4 KB/RTT ...
   In ~350 RTTs (7 s) cwnd grows to ~1 MB
4. Link saturates → queue fills → drop → 3 DUPACKs
   → cwnd = 1 MB/2 = 512 KB, ssthresh = 512 KB (fast recovery)
5. Repeat: linear grow → loss → halve → sawtooth around 1 MB
Throughput ~ 1 MB / 20 ms ≈ 50 MB/s ≈ 400 Mbps peak, ~75% average on this link.
```
Why it works: exponential start finds the ceiling fast; linear + halve keeps us at ~75% utilization while never *staying* overloaded — the "sawtooth" is the algorithm's fingerprint in every bandwidth graph.

## 9. Internal Working
1. **cwnd = 0 init**: at connection start, cwnd = IW (RFC 6928: 10 MSS), ssthresh = high (64 KB+). Each segment's *first* data burst is capped by cwnd.
2. **ACK-driven growth**: every ACK increments a counter; in slow start, cwnd += MSS per ACK; in congestion avoidance, cwnd += MSS×MSS/cwnd (≈1 MSS per RTT). The kernel recomputes on every ACK — O(1) per ACK.
3. **Loss detection**: RTO (retransmission timeout) for a missing ACK; 3 duplicate ACKs trigger *fast retransmit* (resend immediately, don't wait for RTO).
4. **Fast recovery (NewReno)**: on 3 DUPACKs, cwnd = cwnd/2, ssthresh = cwnd/2; the sender keeps sending while DUPACKs arrive (window inflated by DUPACK count) — pipe stays full during recovery.
5. **RTO**: timeout → cwnd = 1 MSS, ssthresh = cwnd/2 → full slow start. RTO is the "serious" signal (whole window lost); DUPACK is the "partial" signal.
6. **ECN (optional)**: if ECN negotiated, a marked (CE) segment → receiver echoes ECE → sender halves cwnd and sets CWR — same decrease, but *before* an actual drop (no loss incurred).
7. **CUBIC specifics**: window = C×(t − K)³ + Wmax (C≈0.4, K the time to reach Wmax); it "remembers" the last congestion window Wmax and ramps quickly back, then flattens near it — delay-independent, RTT-fair.
8. **BBR specifics**: two estimators — bottleneck bandwidth (BTBW) via max over time of delivery rate, and min-RTT via filtered RTT minimum; it sets cwnd ≈ BDP and paces at ~1.25× BTBW, adapting each RTT (startup, drain, probeBW, probeRTT states). No loss reaction — it *avoids* loss.
9. **Per-flow isolation**: each connection has its own cwnd (per-socket kernel state); sysctls (`tcp_congestion_control`) select the default (cubic) globally; `ss -tin` exposes cwnd/ssthresh/pacing.

## 10. Time Complexity
- **Per-ACK work**: O(1) (increment, compare, maybe halve). The whole algorithm is a few arithmetic ops per ACK.
- **Time-to-probe**: slow start reaches capacity in O(log2(BDP/IW)) RTTs — e.g., 1 GB BDP, IW 10 MSS: ~17 RTTs to discover. This *is* the startup latency tax.
- **Throughput vs loss (the model)**: Mathis equation: `Throughput ≈ MSS×c/(RTT×√p)` (c≈1.22 for Reno) — a 1% loss rate on a 100 ms link caps you at ~1460×1.22/(0.1×0.1) ≈ 178 KB/s. Random loss is the ultimate ceiling; this equation is why "it's not the network" diagnoses matter.
- **Fairness convergence**: AIMD flows converge in O(number of flows / decrease factor) RTTs — practical on real links.
- **Buffer cost**: cwnd growth uses sender buffers (wmem); the algorithm's sawtooth deliberately oscillates around BDP → router queues fill (bufferbloat) unless AQM/BBR.

## 11. Advantages
- **Self-managing, no network support**: works on 1988 routers; ECN is optional. Deployed *everywhere* by default.
- **Stable + fair**: AIMD provably converges; congestion collapse is prevented as long as everyone's TCP.
- **Fast startup**: slow start reaches capacity in ~log(BDP) RTTs — good enough for most downloads.
- **Evolvable**: cwnd math is sender-side only — CUBIC/BBR ship as kernel patches with zero wire changes.
- **Modern speed**: CUBIC handles long-fat pipes; BBR fills BDP with low queueing and tolerates real-world loss.
- **Observable**: `ss -tin` exposes cwnd/ssthresh/pacing for real debugging.

## 12. Disadvantages
- **Loss-based signaling is wrong on lossy links**: any random loss (wifi, cellular, satellite) → AIMD reads it as congestion → needless halving → awful throughput. BBR fixes most of it.
- **Bufferbloat**: AIMD fills queues before detecting loss → latency spikes (100 ms → 1 s+ under load) unless AQM.
- **Slow-start ramp cost**: the first ~1 MB of every connection is at low cwnd; short-lived connections (HTTP/1.1 requests) never leave slow start — hence HTTP/2 multiplexing & TFO.
- **Fairness vs non-TCP**: UDP/QUIC-with-bad-CC can starve TCP; "TCP-friendly" is a promise, not an enforcement.
- **Parameter sensitivity**: ssthresh, initial window, timers, and sysctls must be tuned per environment (DC vs WAN vs mobile) — wrong defaults silently hurt.
- **Head-of-line + throughput coupling**: TCP couples reliability with pacing; losing the retransmission logic also resets pacing — one reason QUIC exists.

## 13. Interview Questions
1. **Q: What is congestion control?** A: The sender-side algorithm that adjusts cwnd so TCP fills available network capacity without overloading it — protecting the *network*, unlike flow control which protects the receiver.
2. **Q (tricky): Difference between cwnd and rwnd?** A: cwnd = sender's congestion window (network capacity probe, kernel algorithm); rwnd = receiver's advertised window (receiver buffer, in the header). Effective = min(cwnd, rwnd).
3. **Q: Describe slow start.** A: cwnd starts at IW (RFC 6928: 10 MSS) and adds 1 MSS per ACK → *doubles every RTT* (exponential) until ssthresh or a loss. It's how TCP discovers the path's capacity fast.
4. **Q: What is AIMD?** A: Additive Increase, Multiplicative Decrease: in congestion avoidance, cwnd grows linearly (+1 MSS/RTT) to probe; on loss it halves. The sawtooth shape; provably fair and stable.
5. **Q (FAANG): What happens on a timeout vs 3 duplicate ACKs?** A: Timeout = whole window lost → cwnd = 1 MSS, ssthresh = cwnd/2, restart slow start (serious). 3 DUPACKs = some lost → *fast retransmit* + *fast recovery* → cwnd = ssthresh = cwnd/2, keep sending (less serious).
6. **Q: What is ssthresh?** A: The slow-start threshold: cwnd grows exponentially below it, linearly above. Set from the initial value or the last loss (cwnd/2).
7. **Q (production): Throughput is low but loss is high. What's the math?** A: Mathis: throughput ≈ MSS×1.22/(RTT×√loss). 1% loss on 100 ms ≈ 178 KB/s. Fix: reduce loss (wifi/cellular quality), lower RTT, or use a loss-tolerant CC (BBR). Loss is the #1 throughput cap.
8. **Q: What is fast retransmit and fast recovery?** A: Fast retransmit = resend on 3 DUPACKs without waiting for the RTO. Fast recovery = keep cwnd at halved value and keep transmitting (window inflation) so the pipe stays full during recovery — avoids a full slow-start restart.
9. **Q: How is TCP fairness achieved?** A: All AIMD flows on a shared bottleneck converge to equal shares: additive increase grows everyone's share equally, multiplicative decrease shrinks big flows more — the equilibrium is equal bandwidth per flow.
10. **Q (tricky): Why does TCP see random loss as congestion?** A: Classic loss-based CC (Reno/CUBIC) treats *any* loss as congestion — it has no way to distinguish wireless corruption from queue overflow. BBR's delay-based estimation avoids this; loss-based CC is the historical compromise for router compatibility.
11. **Q: What is CUBIC and why is it default?** A: A TCP variant using a cubic function in time since the last loss: it ramps aggressively back toward the remembered Wmax on high-BDP links, then flattens — delay-independent, RTT-fair, and best for long fat pipes. Default on Linux since 2.6.19.
12. **Q: What is BBR and how is it different?** A: It estimates the bottleneck *bandwidth* and *min-RTT* (the BDP) and paces at ~1.25× the estimated rate — no loss reaction, no sawtooth, low queueing, works on lossy links. Google's algorithm (2016), now used by Google/YouTube/Cloudflare TCP stacks.
13. **Q (FAANG): What is bufferbloat and how do CC + AQM fight it?** A: Loss-based CC fills router queues before dropping → latency balloons. Fixes: AQM (fq_codel/cake drop early), BBR (targets BDP, keeps queues ~1 BDP), and bigger drop thresholds. Latency-under-load is the metric that matters.
14. **Q: What is the initial window?** A: IW = 10 segments (RFC 6928, up from 2-4 historically) — modern slow start starts faster, cutting the ramp cost for short connections.
15. **Q (tricky): Can congestion control be deployed without kernel changes?** A: Yes — QUIC runs CC in *user space* (its RFC 9002 uses similar AIMD/slow-start logic); that's exactly why QUIC is attractive: new CC algorithms deploy in apps, not kernels. Same math, new home.
16. **Q: What is ECN?** A: Explicit Congestion Notification: routers *mark* packets (CE bit in IP header) instead of dropping; the receiver echoes ECE; the sender halves cwnd and sets CWR. Same decrease, no packet loss — a drop-free congestion signal.
17. **Q (production): `ss -tin` shows `cwnd:10`. What does that mean?** A: The congestion window is 10 segments — slow start just started (IW), so throughput is ramping. Watch it double per RTT until ssthresh, then grow linearly; halving on DUPACKs = congestion events.

## 14. Follow-Up Questions
1. **Q: How does HTTP/2/3 cope with slow start?** A: HTTP/2 multiplexes many requests over one TCP connection → one slow-start ramp serves many transfers (amortized). HTTP/3/QUIC adds 0-RTT and connection migration, and can warm cwnd across requests — cutting the per-request startup tax.
2. **Q: What is DCTCP and when is it used?** A: Datacenter TCP: uses ECN marks at low thresholds to cut cwnd *proportionally* (not halve) — sub-millisecond, high-utilization, low-latency CC for the 1-10 Gbps DC fabric (used in cloud backends). Different regime, different math.
3. **Q (tricky): Why does BBR sometimes show *higher* RTT than CUBIC?** A: BBR fills the pipe to ~1.25× BTBW in probeBW — it *intends* a bounded queue (~1-2 BDP) rather than zero. Its min-RTT estimator is the *base* RTT, not the current one; the added ~1 BDP queueing is the deliberate cost of keeping the bottleneck full.
4. **Q: How do you choose the congestion control algorithm for a workload?** A: WAN/long-fat → CUBIC (default) or BBR; lossy/cellular → BBR; DC latency-sensitive → DCTCP via ECN; small-request latency → any (startup is the issue, not steady-state). `sysctl net.ipv4.tcp_congestion_control` per host, per-connection in some stacks.
5. **Q (FAANG): "Why is my transfer slow from Europe but fast locally?"** A: RTT: throughput ≈ window/RTT — same window, 20× the RTT → 20× less throughput; plus loss (Mathis) and slow-start restarts. The fix is window/CC tuning (BBR or large-window CUBIC) and reducing RTT/ECN.

## 15. Coding Example
```python
# Simulate the cwnd sawtooth (slow start + AIMD) — see the algorithm's fingerprint
import random
MSS, RTT = 1460, 0.02

cwnd, ssthresh = 10 * MSS, 64 * 1024   # IW=10, ssthresh 64 KB
loss_rate = 0.003
t, history = 0.0, []

while t < 10:
    history.append((t, cwnd))
    # each RTT: send cwnd bytes; if ACKed -> grow; else -> halve
    lost = random.random() < (loss_rate * (cwnd / MSS))   # loss prob grows with cwnd
    if lost:
        ssthresh = max(2 * MSS, cwnd // 2)
        cwnd = ssthresh                  # fast recovery halve
    elif cwnd < ssthresh:
        cwnd += MSS                      # slow start: +1 MSS per ACK ~ doubles/RTT
    else:
        cwnd += MSS * MSS // cwnd        # congestion avoidance: ~ +1 MSS per RTT
    t += RTT

import matplotlib.pyplot as plt          # the classic sawtooth
plt.plot([a for a, _ in history], [b for a, b in history])
plt.xlabel("time (s)"); plt.ylabel("cwnd (bytes)"); plt.show()
```
```bash
# Inspect the live congestion state of a connection
$ ss -tin dst 93.184.216.34
#   ... cwnd:22 ssthresh:14 rtt:18.3/0.6 pacing_rate 22.4Mb/s
#   cwnd=22 segments (32 KB), ssthresh=14 → it recently halved → past loss
$ sysctl net.ipv4.tcp_congestion_control    # cubic (default)
$ iperf3 -c host -t 30                      # measure realized throughput vs cwnd math
```

## 16. Industry Usage
- **The Internet itself**: every TCP connection runs *some* CC algorithm — Reno/NewReno (legacy), CUBIC (Linux/Windows/macOS default), BBR (Google-owned + Cloudflare), compound (Windows' hybrid). It's the largest deployed distributed algorithm in history.
- **Cloud throughput engineering (AWS, GCP, Azure)**: documented best practices = CUBIC vs BBR for high-latency transfers, ECN enablement, and window/BDP tuning; "use BBR for lossy/cellular workloads" is standard guidance.
- **Google's network stack**: BBR (draft-cardwell-cc-bbr) runs Google's internal + YouTube + Google Cloud — 2-3× throughput on typical long-distance paths vs CUBIC, per Google's own measurements.
- **CDNs & media (Cloudflare, Akamai, Netflix)**: edge servers tune CC + AQM (fq_codel/cake) — Netflix moved to BBR/ECN for lower latency under load; CDN throughput tests are CC bake-offs.
- **Datacenter fabric (Meta, Alibaba, Google DCs)**: DCTCP/DCQCN/HPCC with ECN at 10-400 Gbps — congestion control at microsecond timescales is a hot research + deployment area.

## 17. References
- RFC 5681 — TCP Congestion Control (Reno/NewReno core): https://www.rfc-editor.org/rfc/rfc5681
- RFC 9438 — CUBIC for Fast Long-Distance Networks: https://www.rfc-editor.org/rfc/rfc9438
- RFC 9002 — QUIC Congestion Control (user-space CC): https://www.rfc-editor.org/rfc/rfc9002
- Jacobson, "Congestion Avoidance and Control" (1988) — the foundational paper.
- Cardwell et al., "BBR: Congestion-Based Congestion Control" (ACM Queue 2016).
- Mathis et al., RFC 3649 / "The macroscopic behavior of the TCP congestion avoidance algorithm."
- Kurose & Ross, *Computer Networking*, Ch. 3 §3.7 (TCP congestion control).

## 18. Cheat Sheet
- cwnd = sender congestion budget; effective window = min(cwnd, rwnd).
- Slow start: ×2/RTT (exp) until ssthresh; cwnd starts at IW=10 MSS (RFC 6928).
- Congestion avoidance: +1 MSS/RTT (AIMD additive).
- Loss: timeout → cwnd=1, ssthresh=cwnd/2, restart SS; 3 DUPACKs → fast retransmit + recovery → cwnd=ssthresh=cwnd/2.
- Mathis: throughput ≈ 1.22×MSS/(RTT×√loss) — loss is the ceiling.
- CUBIC: cubic-in-time ramp; default on Linux; best long-fat.
- BBR: model BDP (BW × minRTT), pace ~1.25×, no loss reaction, low queueing.
- Bufferbloat: AIMD fills queues → AQM (fq_codel/cake) + BBR fix.
- ECN: mark instead of drop; ECE/CWR flags → halve cwnd.
- Fairness: AIMD converges to equal per-flow shares.
- `ss -tin` shows cwnd/ssthresh/pacing_rate; `sysctl tcp_congestion_control`.

## 19. Quiz
1. Congestion control protects: a) receiver b) network c) sender buffer d) CPU → **b**
2. Slow start growth: a) linear b) exponential c) cubic d) none → **b**
3. AIMD decrease on loss: a) halve b) double c) zero d) +1 MSS → **a**
4. 3 DUPACKs trigger: a) RTO b) fast retransmit c) FIN d) reset → **b**
5. ssthresh is set to ___ on loss: a) cwnd/2 b) cwnd c) 1 d) 2×cwnd → **a**
6. Timeout sets cwnd to: a) half b) 1 MSS c) ssthresh d) IW → **b**
7. Default Linux CC: a) Reno b) BBR c) CUBIC d) Vegas → **c**
8. BBR targets: a) loss b) BDP c) ssthresh d) rwnd → **b**
9. Mathis: throughput ∝ a) RTT b) 1/√loss c) loss d) 1/cwnd → **b**
10. ECN uses what instead of drop: a) mark b) RST c) FIN d) ICMP → **a**

## 20. Flashcards
- **Q: Congestion vs flow control?** → **A:** network (cwnd) vs receiver (rwnd); effective = min.
- **Q: Slow start?** → **A:** cwnd doubles per RTT to ssthresh; IW=10 MSS.
- **Q: AIMD?** → **A:** +1 MSS/RTT linear, halve on loss; the sawtooth.
- **Q: Timeout vs 3 DUPACKs?** → **A:** timeout=full restart (cwnd=1); DUPACKs=fast recovery (halve).
- **Q: Mathis equation?** → **A:** T≈1.22×MSS/(RTT×√p); loss caps throughput.
- **Q: CUBIC?** → **A:** cubic-in-time, delay-independent, long-fat winner.
- **Q: BBR?** → **A:** models BDP (BW×minRTT), paces, no loss reaction.
- **Q: Bufferbloat fix?** → **A:** AQM (fq_codel/cake) + BBR + ECN.

## 21. Revision
Congestion control = sender cwnd throttling for the network (vs rwnd for the receiver). Slow start: ×2/RTT from IW=10 MSS to ssthresh. AIMD: +1 MSS/RTT, halve on loss. Timeout → cwnd=1 + restart; 3 DUPACKs → fast retransmit/recovery → halve. Mathis: T≈1.22·MSS/(RTT·√p). CUBIC (default) = cubic-in-time, great long-fat; BBR = models BDP, paces, no loss reaction, low queueing. Bufferbloat fought by AQM + BBR + ECN. Fair via AIMD convergence. Debug with `ss -tin`, tune via `tcp_congestion_control`.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is congestion control?" | 2 How It Works / 7 Formal Definition |
| "cwnd vs rwnd?" | 13 Q&A / 4 Why Not Another Approach |
| "Describe slow start / AIMD." | 13 Q&A / 5 Intuition |
| "Timeout vs 3 DUPACKs?" | 13 Q&A / 9 Internal Working |
| "Why is loss a throughput cap (Mathis)?" | 13 Q&A / 10 Time Complexity |
| "What is CUBIC / BBR?" | 13 Q&A / 11 Advantages |
| "What is bufferbloat?" | 13 Q&A / 14 Follow-Up |
| "Why is QUIC's CC in user space?" | 13 Q&A / 15 Coding |
| "How do CDNs/clouds tune CC?" | 16 Industry Usage |
