# TCP Flow Control — The Sliding Window

> **TL;DR**: Flow control keeps a fast sender from flooding a slow receiver's buffer. The receiver advertises its free buffer (the **rwnd**, in the Window field, scaled up to 2^30), and the sender is forbidden from having more than that much unacknowledged data in flight — the sliding window mechanism enforces the limit byte-by-byte as ACKs slide it forward.

## 1. Why Does This Exist?
The two ends of a TCP connection run at different speeds with **different buffer sizes**. If the sender pours bytes without limit, the receiver's receive queue overflows → the OS must drop data → TCP would retransmit endlessly, degrading into pathological thrashing even on a perfect link. Flow control exists to make the sender *self-limit* to what the receiver can physically absorb right now. It's a **receiver-side** problem ("my buffer"), as opposed to congestion control's **network-side** problem. The sliding-window algorithm is the mechanism: it lets the sender keep the *pipe full* (multiple segments in flight — not stop-and-wait) while never exceeding the receiver's advertised capacity. It converts "don't overwhelm me" into a precise, self-respecting byte budget.

## 2. How Does It Work?
- **rwnd (receive window)**: every segment's Window field advertises *current free buffer* = `rcv_buffer_size - (buffered-but-not-consumed bytes)`. The receiver recomputes it as the app consumes data.
- **Effective send window** = `min(rwnd, cwnd)` (cwnd = congestion window). Flow control is the rwnd half.
- **In-flight budget**: the sender may have at most `min(rwnd, cwnd)` *unacknowledged* bytes. As ACKs arrive, the window slides forward: `usable_window = rwnd - (highest_sent_byte - highest_acked_byte)`.
- **Sliding**: bytes are numbered; the sender tracks `sent-but-unacked`, `sent-and-acked`, `not-yet-sent`. ACK "k" lets the window move up to include bytes up to `k + rwnd`.
- **Zero window**: when rwnd = 0, the sender must stop sending. To prevent deadlock, it polls with **window probes** (1-byte segments) and the receiver sends an **ACK announcing the new window** when space frees up.
- **Window scaling (RFC 7323)**: rwnd field is 16 bits (max 64 KB); negotiated at SYN, the Window Scale option multiplies it by 2^shift (shift ≤ 14 → up to 1 GB) — necessary for high-BDP links.
- **The app matters**: rwnd grows only as fast as the app calls `recv()`; a slow consumer shrinks rwnd → the sender throttles → backpressure propagates end-to-end.

## 3. When Is It Used?
- **Every TCP connection, always**: flow control is always active — it's the Window field on every segment. You just notice it when it bites.
- **Slow consumers**: a client reading slowly (UI, streaming to disk) makes rwnd small → the server's effective throughput collapses → "why is my download slow?" is often rwnd, not the network.
- **Kernel tuning**: `rmem_max`/`wmem_max`, `tcp_rmem`, `tcp_wmem`, and autotuning set the buffer size; the *advertised* rwnd is derived from them. Raising buffers raises the throughput ceiling (window ≈ BDP).
- **Windows of death**: rwnd=0 stall → window probe storms; persistent small rwnd (window cling) — the classic TCP pathologies.
- **HTTP/SMB/NFS throughput debugging**: `ss -tin` shows the receiver window; a receiver window far below BDP explains capped throughput on otherwise-fast links.

## 4. Why Wasn't Another Approach Chosen?
- **Why a sliding window and not stop-and-wait?** Stop-and-wait (send 1, wait for ACK, send next) uses the link 1/N of the time (only one packet in flight) — throughput ≈ 1×MSS/RTT, useless. The sliding window keeps up to `rwnd` bytes in flight, filling the pipe while still bounding receiver buffer use. It's the classic trade: utilization vs bounded memory.
- **Why not let the receiver's OS just discard overflow (like UDP)?** UDP does exactly that — but TCP promises *reliability*, and discarding would trigger retransmissions that *reload* the same full buffer → infinite loop + wasted bandwidth. Advertising a window *prevents* the overflow in the first place.
- **Why a *receiver-advertised* window instead of a sender-chosen one?** Only the receiver knows its true buffer state (free space changes as the app drains). The sender can't observe the receiver's memory — so the receiver must *tell* it, per-segment, and the sender must obey. It's an explicit signaling channel riding on the header.
- **Why 16-bit window + scaling instead of a bigger field?** 1981: 64 KB was generous. Modern links need GBs. The Window Scale option is backwards-compatible (only used when both negotiate it at SYN) — the only way to extend without breaking 40 years of stacks.
- **Why ACK-based sliding instead of credit-based (like RDP)?** TCP's byte-counting + cumulative ACK is simpler and already used for reliability — one number does double duty (flow credit + reliability confirmation).

