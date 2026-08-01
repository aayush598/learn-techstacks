# TCP Reliability — Retransmission and Timers

> **TL;DR**: TCP guarantees every byte arrives, in order, exactly once — enforced by **ACKs, the retransmission timeout (RTO), duplicate-ACK fast retransmit, and Selective ACK (SACK)**. The RTO is computed from live RTT samples with exponential backoff (Karn's), making reliability adaptive to the actual network; SACK lets TCP retransmit *only the gaps* instead of whole windows.

## 1. Why Does This Exist?
IP delivers packets best-effort — they can be lost, duplicated, corrupted, or reordered. TCP's *raison d'être* is turning that into a reliable byte stream: the application must see every byte, in order, exactly once, no matter what the network does. Reliability needs (a) a way to know *what's missing* (ACKs + sequence numbers), (b) a way to *recover* it (retransmission), and (c) a *timer* to decide when a message is likely lost rather than merely slow. The sophistication is in (c): a fixed timeout is useless on the Internet because RTT varies from 1 ms (datacenter) to 600 ms (satellite), and even within a connection. So TCP *measures* RTT continuously, adapts the timeout to the measured mean+deviation, backs off exponentially on retransmission, and layers fast retransmit + SACK on top to recover *without* waiting for the timer. That combination is what makes "reliable" also *fast*.

## 2. How Does It Work?
- **ACK-based**: each byte has a sequence number; the receiver ACKs the *next expected* byte (cumulative). Anything unacked past the RTO is retransmitted.
- **RTO (Retransmission Timeout)**: computed as `RTO = SRTT + 4×RTTVAR` (RFC 6298), where SRTT = smoothed RTT, RTTVAR = RTT variance. Clamped to [1 s, 60 s], with exponential backoff (×2 per retransmit). The 1 s floor exists because of old problems (clock granularity, self-induced congestion); modern stacks allow sub-second floors in DCs.
- **RTT measurement**: via timestamps (TSval/TSecr, RFC 7323) or Karn's algorithm (don't sample RTT from retransmitted segments — the ACK might be for the *original*, not the retransmit). Karn's: samples only unambiguous segments; backoff persists until the first clean sample.
- **Fast retransmit**: 3 duplicate ACKs (same ack number 3×) → the segment after the ACKed one is almost certainly lost → retransmit *immediately*, no RTO wait.
- **SACK (Selective ACK, RFC 2018/6675)**: the receiver reports exact non-contiguous received ranges; the sender retransmits only the missing blocks. Without SACK, a lost middle segment forces retransmitting everything after it (go-back-N).
- **Duplicate suppression**: sequence numbers let the receiver detect and drop duplicates (retransmitted segments that actually arrived) — the "exactly once" guarantee.
- **RTO vs fast retransmit**: RTO = "I'm worried everything after this is gone" (usually whole-window loss) → severe, resets to slow start; fast retransmit = "I know one segment is missing but the rest is flowing" (partial loss) → mild, cwnd halves only.

## 3. When Is It Used?
- **Every lossy path**: cellular, wifi, satellite, cross-ocean — where drops happen, this machinery decides between a snappy retransmit and a 1-4 s stall.
- **Timeout tuning in production**: `tcp_rto_min` (min RTO, default 200 ms on Linux; 1 s RFC floor), RTO backoff — the dials that determine how quickly a dead link is detected.
- **SACK negotiation**: `net.ipv4.tcp_sack` (on by default); if a middlebox or peer strips SACK, performance on lossy links collapses → the classic "SACK disabled" diagnosis.
- **Loss diagnostics**: `netstat -s` shows `RetransSegs`, `TCPLostRetransmit`, `TCPSynRetrans`, `OutOfWindowIcmps`; `tcpdump` shows the DUPACK + retransmit pattern (`[R]` / `[S]`), `ss -tin` shows `rtt` and `rto`.
- **Retransmission storms / spurious retransmits**: reordering, queueing, and ARED can trigger false fast retransmits — DSACK (RFC 2883) tells the sender "you retransmitted unnecessarily" and the sender recovers.
- **Path MTU blackholes**: tiny MTUs drop big segments silently → RTO loops; `tcp_timestamps`+PLPMTUD and MSS clamps fix.

