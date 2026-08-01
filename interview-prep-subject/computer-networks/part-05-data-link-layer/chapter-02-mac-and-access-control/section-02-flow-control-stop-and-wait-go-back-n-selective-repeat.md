# Flow Control: Stop-and-Wait, Go-Back-N, Selective Repeat

> **TL;DR**: Flow control keeps a fast sender from overrunning a slow receiver (and from idling on a high-delay link) by gating how many unacknowledged frames may be in flight — Stop-and-Wait sends one frame and waits (simple but ~50% efficient on long links), while windowed schemes (Go-Back-N, Selective Repeat) keep the pipe full with sliding-window retransmission logic.

## 1. Why Does This Exist?
Two independent problems force flow control. **(1) Receiver overrun**: a fast sender and a slow receiver — if the sender pours frames into a receiver whose buffers are full, frames are dropped, which triggers pointless retransmission and thrashes the link. **(2) Sender idle time (pipeline underutilization)**: on a high-latency link, if a sender must wait for an ACK before sending the next frame (Stop-and-Wait), the link is empty most of the time — the "utilization" collapses as bandwidth·delay grows. Flow control exists to solve both: *window-based* schemes allow a bounded number (the window) of frames in flight, filling the pipe without flooding the receiver, and provide an *efficient* retransmission policy on top. It's the L2 analog of what TCP calls flow control + its sliding-window reliability; every networking course tests the math, which is why it's a favorite interview topic.

## 2. How Does It Work?
The sender numbers frames with sequence numbers (mod some size) and keeps a **window**: the set of frames sent but not yet ACKed (in flight). It may send as many frames as the window allows; when an ACK arrives, the window slides forward. **Stop-and-Wait** = window of 1. **Go-Back-N (GBN)**: if a frame is lost/corrupt, the sender re-sends *that frame and every frame after it* (the receiver discards out-of-order arrivals, sending duplicate ACKs). **Selective Repeat (SR)**: only the *missing* frame is retransmitted; the receiver buffers out-of-order frames. The receiver uses a running timer per frame (SR) or one timer for the oldest unACKed frame (GBN).

