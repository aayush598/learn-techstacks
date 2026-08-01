# TCP Segment Structure

> **TL;DR**: The TCP header is a variable-length structure (20-60 bytes) built around **sequence** and **acknowledgment numbers** (32-bit each) that make byte-stream reliability possible; flags mark control segments (SYN/FIN/RST), the Window field advertises flow control, and Options (window scaling, SACK, timestamps) unlock modern throughput.

## 1. Why Does This Exist?
TCP's core promise — a *reliable byte stream* between two processes — needs a wire format that can express: which byte is this segment carrying (sequence number), which byte I'm expecting next (acknowledgment), how much buffer I have left (window), control transitions (SYN/FIN/RST), and negotiated capabilities (options). The header *is* that contract. Every design decision in TCP's 40-year history is encoded in these 20-60 bytes: the 32-bit sequence space, the 16-bit window (later scaled), the option field (SACK, timestamps, window scale), and the checksum. Understanding the header is understanding the entire protocol — interviewers probe it because it's the intersection of "protocol design" and "systems engineering."

## 2. How Does It Work?
Header (min 20 bytes, offset 0):
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |        Destination Port       |   0
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                       |   4
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                     |   8
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Data| Resv|C|E|U|A|P|R|S|F|                                  |
| Offset|  |E|C|C|S|S|Y|I|        Window                       |  12
|       |  |N|E|C|H|I|N|N|                                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |       Urgent Pointer          |  16
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (variable)                        |  20
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                     Data (payload)                           |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
- **Src/Dst port (16b each)**: demultiplexing the byte stream to a process.
- **Sequence (32b)**: number of the *first data byte* in this segment (relative to the ISN). Confusingly, SYN/FIN consume one sequence number each even with no payload.
- **Ack (32b)**: the next byte I expect (all data up to ack-1 received) — *cumulative*.
- **Data offset (4b)**: header size in 32-bit words (min 5, max 15 → 60 bytes).
- **Flags (9b)**: NS, CWR, ECE, URG, ACK, PSH, RST, SYN, FIN (from reserved bits). Only ACK is "always on" after the handshake.
- **Window (16b)**: the receiver's advertised free buffer (rwnd) in bytes — scaled by the Window Scale option (up to 2^30).
- **Checksum (16b)**: over pseudo-header (IPs+proto+len) + header + data.
- **Urgent pointer (16b)**: with URG flag (obsolete in practice).
- **Options**: MSS, Window Scale, SACK-permitted, SACK blocks, Timestamps (PAWS + RTTM), NOP padding.

## 3. When Is It Used?
- **Every reliable connection**: HTTPS (443), SSH (22), SMTP (25), database drivers (5432/3306), container runtimes, service meshes — every stream that needs ordering and delivery.
- **The handshake/teardown segments**: SYN, SYN-ACK, ACK, FIN, RST — the header's flags drive the state machine.
- **Performance engineering**: window scaling and timestamps are *the* reason modern TCP reaches line-rate; debugging TCP throughput is debugging these fields.
- **Tooling**: `tcpdump -nn -vvv` prints every field; `ss -tin` shows options like wscale/sack/timestamps negotiated per connection.
- **Kernel tuning**: `net.ipv4.tcp_*` (window scale, SACK, timestamps) change what the header carries.

## 4. Why Wasn't Another Approach Chosen?
- **Why 32-bit sequence numbers instead of per-packet IDs?** A byte stream needs *absolute position* so reassembly is trivial and holes are detectable; 2^32 = 4 GB wraps but TCP's timestamps/PAWS and the SYN-ISN randomization make wrap-safe. Per-packet IDs would break reordering and make ACK cumulative semantics awkward.
- **Why a cumulative ACK (next expected byte) instead of per-packet ACKs?** Cumulative = one number covers all past data, so a single ACK can be lost without harm (any later ACK covers it). Per-packet ACK maps explode and drop messages break the invariant.
- **Why 16-bit window, then Window Scale option?** 64 KB was fine in 1981 but limited high-BDP links; the option (shift up to 14 bits → 1 GB) was added *backwards-compatibly* because it's negotiated at SYN time. Chose option over widening the field to avoid breaking old stacks.
- **Why options instead of fixed fields?** Backwards compatibility: new features (SACK, timestamps, TFO) are opt-in via options; a fixed header would break every old implementation.
- **Why a 16-bit checksum over the whole payload?** One pass, cheap hardware offload, and catches corruption anywhere in the datagram (receiver recomputes). Stronger than a per-header CRC and free on modern NICs.

