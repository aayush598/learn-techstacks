# QoS and Traffic Management

> **TL;DR**: **QoS** (Quality of Service) allocates *congested* bandwidth by priority — classify traffic (voice/video/bulk), mark it (**DSCP**), then queue + schedule it (strict priority/WFQ) so latency-sensitive traffic wins. **Shaping/policing** cap rates, **WRED** drops before queues fill, and admission control keeps promises. QoS doesn't create bandwidth — it *manages scarcity* so that when links congest, the important traffic goes first.

## 1. Why Does This Exist?
Networks are built for the **worst moment**: a 10 Gbps link is great until a backup floods it. Links *do* saturate — bursts, viral traffic, backups, and video calls all compete for the same pipe — and when they do, *everyone* suffers equally unless someone decides who goes first. **QoS** exists to make *deliberate* choices during congestion: **voice** (a phone call) needs low, *stable* latency — a 100 ms hiccup makes the call unusable; **bulk transfer** (a backup) can wait seconds — nobody notices. Without QoS, FIFO queues let one bulk transfer add seconds of jitter to everyone's voice/video. QoS **classifies** traffic, **marks** it (DSCP), and **queues + schedules** it so that: voice/video jump the queue (bounded latency/jitter), critical apps get guaranteed share, and bulk traffic *uses the leftover capacity* (but never drowns the rest). It also **caps offenders** (policing/shaping) and **protects TCP** (WRED drops *early* so TCP slows before queues explode). QoS is the difference between "the network works" and "the network works for what actually matters" under load — the mechanism behind VoIP, video conferencing, and critical-app SLAs.