## 4. Why Wasn't Another Approach Chosen?
- **Why adaptive RTO instead of fixed?** RTT varies wildly per path and over time (queueing, routing, radio). A fixed 1 s timeout wastes seconds in a 20 ms DC; a fixed 20 ms timeout retransmits everything on a satellite link. Adaptive = always "about one round trip + margin," which is the minimum wait that won't spam duplicates. The `+4×RTTVAR` term is the insight: variance, not just mean, must drive the timeout.
- **Why Karn's algorithm instead of sampling retransmits?** An ACK after a retransmit is ambiguous (original or copy?). Sampling it corrupts the RTT estimate → wrong RTOs. Karn's refuses ambiguous samples and keeps the backoff — correctness over sample count.
- **Why fast retransmit (DUPACKs) instead of just waiting for RTO?** The receiver's DUPACKs *are* information: "I got byte 100 repeatedly but never byte 101" → the loss is localized. Waiting for the RTO (1 s+) on a 20 ms link wastes 98% of a retransmit window. DUPACKs convert a timeout wait into a 1-RTT recovery.
- **Why SACK instead of go-back-N?** One lost packet shouldn't cost retransmitting 100 good ones. SACK tells the sender the *exact* holes → only missing blocks re-sent → loss recovery costs 1 RTT per hole, not a full window. SACK's absence is a legacy-compat relic.
- **Why not a per-packet ACK (like TCP's early RFC 793 style)?** Cumulative ACK (next expected) compresses ACKs: one number covers all prior data, so ACK loss is harmless. Per-packet ACK maps break under reordering.
- **Why timestamps for RTT instead of seq-based?** Sequence-based RTT sampling fails when segments are retransmitted (Karn's); TSval/TSecr give an *unambiguous* sample per ACK, improving RTO precision and enabling PAWS.

## 5. Intuition
**A teacher checking homework by number**: The student (sender) numbers every assignment (sequence). The teacher (receiver) reports "I have everything through #40" (cumulative ACK). If #41 is lost but #42 arrives, the teacher says "still waiting for #41, I got #42" (DUPACK) — the student instantly re-sends #41 (fast retransmit). If the teacher goes quiet entirely (no ACK at all), the student must *guess* how long to wait before re-sending — and the guess must be based on how slow the teacher has been lately (adaptive RTO): normally ~"how long it usually takes + margin," doubled each time they're wrong (backoff). The student never re-sends an assignment they *think* might have arrived without knowing for sure (Karn's) — ambiguous cases just keep waiting. This "know when to resend, and how long to wait" is the entire reliability problem.

## 6. Real-World Analogy
**Snail-mail pen pals with numbered letters**: You number every letter (seq). Your friend replies "received up to #42" (cumulative ACK). When letter #43 is lost but #44 arrives, your friend's reply mentions "#44 arrived, but where's #43?" — a hint (DUPACK) that lets you *immediately* re-mail #43 without waiting for a long silence. When letters go missing entirely and no replies come, you must wait before re-sending — and you learn from experience: if replies usually take 5 days, wait ~7; if it's a storm season (variable), wait longer (SRTT + 4×variance). Each time you're wrong, double the wait (exponential backoff). And you never re-send a letter based on an ambiguous reply — you'd risk your friend getting two #43s. Reliable mail = knowing what's missing + a smart, learned "how long to wait" policy.

## 7. Formal Definition
TCP reliability (RFC 9293, RFC 6298 RTO, RFC 2018/2883 SACK, RFC 6675) guarantees in-order, exactly-once byte delivery. Mechanisms: (1) sequence/ACK arithmetic with cumulative ACKs; (2) Retransmission Timeout `RTO = SRTT + 4×RTTVAR`, SRTT = 0.875×SRTT + 0.125×RTT, RTTVAR = 0.75×RTTVAR + 0.25×|SRTT−RTT| (RFC 6298, min 1 s, max 60 s, clamp 60 s, exponential backoff ×2); (3) fast retransmit on 3 duplicate ACKs; (4) Selective ACK with SACK blocks enabling hole-only retransmission (RFC 6675); (5) DSACK (RFC 2883) detecting spurious retransmits; (6) Karn's algorithm (no RTT samples from ambiguous retransmits); (7) timestamp-based RTT measurement + PAWS (RFC 7323). TCP retransmits from the oldest unacked byte; recovery state is governed by the RTO and cwnd.

## 8. Example
Real loss + recovery captured (the signature pattern):
```
$ sudo tcpdump -nn -i eth0 tcp port 443
1: seq 10000-10100  (seg A)   <- sent
2: seq 10101-10201  (seg B)   <- LOST
3: seq 10202-10302  (seg C)   <- arrives
4: ack 10001        (DUPACK, ack=10001: "still need A+1")
5: ack 10001        (DUPACK #2)
6: ack 10001        (DUPACK #3)     <- fast retransmit threshold
7: seq 10101-10201  (seg B RETRANSMITTED, no RTO wait)
8: ack 10303        (all caught up; RTT sampled, RTO recalibrated)
```
Had SACK been off: after losing B, the sender would retransmit *everything* from B onward (go-back-N), wasting seg C. With SACK, the receiver's ACK would include `SACK: 10202-10302`, so only B is re-sent. The whole recovery cost: 1 RTT (fast retransmit) instead of 1+ s (RTO). That's the entire reliability budget in practice.

## 9. Internal Working
1. **Send pipeline**: the sender keeps `SND.UNA` (oldest unacked) → `SND.NXT` (next new byte) and a retransmission queue keyed by seq. Each segment is scheduled; the RTO timer starts when data is sent with nothing pending.
2. **RTT measurement**: with timestamps, every ACK yields an unambiguous sample (`now - TSecr`). Kernel maintains SRTT/RTTVAR per connection (RFC 6298); computes RTO on each update. Without timestamps, Karn's rules apply (no samples from retransmitted segments).
3. **RTO expiry**: timer fires → retransmit from SND.UNA, **double RTO** (backoff), restart timer. Each successive loss doubles again; the RTO resets to the base only after a *clean* (non-retransmit) ACK sample (Karn's keeps the backoff through ambiguity).
4. **Duplicate ACK handling**: on the 3rd DUPACK, *fast retransmit* the earliest missing segment, set ssthresh = cwnd/2, enter fast recovery: for each subsequent DUPACK, inflate cwnd and send a new segment (keeps pipe full). On ACK covering the hole → exit recovery.
5. **SACK engine (RFC 6675)**: the receiver's ACK carries SACK blocks (up to ~4 ranges); the sender keeps a *scoreboard* of received/out-of-order data and retransmits the exact missing ranges — a *retransmission pipeline* even with multiple holes.
6. **DSACK**: if a SACK block covers data *already* ACKed, the sender learns its retransmit was unnecessary (spurious) → it can shrink cwnd back / clear the "congestion" misread.
7. **Spurious RTO handling (Eifel/FRTO)**: timestamps detect a spurious RTO (network delayed, not lost) → the sender "undoes" the slow-start reset, avoiding an unnecessary throughput collapse (common on mobile with radio gaps).
8. **The RTO floor**: Linux `tcp_rto_min` (default 200 ms) beats the RFC's 1 s in DCs where RTT ~ 100 µs-1 ms — a 1 s floor would stall every small loss for a second. Modern stacks tune this.
9. **Interaction with cwnd**: retransmissions count against cwnd; fast recovery keeps cwnd high; RTO resets it (slow start). Reliability and congestion control are *interlocked* — this coupling is exactly what QUIC re-implements in user space.

## 10. Time Complexity
- **Per-segment overhead**: O(1) — queue insert + timer math. Reliability bookkeeping is free at line rate.
- **Recovery latency**: fast retransmit + SACK ≈ 1 RTT per hole; RTO ≈ RTO (≥1 s RFC, ≥200 ms Linux) per event; timeout-driven recovery for a *whole window* can cost RTO + full slow-start ramp.
- **The cost of wrong timeouts**: RTO too small → spurious retransmits (bandwidth waste + throughput collapse); too large → dead-link stalls. The RTO's variance term is what keeps it just barely large enough.
- **Mathis bound still applies**: retransmission is bounded by cwnd; loss rate p sets effective throughput ≈ 1.22·MSS/(RTT·√p) — retransmission can't create bandwidth, only recover it.

## 11. Advantages
- **Correctness by construction**: sequence+ACK+retransmit+dedup = every byte exactly once — the app never sees holes or duplicates.
- **Adaptive and self-tuning**: RTT-measured RTO follows the path; backoff survives persistent loss; SACK minimizes wasted retransmits.
- **Fast recovery**: DUPACKs make single-packet loss cost ~1 RTT, not seconds.
- **Robust under reordering**: SACK + DSACK distinguish reordering from loss (mostly), avoiding spurious slow-start.
- **Battle-tested**: 40 years of edge cases (Karn's, Eifel, FRTO, DSACK) — the most debugged protocol machinery in existence.

## 12. Disadvantages
- **Complexity**: the RTO/backoff/SACK state machine is notoriously subtle — bugs and misconfigurations (wrong `tcp_rto_min`, disabled SACK, timestamps off) silently wreck throughput.
- **Spurious retransmits**: reordering/queueing jitter triggers false fast retransmits and false RTOs → wasted bandwidth + cwnd halving (the classic "why is my good link slow" mystery).
- **RTO floor costs latency**: the RFC's 1 s floor (and Linux's 200 ms) means even a cleanly-detected loss costs a sub-second stall when DUPACKs can't help (whole-window loss).
- **Go-back-N without SACK**: middleboxes that strip SACK force whole-window retransmits — a 1% loss becomes 5-10% of retransmitted bytes.
- **Timer math sensitivity**: wrong RTT samples (ambiguous ACKs, spikes) poison RTO → cascading stalls; Karn's and timestamps mitigate but can't eliminate.
- **Coupling with congestion**: one timeout = slow-start reset = big throughput cliff for a single lost packet.

## 13. Interview Questions
1. **Q: How does TCP guarantee reliability?** A: Sequence numbers + cumulative ACKs + retransmission on RTO / 3-DUPACK fast retransmit + duplicate suppression — every byte arrives in order exactly once.
2. **Q (tricky): What is the RTO and how is it computed?** A: Retransmission Timeout = SRTT + 4×RTTVAR (RFC 6298), SRTT/RTTVAR exponentially smoothed from RTT samples, clamped [1 s, 60 s] (Linux floor 200 ms), doubled per retransmission (backoff).
3. **Q: Why is the RTO adaptive rather than fixed?** A: RTT varies per path and over time (queueing, radio, routing). A fixed timeout is too long in DCs and too short on satellites; adaptive = "mean + 4×variance" tracks the real path.
4. **Q: What is Karn's algorithm?** A: Never sample RTT from retransmitted segments (the ACK is ambiguous — original or copy?), and keep the backoff until a clean sample. Correctness of the RTT estimate over sample count.
5. **Q (FAANG): What is fast retransmit?** A: 3 duplicate ACKs (receiver says "still need byte X, I have X+1, X+2...") → retransmit X immediately instead of waiting for the RTO — recovery in ~1 RTT.
6. **Q: What is SACK and why does it matter?** A: Selective ACK — the receiver reports exact received ranges; the sender retransmits *only missing blocks* (RFC 6675), avoiding go-back-N whole-window retransmits. Essential on lossy links.
7. **Q (tricky): What's the difference between RTO and fast retransmit triggers?** A: RTO fires on *silence* (no ACK at all) — usually whole-window loss → cwnd=1, full slow start (severe). DUPACKs mean *some* data is flowing — partial loss → fast retransmit + recovery, cwnd halves (mild). 3 DUPACKs = threshold.
8. **Q: What is DSACK?** A: A SACK block for data *already* ACKed — it tells the sender "you retransmitted something I already had" (spurious). Used to detect duplicate/spurious retransmits and avoid misreading them as congestion.
9. **Q (production): `netstat -s` shows high `RetransSegs`. What do you do?** A: First determine *why*: `tcpdump` to see retransmit patterns (DUPACK vs RTO), check loss (wifi/cellular), SACK negotiated?, timestamps on?, RTO floor, and whether it's reordering (DSACK events). Retransmits themselves aren't bad — their *rate* and *cause* are.
10. **Q: What is a spurious retransmit?** A: A retransmit for data that actually arrived (delayed, not lost) — triggered by reordering or RTO too small. Eifel/FRTO detect it via timestamps and "undo" the cwnd/slow-start reset so throughput doesn't collapse unnecessarily.
11. **Q (tricky): Why do we need timestamps for RTT?** A: Sequence-based RTT sampling fails on retransmits (Karn's ambiguity). TSval/TSecr give an unambiguous per-ACK RTT sample (RTTM), improve RTO precision, and enable PAWS (wrapped-seq protection).
12. **Q: What happens if the RTO is too small / too large?** A: Too small → premature retransmits (bandwidth waste, spurious cwnd halving). Too large → long stalls on real loss and slow dead-link detection. The variance term + floor keep it "just big enough."
13. **Q (FAANG): One packet lost out of 100 on a 200 ms link. How long to recover with and without SACK?** A: With fast retransmit + SACK: ~1 RTT (200 ms) for the hole only. Without SACK, go-back-N: retransmit the missing segment *plus* everything after it that was already received — the missing byte is recovered in 1 RTT, but wasted bandwidth ≈ the rest of the window. With only RTO (whole window lost): RTO (~200 ms+ floor) + slow-start ramp.
14. **Q: What is the retransmission queue?** A: The sender's buffer of sent-but-unacked segments keyed by seq — the source of retransmits on RTO, and the window of SACK-driven retransmits. Freed as ACKs slide forward.
15. **Q: How do you measure loss on a path?** A: `iperf3`/`ping -c 100` (packet loss), `mtr` (per-hop loss), `ss -tin` (rtt/rto), `netstat -s` (RetransSegs, TCPLostRetransmit), and tcpdump's `[R]`/`[S]` analysis. Distinguish *wire* loss (radio, physical) from *queue* loss (congestion, bufferbloat).
16. **Q (tricky): Can TCP retransmit a segment that was never lost?** A: Yes — that's a *spurious retransmit*: reordering, a too-small RTO, or delayed ACKs make the sender resend something the receiver already has. DSACK/Eifel detect and compensate; but each spurious retransmit wastes bandwidth and can halve cwnd.
17. **Q: What does `TCPLostRetransmit` in netstat -s mean?** A: A segment the sender retransmitted was itself declared lost (its retransmit also timed out / SACKed lost) — a sign of severe loss or persistent congestion, or a bad RTO floor. High values warrant a loss investigation.

## 14. Follow-Up Questions
1. **Q: How does QUIC's reliability differ from TCP's?** A: Same ideas (seq + ACK + retransmit + SACK-ish), but *in user space*: per-stream independent retransmission (no head-of-line blocking across streams), packet-number-based (not byte-based) ACKs, and connection IDs. It's TCP reliability without TCP's kernel coupling.
2. **Q: What is Eifel and why does it matter?** A: An algorithm (RFC 3522) using timestamps to detect a *spurious RTO* — when the RTO fired but the original segments were just delayed. It reverts cwnd/ssthresh so the sender doesn't collapse into slow start unnecessarily — a real win on mobile/radio links.
3. **Q (tricky): Why is the RFC RTO floor 1 second?** A: Historical: coarse clock granularity and the risk of self-induced congestion from too-aggressive retransmits. Modern kernels lower it (`tcp_rto_min`, 200 ms) where clocks are fine and RTTs are small — a deliberate, safe deviation for DC performance.
4. **Q: What is the difference between "retransmission" and "recovery"?** A: Retransmission = re-sending data; recovery = the *state* after loss (fast recovery: cwnd halved + window inflation; RTO recovery: slow-start restart). They're different dimensions: SACK targets *what* to resend; recovery governs *how fast* while doing it.
5. **Q (FAANG): Your CDN sees "spurious retransmits" under load. Root cause and fix?** A: Likely buffer-induced *reordering* (multi-path, queueing) or AQM too aggressive → false fast retransmits/RTOs. Fixes: enable DSACK/timestamps, raise `tcp_reordering` (default 3), use BBR (delay-based, less sensitive), and add AQM smoothing. The retransmit counter is the *symptom*; the queue behavior is the disease.

## 15. Coding Example
```python
# A toy reliability engine — the RTO + retransmit loop, in miniature
import random, time

class ReliableSender:
    def __init__(self, base_rtt=0.02):
        self.srtt, self.rttvar = base_rtt, base_rtt / 2   # RFC 6298 init
        self.rto = self.srtt + 4 * self.rttvar
        self.ackq = {}        # seq -> time sent (unacked)
    def send(self, seq, now):
        self.ackq[seq] = now
        return random.random() < 0.9       # 90% "delivery"
    def on_ack(self, seq, now):            # unambiguous sample
        sample = now - self.ackq.pop(seq, now)
        self.rttvar = 0.75 * self.rttvar + 0.25 * abs(self.srtt - sample)
        self.srtt = 0.875 * self.srtt + 0.125 * sample
        self.rto = max(0.1, self.srtt + 4 * self.rttvar)
    def check_timeout(self, now):
        for seq, t in list(self.ackq.items()):
            if now - t > self.rto:
                print(f"  RTO! retransmit seq {seq} (rto={self.rto:.3f}s)")
                self.ackq[seq] = now      # Karn's: keep backoff, resend
                self.rto *= 2              # exponential backoff
```
```bash
# Watch retransmits on a real connection
$ netstat -s | grep -E 'retransmits|RetransSegs|TCPLostRetransmit|DupAcks'
$ sudo tcpdump -nn -i eth0 'tcp[tcpflags] & (tcp-syn|tcp-ack) == 0' | grep -E '\[R\.\]|DUP ACK'
# Retransmitted segment = same seq seen again; RTO = silence followed by [R.]
$ ss -tin | grep -oE 'rtt:[0-9.]+/[0-9.]+ rto:[0-9]+'
```

## 16. Industry Usage
- **The entire Web + cloud**: HTTPS/TLS, S3, RDS, SSH, Kafka — every reliable protocol's foundation is this retransmission machinery; `RetransSegs` is one of the most-read counters in NOC dashboards.
- **CDNs and media (Cloudflare, Netflix, YouTube)**: they tune `tcp_rto_min`, enable SACK/timestamps, and watch DSACK/spurious-retransmit stats; Netflix/BBC use ECN + BBR partly to *reduce* loss-driven retransmits.
- **Mobile & satellite (SpaceX Starlink, LTE/5G stacks)**: high variable RTT + random loss makes adaptive RTO + timestamps + SACK the difference between usable and unusable — Eifel/FRTO designed for exactly these links.
- **Datacenter fabrics (Meta, Google, Alibaba)**: at 10-400 Gbps, retransmits cost real money; DCTCP/ECN avoid drops entirely (no retransmits), and switches use fast-congestion signaling so recovery never triggers.
- **Middleware & WAN acceleration**: proxy/LB stacks (Envoy, HAProxy) do *forward error correction* + selective retransmission on top of TCP for lossy WANs — supplementing, not replacing, TCP's built-in reliability.

## 17. References
- RFC 6298 — Computing TCP's Retransmission Timer: https://www.rfc-editor.org/rfc/rfc6298
- RFC 2018 / RFC 6675 — SACK + SACK-based loss recovery: https://www.rfc-editor.org/rfc/rfc6675
- RFC 2883 — DSACK: https://www.rfc-editor.org/rfc/rfc2883
- RFC 3522 — Eifel (spurious RTO detection): https://www.rfc-editor.org/rfc/rfc3522
- RFC 7323 — Timestamps (RTTM + PAWS): https://www.rfc-editor.org/rfc/rfc7323
- RFC 9293 — TCP (reliability semantics): https://www.rfc-editor.org/rfc/rfc9293
- Kurose & Ross, *Computer Networking*, Ch. 3 §3.5.3 (reliable data transfer).

## 18. Cheat Sheet
- RTO = SRTT + 4×RTTVAR (RFC 6298); SRTT=0.875·SRTT+0.125·RTT; clamp [1 s, 60 s] (Linux floor 200 ms); ×2 backoff.
- Karn's: no RTT samples from retransmits; keep backoff until clean sample.
- Fast retransmit: 3 DUPACKs → resend immediately (≈1 RTT recovery).
- SACK: receiver reports exact ranges → retransmit only holes (RFC 6675).
- DSACK: "you resent unnecessarily" → spurious-retransmit detection.
- Eifel/FRTO: timestamps undo spurious RTO's slow-start reset.
- Retransmit triggers: RTO (silence, whole window) vs DUPACKs (partial loss).
- `netstat -s`: RetransSegs, TCPLostRetransmit, DupAcks; `ss -tin`: rtt/rto.
- RTO too small → spurious retransmits; too large → stalls. Keep SACK + timestamps on.
- Path MTU blackholes → silent drops → RTO loops; clamp MSS / PLPMTUD.

## 19. Quiz
1. RTO formula: a) SRTT b) SRTT+4×RTTVAR c) 2×SRTT d) RTTVAR → **b**
2. RFC RTO floor: a) 1 s b) 200 ms c) 10 ms d) 60 s → **a**
3. Karn's algorithm: a) sample all RTTs b) skip ambiguous retransmit samples c) double RTO always d) use fixed RTO → **b**
4. Fast retransmit triggers on: a) 1 DUPACK b) 2 DUPACKs c) 3 DUPACKs d) 10 DUPACKs → **c**
5. SACK allows: a) bigger windows b) retransmit only holes c) no retransmits d) pacing → **b**
6. DSACK detects: a) loss b) spurious retransmits c) congestion d) reordering always → **b**
7. Whole-window loss triggers: a) DUPACKs b) RTO c) SACK d) ECN → **b**
8. Eifel/FRTO: a) undoes spurious RTO b) doubles RTO c) disables SACK d) tunes MSS → **a**
9. Timestamps enable: a) RTTM + PAWS b) bigger MSS c) SYN cookies d) wscale → **a**
10. High RetransSegs first check: a) increase RTO b) find the cause (loss vs reordering) c) disable SACK d) raise wmem → **b**