## 5. Intuition
Imagine a **numbered conveyor belt of cartons (bytes)**: each carton has a stamped number (sequence) so you can reassemble an order that arrives out of order. Your *receiving* assistant shouts the number of the next carton they need ("I have everything up to #500, send #501+") — that's the cumulative ACK. There's a sign at the receiving dock showing how many empty shelves are free (Window) so the sender doesn't overwhelm you. A few cartons are special: SYN = "start a new delivery batch," FIN = "I'm done sending, here's my final carton," RST = "this batch is cancelled, stop." The header is the label stamped on every carton — without it, the conveyor is just a heap of identical boxes.

## 6. Real-World Analogy
**FedEx with page-numbered shipments**: You're sending a 10,000-page book (byte stream). Every page is stamped with its *page number* (sequence) and you tell the recipient "I'll mark the page after the last one you should expect to confirm you got everything up to page X" (ack). The recipient's warehouse says "I have shelf space for 500 pages right now" (window) — you don't ship more than that at once. Special labels: "This is the first page" (SYN) starts the job; "This is the last page" (FIN) closes the job; "Never mind, stop the shipment" (RST) cancels it. The shipper guarantees: if the warehouse says "I got everything through page 200" and you see the page-200 label, every page before it arrived intact — that's the cumulative ACK's power in one sentence.