## 5. Intuition
Imagine a **water bucket brigade** where the *receiver* has a fixed-size bucket and the *sender* must never have more buckets-in-flight than the receiver has empty shelf space. The receiver tapes a sign on its last reply: "I currently have room for 300 buckets." The sender keeps a *moving tally*: buckets sent minus buckets confirmed = in flight; as long as in-flight ≤ 300, keep sending; when the receiver's app drains the buckets (recv()), it updates the sign to "room for 500" and the sender speeds up. When the shelf is full (0 space), the sender waits — but to be sure the sign changed, it occasionally pokes the receiver ("still full?") rather than assuming. The "sliding window" is just this running budget, sliding forward as confirmations arrive.

## 6. Real-World Analogy
**A conveyor belt feeding a kitchen with limited counter space**: The chef (receiver) tells the supplier (sender): "I can only have 20 dishes on my counter right now." The supplier ships batches, keeping a tally of *dishes shipped minus dishes confirmed eaten*. As the chef plates them (consumes), they send "counter clear for 20 more" (ACK with rwnd). If the counter is full, the supplier must stop — but every few seconds sends a "hello, is there space yet?" poke (window probe) to avoid stalling forever. If the chef upgrades to a bigger counter (larger buffer), the limit grows; if the chef is slow (slow app), the counter shrinks and the supplier throttles. The key insight: the supplier never lets more than *what the chef can currently hold* be on the road — the road stays full, but never overflows the kitchen.

## 7. Formal Definition
TCP flow control (RFC 9293 §3.8.1, RFC 7323 for scaling): the receiver advertises its receive window `rwnd` (16-bit Window field × 2^wscale) in every segment; the sender must keep unacknowledged bytes `Unacked ≤ rwnd`. Effective window is `min(rwnd, cwnd)` where cwnd is the sender's congestion window. The sender maintains `SendUnacknowledged`, `SendNext`, and `SendWindowEnd = SendUnacknowledged + min(rwnd, cwnd)`; the window slides forward on cumulative ACKs. A zero window stops the sender; the receiver advertises updates and the sender may send 1-byte *window probes* (RFC 793 §3.5). Autotuning adjusts buffer sizes (Linux: `net.ipv4.tcp_rmem`/`tcp_wmem`, `rmem_max`/`wmem_max`) to match the bandwidth-delay product.

## 8. Example
Throughput math — why the window *is* the throughput:
```
Bandwidth-delay product: BDP = bandwidth × RTT
Example: 10 Gbps link, RTT = 40 ms
  BDP = (10e9 bits/s) × 0.04 s = 400 Mbits = 50 MB

Without window scaling (window ≤ 64 KB):
  Throughput ≤ rwnd / RTT = 65536 / 0.04 = 1.6 MB/s ≈ 13 Mbps  (!!)
  The 10 Gbps link is used at 0.13%.

With window scaling (window = 64 MB, buffer autotuned to BDP):
  Throughput = min(rwnd, cwnd) / RTT = 50 MB / 0.04 s = 1.25 GB/s ≈ 10 Gbps  ✓
  The link saturates.
```
This single equation — `throughput ≈ window / RTT` — is why `net.core.rmem_max` / `net.ipv4.tcp_rmem` exist, why you `sysctl net.ipv4.tcp_window_scaling=1`, and why big-window tuning is *the* first thing people do for WAN transfers. A tiny rwnd is a throughput killer no matter how fast the network is.