## 3. When Is It Used?
- **Stop-and-Wait**: legacy HDLC NRM, HTTP/1.0's "one request, one response" spirit, satellite ARQ at very low rates, and as the *correctness baseline* every more advanced scheme is compared against. TCP starts each connection in slow-start, which is effectively a growing window, not SW.
- **Go-Back-N**: classic sliding-window links — HDLC, X.25, and early reliable L2; its "resend everything after the hole" logic is the ancestor of TCP's fast retransmit style.
- **Selective Repeat**: modern reliable protocols with reordering (WiFi 802.11 block-ACK and MPDU aggregation, SCTP, and TCP's SACK option) — receivers *must* buffer out-of-order data, which is exactly SR's design.
- **TCP**: uses a hybrid — cumulative ACK (GBN-ish) + SACK (SR-ish) + window size, so the math here transfers directly to TCP interview questions (Part 03).

## 4. Why Wasn't Another Approach Chosen?
- *Alternative: no flow control, just drop and let upper layers retransmit.* Works for loss-tolerant media (UDP, best-effort Ethernet) but wastes bandwidth and can collapse under bursty loss; L2 flow control is cheap and avoids head-of-line stalls.
- *Alternative: Stop-and-Wait for everything.* Dead simple and perfectly reliable, but utilization = T_frame/(T_frame + 2·T_prop + T_ack) → on a satellite link (270 ms prop) with a 1-ms frame, utilization ≈ 0.2% — the pipe sits empty. Windowed schemes exist precisely to fix this idle time.
- *Alternative: Go-Back-N for everything.* Simple receiver (just discard out-of-order, send dup ACKs) but retransmits *everything* after an error — on a lossy, high-delay link that's enormous waste.
- *Alternative: Selective Repeat for everything.* Minimal retransmission but the receiver must buffer out-of-order frames and each frame needs its own timer — more state, more memory, more complexity. The trade is: GBN is cheap when errors are rare; SR pays for itself when errors are common or reordering happens.
- *Alternative: credit/stop signals only (no windows).* Pure XON/XOFF or sliding *credit* (receiver announces free buffer space) handles receiver-overrun but does nothing about sender idle time; the window of "outstanding" frames addresses both at once.

## 5. Intuition
Think of a **water pump filling a tank with a pipe that takes 1 second per liter one-way**. Stop-and-Wait: pump one liter, wait 2 seconds for the return signal, repeat — the pipe is empty most of the time. A *window* says "you may have up to W liters in the pipe at once" — so with W = 10, ten liters travel continuously and the pipe is full. GBN's rule: "if one liter gets ruined, re-pump that liter *and everything after it*." SR's rule: "only re-pump the ruined liter; keep the others in your holding tank." The window size is the amount of unacknowledged "trust" you give the sender; the sequence-number space must be big enough that you never confuse an old frame with a new one.

## 6. Real-World Analogy
A **drive-through with numbered orders**. Stop-and-Wait: the cook prepares order 1, waits for the car to drive off, then starts order 2 — the kitchen (link) idles between orders. A window: the cook prepares up to W orders before any is collected. Go-Back-N: if order 3 was wrong, the cook re-makes order 3 *and 4 and 5* (they're thrown out). Selective Repeat: the cook re-makes only order 3, while 4 and 5 wait in the warmer (buffer). The bigger the parking lot (delay × bandwidth), the more orders you can have in flight before the first collection (ACK) returns.

## 7. Formal Definition
Given link bandwidth *R*, frame size *L* (bits), one-way propagation *d* (seconds), processing/ACK time negligible: **transmission time** t_f = L/R, **propagation** t_p = d, **RTT** = 2d (plus ACK time). **Stop-and-Wait utilization** U = t_f / (t_f + 2·t_p + t_ack) ≈ L/R / (L/R + 2d). For a window of W frames: U = W · t_f / (t_f + 2·t_p) when W ≤ (t_f + 2·t_p)/t_f (i.e., the window doesn't exceed the bandwidth-delay product), capped at 1. **Reliability constraints**: with N-bit sequence numbers (values 0..2^N − 1), Go-Back-N requires **window ≤ 2^N − 1**; Selective Repeat requires **window ≤ 2^N / 2** (window ≤ half the sequence space). The optimal window equals the **bandwidth-delay product** BDP = R × RTT (in bits) / L (in frames).

## 8. Example
Link: R = 1 Mbps, frame L = 1000 bytes = 8000 bits, d = 50 ms one-way, ACK ignored.
- t_f = 8000 / 1,000,000 = **8 ms**; RTT = 100 ms.
- **Stop-and-Wait**: U = 8/(8 + 100) = **7.4%** — the link is idle 92.6% of the time.
- **Window needed for 100%**: W = (t_f + RTT)/t_f = 108/8 = **13.5 → 14 frames** in flight. BDP in bits = 1 Mbps × 100 ms = 100,000 bits = **12.5 frames**; same ballpark.
- **GBN with 4-bit seq (0..15)**: need window ≤ 15 ✓ (using 13). But if you incorrectly allowed window = 16, an ACK could be confused with a new frame's number.
- **SR with 4-bit seq**: window must be ≤ 16/2 = 8. With W=13, SR is *impossible* with 4 bits — you'd need 5-bit seq (window ≤ 16).

## 9. Internal Working
1. **Sender (both GBN/SR)**: keeps `base` (oldest unACKed) and `nextseqnum`; window = frames [base, base+W−1]; send while nextseqnum − base < W. Single timer at `base` (GBN) or per-frame timers (SR).
2. **Receiver (GBN)**: expected `rcvbase`; accept only if seq == rcvbase → deliver + slide; anything else → discard + send duplicate ACK of last good frame. No buffering.
3. **Receiver (SR)**: accepts *any* in-window frame; buffers out-of-order; ACKs each; delivers contiguous data to network layer; window slides over the hole.
4. **Timeout**: GBN → retransmit base..nextseqnum−1, restart timer. SR → retransmit only the timed-out frame.
5. **ACK semantics**: GBN = cumulative (ACK n ⇒ everything ≤ n received); SR = selective (per-frame ACK).
6. **Window sizing at deploy time**: set W ≥ BDP/L so the sender never waits; for TCP this is what window scaling + congestion window do dynamically.
7. **Sequence-space wrap**: after 2^N frames the numbers wrap; the window/sequence constraint exists so a wrapped old frame is never mistaken for new (the classic "why ≤ 2^N − 1" proof).

## 10. Time Complexity
- **Time to first ACK / pipeline fill**: O(BDP/L) frames in flight; throughput approaches min(R, W·L/RTT).
- **GBN retransmission cost**: on a frame loss, resend W frames — worst-case overhead ×W.
- **SR retransmission cost**: 1 frame per loss (plus buffering).
- **Receiver state**: GBN = O(1) (one expected seq); SR = O(W) buffering.
- **Utilization formula**: O(1) arithmetic — the interview-relevant math, not algorithmic complexity.

## 11. Advantages
- **Stop-and-Wait**: trivial to implement, zero receiver buffering, perfectly reliable, immune to sequence-space ambiguity.
- **Go-Back-N**: simple receiver (O(1) state, discard-and-dup-ACK), works with cumulative ACKs, minimal per-frame machinery.
- **Selective Repeat**: retransmits only what's lost → best throughput on lossy/high-BDP links; tolerates reordering; the basis of TCP SACK and WiFi block-ACK.
- **All schemes**: decouple reliability from speed, bound the sender's memory (≤ W frames), and make retransmission deterministic.

## 12. Disadvantages
- **Stop-and-Wait**: terrible utilization on any link where RTT >> t_f (the idle problem).
- **Go-Back-N**: retransmits everything after the first loss; on lossy long links that's W× wasted bandwidth and bursty traffic.
- **Selective Repeat**: complex — per-frame timers, reordering buffers at the receiver, and tricky window-slide logic; needs bigger sequence space.
- **All**: window size must be tuned (too small → idle, too big → receiver buffer pressure); sequence-number wrap bugs are notorious.
- **Not congestion-aware**: these are *flow* control (receiver-limited); without congestion control a windowed sender can still collapse a shared network (why TCP adds cwnd).

## 13. Interview Questions
1. **Q: What's the difference between flow control and congestion control?** A: Flow control is *receiver*-limited — the sender respects the receiver's buffer (this section, and TCP's rwnd). Congestion control is *network*-limited — the sender respects the network's capacity (TCP's cwnd, Part 03). Both use windows; the target differs.

2. **Q: Derive Stop-and-Wait utilization.** A: U = t_f / (t_f + 2·t_p + t_ack). With 1000-byte frames on 1 Mbps and 50 ms prop: t_f = 8 ms, U = 8/(8+100) ≈ 7.4%. The 2·t_p is the RTT — one round trip *per frame*.

3. **Q: What is the bandwidth-delay product and why does it matter?** A: BDP = R × RTT (bits) — the amount of data the pipe holds. To fill the pipe you need that many bits in flight; a window < BDP means idle time, > BDP means buffer pressure. It's the optimal window in frames = R·RTT / L.

4. **Q: Why must Go-Back-N's window be ≤ 2^N − 1 with N-bit sequence numbers?** A: With window = 2^N, all N bits are used by outstanding frames; an ACK for frame 0 (wrapped) is indistinguishable from a fresh frame numbered 0, so the sender can't tell an old ACK from a new frame. Capping at 2^N − 1 leaves at least one number to disambiguate.

5. **Q: Why must Selective Repeat's window be ≤ 2^N / 2?** A: SR's receiver buffers out-of-order frames and both sides' windows slide independently; with a window > half the sequence space, a wrap can make the sender and receiver disagree about whether a received number is a new frame or an old duplicate. Half the space is the safe bound.

6. **Q: TRICKY — You have 8-bit sequence numbers. GBN window 200, SR window 120 — valid or invalid?** A: GBN: 200 ≤ 255 ✓ valid. SR: 120 ≤ 128 ✓ valid. (With 8 bits, 2^8 = 256; GBN limit 255, SR limit 128.) This is the classic numbers trap — many candidates answer "invalid" reflexively.

7. **Q: What happens in GBN when frame 3 is lost but 4,5,6 arrive?** A: The receiver discards 4,5,6 and keeps sending ACK 2 (duplicate ACKs for the last good frame). The sender times out and retransmits *3,4,5,6* — the cost of GBN's simplicity.

8. **Q: What happens in SR when frame 3 is lost but 4,5,6 arrive?** A: The receiver *buffers* 4,5,6 and ACKs each; the sender retransmits only 3; the receiver delivers 3,4,5,6 in order to the network layer. Same loss, 1 frame retransmitted vs GBN's 4.

9. **Q: PRODUCTION — Why does TCP effectively use both GBN and SR?** A: TCP's cumulative ACK is GBN-like, but duplicate ACKs trigger fast retransmit (only the missing segment) and SACK (RFC 2018) tells the sender *which* holes to fill — that's Selective Repeat behavior. Modern kernels send only what's missing → SR behavior wins.

10. **Q: SCENARIO — Link R=10 Mbps, prop 20 ms, frame 1250 bytes. What window (frames) gives 100% utilization, and is SR possible with 5-bit seq?** A: t_f = 10,000 bits/10 Mbps = 1 ms; RTT = 40 ms; W = (1+40)/1 = 41 frames. SR with 5 bits: max 2⁵/2 = 16 — **not possible**; you need ≥ 7 bits (2⁶/2 = 32 still < 41; 2⁷/2 = 64 ✓). GBN would need 5 bits (≤31 no; 6 bits ≤63 ✓).

11. **Q: What does the receiver do differently between GBN and SR for a *corrupted* (not lost) frame?** A: Same as loss: GBN discards-and-dups-ACK (FCS failed → frame never acknowledged); SR also treats it as a hole and later retransmits just that frame. Both rely on the FCS/CRC (Section 02) to *detect* the corruption.

12. **Q: TRICKY — Two frames in flight, both lost; SR retransmits each on its own timer. Can ACKs cross?** A: Yes — timers fire independently and ACKs may arrive out of order; SR's design (per-frame ACK, buffering, half-space window) specifically tolerates this. GBN cannot handle much ACK reordering because its single cumulative timer assumes ordered ACKs.

13. **Q: What is a NACK and where do you find it?** A: A negative acknowledgment ("I got an error at seq X") lets the sender retransmit immediately instead of waiting for the timer — used in HDLC/ARQ variants and in TCP when out-of-order duplicate ACKs imply a hole. NACKs cut the timeout delay on lossy links.

14. **Q: Why doesn't the *receiver* need a timer in these schemes?** A: Reliability is the sender's job in ARQ: the sender holds unACKed frames and retransmits on timeout. The receiver only reacts (ACK, NACK, discard, buffer). This asymmetry avoids duplicate-delivery ambiguity and keeps receiver state simple.

15. **Q: PRODUCTION — WiFi's 802.11 uses immediate per-frame ACK but with block-ACK it's more like SR. Why the evolution?** A: Per-frame ACK + retransmit on lossy air is reliable but ACK-heavy (each frame costs an ACK round trip). Block-ACK acknowledges a whole aggregated burst (A-MPDU), and only missing subframes are retransmitted — exactly Selective Repeat, with far better throughput on Wi-Fi's 802.11n/ac/ax aggregated links.

16. **Q: What is "pipelining" and how do GBN/SR enable it?** A: Pipelining means sending many frames before the first ACK returns — filling the pipe. SW has no pipelining (U ≈ t_f/RTT); GBN/SR pipeline up to W frames, pushing utilization toward 100% when W ≥ BDP.

17. **Q: TRICKY — Frame 1500 bytes, link 1 Gbps, RTT 0.3 ms. Is a window of 20 frames enough?** A: t_f = 12,000/1e9 = 12 µs; RTT = 300 µs; BDP = 0.3ms×1Gbps = 300,000 bits = 25 frames. Window 20 < 25 → utilization = 20/25 = 80%, not 100%. Classic under-sizing.

18. **Q: What happens if an ACK is lost in SR vs GBN?** A: GBN: the cumulative ACK protects — a later ACK covers the lost one, so often nothing is retransmitted. SR: a lost per-frame ACK means the sender's timer for that frame eventually fires and retransmits a frame the receiver already has (harmless duplicate, but wasteful — mitigated by ACKing).

## 14. Follow-Up Questions
1. **Q: Why is a "window" called a window?** A: The sender's sequence space [base, base+W−1] forms a contiguous sliding band of allowed numbers that advances ("slides") as ACKs arrive — picture a window moving along the sequence-number timeline.

2. **Q: How does TCP's window scaling relate to the BDP?** A: TCP's advertised window is 16 bits (64 KB max); window scaling (RFC 7323) shifts it up to 2³⁰ so it can cover large BDPs — exactly the "need W ≥ BDP/L" requirement at 10 Gbps+.

3. **Q: Can Selective Repeat deliver data out of order?** A: No — the receiver buffers and delivers *in order* to the upper layer; only the *internal* arrival is out of order. The network layer must never see reordered data (that's the reliability contract).

4. **Q: What is the "silly window syndrome"?** A: A receiver that advertises tiny windows forces tiny sends — link thrash. Fixed by the receiver not advertising windows < MSS/2 and the sender not sending tiny segments (Nagle). It's a flow-control pathology from exactly this windowed model.

## 15. Coding Example
```python
import time
from collections import deque

def stop_and_wait(send, recv, t_frame, rtt):
    """Simulated SW: one frame in flight, utilization math."""
    frames = deque(range(10))
    sent = acked = time_in_flight = 0
    while frames:
        f = frames.popleft()
        send(f)
        sent += 1
        time_in_flight += t_frame + rtt      # busy + idle
        if recv() is not None:
            acked += 1
    return acked, sent, t_frame / (t_frame + rtt)

def go_back_n(send, ack, loss_rate=0.0, window=4, total=20):
    """GBN: single timer at base; on timeout resend base..next-1."""
    base = nextseq = 0
    while base < total:
        while nextseq < base + window and nextseq < total:
            send(nextseq); nextseq += 1
        if random_loss(loss_rate):
            for i in range(base, nextseq):      # retransmit the whole window
                send(i)
        else:
            a = ack()                            # cumulative ACK
            if a is not None:
                base = max(base, a + 1)

def selective_repeat(send, ack, loss_rate=0.0, window=4, total=20):
    """SR: per-frame retransmission; only the missing frame is resent."""
    acked = set(); base = 0; sent = {}
    while base < total:
        for i in range(base, base + window):
            if i < total and i not in sent:
                sent[i] = send(i)
        for i in range(base, base + window):
            if i not in acked and random_loss(loss_rate):
                send(i)                          # ONLY frame i
        a = ack()
        if a is not None:
            acked.add(a)
            while base in acked: base += 1
```
```python
# Window/sequence constraints — the interview math
def window_check(seq_bits: int, scheme: str) -> int:
    space = 2 ** seq_bits
    return space - 1 if scheme == "GBN" else space // 2

def utilization_sw(t_frame_s: float, rtt_s: float) -> float:
    return t_frame_s / (t_frame_s + rtt_s)

def window_for_full_pipe(r_bps: int, rtt_s: float, frame_bits: int) -> float:
    return r_bps * rtt_s / frame_bits

print(window_for_full_pipe(10**6, 0.1, 8000))      # 12.5 frames
print(utilization_sw(8e-3, 0.1))                   # 7.4%
print(window_check(4, "GBN"), window_check(4, "SR"))  # 15, 8
```
```bash
# Observe TCP's window in action (GBN/SR analog at L4)
ss -tin | head                          # cwnd, rwnd, ssthresh, retransmits
cat /proc/net/tcp                       # window values per socket
ip route show | head                    # RTT estimate (rtt/2) per destination
tcpdump -i eth0 -nn 'tcp' | grep -i sack # selective ACK behavior on loss
```

## 16. Industry Usage
- **TCP (RFC 793, 7323, 2018)**: cumulative ACK (GBN-like) + SACK (SR-like) + rwnd (flow control) + cwnd (congestion) — the L4 descendant of everything here; `ss`, `tcpdump`, and `ss` window fields are how engineers observe it.
- **WiFi (IEEE 802.11)**: immediate per-frame ACK + retransmission; 802.11n/ac/ax use block-ACK and A-MPDU aggregation = Selective Repeat at L2.
- **HDLC/SDLC**: standard ARQ classes with windows; satellite HDLC uses big windows and SR-like selective retransmission.
- **SCTP (RFC 4960)**: fully Selective-ACK based with explicit SR semantics.
- **DSL/cable DOCSIS**: RLP/ARQ sublayers retransmit lost L2 frames (SR-style) because line errors are bursty.
- **Data centers**: RoCE (RDMA over Converged Ethernet) and NVMe-oF use credit-based flow control — a hardware window — to keep 100 GbE pipes full with zero packet drops.

## 17. References
- Kurose & Ross, *Computer Networking*, 8th ed., §3.4 (Reliable Data Transfer: SW/GBN/SR) — the canonical treatment.
- Tanenbaum & Wetherall, *Computer Networks*, 6th ed., §3.3 (Sliding Window Protocols), §5.2.2 (TCP windows).
- RFC 793 (TCP), RFC 7323 (Window Scale), RFC 2018 (SACK) — https://datatracker.ietf.org/doc/html/rfc2018
- IEEE Std 802.11-2020 (block-ACK/aggregation) — https://standards.ieee.org/ieee/802.11/7028/
- ISO 3309/HDLC (Frame check, ARQ classes) — https://www.iso.org/standard/16274.html
- Peterson & Davie, *Computer Networks: A Systems Approach*, §2.5 (Reliable transmission).

## 18. Cheat Sheet
- U_SW = t_f / (t_f + 2·t_p + t_ack) ≈ t_f / (t_f + RTT).
- Optimal window = BDP/L = R·RTT / L frames; window < BDP → idle, > → buffer pressure.
- GBN: resend everything after loss; receiver = O(1) state; cumulative ACK; window ≤ 2^N − 1.
- SR: resend only the loss; receiver buffers O(W); per-frame ACK/timer; window ≤ 2^N / 2.
- GBN receiver discards out-of-order; SR receiver buffers them.
- TCP = GBN cumulative ACK + SR-style SACK; rwnd = flow control, cwnd = congestion control.
- Flow control (receiver) vs congestion control (network) — never conflate.
- NACK retransmits immediately; ACK timeout waits.

## 19. Quiz
1. Stop-and-Wait utilization on a link where RTT = 10× t_f is: a) 10% b) 9.1% c) 50% d) 100% → **b**
2. GBN with 4-bit seq numbers allows window at most: a) 16 b) 8 c) 15 d) 32 → **c**
3. SR with 4-bit seq numbers allows window at most: a) 16 b) 8 c) 15 d) 4 → **b**
4. In GBN, after frame 3 is lost, frames 4,5,6 received are: a) buffered b) discarded c) delivered d) NACKed → **b**
5. In SR, after frame 3 is lost, frames 4,5,6 are: a) discarded b) buffered and ACKed c) delivered out of order d) resent → **b**
6. The optimal window in frames equals: a) RTT/t_f b) R·RTT/L c) L/R d) 2^N → **b**
7. Flow control protects against: a) network congestion b) receiver overrun c) link noise d) routing loops → **b**
8. Which is GBN-like and SR-like in TCP? a) cwnd, rwnd b) cumulative ACK, SACK c) MSS, MTU d) FIN, RST → **b**