## 7. Formal Definition
The TCP header (RFC 793/9293) is 20-60 bytes: Source Port, Destination Port (16-bit each), Sequence Number (32-bit, byte position of the first payload byte), Acknowledgment Number (32-bit, next byte expected — valid when ACK flag set), Data Offset (4-bit, header in 32-bit words), Reserved (3-bit), NS/CWR/ECE/URG/ACK/PSH/RST/SYN/FIN control bits (9-bit), Window (16-bit, receiver's rwnd, possibly shifted by Window Scale), Checksum (16-bit, over pseudo-header+header+data), Urgent Pointer (16-bit, with URG). Options include MSS, Window Scale (max 14-bit shift), SACK-permitted, SACK blocks, Timestamps (TSval/TSecr, enabling PAWS and RTT measurement), TFO, and NOP alignment. Data follows the header.

## 8. Example
A real SYN-ACK on a web connection (tcpdump):
```
$ sudo tcpdump -nn -i eth0 'tcp[13] & 2 != 0' -v   # SYN-ACKs only
IP 10.0.0.5.443 > 192.168.1.10.54321: Flags [S.],
    seq 3000000000, ack 1000000001, win 65535,
    options [mss 1460,sackOK,TS val 12345 ecr 54321,
             nop,wscale 7], length 0
```
Reading the header: src port 443, dst 54321; SYN+ACK flags (`.` = ACK, `S` = SYN); seq=3000000000 = the *server's* initial sequence number (random ISN); ack=1000000001 = "I confirm your SYN at seq 1000000000; expect your next byte at 1000000001"; win 65535 (scaled ×128 by wscale 7 → effective 8 MB); options: MSS 1460, SACK OK, timestamps for RTT/PAWS, window scale 7. Length 0 — no payload, just the header. Every field is doing a specific job.

## 9. Internal Working
1. **Sequence/ack bookkeeping**: sender numbers each byte (starting at ISN). Every segment carries `seq = first byte's number`. Receiver tracks `rcv_nxt` (next expected) and ACKs it — cumulative, so "ack=N" means "all bytes < N received."
2. **SYN/FIN consume a seq**: SYN(seq=ISN) → peer ACKs ISN+1 (SYN counts as byte 0). Same for FIN. Data offset 4 bits × 4 = header size; a segment can carry options and no data.
3. **Window scaling**: negotiated at SYN (wscale). Effective window = `Window × 2^wscale` (max 2^30). Without it, throughput capped at 64 KB/RTT ≈ ~50 Mbps at 10 ms — scaling is *why* 10+ Gbps is reachable.
4. **Timestamps option**: TSval (sender's clock) + TSecr (echo of peer's TSval) → precise RTT sampling (RTTM) and PAWS (protect against wrapped sequence numbers).
5. **SACK**: SACK-permitted negotiated; on loss, receiver sends SACK blocks listing out-of-order ranges so the sender retransmits only the *gaps*, not everything.
6. **Checksum compute/verify**: on send, sum pseudo-header (IPs+protocol=6+TCP len) + header + data (with checksum field 0), ones' complement; receiver recomputes — mismatch = drop silently (counters in `netstat -s`).
7. **MSS option**: advertised maximum segment size (usually MTU - 40 = 1460 at 1500 MTU) so senders don't fragment; the *only* thing preventing gratuitous fragmentation in TCP.
8. **Flags drive the FSM**: ACK always-on after handshake; PSH flushes the send buffer; RST aborts; SYN/FIN enter/leave the connection; ECE/CWR signal ECN (congestion marking echo).

## 10. Time Complexity
- **Header processing**: O(1) per segment — a few field reads + checksum + queue ops; NIC offload (TSO, checksum) moves it to hardware at line rate (100+ Gbps).
- **Memory**: ~1 KB per connection in the kernel + autotuned buffers (a few MB each for high-BDP) + the reassembly tree for out-of-order data (SACKed gaps).
- **Sequence arithmetic**: modular 32-bit — "wraps around" every 4 GB; the 2.5-byte/second rule of thumb at the 1981 speed, today's PAWS handles wrap.
- **Option parsing**: linear, bounded (max 40 bytes of options) — effectively O(1).
- **The real cost is algorithmic, not CPU**: slow start (exponential ramp) + AIMD (linear + halve) define *how fast* data flows — throughput ~ min(rwnd, cwnd)/RTT.

## 11. Advantages
- **Reliability for free (kernel-level)**: ordering, retransmission, duplicate suppression, checksum — apps don't reimplement any of it.
- **Byte-stream abstraction**: apps read/write a stream; TCP handles segmentation/buffering. Clean API.
- **Flow + congestion control**: doesn't overwhelm receiver or network; self-pacing, fair, and efficient on modern links (CUBIC/BBR).
- **Battle-tested**: 40+ years, every edge case (half-open, simultaneous open, wrapped seq) studied; kernel implementations are extremely mature.
- **Path-mtu discovery, ECN, SACK**: the option space evolves without breaking old hosts.

## 12. Disadvantages
- **Head-of-line blocking**: one lost segment stalls all later bytes — brutal for multiplexed streams (HTTP/2 on TCP; the big reason for QUIC).
- **Latency floors**: handshake (1 RTT) + slow start ramp; on long RTTs that's a real startup tax. (TFO/TLS 1.3 help.)
- **Kernel-bound**: tuning, versions, and per-connection cost are OS-dependent; no app-level control over timing (which is why QUIC/UDP exists).
- **AIMD sawtooth + bufferbloat**: classic TCP fills router buffers → latency spikes (mitigated by CUBIC/BBR + AQM).
- **Overkill for real-time/loss-tolerant**: ordering+retransmission for data that's useless when late (games, video) is pure overhead.

## 13. Interview Questions
1. **Q: Minimum and maximum TCP header size?** A: 20 bytes fixed, up to 60 bytes with options (Data Offset max 15 × 4 bytes).
2. **Q: What does the sequence number mean?** A: The byte number of the first data byte in this segment. It's 32-bit, starting at the connection's random ISN; SYN and FIN each consume one sequence number.
3. **Q: What does the acknowledgment number mean?** A: The next byte the receiver expects — "I have received everything up to ack-1." It's *cumulative*: one number acknowledges all prior data.
4. **Q (tricky): A segment has no data. Does its seq matter?** A: Only SYN/FIN (and RST) consume sequence numbers without data; plain ACK-only segments carry seq but advance nothing.
5. **Q: What is the Window field?** A: The receiver's advertised free receive buffer (rwnd) in bytes — the flow-control signal. With Window Scale (shift up to 14), effective window up to 2^30 bytes (1 GB).
6. **Q (FAANG): Why is window scaling needed?** A: Without it, max window = 64 KB → throughput ≤ 64 KB/RTT (~50 Mbps at 10 ms RTT). Scaling multiplies the advertised window so high-BDP links (10 Gbps, 100+ ms) actually fill the pipe: window ≈ BDP = bandwidth × RTT.
7. **Q: Name the TCP flags.** A: URG, ACK, PSH, RST, SYN, FIN (+ ECE, CWR, NS). SYN/FIN for setup/teardown, RST to abort, ACK acknowledges, PSH flushes.
8. **Q: What is the MSS option?** A: Maximum segment size (usually MTU - 40 = 1460) — tells the peer the largest payload without fragmentation. It's why TCP doesn't fragment in practice.
9. **Q: What does the checksum cover?** A: Pseudo-header (src/dst IP, protocol=6, TCP length) + TCP header + data. Detects corruption *and* misdelivery across IP+TCP.
10. **Q (tricky): How does the receiver know where the header ends?** A: The Data Offset field (4 bits, ×4 bytes). Min 5 (20 bytes), max 15 (60 bytes) — options are between header and data.
11. **Q: What are TCP timestamps used for?** A: RTT measurement (TSecr echo) and PAWS (Protect Against Wrapped Sequence numbers) — old segments can't be mistaken for new ones when seq wraps.
12. **Q (production): What is SACK and why does it matter?** A: Selective ACK — the receiver reports exact out-of-order byte ranges (SACK blocks), so the sender retransmits *only the gaps* instead of everything after the first loss. Massive win on lossy links; without it, one loss forces a full retransmission of the tail.
13. **Q: What's the difference between rwnd and cwnd?** A: rwnd = receiver's advertised window (flow control, in the header); cwnd = sender's congestion window (network safety, in the kernel). Effective send window = min(rwnd, cwnd).
14. **Q (FAANG): What limits TCP throughput?** A: Throughput ≤ min(rwnd, cwnd)/RTT. If you want more: raise buffers (rwnd), avoid loss (cwnd collapse), lower RTT, and use window scaling. The BDP formula: window_size = bandwidth × RTT.
15. **Q: What does the Urgent pointer do?** A: Marks urgent data (with URG flag) for immediate delivery ahead of the stream — essentially obsolete in practice (RFC 6093 discourages it).
16. **Q: How do you inspect a TCP header in practice?** A: `tcpdump -nn -vv -i eth0 'tcp[13] & 2 != 0'` (SYN-ACKs), `ss -tin` (per-connection options: wscale/sack/timestamps), Wireshark's "TCP Segment Len / window" columns.
17. **Q (tricky): Why is the Window field only 16 bits if we need more?** A: Historical (1981 hardware). The fix is backwards-compatible: the Window Scale *option* negotiated at SYN shifts the field. Old stacks just don't advertise scaling — still interoperable.

## 14. Follow-Up Questions
1. **Q: What is "sequence number wrap" and PAWS?** A: After 4 GB of data the 32-bit seq wraps to 0; a delayed old segment could then be mistaken for new. PAWS uses timestamps to reject segments whose TSval is old — the standard fix since RFC 7323.
2. **Q: How does TSO/GRO offload interact with the header?** A: The NIC segments a large send into header-correct segments (TSO) and reassembles inbound segments (GRO) in hardware — the CPU sees fewer, larger segments; the header math is done by silicon.
3. **Q: Why does the header carry a "data offset" instead of a length?** A: TCP is a byte stream — total length is implied by the IP length minus header; only the *header's* length varies (with options), so only it needs encoding. UDP's length field exists because UDP is datagram-based.
4. **Q: What is ECN and how is it signaled in the header?** A: Explicit Congestion Notification: routers set the CE bit (in the IP ECN field); the receiver echoes it via the ECE flag; the sender halves cwnd and stops on CWR. Cooperation between IP + TCP header flags.
5. **Q (tricky): Can a single TCP segment carry both SYN and data?** A: Not in standard TCP — a SYN segment has length 0 (data-less); "TCP Fast Open" (TFO) sends a small cookie+data with the SYN in a backwards-compatible option. Saves the handshake RTT for repeat connections.

## 15. Coding Example
```python
# Parse the TCP header fields of a captured packet (no libraries)
import socket

def parse_tcp(pkt):
    if len(pkt) < 20:
        return None
    src, dst = socket.ntohs(struct_uint16(pkt, 0)), socket.ntohs(struct_uint16(pkt, 2))
    seq, ack = struct_uint32(pkt, 4), struct_uint32(pkt, 8)
    data_offset = (pkt[12] >> 4) & 0x0F          # header length in 32-bit words
    flags = pkt[13]
    win = socket.ntohs(struct_uint16(pkt, 14))
    print(f"src={src} dst={dst} seq={seq} ack={ack} "
          f"header={data_offset*4}B flags={flags:08b} window={win}")

# stream helper stubs
def struct_uint16(b, o): return int.from_bytes(b[o:o+2], "big")
def struct_uint32(b, o): return int.from_bytes(b[o:o+4], "big")

parse_tcp(bytes([0x00,0x50, 0x01,0xBB,  0,0,0,1,  0,0,0,0,  0x50,0x02,  0xFF,0xFF,  0,0,0,0]))
# -> src=80 dst=443 seq=1 ack=0 header=20B flags=00000010 window=65535
```
```bash
# Watch header fields live on a real connection
$ sudo tcpdump -nn -i eth0 'tcp port 443' -vvv | head
#   ... Flags [S.], seq 3000000000, ack 1000000001, win 65535,
#   options [mss 1460,sackOK,TS val 123 ecr 456,nop,wscale 7], length 0
$ ss -tin                          # per-connection: cwnd, rwnd, wscale, sack
```

## 16. Industry Usage
- **The entire web**: HTTP/1.1, HTTP/2, and TLS all ride TCP (443). Nginx, Envoy, Cloudflare, AWS — TCP tuning (window scaling, buffers, CUBIC) is the difference between 1 Gbps and 8 Gbps per connection.
- **Data planes**: databases (Postgres/MySQL on 5432/3306), object storage (S3 on HTTPS/TCP), message queues (Kafka), container networking (CNI), service meshes — everything reliable is TCP.
- **The transport "crown jewels"**: Netflix/Youtube on-demand video (TCP + CDN), SSH/shells, file transfers (SFTP/FTPS), email — all byte-stream consumers.
- **Kernel engineering**: Linux `net.ipv4.tcp_*` sysctls, CUBIC/BBR selection, DCTCP in datacenters, `tc`/AQM (fq_codel) — the header is what every router/host-level algorithm reads.
- **Tooling industry**: Wireshark, tcpdump, mtr, `ss`, `tcptrace` all parse the header; Cloudflare/Google publish TCP-debugging postmortems using exactly these fields.

## 17. References
- RFC 793 — TCP original: https://www.rfc-editor.org/rfc/rfc793
- RFC 9293 — TCP (obsoletes 793, consolidated): https://www.rfc-editor.org/rfc/rfc9293
- RFC 7323 — Window scale + timestamps + SACK: https://www.rfc-editor.org/rfc/rfc7323
- RFC 2018 — SACK: https://www.rfc-editor.org/rfc/rfc2018
- RFC 7413 — TCP Fast Open: https://www.rfc-editor.org/rfc/rfc7413
- Kurose & Ross, *Computer Networking*, Ch. 3 §3.5 (TCP segment structure).

## 18. Cheat Sheet
- Header: 20-60 B = src(16) dst(16) seq(32) ack(32) dataoff(4)+resv+flags(12) win(16) cksum(16) urg(16) + options.
- seq = first data byte's number; SYN/FIN each consume one seq.
- ack = next expected byte; cumulative.
- Flags: URG ACK PSH RST SYN FIN (+ECE CWR NS).
- Window = advertised rwnd; scaled ×2^wscale (max 2^30).
- Options: MSS(1460), wscale(≤14), SACK, Timestamps (RTTM+PAWS), TFO.
- Checksum over pseudo-header+header+data.
- Throughput ≈ min(rwnd,cwnd)/RTT; BDP = bandwidth×RTT.
- `ss -tin`, `tcpdump -vvv` to inspect.

## 19. Quiz
1. Min TCP header: a) 20 b) 8 c) 40 d) 60 → **a**
2. seq number is: a) packet count b) byte number of first payload byte c) a counter d) unused → **b**
3. Cumulative ACK means: a) per-packet b) next expected byte covers all prior c) only last c) window → **b**
4. Window field is scaled by: a) MSS b) wscale option c) PSH d) never → **b**
5. Which flag is set on nearly every post-handshake segment? a) SYN b) RST c) ACK d) FIN → **c**
6. SACK enables: a) bigger windows b) selective retransmission c) fast open d) pacing → **b**
7. Data Offset field units: a) bytes b) 32-bit words c) bits d) MTU → **b**
8. Max header with options: a) 20 b) 40 c) 60 d) 64 → **c**
9. PAWS uses what to prevent seq-wrap confusion? a) MSS b) timestamps c) SACK d) flags → **b**
10. Effective send window = a) rwnd b) cwnd c) min(rwnd,cwnd) d) max → **c**