## 20. Flashcards
- **Q: RTO formula?** → **A:** SRTT + 4×RTTVAR (RFC 6298), clamp [1 s, 60 s], ×2 backoff.
- **Q: Karn's algorithm?** → **A:** never sample RTT from retransmitted segments.
- **Q: Fast retransmit?** → **A:** 3 DUPACKs → immediate resend, ~1 RTT recovery.
- **Q: SACK?** → **A:** receiver reports exact ranges; resend only holes.
- **Q: DSACK?** → **A:** "you retransmitted what I already had" → spurious detection.
- **Q: RTO vs DUPACK?** → **A:** RTO=whole-window loss (severe, slow start); DUPACKs=partial loss (mild, halve).
- **Q: Timestamps?** → **A:** unambiguous RTT (RTTM) + PAWS.
- **Q: spurious retransmit cause?** → **A:** reordering or RTO too small.

## 21. Revision
TCP reliability = seq + cumulative ACK + retransmission + dedup. RTO = SRTT + 4×RTTVAR (RFC 6298), min 1 s (200 ms Linux), ×2 backoff; Karn's avoids ambiguous RTT samples; timestamps give clean RTTM + PAWS. Fast retransmit on 3 DUPACKs (~1 RTT); SACK retransmits only holes; DSACK detects spurious; Eifel undoes false RTOs. RTO = severe (whole window, slow start); DUPACKs = mild (halve). Loss is the throughput ceiling (Mathis). Debug via netstat -s (RetransSegs, TCPLostRetransmit), tcpdump, ss -tin.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How does TCP guarantee reliability?" | 2 How It Works / 7 Formal Definition |
| "What is RTO / how computed?" | 13 Q&A / 8 Example |
| "Why adaptive RTO / Karn's?" | 13 Q&A / 4 Why Not Another Approach |
| "What is fast retransmit / 3 DUPACKs?" | 13 Q&A / 5 Intuition |
| "What is SACK and why does it matter?" | 13 Q&A / 9 Internal Working |
| "Spurious retransmits / Eifel / DSACK?" | 13 Q&A / 14 Follow-Up |
| "High RetransSegs — how to debug?" | 13 Q&A / 15 Coding |
| "Why does QUIC need its own reliability?" | 14 Follow-Up / 16 Industry Usage |