**Answers**: 1-b, 2-c, 3-b, 4-b, 5-b, 6-b, 7-b, 8-b.

## 20. Flashcards
- **Q: Stop-and-Wait utilization formula?** → **A:** U = t_f/(t_f + 2·t_p + t_ack); low whenever RTT >> t_f.
- **Q: What does the window control?** → **A:** How many unACKed frames may be in flight = the BDP fill level.
- **Q: GBN window limit?** → **A:** ≤ 2^N − 1 with N-bit sequence numbers (avoid wrap ambiguity).
- **Q: SR window limit?** → **A:** ≤ 2^N / 2 (half the sequence space).
- **Q: GBN receiver behavior on out-of-order?** → **A:** Discard + duplicate ACK of last good frame; no buffering.
- **Q: SR receiver behavior?** → **A:** Buffer out-of-order, ACK each, deliver in order.
- **Q: What is BDP?** → **A:** R × RTT (bits) — data the pipe holds; optimal window = BDP/L frames.
- **Q: How does TCP combine the schemes?** → **A:** Cumulative ACK (GBN) + SACK (SR) + fast retransmit.

## 21. Revision
Flow control gates how many frames can be in flight, solving both receiver-overrun and sender idle time. **Stop-and-Wait** (window 1) is perfectly reliable but U = t_f/(t_f+RTT) — terrible when RTT >> t_f. **Go-Back-N** allows a window and, on loss, resends *everything after* the hole; its receiver is trivial (discard + dup-ACK) and its window ≤ 2^N − 1. **Selective Repeat** resends *only* the lost frame and buffers out-of-order at the receiver, at the cost of complexity; its window ≤ 2^N/2. The optimal window is the bandwidth-delay product R·RTT/L frames — fill the pipe, no more. TCP's rwnd (flow) vs cwnd (congestion) is the L4 version, and SACK makes TCP behave like SR. Interview anchors: derive U for SW, size the window from BDP, and state the two sequence-number limits.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Derive Stop-and-Wait utilization" | 8 / 13-Q2 |
| "What is the bandwidth-delay product?" | 13-Q3 |
| "Why window ≤ 2^N − 1 for GBN?" | 13-Q4 / 7 |
| "Why window ≤ 2^N/2 for SR?" | 13-Q5 / 7 |
| "GBN vs SR on a lost frame" | 13-Q7,8 |
| "How does TCP combine both?" | 13-Q9 / 16 |
| "Size the window for 100% utilization" | 13-Q10,17 |
| "Flow vs congestion control" | 13-Q1 |
| "Why does WiFi need block-ACK/SR?" | 13-Q15 |