## 20. Flashcards
- **Q: TCP header fields?** → **A:** src/dst port, seq, ack, dataoff, flags, window, checksum, urgent, options.
- **Q: What does seq number encode?** → **A:** byte position of the segment's first data byte (32-bit, from ISN).
- **Q: Cumulative ACK?** → **A:** ack = next expected byte; acknowledges everything before it.
- **Q: Window scaling?** → **A:** wscale option shifts window; max 2^30 bytes → high-BDP throughput.
- **Q: Flags?** → **A:** URG ACK PSH RST SYN FIN ECE CWR NS.
- **Q: MSS default?** → **A:** MTU − 40 = 1460 at 1500 MTU.
- **Q: SACK?** → **A:** selective ack ranges → retransmit only gaps.
- **Q: PAWS?** → **A:** timestamps reject wrapped-seq old segments.

## 21. Revision
TCP header = 20-60 bytes: ports, 32-bit seq (byte position of first payload byte), 32-bit cumulative ack (next expected), data offset (words), 9 flags, 16-bit window (scaled by wscale up to 2^30), checksum (pseudo-header+header+data), urgent pointer, options (MSS, wscale, SACK, timestamps→RTTM+PAWS, TFO). SYN/FIN consume a seq. Throughput ≈ window/RTT; window scaling unlocks high-BDP links. Inspect with tcpdump -vvv / ss -tin.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What's in the TCP header?" | 2 How It Works / 8 Example |
| "What is the sequence number?" | 13 Q&A / 7 Formal Definition |
| "Why cumulative ACKs?" | 13 Q&A / 4 Why Not Another Approach |
| "Why window scaling / high-BDP?" | 13 Q&A / 9 Internal Working |
| "What does SACK do?" | 13 Q&A / 14 Follow-Up |
| "What limits TCP throughput?" | 13 Q&A / 10 Time Complexity |
| "How do you debug TCP with tcpdump/ss?" | 13 Q&A / 15 Coding |
| "How does the header prevent fragmentation?" | 13 Q&A / 8 Example (MSS) |