## 2. How Does It Work?
- **Classification**: identify traffic — by 5-tuple (IP, port, proto), application signature (deep packet inspection), DSCP value, or interface. "This is VoIP." The classifier decides *which class* a packet belongs to.
- **Marking**: stamp the packet — set **DSCP** (Differentiated Services Code Point, 6 bits in the IP ToS byte, RFC 2474) at the *trusted* edge (e.g., EF = Expedited Forwarding for voice, AF41 = video, CS1 = bulk, BE = default best-effort). Interior routers **trust** the DSCP; they don't re-classify (that's the trust boundary design).
- **Queuing**: on a congested interface, packets wait in *per-class* queues (not one FIFO): strict-priority queue (PQ), **WFQ/CBWFQ** (weighted fair queuing — per-class weight = bandwidth share), LLQ (low-latency queuing = PQ for voice *with a policed cap* so voice can't starve everything).
- **Scheduling**: the scheduler decides which queue drains next — priority always first (bounded latency), then WFQ shares the rest by weight.
- **Shaping vs policing**: both limit rate. **Policing** *drops* excess (or marks it); **shaping** *buffers* excess and sends it later (burst-smoothing, keeps the packet, adds delay). Token bucket: tokens refill at rate R, bucket size B = burst; packet needs ≥ its size in tokens.
- **Congestion avoidance (WRED)**: Weighted Random Early Detection — *before* the queue fills, randomly drop/ECN-mark packets *from low-priority classes first*; TCP sees the drop → slows → queue stays manageable (no tail-drop's TCP synchronization).
- **Admission control**: for hard guarantees (RSVP for strict bandwidth), request resources before sending — "can I have 64 Kbps?" — rarely used in the modern Internet (diffserv is the pragmatic default), but the *theory* behind "guaranteed QoS."

## 3. When Is It Used?
- **Voice/video (VoIP, WebRTC, video conferencing)**: priority over bulk — the *original* QoS use case (SIP/RTP gets EF; the call stays clear under congestion).
- **Enterprise WAN / MPLS**: site-to-site links carry voice + video + data; QoS classes (voice EF, video AF4x, critical apps AF3x, default BE, bulk CS1) are the standard enterprise template.
- **Data center (DC)**: lossless Ethernet for storage (DCB/PFC — priority flow control gives no-drop classes to storage traffic), plus latency classes for trading/HPC.
- **ISP/carrier networks**: per-service tiers (business = premium DSCP handling), traffic conditioning at the edge, and DDoS scrubbing priorities.
- **Mobile/cable**: per-user/per-plan rate enforcement (shaping/policing per subscriber) — "your plan is 100 Mbps" is a policer.
- **APIs/cloud**: rate limiting at LBs (the app-layer cousin of policing) and edge QoS classes for streaming.

## 4. Why Wasn't Another Approach Chosen?
- **Why not just build bigger links (overprovisioning)?** Cheap when you can — "the best QoS is bandwidth." But *worst-case* spikes always exist (launches, backups, DDoS), bursty apps are inherently greedy (TCP fills whatever it can), and WAN links (leased lines, satellite) can't be overprovisioned. QoS is the *always-available* fallback when money/physics can't buy headroom. The industry does both: overprovision the core, apply QoS at the constrained edges.
- **Why diffserv (per-class), not intserv/RSVP (per-flow)?** Per-flow reservation (RSVP) scales terribly (state per flow, every router, setup latency) and doesn't fit the Internet's stateless core. **Diffserv** marks classes in one DSCP byte and lets each router apply local queueing — *no per-flow state, scales to the Internet*. The tradeoff: "relative priority," not hard guarantees — the pragmatic choice.
- **Why not just use one FIFO queue?** Tail-drop FIFO is the *no-QoS* baseline: one TCP bulk flow fills the buffer, everyone else waits, and TCP synchronization (all flows see the drop together) causes sawtooth stalls. Multiple queues + weighted scheduling *isolate* classes: voice's queue is always small, bulk's queue can grow. Isolation *is* the fix.
- **Why DSCP marking, not per-interface config everywhere?** Marking once at the trusted edge means interior routers just *honor the bit* — consistent policy without re-classifying at every hop (and classification is expensive — deep packet inspection at line rate is hard). Trusted-edge marking is the scalable design.
- **Why WRED over pure tail-drop?** Tail-drop is *burst-blind* — it drops a whole burst from everyone at once (TCP synchronization → oscillation). WRED drops a *trickle* from the aggressive flows early → TCP slows smoothly → the queue never hits the cliff. Proactive beats reactive.

## 5. Intuition
QoS is a **hospital triage system for a congested emergency room** (the congested link). Patients (packets) arrive; a triage nurse (classifier) sorts them: *critical* (voice call — needs attention *now*, any delay is fatal), *urgent* (video call — needs quick attention), *stable* (web browsing — can wait a little), and *chronic* (big file backup — can wait a long time). Instead of one room where everyone waits in arrival order (FIFO — a backup would block the cardiac arrest), there are *separate waiting rooms* (queues) and the doctor (scheduler) *always* sees critical patients first (strict priority), then urgent, and only uses leftover time for chronic patients (WFQ weight). The triage nurse *caps* how many "critical" patients can be admitted at once (policing — so a flood of criticals can't starve the ER), and flags a patient who keeps coming back (WRED — "we're about to be full, slow down"). And at the door, the system *labels* every patient with their urgency level (DSCP) so the next hospital can treat them the same way without re-examining them (trusted edge marking).

## 6. Real-World Analogy
**The VIP lounge at a busy airport** — that's what QoS is to a congested network. Passengers (packets) queue at security (the congested link). The airline's *priority system* (classification + DSCP): a first-class passenger (voice) holds a red boarding pass (EF), business (video) gold (AF), economy (web) blue (BE), and cargo (backup) grey (CS1). The security *queues are separate* (per-class queues): first-class always goes first (strict priority — the flight doesn't wait), then business, then economy — economy still *gets through*, just after priority (WFQ: everyone eventually boards). The airline *caps* how many "first-class upgrades" (EF marking) a passenger can claim at the counter (policing — voice can't flood the lounge and starve everyone), and the gate agent tells heavy cargo shippers "you'll be delayed; please slow down" (WRED — TCP pacing). And the boarding pass is *stamped once at check-in* (trusted edge marking) so every gate (router) along the way honors it without re-checking your whole itinerary (no per-flow state). The system doesn't make the airport bigger — it just makes sure the *right* people move first when it's crowded.

## 7. Formal Definition
**QoS** = network capability to treat traffic classes differently to meet performance objectives (delay, jitter, loss, throughput) under congestion. **DiffServ** (RFC 2474/4594): 6-bit **DSCP** in the ToS byte (64 classes); PHBs (per-hop behaviors): **EF** (RFC 3246 — low latency, low loss, for voice), **AF** (RFC 2597 — assured forwarding, 4 classes × 3 drop precedences, for video/critical data), **BE** (default), plus **CS** classes. **Queuing/scheduling**: FIFO, **PQ** (strict priority), **WFQ/CBWFQ** (weighted fair, RFC 8130-ish), **LLQ** (PQ + policed voice cap). **Rate control**: token bucket (rate R, burst B); **policing** = drop/mark excess, **shaping** = buffer excess (smooth bursts). **Congestion avoidance**: **RED/WRED** (RFC 2309) — probabilistic early drop by class → TCP slows smoothly; **ECN** (RFC 3168) marks instead of dropping. **RSVP** (RFC 2205) = per-flow admission control (intserv), largely legacy; **PFC/DCB** (802.1Qbb) = no-drop classes for DC storage.

## 8. Example
The enterprise WAN QoS template (recreate the table):
```
Class          DSCP     Queue      Guarantee            Example
Voice          EF        PQ         10% (capped)        SIP/RTP calls
Video          AF41      WFQ        20% (weight 4)      Webex/Zoom
Critical data  AF31      WFQ        30% (weight 3)      ERP/DB/SSH
Default (BE)   CS0/BE    WFQ        30% (weight 1)      web/email
Bulk           CS1       WFQ        10% (weight 1, low)  backups/downloads

On a 100 Mbps WAN link:
- Voice queue: strict priority, but POLICED to 10 Mbps (can't starve the rest)
- Video/critical/data share the remaining 90 Mbps by weight (4:3:1:1)
- Backup: always gets its 10% — never blocks voice; never starves
Under congestion: voice jitter stays < ~5 ms; backups slow down (WRED drops their
packets first → TCP throttles), and the phone call is never the victim.
```
The *essential* detail: **priority is policed**. Strict-priority voice with an *unbounded* cap could flood the link and starve everything — LLQ's policed cap is the "priority without privilege" design that makes QoS actually work.

## 9. Internal Working
1. **Trust boundary**: the edge device (CE, switch, VoIP phone) marks DSCP; interior routers *trust* and honor it — a client can't set its own EF and jump the queue (edge re-marks/drops untrusted DSCP).
2. **Classification → marking**: match on 5-tuple/interface/DSCP/DPI → assign DSCP (e.g., voice RTP → EF). Marking once at ingress is the cheap, consistent step.
3. **Queuing**: on egress (congestion happens *out* of a router), per-class queues; the interface scheduler runs LLQ (PQ for EF, policed) then CBWFQ (weighted). Class weights map to bandwidth guarantees ("20% to video").
4. **Shaping/policing**: token bucket at ingress/egress — packets exceeding rate are dropped (policing) or buffered (shaping). *Shaping is why "100 Mbps plan" actually bursts*; policing is why "you can't download at 1 Gbps on a 100 Mbps plan."
5. **WRED/ECN**: as a queue fills, WRED computes a drop probability per class/drop-precedence; aggressive/bulk flows get dropped early (their TCP slows), voice (EF, small queue) is never dropped — plus ECN marks (CE bit) instead of dropping when endpoints support it.
6. **Monitoring**: QoS is validated with traffic counters, per-class stats, and "queue depth" — QoS silently degrades if queues are mis-sized or the DSCP marking is wrong (the classic "QoS is configured but nothing is marked" failure).
7. **End-to-end**: QoS is *per-hop* — every router on the path must honor the class for the end-to-end guarantee to hold (the reason "QoS across the Internet" doesn't exist — each ISP only trusts its own edges).

## 10. Time Complexity
- **Classification**: O(header) for 5-tuple (fast, TCAM/cache); O(payload) for DPI (expensive — that's why DPI is done at the trusted edge, not per-hop).
- **Queue operations**: enqueue O(1); scheduling is the per-packet cost — a weighted-fair scheduler (like WRR/CBWFQ) is O(1)-ish amortized per packet (a small number of classes); hardware does millions of packets/sec.
- **Shaping/policing**: O(1) per packet (token bucket compare) — the "rate limiter" is one of the cheapest operations in networking.
- **WRED**: O(1) per packet (average queue size + random draw); the *constant* cost is tiny but adds latency nanoseconds — always on modern hardware.
- **The real constraint**: queue *depth* × line rate sets latency/delay budget (bufferbloat!); QoS math is about *bounds* (delay = queue/rate), not O() — "how big are the queues and how fast do they drain" is the QoS performance question.

## 11. Advantages
- **Latency-sensitive traffic survives congestion**: voice/video keep stable, low jitter even when the link saturates — the *point* of QoS.
- **Isolation**: one aggressive flow (backup) can't starve the rest — per-class queues contain the blast radius.
- **Efficiency**: bulk traffic *uses the leftover bandwidth* — no idle capacity while voice is quiet (unlike hard reservations).
- **Scalable (DiffServ)**: one DSCP byte, no per-flow state, works across the whole Internet — the only QoS that could ever be global.
- **Granularity**: weights, policed priority, drop precedences (AF), and WRED give fine policy control.
- **Simple to reason about**: mark at the edge, honor at every hop — the model is small enough to debug.

## 12. Disadvantages
- **No hard guarantees**: DiffServ gives *relative* priority, not "you WILL get 64 Kbps" — under overload, even EF suffers (soft QoS).
- **Not end-to-end on the Internet**: each ISP only trusts its own edge; your DSCP gets re-marked/lost across provider boundaries — "QoS to the Internet" doesn't work.
- **Bufferbloat & sizing**: queues are a *delay* — wrongly sized (too deep) queues add latency even without congestion; QoS tuning is a black art of trial-and-error.
- **Complexity/ops**: classification rules, DSCP maps, queue weights, policers, WRED tuning — a huge config surface that's easy to get subtly wrong (and silent when wrong).
- **Trust issues**: marking must be enforced at the trusted edge or anyone can set EF and jump queues (and DDoS your priority queue).
- **TCP-unfriendly surprises**: aggressive shaping/policing *increases* latency and hurts throughput (your TCP reacts to the drops) — the "QoS made it worse" trap.

## 13. Interview Questions
1. **Q: What is QoS and why is it needed?** A: Quality of Service — treating traffic classes differently so that under congestion, latency-sensitive traffic (voice/video) gets priority and bulk traffic uses the rest. It *allocates* scarce bandwidth by policy instead of letting a FIFO queue let one flow ruin everyone.
2. **Q (tricky): DiffServ vs IntServ?** A: IntServ (RSVP) reserves resources *per-flow* — hard guarantees but state per flow on every router (doesn't scale to the Internet). DiffServ marks *classes* (DSCP byte) and applies local queueing — no per-flow state, scales globally, but gives relative priority, not hard guarantees. DiffServ won.
3. **Q: What is DSCP and how does marking work?** A: The 6-bit Differentiated Services Code Point in the IP ToS byte (64 classes). The trusted edge marks traffic (voice→EF, video→AF, bulk→CS1); interior routers *honor the bit* without re-classifying. Marking once at the edge is the scalable design.
4. **Q (FAANG): How do you queue/schedule a congested link?** A: Per-class queues + a scheduler: **strict priority (PQ)** for voice (bounded latency/jitter), then **WFQ/CBWFQ** (weighted) for video/critical/bulk. **LLQ** = strict-priority voice *policed to a cap* so it can't starve the rest. Isolation + weighting *is* the mechanism.
5. **Q: Policing vs shaping?** A: Both enforce a rate via token bucket (rate R, burst B). **Policing** *drops* (or re-marks) excess — no added delay, but lossy. **Shaping** *buffers* excess and sends it later — no loss, but adds delay and needs a buffer. Policing is cheap (no buffer); shaping smooths bursts.
6. **Q (tricky): What is WRED and why is it better than tail-drop?** A: Weighted Random Early Detection: *before* the queue fills, randomly drop packets (bulk classes first) so TCP flows slow smoothly — instead of tail-drop's "drop a whole burst at once," which makes all TCP flows stall together (TCP synchronization, sawtooth). WRED = proactive, class-aware congestion avoidance.
7. **Q: What is bufferbloat and how does QoS relate?** A: Oversized queues *add latency* — a full 100 ms buffer means every packet waits 100 ms even with no real congestion (TCP's sawtooth keeps filling it). Fix: active queue management (AQM — CoDel, FQ-CoDel), smaller buffers, and QoS classes so voice never waits behind a bulk fill. "Deep buffers are a delay, not a feature."
8. **Q (FAANG): "Design QoS for a corporate WAN carrying voice, video, and backups."** A: Classify at the edge (voice→EF, video→AF41, ERP→AF31, web→BE, backup→CS1), trust DSCP internally, use LLQ (policed EF for voice) + CBWFQ weights for the rest, WRED on the AF/BE queues, shape each site to the contracted rate, and monitor per-class stats. The template IS the answer — know it cold.
9. **Q: Why can't you get end-to-end QoS across the Internet?** A: QoS is per-hop and trust-based: your ISP trusts your edge marking and honors it *within its network*, but the next ISP re-marks/ignores it. No single authority enforces DSCP globally, so Internet-wide guarantees don't exist — QoS lives in enterprise/ISP *intradomain* networks (MPLS, metro, DC).
10. **Q (tricky): What is ECN and how does it improve on drops?** A: Explicit Congestion Notification (RFC 3168): instead of *dropping* packets when WRED triggers, routers *mark* them (CE bit); ECN-capable TCP slows on the mark without losing data. Removes the retransmission waste — "signal congestion, don't punish with loss."
11. **Q: What is the trust boundary in QoS?** A: The edge device that *marks* and the point beyond which DSCP is trusted. If marking isn't enforced at the edge, any client sets EF and jumps the priority queue (or floods your PQ) — the trust boundary is a security control, not just policy.
12. **Q (FAANG): Token bucket — how does it actually work?** A: Tokens refill at rate R (bps) up to burst B. A packet needs its size in tokens; enough → forward and consume; not enough → either drop (policer) or buffer (shaper). Average rate = R, burst tolerance = B. It's *the* rate-limit model — every shaper/policer/LB rate-limit is a token bucket.
13. **Q: Why does QoS often "not work" in practice?** A: (1) Nothing is *marked* (no classification → all BE), (2) the trust boundary isn't enforced, (3) queue weights/depths are mis-sized (or the buffer bloat is the real problem), (4) QoS is configured on one router but not the path, (5) WRED/dropping fights TCP. Diagnose with per-class counters — "show policy-map" is where the truth lives.
14. **Q (tricky): What is LLQ and why is it the industry standard for voice?** A: Low-Latency Queuing = a strict-priority queue for voice *with a policed bandwidth cap*. Priority without the cap lets voice starve everything; the cap guarantees voice's latency *and* the other classes' share. The "policed priority" design is why LLQ is the default voice queue.
15. **Q: Per-subscriber rate limiting (ISP plans)?** A: Shaping/policing per subscriber via token buckets — "your 100 Mbps plan" is a policer at the access node. This *is* QoS applied to the access network: fairness between subscribers, not just classes.

## 14. Follow-Up Questions
1. **Q: How does QoS interact with TCP?** A: TCP adapts to drops/marks (congestion avoidance) — so WRED/ECN *engineers* TCP to slow the aggressive flows while voice (UDP, no adaptation) is protected. That's the trick: QoS shapes the *TCP* flows and gives UDP flows priority *because* UDP can't adapt. This is why voice is always prioritized — it can't slow itself down.
2. **Q: What is AF (Assured Forwarding) class structure?** A: RFC 2597: 4 classes (AF11–AF43) × 3 drop precedences (1 low, 2 mid, 3 high). Within a class, under congestion the *higher* drop precedence (AFx3) is dropped first — "business data, and if I must drop, drop the least critical." The 2-D (class × drop) model is the flexible enterprise template.
3. **Q (production): "Voice is still choppy on a 100 Mbps link that's only 30% used." Diagnose?** A: Not congestion — likely (1) jitter/latency from a *path* problem (long buffering on a slow link, deep queue on a wireless hop, or serialization delay on a low-speed link), (2) marking missing (voice went in as BE and joined the bulk queue), (3) a shaping router downstream adding delay. QoS fixes *congestion*; it can't fix a bad path — separate the diagnosis.
4. **Q: What is PFC/DCB and when is no-drop QoS used?** A: Priority Flow Control (802.1Qbb) gives specific DC classes (storage) a *no-drop* guarantee via pause — used in lossless DC Ethernet for iSCSI/NVMe-over-Fabric/storage. It's "QoS with absolute loss guarantees" — different from the Internet's best-effort-diffserv, because the DC is a single controlled domain.
5. **Q (tricky): QoS in the cloud / APIs?** A: App-layer cousins: rate limiting (token bucket per client/API key), priority queues in message brokers (SQS priority), and per-tenant bandwidth classes in managed networks. The *principle* is identical — classify → enforce rate/priority — but the mechanism lives at L7 in APIs vs L3 in routers.

## 15. Coding Example
```python
# A token-bucket policer + a 2-queue WFQ-ish scheduler (the QoS core)
import time
import random

class TokenBucket:
    def __init__(self, rate, burst):
        self.rate, self.burst = rate, burst
        self.tokens, self.last = burst, time.monotonic()

    def allow(self, size):
        self.tokens = min(self.burst, self.tokens + (time.monotonic() - self.last) * self.rate)
        self.last = time.monotonic()
        if self.tokens >= size:
            self.tokens -= size
            return True                      # forward (policer passes)
        return False                         # drop excess (policing)

class LLQ:
    """strict-priority (policed) + weighted queues — the enterprise voice template"""
    def __init__(self, voice_cap, weights):
        self.voice_cap, self.weights = voice_cap, weights   # weights: {'ef':.1,'af':.4,'be':.5}
        self.queues = {"ef": [], "af": [], "be": []}
        self.policer = TokenBucket(voice_cap, voice_cap)

    def enqueue(self, pkt, cls):
        if cls == "ef" and not self.policer.allow(pkt):
            return "policed (voice capped)"   # LLQ's cap
        self.queues[cls].append((pkt, cls))
        return "queued"

    def schedule(self):
        for cls in ["ef", "af", "be"]:          # strict order: voice first
            if self.queues[cls]:
                return self.queues[cls].pop(0)  # (weight selection simplified)
        return None

llq = LLQ(10_000, {"ef": 0.1, "af": 0.4, "be": 0.5})
print(llq.enqueue(500, "ef"))       # queued (voice priority)
print(llq.enqueue(999999, "ef"))    # policed — voice can't starve the link
print(llq.schedule())               # ('ef',) — voice drained first
```
```bash
# The QoS toolbox
$ tcpdump -ni eth0 -v 'ip[1:2] & 0xfc != 0' -c 20     # show DSCP of packets
$ tc -s qdisc show dev eth0                            # Linux shaping/queues + stats
$ tc qdisc add dev eth0 root handle 1: htb default 30   # Hierarchical Token Bucket (shaper)
$ tc qdisc add dev eth0 parent 1:1 handle 10: netem delay 20ms   # simulate latency/jitter
$ tc qdisc add dev eth0 parent 1:1 handle 20: red limit 60KB     # RED/WRED (early drop)
# Measure what QoS is actually doing:
$ ping -i 0.05 -c 100 <host> | tail -1                 # jitter/loss under load
```

## 16. Industry Usage
- **Enterprise WAN/MPLS**: the canonical voice/video/data class template on every branch router (Cisco/Fortinet/Palo Alto QoS configs are the industry's most-copied config).
- **Carrier/ISP**: per-service classes (business premium, consumer), DSCP conditioning at peering, and per-subscriber policing (plan rates) — QoS is how carriers sell "priority" and enforce plans.
- **Data centers**: lossless Ethernet (PFC/DCB) for storage/iSCSI/NVMe-over-fabric, low-latency classes for trading/HPC, and TCP-centric AQM (CoDel) on spine links.
- **Voice/video apps**: VoIP platforms and WebRTC rely on the network honoring EF/AF — "the network is why your call is clear" is a QoS statement.
- **Streaming/CDN edge**: egress shaping per-region, adaptive-bitrate and QoE-aware delivery (the "QoS of video" = QoE metrics like rebuffering).
- **Cloud/LB APIs**: rate limiting (token buckets) per tenant/API key at the edge — the app-layer QoS that every API platform ships.

## 17. References
- RFC 2474 — DSCP (ToS byte): https://www.rfc-editor.org/rfc/rfc2474
- RFC 3246 — EF (expedited forwarding): https://www.rfc-editor.org/rfc/rfc3246
- RFC 2597 — AF (assured forwarding): https://www.rfc-editor.org/rfc/rfc2597
- RFC 4594 — QoS configuration guidelines: https://www.rfc-editor.org/rfc/rfc4594
- RFC 2309 — RED (congestion avoidance): https://www.rfc-editor.org/rfc/rfc2309
- RFC 3168 — ECN: https://www.rfc-editor.org/rfc/rfc3168
- RFC 2205 — RSVP: https://www.rfc-editor.org/rfc/rfc2205
- Bufferbloat project (CoDel/FQ-CoDel): https://www.bufferbloat.net/
- Kurose & Ross, *Computer Networking*, Ch. 7 §7.5 (QoS/queueing).

## 18. Cheat Sheet
- QoS = allocate congested bandwidth by priority; doesn't add bandwidth.
- DiffServ: 6-bit DSCP in ToS; classes: EF (voice, low-lat), AF1–4×drop3 (video/data), BE, CS.
- Mark at the trusted edge; honor the bit everywhere (no per-flow state).
- Queues: FIFO (bad) vs PQ (strict) vs WFQ/CBWFQ (weighted) vs LLQ (PQ + policed cap).
- LLQ = voice priority *with* a policed cap — can't starve the rest.
- Token bucket: refill R, burst B; policer drops, shaper buffers.
- WRED: drop early, low-priority-first → TCP slows smoothly (vs tail-drop sync).
- ECN: mark, don't drop (RFC 3168). Bufferbloat: deep queues = added delay.
- IntServ/RSVP = per-flow (no scale); DiffServ won. QoS is intradomain, not end-to-end.
- PFC/DCB = no-drop classes for DC storage. Per-subscriber = plan enforcement.
- Debug: per-class counters (`show policy-map`, `tc -s`), DSCP capture, jitter ping.

## 19. Quiz
1. DSCP lives in: a) TCP header b) IP ToS byte c) UDP d) payload → **b**
2. EF (DSCP 46) is for: a) backup b) voice c) DNS d) web → **b**
3. Policing: a) buffers excess b) drops excess c) encrypts d) marks only → **b**
4. Shaping adds: a) loss b) delay (buffering) c) DSCP d) jitter only → **b**
5. WRED drops: a) at queue-full b) early, by class c) voice d) everything → **b**
6. LLQ caps voice so it: a) starves others b) can't starve others c) encrypts d) drops → **b**
7. ECN: a) drops packets b) marks instead of dropping c) adds DSCP d) shapes → **b**
8. Bufferbloat = a) too-small queues b) oversized queues add delay c) no QoS d) WRED → **b**
9. End-to-end QoS on the Internet: a) works b) doesn't (per-domain trust) c) RSVP d) always → **b**
10. AF has drop precedences: a) 1 only b) 3 per class c) 6 d) 64 → **b**