## 9. Internal Working
1. **Receiver side**: the kernel tracks `rcv_nxt` (next expected) and the *used* buffer (bytes queued, not yet `recv()`-ed). On every segment sent (data or pure ACK), it sets `Window = rcvbuf_allocated - used_bytes`, scaled by the negotiated wscale.
2. **Sender side**: maintains three pointers over its byte stream: `SND.UNA` (oldest unacked), `SND.NXT` (next to send), and the window edge `SND.UNA + min(rwnd, cwnd)`. It sends while `SND.NXT < window edge`. ACK k → SND.UNA jumps to k → window slides → new bytes become sendable.
3. **Zero-window handling**: if rwnd = 0, the sender freezes `SND.NXT`. To avoid deadlock (a lost "window update" ACK), the sender sends **persist timer** probes (1 byte, exponential backoff) until the receiver's ACK shows rwnd > 0.
4. **Autotuning**: Linux continuously adjusts `tcp_rmem[2]`/`tcp_wmem[2]` based on observed RTT and buffer-use — the *advertised* window grows to ~BDP automatically, up to `rmem_max` (default ~6 MB) / `wmem_max`.
5. **Interaction with congestion control**: the *effective* send window is `min(rwnd, cwnd)`. Flow control is "what the receiver allows"; congestion control is "what the network allows"; the sender obeys the smaller.
6. **Silly Window Syndrome (SWS)**: if the receiver ACKs with a *tiny* rwnd repeatedly, the sender sends tiny segments → bandwidth waste. Defenses: receiver waits until rwnd ≥ MSS before advertising (Clark's solution); sender delays until it can send ≥ MSS or half-window (Nagle).
7. **Delayed ACKs**: the receiver delays ACKs up to 500 ms (or 2 segments) to piggyback — this *temporarily* shrinks the effective window, interacting with Nagle (the famous 40 ms latency interaction).

## 10. Time Complexity
- **Per-segment**: O(1) — read the Window field, update pointers. Flow control itself is free.
- **Throughput ceiling**: `T ≤ min(rwnd, cwnd) / RTT`. Raising the *bottleneck* (window, buffers) is the only way to raise throughput for a fixed RTT. This is a mathematical bound, not an implementation detail.
- **Memory**: receiver buffers up to `tcp_rmem[2]` per connection (default ~6 MB, up to rmem_max) — multiplied by connections; a server with 100k connections holds ~GBs of receive buffer. Sizing vs connection count is a real tension.
- **Buffer-bloat corollary**: big windows + big buffers + loss-based congestion = router queues fill → latency spikes. Flow control + congestion control *together* set the effective queueing.

## 11. Advantages
- **Prevents overflow**: the receiver never drops due to buffer exhaustion — reliability + flow control cooperate (no retransmit storms).
- **Pipe utilization**: the sliding window keeps the link full (vs stop-and-wait), making high throughput possible over long RTTs.
- **Backpressure, built-in**: slow consumer → small rwnd → sender throttles — a clean, automatic end-to-end feedback loop with no extra protocol.
- **Scalable**: window scaling extends it to modern BDPs (up to 1 GB) with zero protocol breakage.
- **Autotuned**: the kernel adapts window sizes to the observed path; default config is good on typical links.

## 12. Disadvantages
- **Buffer-dependent**: throughput is *bounded by* rwnd; un-tuned defaults (64 KB or small rmem) silently cap fast links → "it's the window" is a top production diagnosis.
- **Zero-window stalls**: rwnd=0 → sender waits → latency spikes; persist probes add chatter; a stuck receiver (app not draining) wedges the connection.
- **Silly Window Syndrome**: tiny-window/tiny-segment oscillation wastes bandwidth and CPU — needs Clark + Nagle-style fixes (which add their own latency).
- **Interaction bugs**: delayed ACK × Nagle = 40 ms+ per request on some workloads; window scaling mismatch breaks old middleboxes (NAT/firewalls that don't understand wscale).
- **Not congestion control**: a big rwnd doesn't protect the *network* — a fast sender can still overload the path (that's cwnd's job). Misreading the two is a classic interview trap.

## 13. Interview Questions
1. **Q: What is TCP flow control?** A: Limiting the sender to the receiver's advertised buffer space (rwnd) so the receiver never overflows — receiver-side pacing, vs congestion control which protects the network.
2. **Q (tricky): Flow control vs congestion control?** A: Flow control = don't overwhelm the *receiver* (rwnd, receiver's buffer, carried in the header). Congestion control = don't overwhelm the *network* (cwnd, sender-side, kernel algorithm). Effective window = min(rwnd, cwnd).
3. **Q: What is the sliding window?** A: The sender's byte budget: it may have at most `rwnd` unacknowledged bytes in flight; ACKs slide the window forward, letting new bytes be sent. Keeps the pipe full without overflowing the receiver.
4. **Q: How does the receiver advertise its window?** A: The Window field (16 bits) in every segment = current free receive buffer, scaled by the Window Scale option negotiated at SYN (2^shift, up to 2^30 bytes).
5. **Q (FAANG): Why is throughput limited by the window?** A: Because at any moment only `min(rwnd, cwnd)` bytes can be in flight; throughput ≈ window / RTT. To hit a BDP = bandwidth × RTT, the window must be ≥ BDP. Small window = capped throughput regardless of link speed.
6. **Q: What is a zero window and what happens?** A: rwnd=0 → the sender must stop. To avoid deadlock it sends 1-byte *window probes* on a persist timer until the receiver ACKs a positive window.
7. **Q: What is the Silly Window Syndrome?** A: Receiver keeps advertising tiny windows (splitting ACKs) → sender sends tiny segments → bandwidth waste. Fixed by Clark's solution (receiver withholds ACKs until rwnd ≥ MSS) and Nagle (sender coalesces).
8. **Q (production): A 10 Gbps link shows 500 Mbps throughput. What do you check?** A: Window size first: `ss -tin` (receiver window), `tcp_rmem`/`tcp_wmem`/`rmem_max`, autotuning, window scaling on both ends, then actual path loss (congestion). The window/BDP mismatch is the #1 silent cap.
9. **Q: What is window scaling and why is it needed?** A: The Window field is 16 bits (64 KB max) — enough in 1981 but far below modern BDPs. The Window Scale option (negotiated at SYN, shift ≤ 14) multiplies it to up to 1 GB, enabling high throughput on high-bandwidth, high-latency links.
10. **Q (tricky): Can the window grow arbitrarily?** A: Practically, it's bounded by negotiated wscale (2^30) and OS buffer limits (rmem_max/wmem_max); also, the *sender's* cwnd and the path's loss rate cap effective throughput regardless.
11. **Q: What is TCP autotuning?** A: The kernel automatically adjusts socket buffers (hence advertised rwnd) to observed RTT and buffer use, up to `rmem_max`/`wmem_max` — so the window tracks the BDP without manual tuning on typical links.
12. **Q: What is the persist timer?** A: The timer that fires when rwnd=0 — it makes the sender send window probes (1-byte segments) to check whether the receiver has reclaimed space, preventing deadlock if a window-update ACK was lost.
13. **Q (FAANG): Slow download from a fast server. What's the cause and fix?** A: Likely the client's rwnd is small (small socket buffers, slow app draining, or window scaling disabled) → raise client `rmem_max`, ensure `tcp_window_scaling=1`, drain faster; also check cwnd/congestion + loss. Throughput is *the window*, so inspect it first.
14. **Q: How does flow control interact with delayed ACK?** A: Delayed ACK postpones the window update up to 500 ms, effectively shrinking the sender's window and throughput for that period — and paired with Nagle it adds ~40-500 ms per request. Classic tuning interaction.
15. **Q (tricky): If rwnd is 64 KB and RTT is 100 ms, max throughput?** A: 65536 B / 0.1 s ≈ 5.2 Mbps — regardless of a 10 Gbps network. To go faster: window scaling + bigger buffers (rwnd ≥ BDP). This equation is the whole point of window tuning.
16. **Q: What happens if the receiver's app doesn't read?** A: rwnd → 0, sender stalls (zero-window), probes follow; if it never drains, the connection sits idle holding its tuple — a silent resource leak visible as ESTABLISHED-but-idle sockets.
17. **Q: What is the difference between rwnd and MSS?** A: MSS is the max *segment* size (1460 at 1500 MTU); rwnd is how many *bytes* may be in flight (multiple segments). rwnd/MSS ≈ max segments in flight.

## 14. Follow-Up Questions
1. **Q: How does BBR/CUBIC interact with the advertised window?** A: They manage *cwnd* (network side); the effective window stays min(rwnd, cwnd). BBR paces and models the path; but if rwnd < BDP, nothing helps — the receiver caps you. Tuning both sides is how WAN teams hit line-rate.
2. **Q: What is "window cling"?** A: When the receiver's rwnd is stuck at a small-but-nonzero value (e.g., the app drains slowly), the sender sends small, low-efficiency segments indefinitely. Fixed by ensuring the app drains fast and by receiver-side buffering policy.
3. **Q (tricky): Can a zero-window be "stolen" to attack?** A: It's a resource that can be hoarded: a slow-reading peer makes you waste buffer + probes; with many connections, malicious slow-readers ("slowloris"-adjacent) hold server buffers hostage. Rate-limit, cap buffers, and monitor rwnd.
4. **Q: What's the difference between advertised window and the actual socket buffer?** A: Advertised rwnd = free portion of the *receive* buffer (allocated - queued). `tcp_rmem` controls allocation (min/default/max) and autotuning grows it; rwnd is the *instantaneous free space*, recomputed per segment.
5. **Q (FAANG): Your proxy sits between a fast origin and slow mobile clients. What's the flow-control story?** A: The proxy's receive window vs the mobile client's tiny rwnd — the proxy must buffer (rwnd from client caps the flow), so it needs large buffers and offloads (streaming, chunked reads). This is why CDN edge nodes have big buffers and tune `rmem`.

## 15. Coding Example
```python
# The sliding-window math, simulated
import random

MSS, rwnd = 1460, 65536          # receiver advertises 64 KB (no scaling)
unacked, next_seq = 0, 0          # bytes we've sent, next byte number

def ack(k):
    global unacked, next_seq
    freed = k - unacked
    unacked = max(unacked, k)
    return freed                  # window slides forward by `freed`

window = rwnd
for _ in range(10):
    in_flight = next_seq - unacked
    can_send = max(0, window - in_flight)      # usable = rwnd - in-flight
    sent = min(can_send, MSS * 3)              # send up to 3 segments
    next_seq += sent
    print(f"in_flight={in_flight:5d} usable={can_send:5d} sent={sent:5d}")
    if random.random() < 0.7:
        acked = ack(next_seq)                   # ACK everything (unlikely in real life)
        print(f"   ACK -> window slid by {acked}")
```
```bash
# See the receiver window in action on a real connection
$ ss -tin | head -20
#   ... rtt:0.5/0.2 cwnd:10 rcv_rtt:40 rcv_space:26883   (autotuned buffer)
$ ss -tan | awk '$1=="ESTAB" {print $2,$3}'        # Recv-Q / Send-Q
# Send-Q near rwnd ⇒ receiver is slow (flow control is the bottleneck)
# Check/raise the buffers that back the advertised window:
$ sysctl net.core.rmem_max net.core.wmem_max net.ipv4.tcp_rmem net.ipv4.tcp_wmem
```

## 16. Industry Usage
- **CDN & edge caching (Cloudflare, Akamai, AWS CloudFront)**: aggressively tune windows (`rmem_max` 6-64 MB, autotune) so a single connection to an origin saturates WAN links — BDP math drives every buffer setting.
- **WAN acceleration / file transfer (Aspera, IBM, S3 large uploads)**: long fat pipes (satellite, transoceanic) are *pure window problems* — their whole business is bigger-than-default windows (and often UDP-based replacements precisely because TCP's window default underperforms).
- **Cloud networking (AWS/Azure/GCP)**: documented best practices = raising `rmem_max`/`wmem_max`, enabling window scaling, and matching buffers to BDP for EBS/EFS/S3 transfers; NAT gateways and ALBs advertise tuned windows.
- **Proxy / API gateways (Envoy, nginx, HAProxy)**: they buffer between fast origins and slow clients — their `proxy_buffering`, socket buffer sizing, and connection limit tuning *is* flow control engineering.
- **Databases (Postgres, MySQL, Redis)**: large result sets / replication are window-bound; DBAs tune `wmem`/`rmem` and check `ss -tin` when WAL/replication streams lag.

## 17. References
- RFC 9293 §3.8.1 — flow control & window semantics: https://www.rfc-editor.org/rfc/rfc9293
- RFC 7323 — Window Scale, SACK, timestamps: https://www.rfc-editor.org/rfc/rfc7323
- RFC 813 — Nagle (sender coalescing, SWS mitigation).
- RFC 1122 §4.2.3 — host requirements (Clark's solution).
- Linux docs: `Documentation/networking/ip-sysctl.rst` (tcp_rmem/tcp_wmem, window scaling).
- Kurose & Ross, *Computer Networking*, Ch. 3 §3.5.4 (principles of flow control).

## 18. Cheat Sheet
- rwnd = advertised free receive buffer (Window field × 2^wscale).
- Effective window = min(rwnd, cwnd). Flow = receiver; congestion = network.
- In-flight ≤ rwnd always; ACKs slide the window forward.
- Throughput ≈ window / RTT; window must be ≥ BDP to fill the pipe.
- BDP = bandwidth × RTT (10 Gbps × 40 ms ≈ 50 MB).
- Window field 16 bits (64 KB) → wscale ≤ 14 → up to 2^30.
- Zero window → sender stalls + 1-byte window probes (persist timer).
- SWS: Clark (receiver withholds tiny ACKs) + Nagle (sender coalesces).
- Autotune: tcp_rmem/tcp_wmem, rmem_max/wmem_max set the ceiling.
- Debug: `ss -tin` rcv_space, `ss -tan` Recv-Q/Send-Q.

## 19. Quiz
1. Flow control protects: a) the network b) the receiver's buffer c) the sender d) routers → **b**
2. rwnd is carried in: a) options b) Window field c) flags d) checksum → **b**
3. Effective send window = a) rwnd b) cwnd c) min(rwnd,cwnd) d) max → **c**
4. Window scaling max shift: a) 4 b) 7 c) 14 d) 16 → **c**
5. Throughput ≈ a) window×RTT b) window/RTT c) MSS×RTT d) BDP×window → **b**
6. BDP = a) bandwidth×RTT b) bandwidth/RTT c) window/MSS d) MSS/RTT → **a**
7. Zero window means: a) fast b) sender must stop c) no buffer d) RST → **b**
8. Persist timer sends: a) FIN b) window probes c) SYNs d) data → **b**
9. SWS is fixed by: a) Clark + Nagle b) SACK c) wscale d) timestamps → **a**
10. Window field max without scaling: a) 64 KB b) 1 MB c) 1 GB d) 2^30 → **a**