## 20. Flashcards
- **Q: Why QoS?** → **A:** under congestion, prioritize latency-sensitive traffic; allocate, not add.
- **Q: DSCP?** → **A:** 6-bit mark in ToS; EF/AF/BE; mark at trusted edge, honor everywhere.
- **Q: PQ vs WFQ vs LLQ?** → **A:** strict / weighted / strict-but-policed.
- **Q: Policing vs shaping?** → **A:** drop excess vs buffer excess (delay vs loss).
- **Q: Token bucket?** → **A:** refill rate R, burst B; the universal rate-limiter model.
- **Q: WRED?** → **A:** early class-aware drops → TCP slows smoothly (vs tail-drop sync).
- **Q: DiffServ vs IntServ?** → **A:** per-class (scales) vs per-flow (RSVP, doesn't scale).
- **Q: Why not end-to-end?** → **A:** per-hop, trust-based; each ISP trusts only its own edge.
- **Q: Bufferbloat?** → **A:** deep queues add delay; AQM (CoDel) + small queues fix it.

## 21. Revision
QoS allocates congested bandwidth by priority — it can't add bandwidth. DiffServ: 6-bit DSCP in ToS (EF voice, AF video/data with 3 drop precedences, BE, CS); mark at the trusted edge, honor everywhere (no per-flow state — the scalable choice over RSVP/IntServ). Congestion = per-class queues + scheduler: FIFO bad; PQ strict (bounded latency), WFQ/CBWFQ weighted, LLQ = PQ + *policed* voice cap (priority without starvation). Rate control via token bucket (rate R, burst B): policer drops, shaper buffers (loss vs delay). WRED drops early, low-priority-first → TCP slows smoothly (vs tail-drop TCP sync); ECN marks instead of dropping. Bufferbloat = oversized queues adding delay → AQM/CoDel. QoS is intradomain (per-hop trust) — never end-to-end across the Internet. Used: enterprise WAN/MPLS, carrier per-subscriber plans, DC lossless (PFC) + low-latency, VoIP/WebRTC, API rate limiting. Debug: `show policy-map`/`tc -s` per-class counters, DSCP capture, jitter pings.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is QoS / why needed?" | 2 How It Works / 5 Intuition |
| "DiffServ vs IntServ (RSVP)?" | 13 Q&A / 4 Why Not Another Approach |
| "What is DSCP / marking / trust boundary?" | 13 Q&A / 9 Internal Working |
| "Queuing: PQ/WFQ/LLQ?" | 13 Q&A / 5 Intuition |
| "Policing vs shaping / token bucket?" | 13 Q&A / 12 Disadvantages |
| "WRED vs tail-drop / ECN?" | 13 Q&A / 6 Real-World Analogy |
| "Bufferbloat / AQM?" | 13 Q&A / 12 Disadvantages |
| "Design QoS for a corporate WAN?" | 13 Q&A / 8 Example |
| "Why no end-to-end QoS?" | 13 Q&A / 12 Disadvantages |
| "QoS and TCP / voice over UDP?" | 13 Q&A / 14 Follow-Up |