## 20. Flashcards
- **Q: Flow vs congestion control?** → **A:** receiver's buffer (rwnd) vs network (cwnd); effective = min.
- **Q: What is rwnd?** → **A:** receiver's advertised free buffer, Window field × 2^wscale.
- **Q: Sliding window?** → **A:** ≤ rwnd unacked bytes in flight; ACKs slide the budget forward.
- **Q: Throughput bound?** → **A:** window/RTT; need window ≥ BDP.
- **Q: Window scaling?** → **A:** wscale (≤14) → up to 2^30; negotiated at SYN.
- **Q: Zero window handling?** → **A:** stop + window probes on the persist timer.
- **Q: SWS?** → **A:** tiny-window/tiny-segment waste; fixed by Clark + Nagle.
- **Q: Debug slow transfer?** → **A:** check rwnd vs BDP, rmem_max, `ss -tin`.

## 21. Revision
Flow control = receiver-side pacing: rwnd (Window × 2^wscale, up to 2^30) caps unacked bytes in flight; effective window = min(rwnd, cwnd). ACKs slide the window; zero window → persist probes. Throughput ≈ window/RTT, so window ≥ BDP (bandwidth × RTT) is required to fill fast links — that's why rmem/wmem + autotune exist and why small windows silently cap throughput. SWS (tiny windows) fixed by Clark + Nagle; delayed ACK × Nagle = latency interaction. Debug: `ss -tin` rcv_space, Recv-Q/Send-Q.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is TCP flow control?" | 2 How It Works / 7 Formal Definition |
| "Flow control vs congestion control?" | 13 Q&A / 4 Why Not Another Approach |
| "What is the sliding window?" | 13 Q&A / 9 Internal Working |
| "Why is throughput window/RTT?" | 13 Q&A / 8 Example |
| "What is window scaling / BDP?" | 13 Q&A / 6 Real-World Analogy |
| "Zero window / persist timer?" | 13 Q&A / 9 Internal Working |
| "Silly Window Syndrome?" | 13 Q&A / 14 Follow-Up |
| "Slow download — what do you check?" | 13 Q&A / 15 Coding |
| "How do CDNs/proxies tune windows?" | 16 Industry Usage / 13 Q&A |
