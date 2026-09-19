# Network Performance and Troubleshooting — 100 Interview Q&A

## Q1: What is latency?

**A:** Latency is the time delay between when a data packet is sent and when it reaches its destination. It measures the time required for a packet to traverse the network path, typically expressed in milliseconds. Latency is composed of four components: propagation delay (time for the signal to travel through the medium), transmission delay (time to push bits onto the wire), processing delay (time for routers to process the packet), and queuing delay (time spent waiting in router buffers).

Latency is a critical performance metric because it directly affects user-perceived responsiveness. For interactive applications, high latency feels slow even if throughput is excellent. A request that takes 200ms round trip makes an application feel sluggish, while one taking 20ms feels instant. Cloud providers and data centers are often placed close to users precisely to minimize propagation delay.

The physics of propagation delay is unavoidable: light and electrons take time to travel through fiber or copper. A signal crossing the Atlantic incurs roughly 30-40ms of one-way propagation delay just from the physical distance, regardless of how fast the network gear is. This fundamental constraint shapes how distributed systems are architected around latency budgets.

## Q2: What is bandwidth?

**A:** Bandwidth is the maximum rate at which data can be transferred across a network path, typically expressed in bits per second (bps, Kbps, Mbps, Gbps). It represents the capacity of the link, the theoretical upper bound of transmission. Bandwidth depends on the physical and logical characteristics of the network technology: the modulation scheme, the medium, and the link aggregation.

Bandwidth is often confused with throughput, but they differ: bandwidth is what the link can carry (capacity), while throughput is what it actually carries (utilization). A 1 Gbps link has 1 Gbps of bandwidth, but if only 300 Mbps of traffic flows across it, the throughput is 300 Mbps. The phrase "bandwidth is the pipe size, throughput is the water flowing through it" captures the distinction.

The bandwidth of a path is determined by the slowest link in the chain, the "bottleneck link." This is why upgrading a LAN connection doesn't help if the internet connection is the constraint. Understanding bandwidth requires knowing both the capacity and how that capacity is shared across all concurrent flows on the path.

## Q3: What is throughput?

**A:** Throughput is the actual rate at which data is successfully transferred between sender and receiver over a network, expressed in bits or bytes per second. It measures real-world data transfer performance, reflecting the effective capacity after accounting for headers, retransmissions, congestion, and other overhead. Throughput is always less than or equal to bandwidth.

Throughput is affected by many factors: the bandwidth of the bottleneck link, latency, packet loss, protocol overhead, buffer sizes, and the performance of the end hosts. For TCP, throughput is heavily influenced by congestion control, which governs how aggressively the sender transmits based on network conditions. Application-level features like compression or caching can effectively improve useful throughput beyond the raw network throughput.

Measuring throughput reliably requires differentiating application-layer throughput (goodput, the useful data the application receives) from transport-layer throughput (including TCP/IP headers and protocol data). When troubleshooting, comparing observed throughput to expected bandwidth is the first step in identifying whether a performance problem exists and where it lies.

## Q4: What is the relationship between latency, bandwidth, and throughput?

**A:** Latency, bandwidth, and throughput are interdependent but measure different aspects of network performance. Latency measures time delay, bandwidth measures the maximum capacity of the link, and throughput measures the actual achieved data rate. A path with high bandwidth but high latency may still have poor throughput if the protocol can't fill the pipe (e.g., TCP's window limits throughput to roughly window size divided by RTT).

The fundamental relationship is captured by the bandwidth-delay product (BDP), which is bandwidth multiplied by RTT. The BDP represents how much data can be "in flight" on the link at any moment. If the sender's window is smaller than the BDP, throughput is limited by window size, not bandwidth. This is why high-latency, high-bandwidth paths (like satellite links or cross-continental fiber) need large windows and effective congestion control.

In practice, throughput is bounded by the minimum of bandwidth and the BDP constraint, further degraded by packet loss and queueing delays. A simple view: throughput cannot exceed the bottleneck link's bandwidth, and it cannot exceed what the window/RTT math permits. Troubleshooting performance always involves disentangling these three constraints to find which one is binding.

## Q5: What is RTT?

**A:** Round-trip time (RTT) is the time it takes for a packet to travel from a sender to a receiver and for the acknowledgment to travel back. It measures the full round trip of one request-response exchange, expressed in milliseconds. RTT includes all four latency components (propagation, transmission, processing, queuing) in both directions plus any server processing time.

RTT is the key metric that governs TCP behavior. TCP's throughput ceiling is roughly window size divided by RTT, so halving the RTT can double throughput for a given window. RTT also determines timeouts: retransmission timeout (RTO) is calculated from smoothed RTT estimates, and a spiky RTT can cause spurious retransmissions or excessive waits.

Measuring RTT accurately requires care. The ping tool measures RTT at the ICMP level, while TCP RTT can be observed via tools like ss or instrumentation. One-way delay (OWD) is even more useful for pinpointing direction-specific problems, since asymmetric network paths often have very different delays in each direction. RTT is also a moving target, varying with load and queueing, so percentiles (p50, p95, p99) are needed to understand the distribution.

## Q6: What is TTFB?

**A:** Time to First Byte (TTFB) is the duration from when a client sends a request until it receives the first byte of the response. TTFB aggregates the entire request path: DNS resolution, TCP connection establishment, TLS handshake, request transmission, server processing time, and the first byte of response traveling back. It is a crucial web performance metric that directly influences perceived page load speed.

A slow TTFB can stem from multiple layers: slow DNS resolution, packet loss inflating the TCP handshake, TLS negotiation overhead, server-side processing delays, or network congestion along the path. Isolating TTFB components requires measuring each stage separately. Tools like curl can break down the timings (name lookup, connect, TLS handshake, first byte) when verbose timing is enabled with the `--trace-time` or `-w` output options.

Optimizing TTFB involves reducing the number of network round trips (protocol optimizations, connection reuse, HTTP/2 multiplexing), moving the server closer (CDN), and improving server processing such that the first byte is generated quickly. TTFB is a sensitive indicator: it catches network issues, server issues, and application issues in a single number, making it a great first-line diagnostic.

## Q7: What is packet loss?

**A:** Packet loss is the percentage of packets that fail to reach their destination, typically resulting in retransmission or application errors. It can be caused by buffer overflow in routers (congestion), bit errors on the physical medium, signal interference, hardware failures, or deliberate dropping (policing, firewalls, bad links). Packet loss is a critical indicator of network health.

Even small amounts of packet loss dramatically degrade throughput. For TCP, a single lost packet can halve the congestion window, and with Reno-style congestion control, every loss event causes an immediate window reduction. Approximately 1% loss on a high-bandwidth, high-latency path can cut achievable throughput to a fraction of the available bandwidth, while 5-10% loss often renders the path nearly unusable for bulk transfers.

Measuring packet loss requires interpreting subtle signals. ICMP ping loss may not reflect TCP/UDP loss through the same path (filters often treat ICMP differently). TCP loss is observable through retransmission counters and TCP statistics. Since loss is often bursty and correlated (loss events cluster during congestion), measuring loss over time windows and at different layers yields a more accurate picture than a single percentage.

## Q8: What is a retransmission?

**A:** A retransmission is the resending of a packet that was not acknowledged within a timeout or was negatively acknowledged. TCP retransmits when the retransmission timeout (RTO) expires without receiving an ACK, or when duplicate ACKs signal that later packets arrived but the specific packet was lost (fast retransmit). Retransmissions ensure reliable delivery but consume bandwidth and add latency.

Retransmission behavior contains rich diagnostic information. Retransmission gaps (multiple consecutive retransmissions, or retransmitting many packets at once) often indicate a lost connection or severe congestion. Spurious retransmissions (retransmitting packets that actually arrived, just late) point to RTT estimation problems or excessive jitter. The `Retrans` counter in netstat/ss and the retransmission flags in packet captures reveal these patterns.

The retransmission rate (retransmits divided by total packets sent) is a key performance health metric. Sustained retransmission rates above a fraction of a percent typically indicate real network problems worth investigating. Retransmissions also create spikes in effective RTT for the reassembled stream, which can be visible to users as stalls. Telling retransmissions vs. reordering apart (both produce duplicate ACKs) requires looking at the packet sequence numbers in a capture.

## Q9: What is a network bottleneck?

**A:** A network bottleneck is the component in a data path that limits overall throughput or latency, the slowest or most constrained element among the chain. In a multi-hop path, the bottleneck link determines the maximum attainable throughput for flows traversing it, per the "slowest link" principle. Bandwidth bottleneck applies to bulk data transfers; latency bottleneck applies to interactive traffic.

Identifying bottlenecks requires measuring each component rather than guessing. The bottleneck is often not the link with the lowest nominal bandwidth but the one with the most congestion, worst buffering, or highest error rate. A WAN link, a NIC's queue, a CPU-bound router, or even the receiving host's kernel stack can all act as the effective bottleneck.

Bottlenecks are dynamic: they shift with traffic patterns, time of day, and application behavior. A path may be bandwidth-limited at peak hours but latency-limited in the middle of the night. Systematic bottleneck identification uses tools like mtr (to see where loss/delay appears along the path), iperf (to measure per-hop achievable throughput), and TCP statistics to see which resource is saturated when approaching the limit.

## Q10: What is queuing delay and queueing?

**A:** Queuing delay is the time a packet spends waiting in a router or switch's buffer before being transmitted. When packets arrive faster than a link can drain them, they accumulate in buffers, adding delay. The longer the queue, the longer the delay; each packet traversing the queue waits for all packets ahead of it to be transmitted.

Queueing theory describes this dynamic in terms of utilization and arrival patterns. As link utilization approaches 100%, queueing delay grows non-linearly and approaches infinity. Even at moderate utilization, bursty arrival patterns create queue spikes. Queues also cause packet loss when they overflow, and under FIFO discipline they cause head-of-line blocking. The average queue depth correlates with delay, and its variance produces jitter.

Queueing delay is a central concept in performance troubleshooting because it explains the paradox of a link that is "fast" (high bandwidth) yet "slow" (high latency). A saturated 10 Gbps link can introduce hundreds of milliseconds of queueing delay for interactive packets behind bulk transfers. The TCP "bufferbloat" problem is exactly this: excessive buffering that hides congestion signals while creating massive delays.

## Q11: What is the bandwidth-delay product (BDP)?

**A:** The bandwidth-delay product is the product of the available bandwidth and the round-trip time of a path, expressed in bits (or bytes). It represents the amount of data that can be "in flight" on the network segment at any given moment, the volume of the pipe. If bandwidth is 1 Gbps and RTT is 80ms, the BDP is 1e9 * 0.08 = 80 Mbit = 10 MB.

The BDP is the minimum window size required for a sender to fully utilize the link. If the sender's window is smaller than the BDP, the pipe goes partially empty while the sender waits for acknowledgments, and throughput is window-limited (window/RTT) rather than bandwidth-limited. This is the classic "high bandwidth x high delay" problem that requires window scaling and effective congestion control.

The BDP also drives buffer sizing requirements. The standard guidance is that a router's buffer should be at least the BDP to avoid losing a full window of data during congestion; the more modern guidance (RFC 3819) cautions against excessively large buffers that cause bufferbloat. Calculating the BDP for a path is a first step when tuning TCP parameters or choosing congestion control algorithms.

## Q12: What is network buffering and bufferbloat?

**A:** Network buffering is the use of memory in network devices (and end-host stacks) to hold packets during transient congestion. Buffers smooth out bursts, preventing packet loss when arrival rates temporarily exceed departure rates. However, the amount of buffering is a design choice with serious trade-offs, and too much buffering creates "bufferbloat."

Bufferbloat is the pathological situation where buffers are so large that they absorb congestion signals while imposing enormous latency. Instead of dropping packets to signal congestion (which triggers TCP to slow down), bloated buffers let queues grow, adding milliseconds or even seconds of delay for interactive traffic while bulk flows continue saturating the link. The result is consistently high latency on otherwise healthy links.

Detecting and fixing bufferbloat requires measuring latency under load. Measuring RTT when the link is idle vs. when it's saturated reveals the queueing component. Modern mitigation uses active queue management (CoDel, fq_codel, PIE) to control queue depth and produce timely congestion signals, while sender-side algorithms like BBR try to stay at the queue-free operating point. Bufferbloat troubleshooting is a core part of web performance work.

## Q13: What is jitter?

**A:** Jitter is the variation in latency over time, the consistency of packet delivery timing. It's calculated as the difference between consecutive packet delays. For interactive real-time applications (voice, video, gaming) jitter matters more than average latency, because uneven arrival disrupts playback far more than uniformly higher delay.

Jitter is caused by variable queuing delays, route changes, shared medium contention, and scheduling variability in hosts and network equipment. The distribution of jitter (spikes vs. smooth variation) reveals its origin: burst bursts of packets queuing behind bulk transfers indicate buffer contention, while periodic jitter often points to routing or medium issues.

Measuring jitter requires time-stamped packet streams, either through ICMP sequences (ping statistics show min/avg/max and standard deviation) or through real-time transport measurements (RTP jitter is standardized). Tools like iperf measure jitter for UDP streams. Troubleshooting jitter involves checking for queueing, contention, and route stability along the path.

## Q14: What is goodput?

**A:** Goodput is the application-level throughput, the rate of useful data delivered to the application, excluding protocol headers, retransmissions, and overhead. While throughput measures data rate at the transport or network level, goodput measures what the application actually receives. TCP transfer tools and HTTP downloads typically report goodput.

The difference between throughput and goodput comes from overhead: TCP/IP headers consume bandwidth, retransmissions consume bandwidth without delivering new data, and protocol inefficiencies (small packets, inefficient window usage) reduce useful data delivered. On high-latency paths without enough in-flight data, throughput can be good while goodput is terrible because the application is idle waiting.

When users report "slow downloads," they're usually describing goodput. Distinguishing goodput loss (bad UDP/TCP retransmission caused degradation), raw bandwidth loss (link limits), and protocol overhead is the core of performance debugging. Measuring goodput requires application-level instrumentation, correlating bytes delivered with elapsed time.

## Q15: What is network congestion?

**A:** Congestion is the state where demand for a network resource (usually link bandwidth) exceeds supply, causing queues to grow. Congestion manifests as increased latency (queueing delay), packet loss (buffer overflow), and reduced throughput (because of congestion feedback mechanisms like TCP window reduction). Congestion is the fundamental performance killer in real networks.

Congestion is dynamic and often asymmetric. A path can be congested for one direction and idle for the other. The collapse risk is severe: without proper congestion control, senders in a congested network retransmit aggressively, increasing load further, which causes more losses, leading to congestion collapse. TCP's congestion control algorithms exist to prevent this and share capacity fairly.

Troubleshooting congestion means determining both its existence and its location. Packet loss rates, RTT inflation, and TCP's congestion window behavior (visible through ss or captures) reveal congestion and its severity. Distinguishing self-congestion (the host is overloading the link) from cross-traffic congestion (other flows are claiming the capacity) shapes the fix: the former is a capacity/tuning issue, the latter possibly a traffic management or capacity planning question.

## Q16: What does the ping tool do?

**A:** Ping uses ICMP Echo Request and Echo Reply messages to test host reachability and measure RTT. When you invoke `ping`, the sender sends ICMP echo packets to the target; when the target receives one it replies with an echo reply, and the elapsed time provides the RTT. Ping reports per-packet RTT as well as min/avg/max/stddev statistics and a loss percentage.

Ping is a first-line connectivity and latency tool. Its value comes from its simplicity and platform ubiquity, and its coverage of protocol-level reachability. However, modern network environments often rate-limit or filter ICMP, so ping success or failure must be interpreted carefully for hosts behind firewalls, and ICMP loss doesn't always equal TCP loss through the same path.

For troubleshooting, ping helps answer: is the host reachable? Is the path lossy? Is the latency stable or does it spike? Multi-target pinging (from multiple vantage points) is a classic technique for isolating whether a problem is host-specific or path-specific. Ping's RTT is also the basic input for BDP and timeout calculations.

## Q17: What does traceroute do?

**A:** Traceroute reveals the path and per-hop delay across the network towards a destination. It works by sending packets with increasing Time-to-Live (TTL) values: TTL=1 expires at the first router, which returns a "Time Exceeded" ICMP message that reveals the first hop; TTL=2 reveals the second hop, and so on until the destination. Each hop's RTT is measured, showing per-hop latency into the path.

Traceroute output is read as a sequence of hops with three RTT samples each. High delay or packet loss symbols (*) at a specific hop may indicate a problem point, but interpretation requires nuance: unresponsive routers often still forward traffic (firewalls silently discard expired packets), so stars don't automatically mean a broken link. Latency accumulation across hops must also be interpreted carefully since queueing and ICMP prioritization vary.

Modern traceroute takes many forms: ICMP-based (classic), UDP-based (default Linux), TCP-based (like tcptraceroute for firewall-traversed paths). The tool mtr combines continuous traceroute with ping-style measurement, giving a live per-hop picture that update each second, which makes path problems dramatically easier to observe.

## Q18: What does iperf do?

**A:** Iperf is a bandwidth measurement tool that generates controlled traffic between two hosts to measure achievable throughput. It supports both TCP and UDP modes: TCP mode measures the maximum achievable TCP throughput and can reveal protocol-limiting factors (window limits); UDP mode measures raw packet delivery, packet loss, and jitter at configured rates.

The classic methodology runs iperf server on one host and iperf client on the other, measuring in one direction, then reversing to test the return path. The "-P" parallel stream mode and "-w" window configuration let you test how many streams and what window size affect throughput. Running iperf between successive pairs of hosts along a path isolates each segment's achievable bandwidth.

Reading iperf results requires comparing against the expected bandwidth and RTT. If a single TCP stream achieves far less than the link bandwidth but multiple parallel streams achieve more, congestive limits (like BDP) or congestion control behavior is involved. In UDP mode, increasing the send rate until loss appears reveals the link's realistic maximum capacity.

## Q19: What does mtr do?

**A:** MTR (My Traceroute) combines traceroute's hop-by-hop path discovery with continuous ping-style measurement at every hop in real time. It displays each hop with continuously updated loss% and RTT statistics, allowing you to watch path and latency behavior evolve. This makes mtr far more powerful than a single traceroute snapshot for diagnosing transient problems.

Reading an mtr report: columns show hop, host, loss%, sent packets, and recent min/avg/max/stddev RTT. A hop showing high loss combined with subsequent hops showing low loss often indicates that the lossy router deprioritizes or drops the probing traffic (ICMP rate limiting), not an actual data-path problem. Sustained loss and high latency at a consistent hop are meaningful signals of a real bottleneck or fault.

MTR is the tool of choice for reporting network issues to ISPs and cloud providers because it provides per-hop evidence compactly. Running mtr from both directions (client and server) identifies asymmetric problems: a path may be healthy client-to-server but bad server-to-client, which a single-direction mtr misses.

## Q20: What does netstat do?

**A:** Netstat prints network connections, routing tables, interface statistics, and various protocol statistics. It shows active connections (with local and remote addresses, state, and for TCP the send/recv queues), network interfaces (with byte/error counters), and protocol-level counters including TCP retransmissions, resets, and segment statistics.

Its primary role in performance troubleshooting is connection and statistics observation: identifying established vs. stuck connections, checking the current queue sizes (a large Recv-Q with a small connection often indicates a stalled receiver reading), and glancing at protocol counters. The `netstat -s` output shows aggregate TCP/IP counters, and the `-i` output shows per-interface packet and error counts, giving a first clue about interface-level loss.

Modern Linux strongly recommends `ss` as a replacement (netstat is Deprecated and often a wrapper for ss), but netstat remains common in older environments and on non-Linux systems. When reading netstat output, focusing on actual counters (retransmissions, timeouts, out-of-order arrivals) and queue depths yields the troubleshooting value, rather than the listing of connections alone.

## Q21: What does ss do?

**A:** The `ss` tool (socket statistics) provides a fast, rich view of sockets on Linux systems, explicitly designed to replace netstat. It shows TCP/UDP/UNIX sockets, their connection state, local and remote addresses, and the socket configuration — including send and receive buffer sizes, current window sizes, congestion windows, and RTT estimates for TCP connections.

`ss` is particularly valuable because one command gives you per-connection performance state: `ss -ti` shows for each TCP connection details like cwnd, ssthresh, rtt, rttvar, and retransmit counts; `ss -s` summarizes socket statistics by state; `ss -ni` shows interface-level perd-stat packet/byte counts. This data is authoritative for diagnosing TCP-level throughput and latency behaviors in real time.

Troubleshooting usage includes verifying whether a connection's congestion window is stuck small (indicating congestion-related loss), observing RTT and jitter as seen by the kernel, checking buffer usage, and seeing connections stuck in unusual states. `ss`'s speed and the kernel natively reading from netlink sockets make it the standard diagnostic on any modern Linux server.

## Q22: What does tcpdump do?

**A:** Tcpdump is a packet capture and analysis tool that captures packets as they cross an interface, prints or records their contents according to capture filters, and supports Berkeley Packet Filter (BPF) expressions for targeted selection. It operates at the link layer, reading raw packets, which makes it the ground-truth tool when you need to see exactly what traversed the wire.

Basic tcpdump usage involves choosing an interface (`-i`), setting a filter (host, port, protocol, TCP flags), controlling verbosity (`-v`, `-vv`), limiting count (`-c`), and optionally writing to a pcap file (`-w`) for later analysis with Wireshark. The classic troubleshooting workflow is: capture while reproducing the problem, then analyze the sequence of packets — handshake timings, retransmissions, window evolution, queueing.

Tcpdump allows observing real performance signals: inter-packet gaps (revealing application-level stalls vs. network delays), TCP flag patterns (SYN/SYN-ACK/ACK timing tells handshake cost; retransmissions and duplicate ACKs trace loss/reordering; zero-window ACKs tell a slow receiver). Reading tcpdump output requires understanding TCP flow structure, sequence numbers, and flags.

## Q23: What is packet capture analysis?

**A:** Packet capture analysis is the process of examining raw packet data to understand network behavior, diagnose problems, or verify correct operation. It involves capturing packets at strategic points (usually with tcpdump or network taps), storing them in pcap format, and analyzing them with tools like Wireshark, tshark, or scripting. Analysis reveals the ground truth that summary statistics and counters may obscure.

Analysis focuses on timing (packet arrival gaps, RTT per segment), protocol correctness (flags, sequence integrity), and statistics (retransmit rates, windows, throughput timelines). For TCP, the golden analysis artifacts are: the handshake duration, the presence and pattern of retransmissions/duplicate ACKs, the evolution of send/receive windows, and the inter-packet gap behavior that exposes application stalls vs. network delay.

Capture analysis is both craft and discipline: capture during reproduction, filter to the traffic of interest, examine with due attention to details like TCP segmentation offload and capture-time loss that can create false signals. Wireshark's "Expert Information" and statistics panels (Flow Graph, TCP Stream Graphs, I/O Graph) turn a raw capture into an interpretable story of the problem.

## Q24: What is MTU and why does it matter for performance?

**A:** Maximum Transmission Unit (MTU) is the largest packet size a link or layer can carry. Typical values: Ethernet 1500 bytes, loopback 65536, jumbo frames up to 9000. The MTU determines maximum payload per packet; a single TCP segment is bounded by the path MTU, so the packet count for a given transfer increases inversely with MTU. Wrong MTU causes fragmentation or outright loss.

The standard 1500-byte Ethernet MTU must carry TCP/IP headers, leaving a 1460-byte maximum payload for a TCP segment (IPv4), or 1452 bytes with IPv6. Larger packets amortize per-packet overhead (headers, processing) over more payload, which is why jumbo frames (9000) improve throughput for data-center bulk transfer but bring compatibility risks (path MTU mismatches, silently dropped oversized packets through tunnels).

MTU mismatches are a classic troubleshooting trap: a tunnel or VPN with a lower MTU causes packets sized for the nominal 1500 to be dropped exactly when DF (don't fragment) is set, killing a flow while smaller probes succeed. Symptom: ping succeeds at small sizes and fails above a threshold. Diagnostics use `ip link`, `tracepath`, and ping with specific payload sizes (`-s`) plus the DF bit.

## Q25: What is TCP connection establishment and why does its cost matter?

**A:** TCP connection establishment is the three-way handshake (SYN, SYN-ACK, ACK) required before data can be exchanged. The handshake costs one full RTT of time before the first data byte can be sent — no other protocol work — which is why a TCP connection from a client that has been to a remote endpoint cannot send data sooner than 1 RTT after the SYN. Universities and CDNs optimize this RTT cost.

The three-way handshake RTT cost compounds visibility: any page load in browsers involves one or many TCP handshakes (each adding ≥1 RTT + TLS handshake, which costs another R2 via TLYFP ~2 RTTs). Reducing the number of connections (HTTP/2 multiplexing, connection reuse) and using TCP Fast Open where possible reduces the handshake tax. Troubleshooting "slow first byte" often starts by confirming the handshake completed quickly (look at capture: time from SYN to ACK should be ≈ one network RTT).

Handshake anomalies are diagnostics: SYN retransmissions indicate loss or firewall drops; stretched SYN-ACK delays point to overloaded servers or middle-boxes; SYN floods (many unacknowledged SYNs) indicate a DoS or scan. The handshake's packet timing in a capture is therefore simultaneously a performance factor and a rich diagnostic.


## Q26: How do you interpret ping output to diagnose a problem?

**A:** Ping output consists of per-packet RTT values, a derived summary (min/avg/max/mdev), and a packet loss percentage. Interpretation connects these figures to network conditions. Consistent low RTTs with 0% loss indicate a healthy path; RTTs near the physical propagation minimum for the distance imply no queueing; RTTs far above the minimum reveal congestion or buffering along the path.

Patterns matter more than single values. Consistently high RTT = a persistently loaded path; RTT that grows over time = growing queueing (congestion is building); occasional huge RTT spikes = bufferbloat bursts; RTT varying widely (high mdev) = shared-medium contention or fluctuating load. Loss percentages tell a similar story: 0% is healthy, 1%+ sustained loss begins to hurt throughput, and 5%+ loss typically requires diagnostics.

For deeper interpretation, ping RTTs must be related to the expected floor. For a 100km path, ~1ms RTT is the physics floor; for cross-Atlantic fiber it's ~65-75ms. If average RTT is 3x the floor, queueing is significant. Collecting ping data over time (with timestamps) and comparing against the network's known baseline distinguishes healthy variance from emerging problems.

## Q27: How do you measure network throughput correctly?

**A:** Measuring throughput correctly requires isolating the measured transfer from other system variables and using the right tool for the question. iperf measures raw network throughput; consecutive chunks of an HTTP download measure application-level throughput; file-transfer utilities measure filesystem plus network performance combined. The tool must match the layer being tested.

Methodology matters. Run the measurement for sufficient duration (30-60+ seconds) to get past the slow-start ramp and catch sustained rates. Test in both directions (upstream and downstream). Repeat multiple times and take medians, as one sample is noise. Control other variables: other traffic on the host, CPU load, and interference. For TCP tests, be aware that the receiver's buffer, sender's window, and congestion control can mask or create limits.

Comparisons require a baseline: measure against the expected bandwidth of the link and the BDP-implied ceiling for the RTT. If you expect 1 Gbps and achieve 400 Mbps single-stream, the difference might be TCP tuning or host limits — test with parallel streams to separate relationship between stream count and throughput, then relate that to window and congestion behavior.

## Q28: What is the TCP three-way handshake and how does connection reuse help performance?

**A:** The TCP three-way handshake nests SYN → SYN-ACK → ACK and costs one full RTT before the first data byte can flow, because the sender can't transmit data until the third ACK goes out. For real-time clients, each connection adds one RTT of setup, even before the application does anything. TLS adds yet more round trips (usually one or two) on top of TCP's, which is why the handshake stack costs browsers 2-4 RTTs before any HTTP bytes arrive.

Connection reuse eliminates that cost for subsequent requests: keep-alive connections, HTTP/2 multiplexing (many requests over one TCP connection), and HTTP/3 (QUIC) remove the serialized handshake. Browsers and clients reuse sockets aggressively just for this reason. Server-side, connection pooling reuses sockets across requests, amortizing handshake cost over many transactions and eliminating the per-request RTT tax.

Troubleshooting handshake-heavy systems: look at the time distribution between handshake steps in a capture. SYN-ACK delay spikes indicate server or middle-box issues; SYN retransmits indicate loss or gates. If an application creates many connections per user action, the aggregate handshake RTTs might dwarf the actual transfer time, pointing to a design fix rather than a network fix.

## Q29: What causes TCP retransmissions, and how do you diagnose them?

**A:** TCP retransmissions are caused by packets not being acknowledged: timeout-based (RTO) retransmissions fire when the ACK doesn't arrive by the estimated timeout, while fast retransmission fires after receiving three duplicate ACKs indicating a gap in the outbound sequence. Underlying causes include congestion (dropped packets in routers), bit errors, buffer overflow, reordering (triggering duplicate ACKs without real loss), and NIC/driver issues.

Diagnosing retransmissions begins with the retransmission rate: use `netstat -s` or `ss -s` to find TCP retransmission counters. Then capture packets and look at the exact pattern. Timeout-based retransmits (spacing = the RTO, often 1s, 2s...) with no duplicate ACKs before them suggest an ASYMMETRIC loss path or middle-box behavior; fast retransmits with many duplicate ACKs suggest in-path loss or reordering.

The deeper question is distinguishing loss from reordering, since both produce duplicate ACKs. In a capture, reordering shows the "missing" segment arriving later out of order, whereas actual loss shows a retransmission or retransmission gap. Correlating retransmission events with TCP's SACK, window evolution, and queue behavior distinguishes congestion loss from a broken link — congestion shows tightening windows and queueing; link faults show sudden loss spikes without warning.

## Q30: What is TCP slow start and why does it matter for throughput?

**A:** TCP slow start is the congestion control phase that probes for available bandwidth by increasing the congestion window (cwnd) exponentially starting from a small initial value (often 10 segments). The sender doubles the cwnd per RTT of full acknowledgment, so after n RTTs the window is roughly 2^n times its initial value. This grows the in-flight data until loss or the slow-start threshold (ssthresh) stops the growth.

Slow start matters because the achievable throughput is zero until the window grows to the BDP. On high-bandwidth paths, that ramp takes proportional RTTs: on a 100ms RTT path, a 10-MB BDP connection may take 10+ seconds to fully ramp. The resulting "average throughput over the transfer" is far below the steady-state value for small-or-medium transfers, which is why small transfers on high-latency paths appear slow even with abundant bandwidth.

Diagnostics: watch cwnd per connection with `ss -ti`. If cwnd is pinned near its initial value because loss occurred early, the whole transfer is limited by a loss-and-recovery cycle. Enabling TCP fast retransmit tuning, using the right congestion control, TCP tuning (like increasing the initial window within RFC 6928 limits) and protocol-level connection reuse mitigate the slow-start tax.

## Q31: How does TCP congestion control determine throughput?

**A:** TCP congestion control determines the sending rate as the congestion window (cwnd) divided by RTT, where cwnd evolves in response to congestion signals (losses and, in some algorithms, delay). Classic Reno halved cwnd on loss and grew additively per RTT, producing the sawtooth pattern in a window-over-time graph. Modern algorithms (Cubic, BBR, others) use different signals and heuristics to find the equilibrium between utilization and fairness.

The equilibrium cwnd value (and hence throughput) depends on the algorithm plus the path's packet-loss rate and delay. The well-known formula throughput ≤ (window)/(RTT), and with Reno ≈ sqrt(1.5 * MSS / (loss_rate * RTT)), quantifies how drastically loss and RTT cut throughput regardless of bandwidth. This formula is why "high BDP + small loss" still cripples classic congestion control.

Troubleshooting throughput requires knowing the congestion-control algorithm in use (visible via `ss -info` or sysctl/cap), the cwnd evolution (again `ss -ti`), and RTT/loss observations. If achievable throughput sits far below the link bandwidth while cwnd is small, RTT spikes, and loss appears, the congestion control loop is the limiter — the fix is algorithmic (BBR for BDP-heavy paths) or loss-based (improve the path).

## Q32: What is the difference between packet loss detection and packet reordering?

**A:** Packet loss is a packet that never arrives, while reordering is a packet that arrives out of sequence (later than expected) but does arrive. TCP sees both through the same initial signals: gaps in the received sequence number, generating duplicate ACKs. Failing to distinguish them causes misdiagnosis: reordering triggers the same window-reduction response as loss under classic loss-based congestion control, degrading throughput without any actual packet dropping.

In a capture, loss vs. reordering is distinguished by what happens to the "missing" sequence. For real loss, the segment never arrives; the sender retransmits it (or a later timeout-covered window) and the retransmission appears. For reordering, the segment arrives later, still with its original sequence number and without a retransmission — it's just delayed relative to its siblings. Duplicate-ACK spurious retransmissions (retransmits of packets that then arrive) signal reordering or spurious timeouts.

Detection steps: count and classify retransmissions (genuine vs. spurious), watch duplicate-ACK bursts vs. out-of-order arrivals, and check RTT/IPL anomalies around events. Reordering is common in load-balancing, multipath, and packet-spraying environments where distinct paths have different delays. Distinguishing these matters because the fixes differ: reduce loss by fixing the path, or reduce reordering by routing/scheduling changes and possibly reordering-tolerant congestion control.

## Q33: What role do TCP timers play in throughput?

**A:** The main TCP timers are the retransmission timer (fires at RTO), the delayed-ACK/persist timers, and the keepalive timer. The RTO is computed from the smoothed RTT (SRTT) and RTT variance (RTTVAR), giving an upper estimate that tolerates variance: RTO = SRTT + 4×RTTVAR (with minimums like 200ms-1s per RFC rules). Timeout retransmissions are expensive because the sender idles the full RTO (often ≥ 1s) while waiting.

The RTO's relationship to throughput is direct: each timeout event stalls the flow for the RTO duration and often collapses the key congestion window. If the measured RTT is spiky, the RTO is correspondingly conservative, and a spike can trigger a spurious timeout — a retransmission even though no loss happened. TCP's fast retransmit (three duplicate ACKs) avoids waiting for the RTO in most loss cases, which is why timeout-driven retransmission rates above a low level deserve scrutiny.

Diagnosing timer-related problems: check for long gaps in capture inter-packet timing that match RTO values (fast retransmit events vs. timeouts), verify RTT stability (mdev from `ss -ti`), and observe whether cwnd collapses to 1 segment after timeouts. Stable RTT keeps RTO small and throughput high; excessive RTTVAR inflates RTO and harms the flow.

## Q34: How does Nagle's algorithm interact with delayed ACK?

**A:** Nagle's algorithm (enabled by default in most stacks) coalesces small outbound segments: the sender can have only one unacknowledged small segment in flight; pending data is buffered until that segment is ACKed (or the buffer reaches MSS), reducing the number of tiny packets. Delayed ACK (RFC 1122/5681) withholds a fast ACK for up to ~40-200ms (often 40ms Linux, 200ms legacy) to batch ACK responses, reducing ACK overhead.

The classic problem occurs when both interact tail-to-tail for interactive traffic: Nagle holds the second small write while Delayed-ACK holds the ACK, stalling the interaction for one delayed-ACK period per round of small writes. This triple caveat shows up as "clocked staleness" on interactive connections (SSH, Telnet, chat keepalives), latency spikes matching the delayed-ACK window for small request-response patterns.

Performance diagnosis: 40ms+ periodic latency spikes on interactive traffic with small packets strongly indicate Nagle+delayed-ACK interaction. Mitigations include disabling Nagle (TCP_NODELAY) on interactive sockets, ensuring applications flush writes appropriately, and using application-level batching (writev, MSG_MORE) for request-response session patterns. Recognizing this interaction prevents wasting time on "network problem" hunts when the issue is protocol tuning.

## Q35: What is TCP window scaling and when does it matter?

**A:** Window scaling is a TCP option (RFC 1323/7323) that increases the maximum advertised window beyond the base 16-bit field (max 65535 bytes). The window scale field shifts the window value leftward, allowing windows up to 1 GB (scale up to 14). It's negotiated at connection setup, so it must be present and accepted to apply for the entire connection.

Window scaling matters because the window/RTT = throughput ceiling formula means a 64KB window on an 80ms RTT supports at most ~6.5 Mbps. Modern paths (1-10 Gbps, cross-country or cross-continental RTTs) have BDPs far larger than 64KB, so window scaling is mandatory for high throughput. When effectively disabled (some middle-boxes strip or resize this option), connections stall at trivial throughput no matter the bandwidth.

Diagnosing: the connection's negotiated receive window appears in `ss -ti` and in captures (the SYN window plus scale option). Zero-AZACK and window size sitting near 65535 suggest scaling is missing or broken. If downloads and tests are capped at roughly 64KB/RTT, window scaling is the first thing to check, along with receive buffer sizing and the effective socket buffer on the receiver.

## Q36: What are socket buffers and how do they affect throughput?

**A:** Socket buffers are per-socket kernel memory that holds data for sending (send buffer) and receiving (recv buffer). The recv buffer bounds the advertised window, since the receiver can't acknowledge more data than it has memory to hold; the send buffer bounds the sender's ability to queue data ahead of ACKs. Tuning these significantly impacts throughput.

For high BDP paths, the buffers must be at least the BDP. If the recv buffer is smaller than the BDP, the advertised window caps the in-flight data below the available pipe capacity and throughput is window-limited (≈ buffer/RTT). If the send buffer is too small, the sender stalls waiting for ACKs despite available window. Linux auto-tunes these buffers by default (net.ipv4.tcp_rmem/tcp_wmem), enlarging toward tcp_rmem's max when the connection benefits.

Troubleshooting: check `ss -m` (socket memory details) for recv/send buffer sizes and window values. Temporary buffer imbalance during high traffic, or max buffer limits set too low, are common in container and VM setups. Buffer metrics must be interpreted alongside the BDP of the path — a 64KB buffer on a 10MB BDP path is the bottleneck even if all counters look clean.

## Q37: What is the difference between TCP and UDP for performance testing?

**A:** TCP and UDP measure different things and impose different constraints. TCP testing measures achievable reliable throughput, incorporating the overhead and loss recovery of steady congestion-control driving, and reveals protocol-ish limits (windows, slow start, congestion control) in addition to the network's raw delivery capacity. UDP testing measures raw packet delivery rate, packet loss, and jitter at a chosen bitrate, without congestion control or retransmission.

For finding a link's true peak capability, UDP testing (iperf -u) is more direct: send at rate R and measure how much arrives and at what loss. If no loss at rate R, the link supports at least R; when loss appears and grows, resource is saturated. TCP always self-limits to a "safe" throughput and masks the link's raw ceiling. For that reason UDP testing is preferred for finding the maximum deliverable rate.

But UDP's traffic can also starve others and even itself isn't protected by any congestion avoidance — so production-grade UDP testing must be done carefully. For application diagnostics, TCP reflects what real reliable protocols (HTTP, databases, message queues) actually achieve, while UDP shapes what real-time media (RTP) achieves. The measurement question dictates the protocol choice.

## Q38: How do you use tcpdump to see latency and throughput in a TCP flow?

**A:** Tcpdump alone captures packets; latency and throughput require turning timestamps and sequence numbers into derived metrics. The key technique is filtering to one TCP flow (e.g., `tcpdump -i any 'tcp port 443 and host X' -w file.pcap`), then analyzing with Wireshark or tshark: per-segment timing, RTT from SYN to SYN-ACK, flow throughput (bytes delivered over elapsed time), and inter-packet gaps.

For latency: the SYN→SYN-ACK time is one-way path delay plus server overhead; the SYN→ACK is one full RTT that excludes server processing if you subtract elapsed server-side latency. For per-segment RTT, Wireshark's TCP stream graph computes it from ACK timing. For throughput, the I/O Graph or Statistics->TCP Stream Graphs show delivered bytes/sec per flow; comparing this with connection's window and any retransmissions explains a low result.

For diagnosing stalls, look at the packet arrival gap between two segments with the same sequence space: a gap at the application layer (time between last byte of one request and first byte of next) does not equal a network delay. Distinguishing network delay (RTT-inclusive) from application delay (time spent in the app between segments) is the crucial interpretation skill, relying on carefully timestamped captures.

## Q39: What is traceroute underestimation, and how do you interpret per-hop RTT?

**A:** The three RTT samples per hop in traceroute are often dominated by the ICMP-reply behavior of intermediate routers rather than pure one-way propagation. Middle-boxes and routers de-prioritize ICMP or respond before/after forwarding, so a single hop's RTT doesn't equal the transmission time for data packets through that hop. Higher RTT and loss on intermediate hops can indicate a filtering or rate-limiting router while data passing through is fine.

The better interpretation: per-hop RTTs are directional and relative. RTT across hops usually increases monotonically (each hop adds propagation and processing), so a huge jump between consecutive hops (say 5ms to 100ms) indicates a transit change with real added distance/delay, often an inter-city or inter-continental crossing. RTT spikes at one hop also distort every subsequent measurement since the later measurements include the earlier queueing.

Practical guidance: don't blame a single high-RTT middle hop; check the trend and subsequent hops. mtr is better because it continuously samples, letting you see whether the high hop is stable or intermittently spiking. Always run traceroute/mtr in both directions to see asymmetry — many performance problems are directional.

## Q40: How do you identify packet loss location with a capture?

**A:** Locating where loss occurs requires either captures at multiple points on the path or inference from sender-and-receiver observations. The precise method: capture at the sender (or just downstream) and receiver simultaneously, then compare delivered sequences. Gaps present in the sender capture but absent in the receiver capture — combined with the receiver's received-set — bound the loss to the link segment between capture points.

Inference without multiple capture points: retransmission behavior and RTT clues suggest direction. If the sender's retransmissions are all timeout-driven (no duplicate ACKs) on the outbound direction, the loss likely occurred on the outbound link (with the ACK signal never arriving for the missing segment). If fast retransmits and duplicate-ACK storms dominate but the application data ultimately arrives, reordering or return-direction loss is implicated.

Practical intermediate approach: mtr provides per-hop loss probing; capture plus mtr correlation localizes loss to the problematic hop, then capture at that hop's edge (if feasible) confirms the link vs. the device. Remember that losses are often bursty, so synchronous multi-point captures are the reliable confirmation when precision matters.

## Q41: What is a TCP reset and how do you interpret it during troubleshooting?

**A:** A TCP RST (reset) terminates a connection immediately without a graceful FIN exchange. RSTs can be sent by hosts (rejecting an unknown SYN, aborting a connection on close-with-pending-data, or on unexpected segment) or by middle-boxes (anomaly-based blocking). In a capture, RST appears as a segment with the RST flag set; its interpretation depends on the state of the exchange at that point.

Performance story: RSTs also provide a fast signal of real problems. An RST in response to SYN (RST immediately for an open port that then keeps a half-open connection timer) suggests a firewall or host rejecting the port. An RST during an active data exchange often signifies a crash, reboot, or a middle-box that broke a long-lived connection. CRLF-splicing or unsolicited RSTs from a middle-box after idle periods are classic "connection dropped" symptoms for long-lived sessions.

Debugging workflow: note the direction, the exact point in the flow (which sequence/ack), and any TCP option oddities. A burst of RSTs across many connections from one client IP suggests malicious scans; isolated RSTs against one flow point to application- or middle-box behavior. Read the RST's acknowledgment value too: an RST with an ACK confirms the receiver actually processed the prior data.

## Q42: What is a half-open connection, and how does it impact performance?

**A:** A half-open connection is a TCP connection where one side has lost the association (crash, restart, path change) while the other retains state, often with an idle established connection. The unaware side keeps resources (socket, memory, — including NAT table entries) until a keepalive or timeout fires. These leaks build up, wasting memory and NAT-table capacity, and cause "connection established but no data flows" symptoms.

Impact: resource exhaustion. On NAT gateways and servers with finite connection tables, a flood of half-open connections (or even a stable leak over time) exhausts capacity, causing new connections to fail or existing flows to be arbitrarily dropped. Half-open connections also produce odd protocol behavior: retransmissions and RST when the missing side wakes.

Diagnosis: check state-space with `ss -s` or `netstat -an` for many established connections that never transfer data (age tracked counters) or connections stuck in states like LAST_ACK, TIME_WAIT accumulation. Tuning keepalive timers (net.ipv4.tcp_keepalive_time) and NAT timeout values, and detecting half-open leaks across crashes, are part of standard performance hygiene.

## Q43: How does TCP select the retransmission timeout (RTO)?

**A:** The RTO is computed per-connection from smoothed RTT (SRTT) and RTT variance (RTTVAR): RTO = SRTT + max(G, 4×RTTVAR), where G is the system clock granularity, subject to bounds (RFC 6298 minimum 1s for SYN-based and often 200ms for established flows, and 60s maximum). The variance term produces a generous margin: if RTT is very stable, RTO ≈ RTT + small; if RTT is volatile, RTO is much larger to avoid spurious timeouts.

Because RTO is derived from live measurements, RTT instability directly inflates RTO and consequently widens the window during which a genuinely lost packet causes the sender to idle. This is why path stability matters as much as absolute latency: a path with 50ms average but swinging to 400ms creates RTOs far above the bulk of flows, so every real loss costs a full RTO idle.

Troubleshooting RTO-related slowness: look at `ss -ti` rtt and rttvar; the randwidth via `sysctl net.ipv4.tcp_syn_retries` (SYN retry count) governs handshake failures. Watch for patterns of after-timeout retransmits clustering at even values (~1s, 2s, 4s doubles for SYN, and fixed multiples for ESTABLISHED). A high RTO rate (`TcpExtTCPTimeouts`) usually implies loss, RTT instability, or CPU overload.

## Q44: What is slow TCP and how do you measure it?

**A:** "Slow TCP" is the symptom of a TCP flow's achievable throughput being far below link bandwidth. Causes build a cascade: BDP-mismatched windows, loss-driven congestion control, spurious timeouts, buffer limits, scheduling/CPU constraints, sender-receiver memory, or middle-box interference. There is a single math ceiling: throughput ≈ min(bandwidth, window/RTT, loss-derived congestion limit).

Measuring approach: first obtain the link's nominal bandwidth and RTT (know the BDP). Then run iperf single-stream and compare; run parallel streams to separate stream-count dependence; gather per-connection state (`ss -ti` cwnd, rtt, rttvar, snd/rcv wscale, buffers) and protocol counters (retrans, timeouts). The diagnosis becomes: on which constraint did the flow bump?

Structure the analysis:
- If single-stream is low but multi-stream saturates → congestion-control or single-flow window/BDP limit.
- If cwnd is large but throughput still low → RTT inflated by queueing, or loss limiting.
- If buffers tiny → buffer sizing issue.
- If handshake and TFTPB are slow but steady-state fine → connection setup and warm-up bottleneck.
Each directs a different fix.

## Q45: What is the difference between active and passive network measurement?

**A:** Active measurement injects probe traffic and observes the response: ping, traceroute, iperf, mtr, and active resynthesis are active. Passive measurement observes existing traffic without injecting anything: packet capture, netflow/sFlow, and interface counters are passive. Active measurement gives direct control (rates, packets sizes, destinations) — ideal for isolating properties — while passive measurement gives real traffic (accurate load and user behavior) but weaker causal control.

Each serves a purpose. Active tools answer "what can this path do?" and probe config errors (send exact packet sizes, saturate a link). Passive tools answer "what is this path doing now?" and reveal user-impacting behavior (latency percentiles of real flows, retransmission rates in production traffic, queue behavior under real burst patterns) without disturbing anything.

Interpreting both correctly is the craft: active results may not represent user traffic because probes and real flows differ in size, protocol, and queuing interleaving; passive results can be polluted by sampling, by hidden peer traffic, and by the very congestion being measured. Convergent evidence from both types pinpoints whether a "slow network" report reflects a real path property or a protocol/application artifact.

## Q46: What are the RFC 6298 and RFC 1323 timings and why do they matter?

**A:** RFC 1323 extended TCP with window scale, timestamps, and SACK. RFC 6298 (replacing 2988's RTO rules) defined the RTO computation from SRTT/RTTVAR and its bounds. The timestamps option (RFC 1323) matters most for measurement: it gives per-segment RTT estimation untainted by retransmission ambiguity, improves RTO accuracy, and enables the PAWS (protect against wrapping sequence space) mechanism at high rates.

Why it matters in practice: without timestamps, TCP cannot measure RTT for retransmitted segments reliably (the ambiguity of whether the RTT belongs to original or retransmission), and the RTO becomes too conservative or too aggressive. PAWS also prevents vintage sequence-number-wraparound false instrumentation at multi-gigabit rates.

Troubleshooting implications: on high-rate paths, timestamps (now default in Linux) correlate with `ss -ti`'s rtt values and provide real per-flow measurement. When a middle-box strips TCP options, window scaling and timestamps silently fail — visible as negotiated-but-disabled semantics in captures — which caps throughput (no scaling) or degrades RTO accuracy (no timestamps), producing mysterious "network slowdowns" that are actually options-negation issues.

## Q47: What are out-of-order packets and why do they degrade performance?

**A:** Out-of-order packets arrive in a different sequence than the sender transmitted them, requiring the receiver to hold them until the earlier segments arrive. TCP cannot deliver data to the application out of order, so arrivals beyond a gap sit in the reassembly buffer, essentially freezing application consumption until the missing segment arrives or is retransmitted.

The performance cost: out-of-order delivery consumes receiver memory (reassembly buffer), generates duplicate ACKs (the receiver ACKs the highest contiguous byte), triggers spurious fast retransmissions (which waste bandwidth and spuriously reduce cwnd under loss-based congestion control), and adds latency to reassembly. Sustained reordering rates materially reduce throughput even with no actual loss.

Causes: disparate-path routing (multipath, load-spraying), route flapping, queue scheduling differences among parallel links, and virtual switching reordering. Diagnosis: `ss -ti` shows out-of-order arrival counts (`OOO`) per flow; captures show duplicate ACK storms followed by later in-order delivery of the "missing" segment; distinguish reordering from loss by whether the contested segment eventually arrives without retransmission.

## Q48: What is MTU discovery and how does it fail?

**A:** Path MTU discovery (PMTUD) lets a sender discover the largest packet size supported across the entire path. The IPv4 mechanism sets the DF bit and relies on routers to reject (ICMP "Fragmentation Needed") oversized packets, then adjusts the MTU down. In practice PMTUD frequently fails because the required ICMP messages are filtered by firewalls, blackholing large packets silently.

The failure mode is severe: a packet exceeding the actual path MTU with DF set is dropped, ICMP never returns to the sender, and the sender retransmits the (still oversized) packet in a loop — classic symptoms: some transfers work (small requests) while larger ones hang or crawl exactly at the MTU boundary (e.g., everything ≤1460 works, larger stalls).

Diagnostics: the reproduction is deterministic — ping with increasing payload until packets drop (the textbook MTU probe test) — combined with checking for tunnels (VPN, IPsec, VXLAN) that typically shrink MTU. Fixes include setting a conservative MTU manually, enabling ICMP for the tunnel endpoints, and using TCP MSS clamping at NAT-filtered boundaries. Correct MTU at the end-host starts with `ip link show` and `tracepath`.

## Q49: How do you test DNS latency and distinguish it from the rest of network latency?

**A:** DNS latency is the time between a resolver sending a query and receiving the answer, affecting every hostname-based operation once — unless caching removes the cost. Isolate DNS time by first performing timed lookups: `dig example.com` shows query time; `dig +stats` reports the resolver's total processing; `time dig KRR example.com +tcp` isolates transport vs. resolution. The browser/tool-level records also decompose DNS from TCP from TLS from TTFB.

Rules for interpretation: query time of a few ms from a local resolver is fine; 50ms+ usually means a distant authoritative, a slow forwarder, or a globally overloaded resolver. Since DNS is UDP by default, loss or fragmentation shows as retransmission-looking delay; the resolver retries with TCP when truncated. Cache-hit latency vs. cache-miss latency can differ by an order of magnitude even on the same network.

Performance hygiene: check resolver choice, DNS-over-TCP vs UDP behavior, and TTL policy. In high-loss environments, DNS answers delayed by a UDP retry window (often 5s+) are a common invisible latency source. The DNS TTFB isn't a server fault — it's usually only visible when you assemble the whole request timeline.

## Q50: What is a TCP handshake SYN retransmission pattern?

**A:** SYN retransmissions occur when the SYN isn't acknowledged: the sender retries at exponential backoff per `tcp_syn_retries` (default 6, with roughly 1, 2, 4, 8, 16, 32s), then gives up with the connection timing out. The pattern in a capture reveals the failure class: retransmits with no response at all = firewall drop or unreachable host; retransmits followed eventually by RST = the port is refused (or filtered and rejected); retransmits that finally succeed after a doubling pattern often point to one-way path loss.

Interpretation: standard Linux default (~1,2,4,8,16,32s = 63s total) is long; aggressive users set smaller values for fast fail. A single lost SYN (one retransmission then success) means transient loss on the SYN path. Continuous retransmission without any reply up to the cap is a hard reachability problem.

Diagnosis workflow: run ping to the host (but remember ICMP may be filtered while TCP works, and vice versa); use tcptraceroute (`-T port`) to check whether the path forwards TCP; capture near the sender; compare with a capture at the server if possible to see whether the SYN arrived (meaning the ACK/SYN-ACK route is the failure direction). Then tune retry counts or fix the firewall/filtering.


## Q51: How do you systematically isolate a network performance bottleneck?

**A:** Systematic isolation decomposes the problem into measured layers rather than guessing. The top-down sequence: app-level symptom (goodput, TTFB, response time) → transport-level (TCP throughput, retransmits, windows, cwnd) → network-level (RTT, loss per hop, queueing) → link-level (bandwidth, MTU, medium) → host-level (CPU, memory, NIC offload, buffers, scheduling). Each measurement bounds where the problem could be.

The narrowing method uses controlled probes: (1) run iperf between endpoint pairs to determine achievable throughput per segment; (2) run mtr to capture per-hop latency/loss; (3) capture packets at sender and receiver to see RTT, retransmits, windows in the real flow; (4) check host resource state (CPU per-queue softirq saturation, buffer drops, ring buffer, NIC errors) — a surprising share of "network" problems are host bottlenecks like single-queue saturation or buffer exhaustion.

The output is a constraint table: expected bandwidth, BDP, measured throughput, retrans rate, RTT distribution, and limiting host resource. The layer whose constraint tightly matches the symptom is the primary bottleneck. Good practice then validates by "removing" the constraint (raise a buffer, increase parallelism, change MTU) and confirming the measured throughput moves accordingly.

## Q52: How do you interpret `netstat -s` or `ss -s` statistics?

**A:** The `-s` output provides aggregate TCP/IP protocol counters. The key TCP counters and their signals: `active/passive opens` (connection churn), `failed connection attempts` (unreachable or refused), `resets received/sent` (problem hosts), `retransmitted segments` and `TCP retransmit timeouts` (loss/timeout rates), `connections reset due to unexpected data` (protocol misuse), `Discarded packets due to missing routes` (routing problems), `TCP segments with out-of-order` (reordering). IP counters include `Reasm failures` (fragmentation problems), no-buffer losses (host memory drops).

Reading strategy: compute rates, not absolutes. Divide retransmitted segments by total segments to get a retransmit ratio; observe growth between two readings over time (netstat re-reads each second with `-c`). Look for counters that move fast relative to total traffic — that's your candidate problem. Compare MC (multicast), UDP (UDP missed packets = host buffer loss), and error counters as well.

Caveats: counters are system-wide, not per-connection; they include traffic on all interfaces; kernel-level sampling can miss short-lived bursts. Their main value is fleet-level tri-age — identifying that retransmits or resets are elevated at all, which then directs per-flow investigation with captures.

## Q53: What is queueing delay vs propagation delay vs transmission delay?

**A:** Propagation delay is the travel time of a signal through the medium — fixed by physics and distance (≈5μs/km in fiber/cable, ≈3.3μs/km in vacuum/fiber at c). Transmission delay is the time to push a packet onto the medium: size/rate (for 1500 bytes at 1 Gbps ≈ 12μs; at 10 Mbps ≈ 1.2ms). Processing delay is router CPU time per packet (usually microseconds). Queueing delay is the variable time spent in buffers awaiting transmission.

In domain terms, propagation and transmission are near-constants per path; queueing is the variable that swings with load. For a 100-byte voice packet on a 10 Mbps link, transmission delay alone (~0.08ms) is small, but behind 1000 queued packets it's ~80ms of queueing. The sum — propagation + transmission + processing + queueing — is the total one-way latency.

For debugging, separating these matters because they have fundamentally different fixes: propagation is fixed by distance (mitigate with geo/edge placement), transmission by MTU and rate, processing by hardware/setup, queueing by load management and active queue management. When latency is stable near the propagation floor, the path is healthy no matter the absolute number; when it grows with load, queueing is the culprit.

## Q54: What is buffer sizing (bandwidth-delay product) in routers and when does it cause packet loss or bufferbloat?

**A:** Router buffer sizing trades loss against latency under congestion. The classic "Rule of thumb" (RFC 2000s guidance) is the bandwidth-delay product: buffer ≥ BDP so a TCP sender's full window can be absorbed during congestion, avoiding loss. Modern guidance (RFC 3819/7567) warns that large BDP-matching buffers cause bufferbloat: queues absorb congestion signals while inflating delay.

The interaction with TCP: if buffers are too small relative to the BDP (burst congestion), packets drop despite bandwidth being available (congestion control throttles because of loss — underutilizing the link). If buffers are very large (≥ BDP × number of flows), TCP (loss-based) keeps increasing windows until queues fill to their maximum, producing latency of seconds and eventual loss all at once. Neither extreme yields good performance for interactive traffic.

The actionable principle for troubleshooting: measure latency under load vs idle. Heavy queueing when the link is full indicates active buffering. For server/infra capacity, prefer small buffers + active queue management (CoDel/fq_codel) for latency protection, and reserve BDP-scale buffering only where the protocol truly requires loss-opting (rare), or rely on sender-side algorithms like BBR that avoid queueing anyway.

## Q55: How do TCP timestamps and SACK affect performance troubleshooting?

**A:** TCP timestamps (RFC 1323) carry a per-segment timestamp used for RTT estimation and PAWS. Without it, RTT estimation on retransmits is ambiguous; with it, you get precise RTT per flow (`ss -ti` shows rtt/rttvar sourced from timestamps). SACK (Selective Acknowledgment, RFC 2018) lets the receiver inform the sender which specific ranges are missing, sparing the sender from retransmitting the whole window when multiple drops bloin in flight.

Troubleshooting with them: SACK visible in captures (SACK-permitted) lets you see recovery precision — with SACK, recovery is cheap for scattered losses; without it, one burst of loss forces whole-window retransmission (Reno-style go-back-N), which on high BDP paths creates a huge throughput hole. SACK-poor environments (middle-box stripping options) are a classic hidden cause of throughput collapse under multi-drop bursts.

Verification: `ss -ti` and captures show the negotiated options. If options are missing but originally negotiated, IP/transport intermediaries are stripping them — investigate the path (VPN/tunnels/firewalls). Suppose options are present but you see go-back-N behavior anyway; then either SACK handling or congestion behavior is broken — check cwnd evolution and retransmit recovery patterns in the capture.

## Q56: What is the role of IRQ-to-CPU affinity in network performance?

**A:** IRQ affinity binds a NIC's interrupt processing to specific CPU cores, affecting how much CPU the network stack consumes and how quickly packets move in. Without affinity, interrupts and softirqs can run on any core, creating cache thrash, contention, and latency variance. With your-queues (RSS) distributing packets across many queues, each bound to a distinct core, you get parallel packet processing across cores.

The wrong affinity causes asymmetric bottlenecks: one or two cores pinned at 100% softirq CPU processing the entire incoming/outgoing burst while other cores idle, capping overall throughput well below the link speed and NIC capability. This is a classic "network is slow" case where the network is fine and the host's packet-processing is the ceiling.

Diagnosis: `mpstat -P ALL 1` or `top -1` shows softirq CPU across cores; if some Cores are pinned high and others idle, check `cat /proc/interrupts | grep ethX` distribution. Fix: set RPS or proper IRQ affinity (irqbalance or explicit `/proc/irq/*/smp_affinity`) so cores match RSS queues and NUMA. This is a standard host-level network optimization for high-throughput services.

## Q57: How do you use `ss -ti` to diagnose per-connection performance?

**A:** `ss -ti` prints per-TCP-connection transport-layer state: rtt, rttvar, ssthresh, cwnd, bytes_acked/bytes_received, retrans counts, out-of-order, window sizes, pacing info, and negotiation details (wscale, timestamp, sack, mss). It's the fastest window into why a specific connection underperforms, since it reflects the kernel's live model of the flow.

Interpretation recipes:
- cwnd stall-size → window-limited (compare cwnd×mss against BDP).
- ssthresh collapsed after loss → congestion penalty is recent.
- high retrans or ooo counters → loss/reordering active.
- rtt in capture is inflated vs. propagation floor → queueing.
- zero-window / small window advertised → receiver or its buffers are the constraint.
- busy/no-congestion states (`ss -ti` may show pacing/fips) → pacing rate limits throughput.

The right question order: first, is the connection window-limited, loss-limited, RTT-limited, or host-limited? Then pick the layer-specific fix. Because `ss` reflects one kernel instance, capture the connection while the symptom is live, and pair with `ss -em` for memory. This tool plus captures covers most per-flow diagnoses.

## Q58: How does TCP pacing and BBR change throughput behavior vs classic loss-based control?

**A:** Pacing smooths the transmission of a congestion window across an RTT, instead of the bursty "send window back-to-back then idle" behavior of classic stacks. Pacing reduces burst-induced loss and queueing at bottleneck buffers. BBR (Bottleneck Bandwidth and Round-trip propagation time) is the pacing-native algorithm that models the path: it measures the bottleneck rate (with an achieved-rate probe) and minimum RTT, then tries to operate at exactly rate × minRTT without forming queues.

The key behavioral difference: classic loss-based control (Reno/Cubic) fills queues until loss occurs, then backs off — resulting in standing queueing (bufferbloat) and sawtooth throughput. BBR tries to keep the queue empty while saturating the bottleneck, yielding lower latency under load and higher throughput on paths where the loss signal is delayed or undersalted (very-high-BDP fiber links, paths with delay-heavy queueing like some satellite/mobile links).

Troubleshooting implications: seeing high RTT and persistent loss under Cubic does not necessarily mean the path is bad — it may mean the algorithm is filling buffers (swap to BBR to test). But BBR's fairness and queue-emptying properties vary; on a shared bottleneck with Cubic flow mix, BBR's queue-free operation can actually starve or be starved by CBS-style ozone flows. `ss -ti` shows the algorithm (`cubic`/`bbr`) and pacing info; choosing algorithms per path (not globally) is part of modern performance tuning.

## Q59: What is a TCP connection timeout vs a retransmission timeout?

**A:** Connection timeout refers to the total time a connection setup (SYN retries, or connecting to an unreachable host) is allowed to fail — bounded by `tcp_syn_retries` + exponential backoff (Linux default ~63s SYN total, or `tcp_synack_retries` on the server side). Retransmission timeout (RTO) is the per-data-segment timer (SRTT + 4×RTTVAR) governing data retransmission during an established flow. Both are "timeout" but operate at different phases of the connection with different computed values.

Practical consequence: an established connection with a dead path retries a segment at the RTO (≈1s→2s→4s...) until after a fixed number of attempts (tcp_retries2 default 15) the TCP retransmission probe eventually gives up and closes with a timeout; users experience a window of "site times out" before full failure. SYN-phase timeouts apply to new connections. Diagnosing which you're hitting gives the phase: handshake failures = SYN/synack retransmits; mid-session hangs = RTO/RTO-based retransmits and tcp_retries2 exhaustion.

Tuning matters per context: too low `tcp_retries2` on a reliable intranet → connections killed by path flaps invisible to users; too high on flaky WAN → long stuck waits. Both timeout families show in `TcpExtTCPTimeouts` and in captures as retransmit patterns. Tailoring these sysctls to the link's reliability is standard host tuning.

## Q60: What is jitter buffer (in real-time media) vs network jitter?

**A:** Network jitter is the variation in packet arrival times across the network. A jitter buffer is endpoint software that intentionally delays playback by a fixed cushion to absorb network jitter, converting variable arrival to steady playback. The two are linked: higher network jitter demands a bigger jitter buffer, and a bigger buffer adds delay. Real-time media performance is jointly determined by loss, jitter, and buffer settings.

Diagnostic implications: a voice/video call's bad experience could be excessive jitter (buffer underruns — choppy/robotic audio), jitter-buffer size (added mouth-to-ear delay), or loss (gaps). Tools: iperf UDP reports jitter; packet capture of RTP shows per-packet arrival delta. Distinguishing "jittery then smooth-with-delay" vs "glitchy" helps identify the buffer setting vs the network condition.

Operational relevance: measuring jitter distribution (min/max/percentiles) rather than just average, since a low average with occasional huge spikes (rare high-jitter) may break the audio no matter the buffer. Correlate jitter spikes with load (queueing), and check route stability — route flaps cause episodic jitter spikes no buffer sizing can fix.

## Q61: How do you test router/server performance with iperf in both directions?

**A:** Bidirectional iperf testing measures each direction independently, since real links are typically asymmetric, different links / paths are used, and host or NIC capabilities can differ per direction. Run the server on one host, the client on the other, and measure client→server (upload direction), then reverse the roles (or use `-R` reverse mode) to measure the other way on the same pair.

Methodology quality: run at least 30-60s per direction (steady state), capture with `-P 1` (single stream), then `-P 4` / `-P 8` for parallel-stream results to separate single-flow limits from carried capacity. Note the window (`-w`) and buffer settings, and document the algorithm. Also useful: run UDP mode (`-u -b`) to find peak lossless rate per direction. The numbers you get are per-direction ceilings, not "the" throughput.

Reading results: if download (client←server) is high but upload (client→server) is low → asymmetric link or asymmetric host performance; if both are low but parallel streams improve → per-flow or endowment limits; if neither improves its cap → rate-limit or link saturation. Always test against the same physical path and with the same MTU, and accept that iperf's numbers are an upper bound per configuration.

## Q62: What is a TTL and why is interpreting TTL decrements part of tracing?

**A:** TTL (IPv4, Hop Limit in IPv6) is a field decremented by every router; the packet dies at TTL 0, generating an ICMP Time Exceeded message. Traceroute exploits exactly this mechanism to discover hops. The TTL-in-the-ICMP-reply varies per device: most reply with the responding interface's own IP, and the source IP of the reply is that of the egress interface — which is why traceroute can show asymmetric-looking hop IPs even on a symmetric path.

Interpretation pitfalls involve TTL: missing replies at a hop (firewalls that suppress ICMP time-exceeded), replies from a different source than expected (TEC from firewall proxy), and TTL-based spoofing/route-poisoning. When mtr shows `loss 100%` at several consecutive hops but final hops are fine, TTL-sensitive ICMP traffic is the classic explanation, not actual path loss.

For path analysis, the TTL counts also reveal hop counts: a TTL 64 host reached with the ping displaying value 55 indicates 9 hops (64-55+ accounting). If you see TTL much lower than expected (e.g., 45 instead of 60), count hops normally; but TTL=1-2 replies from destinations often indicate they are behind a NAT/proxy rewriting the TTL. Understanding TTL mechanics prevents mis-inferring path length and loss.

## Q63: How do you use tshark (command-line Wireshark) for performance analysis?

**A:** Tshark brings Wireshark's dissection to the CLI, enabling scripted analysis of captures. Performance workflows: `tshark -r file -T fields -e frame.time_delta -e tcp.seq -e tcp.ack ...` extracts per-packet timing and sequence info for custom latency/loss computations; `-q -z io,stat,<interval>` prints bandwidth histograms per time bucket; `-q -z conv,tcp` lists conversation statistics (bytes, duration, retransmits per flow); and `-q -z expert,error` reports expert-diagnosed problems (false-fast-retransmit, duplicate ACK, seq forwards).

RTT from captures: `-z io,stat` gives throughput by interval; computing per-segment RTT requires field extraction of timestamps vs ACK stream; `-z expert` identifies the anomalies the analyzer already classified. For losses, `-z "tcp,rtt"` produces per-interval RTT distributions that reveal queueing growth.

The efficiency gain: you can run tshark over large pcaps programmatically, produce a summary table (retransmits, RTT percentiles, throughput per conversation), and turn captures into SLA-style answers ("was this interval exceeding 200ms p95?") without GUI. Mastery here is selecting the right stats window and interpreting its output correctly against the capture's scale and filters.

## Q64: How do congestion windows grow and shrink (additive increase, multiplicative decrease) affect a server's throughput?

**A:** Classic AIMD: cwnd increases additively (1 segment per RTT in avoidance) and is halved (or collapsed) on loss. The "sawtooth" sums to an average window that depends on loss frequency through the equilibrium formula. Higher loss → smaller average cwnd → lower throughput for the same RTT. This behavior makes throughput a function of loss as much as bandwidth, which is the crux of many "server is slow" complaints on lossy or congested paths.

Impact at the server side: a server handling many concurrent connections experiences each flow's AIMD dynamics independently; buffer sizes, NIC parenting, and RTT heterogeneity across clients affect the aggregate. Multiple flows that share the server's bottleneck contend: with Cubic/BeRamo fairness they converge roughly RTT-fair, and flows with higher RTT get less share, penalizing far-away clients.

Tuning layer: using loss-tolerant or delay-based algorithms (BBR) reclaims throughput where NSC loss is the limiter; increasing the initial window (RFC 6928 allows 10) shortens slow start; concurrent-connection allocation may offload strain from TCP's per-flow dynamics by giving parallelism. Observability: `ss -ti` shows cwnd/ssthresh per flow, so you can see behaviors like all flows stuck at low cwnd — an immediate red flag for loss-driven throttling.

## Q65: What is a receive window scale and its effect on flow throughput?

**A:** Window scale (RFC 1323) extends the 16-bit TCP window field via a shift factor negotiated in the SYN. The actual advertised window = window field × 2^scale (scale 0-14 gives up to 1 GB). The receive window is the receiver's advertised in-flight budget; if it caps below the BDP, throughput = window/RTT regardless of bandwidth or sender aggressiveness.

Failure signals: the receiving host advertises a small window because its recv buffer is small (Linux `net.ipv4.tcp_wmem/tcp_rmem` max limits), because the flow didn't warrant auto-tuning, or because options mismatch (middle-box stripping the option: scale becomes 0 → window stuck at 64KB). Captures expose both the negotiated scale (SYN option) and the live window values (each ACK).

Debug: verify the negotiated scale in capture; confirm the recv buffer — `ss -mi` shows wscale and snd/rcv buffer settings. A connection stuck showing window≈65535 while the BDP is megabytes means scaling was disabled — investigate path intermediaries (VPN/tunnels stripping options) or host buffer hardening limits. Otherwise, window-limited flows are usually a buffer-tuning problem at the receiver.

## Q66: What causes the "high latency, low loss" symptom, and how do you prove it?

**A:** High latency with minimal packet loss typically implicates queueing/buffering — the net is forwarding packets fine (no drops) but holding them long delays. Proof requires measuring latency changes with load: idle-path RTT vs loaded-path RTT (ping while saturating with iperf). If RTT jumps many-fold (e.g., 20→500ms) while loss stays near zero, buffers are deep and draining slowly: classic bufferbloat or a heavily queued bottleneck.

Alternative causes with a different signature: propagation-bound paths (satellite, long haul) show uniformly high RTT independent of load — no change under iperf pressure; application serialization (server or app holding requests) shows high TTFB and end-to-end time with the network itself at idle-floor; middleware (queues, proxies) adds service time per hop. So the measurement is the discriminator: network-load-independent latency = fixed delay; load-sensitive latency = queueing.

The debugging track: (1) ping baseline idle; (2) ping under iperf load — if RTT increases drastically, queues are the latency source; (3) mtr to find which hop adds it; (4) check QoS/queue-management policy at that bottleneck (CoDel/fq_codel install focus). If RTT doesn't move under load, look at the server and application layers, not the network.

## Q67: What is a "black hole" in networking and how do you find one?

**A:** A black hole is a path entity that silently drops packets — no ICMP, no error — while forwarding most traffic. ICMP-filtering routers, broken NAT, opaque hops that drop specific packet sizes, or MTU-mismatched tunnels are frequent culprits. Symptoms: "ping works but TCP service fails" or "large transfers stall while small ones work" — exactly the PMTU-mismatch profile.

Finding black holes: systematic narrowing — test connectivity per protocol (TCP to various ports vs ping to same host), per direction, and per packet size (ping with increasing `-s` to find the size boundary). Use mtr: if loss appears at a specific hop and stays at 100% for that hop while subsequent hops are fine, that hop filters your probe type. tcptraceroute (`-T`) uses TCP instead of ICMP to detect firewalls that pass TCP but drop ICMP.

The size-boundary test is the strongest black-hole indicator: if ping payloads below X succeed and above fail with DF set, you have an MTU hole (likely a tunnel/config issue). Corroborate with path MTU tools (tracepath), check tunnel endpoints' MTU, and verify with captures at the boundary hop. Document that black holes are usually config, not wire failure.

## Q68: What is TCP anomaly detection and what patterns indicate real problems?

**A:** TCP anomaly detection looks for statistically or structurally abnormal patterns in flow data (counters, captures): unusual SYN retransmission rates, many RSTs, retransmission spikes, sequence anomalies, window collapses, TIME_WAIT accumulation, connection setup churn. The patterns that indicate real problems differ from middle-box IDS noise — distinguishing them requires understanding what's normal for your traffic types.

Concrete patterns worth attention: (1) elevated SYN-ACK timeouts at higher-than-normal rate — server semi-connect refusal/backlog or SYN-flooding; (2) resets with ACK after data — application or stack-level abort; (3) high out-of-order rate above baseline — route/load changes; (4) sudden RTT inflation with no throughput change — new queueing at a hop; (5) persistent TIME_WAIT pile-up — connection churn from protocols misusing keep-alive, exhausting ephemeral ports.

Detection approach: baseline the normal distribution (per application, per region) then flag triggers (e.g., RST rate >3x baseline for 10+ min). Sampling captures and correlating with incident windows beats raw counter watching. The false-failure trap: IDS-style filters (RST from security middleware, transparent proxies) look like network faults but are deliberate — know your network's middle-boxes before believing a detected anomaly is a real fault.

## Q69: How do you validate TCP throughput against a baseline (expected results)?

**A:** Validation starts with the expected numbers: the link's nominal bandwidth, the BDP for the measured RTT, and the per-flow/buffer limits of the hosts. Compute the single-stream ceiling ≈ min(bandwidth, BDP/window-derived, loss-derived congestion limit). Then run the iperf/HTTP/file test and compare against that ceiling — the difference between measured and expected, after accounting for overhead, is the performance gap.

Expected-value construction must include protocol overhead: TCP/IP headers (typically ~3-4% for 1500-byte packets), any tunnels, TLS overhead, and application framing. Factor in slow-start ramp for short transfers (time-to-fill-BDP), MTU-effective rates, and NIC/host capability (single-stream per-connection via CPU/hardware limits often ~10-25% below link bandwidth even on good hardware).

Discrepancy analysis: if measured is within ~% of the computed ceiling, the network matches expectations — residual is tuning/algorithm/overhead. If well below, attributes to check in order: window vs BDP, loss/retrans rate, congestion algorithm, host CPU/interrupt conditioning, buffering, MTU, and middle-box option-stripping. Finally, re-test after each change to confirm you moved the number — that's what makes the baseline useful.

## Q70: What is the difference between one-way delay and RTT, and why measure OWD?

**A:** One-way delay (OWD) measures the time for a packet to travel from A to B only; RTT measures the full round trip. OWD exposes asymmetry: paths can be symmetric in latency or wildly asymmetric — different physical routes, different queuing, different provisioning per direction. RTT hides this: a 400ms RTT could be 380ms outbound + 20ms return or 200+200 — with completely different root causes and remedies.

Measuring OWD requires clock synchronization between endpoints (NTP/PTP). Without sync, only RTT is available, and you can only infer asymmetry via packet timing of request/response patterns (e.g., high TTFB with fast response-body flow implies outbound delay dominance; slow response-body with quick TTFB implies return-direction or server issues).

Why it matters: asymmetric queueing is common (more capacity in one direction, downloads >> uploads), and performance fixes apply per-direction. Diagnostic value: isolate a high-RTT component to its actual direction, test with mtr in both directions, and correlate with capacity provisioning. For critical real-time paths, deploy synchronized OWD monitoring — it makes performance problems directional and precise.

## Q71: What is the difference between NIC performance offloads and when they mislead performance tests?

**A:** Offloads move packet processing from software to hardware: GRO (Generic Receive Offload), GSO, TSO (send-side segmentation), LRO, checksum offload, RSS, and flow steering. They dramatically raise throughput and lower CPU. But they warp measurements: TSO/GRO means the kernel's stack deals with large aggregated "super-packets," so byte counters and captures reflect MTU-scale segments instead of the 1500-byte units you physically transmitted.

Misleading consequences come from interpreting capture data naively: tcpdump sees aggregated segments (like 65536-byte "segments") and may misreport RTT/retransmit/sequence patterns; packet counts for "the same traffic" vary with offload settings; checksum-offloaded packets show as bad checksums in older capture tools if not decoded correctly. TSO-visible effects are normal, not bugs.

Best practice: for accurate per-segment analysis, disable LRO/TSO/GRO selectively on the capture host (e.g., `ethtool -K eth0 tso off`) or use capture tools that interpret offloaded segments (or analyze producer/consumer counters instead). Verify `ethtool -S` shows hardware counters and correlate with `ss` — the offload layer hides one reality and shows another; cases where throughput is 5 Gbps but capture shows only 2ms of segments indicate you're looking at aggregated units.

## Q72: What are interface errors and drops, and which ones indicate real problems?

**A:** Interface statistics from ip/netstat/`ethtool -S` include tx/rx errors, dropped packets, overruns, and FIFO errors. Not all are problems: drops can result from filter rules, queue policy, buffer fullness that is normal under bursts, or small system limits. The ability to classify the drop type matters — `ethtool -S` distinguishes RX queue full (overrun), host small buffer (drop due to memory), and device FIFO.

Read the counters with a lifetime-vs-rate view: total errors vs errors/sec under load. Error rates proportional to rate with random distribution suggest a marginal medium (cable, SFP, negotiation); RFC 2544-style testing isolates wire behavior. Drops at receive queues that spike during bursts and correlate with CPU softirq saturation are host-processing ceilings (fix: better affinity, more queues, bigger buffers).

Investigation workflow: `ip -s link`, `ethtool -S dev`, `ethtool -g` (ring buffer inspection — a small ring drops bursts; increase it), then correlate with CPU (`perf`/mpstat). Distinguish NIC errors vs kernel drops vs hardware multicast — each points to physical, config, or host limit. Rare events in an else-healthy interface can be ignored; growth under peak load is the signal.

## Q73: How do you measure and interpret RTT percentiles (p50, p95, p99)?

**A:** Percentiles shape the latency distribution: p50 (median) shows typical experience, p95/p99 reveal worst-excursion behavior. For RTT specifically, the percentiles capture queueing variance: a healthy path has p50 ≈ p95 ≈ p99 near the propagation floor; on a loaded path, p50 stays low but p99 spikes — the telltale sign of bufferbloat or burst congestion. A single average hides exactly where the problem is.

Measurement technique: collect a large RTT sample set (thousands of pings or passive-flow samples over a representative window), then compute percentile distributions — hand-rolled numeric tools or a monitoring stack (Prometheus, Grafana, Carbon) do this well. Time-window breakdown matters: percentile latency at 2am vs peak hours usually diverges massively; report and alert per window.

Interpretation guidance: track p95/p99 trending vs p50. p50 growing with p95/p99 → systemic load increase; p99 growing alone → bursts/queueing spikes; p50 staying at floor while p99 climbs gradually → increasingly severe rare queue events. Alerting on p99 (RTT) is commonly paired with SLOs for interactive paths; the p99-to-p50 ratio is a quick "jitter/queueing" health indicator.

## Q74: What is the TCP fast open (TFO) and how does it reduce connection latency?

**A:** TCP Fast Open (TFO, RFC 7413) lets the client send data with the initial SYN (after a first connection established a shared cookie). Instead of the full 1-RTT wait for the handshake, the server can accept data on the SYN and reply with data immediately, saving the handshake RTT on subsequent connections. This collapses one RTT of connection-setup delay for repeat visits.

Practical bounds: TFO helps repeat connections only (cookie exchange needs a prior session), interacts with middle-boxes (rare incompatibilities), and requires both endpoints to opt in. Enabling it (`net.ipv4.tcp_fastopen`) is a cheap win for browsers/mobile clients that reuse endpoints — the TLS handshake also trims RTTs on subsequent TLS sessions. For HTTP/3/QUIC, the equivalent "0-RTT" gives the same benefit natively.

Verifying benefit: compare TTFB for warm vs cold connections; apply TFO and measure the difference on repeat connections (should drop by approx 1 RTT). When a deployment shows consistent ~1-RTT-lower second-connections, TFO is working; absence of the cookie in captures flags a middle-box blocking the opt-in.

## Q75: What is the interplay between HTTP/2, head-of-line blocking, and TCP?

**A:** HTTP/2 multiplexes many streams over one TCP connection, solving protocol-level HOL blocking at the HTTP layer (multiple requests don't queue behind each other at the application layer). But TCP-level HOL blocking remains: if one segment is lost on the single connection, all streams sharing that TCP connection stall until the retransmission arrives — the "multiple streams, one delivery pipeline" problem that HTTP/3/QUIC solves by moving to per-stream transport (UDP-based).

Impact on performance: HTTP/2's observed latency under loss on a shared connection is worse than the protocol overhead of old mutations — retransmission latency already wastes one connection. But the multiplexing benefit (no serialized request queuing) dominates when the path is clean. Under persistent loss or disorder, the single-connection bottleneck becomes painfully visible — compounding cum-2 retransmission of the shared segment time-stalls every stream.

Troubleshooting: if an HTTP/2 site is slow under loss conditions but police shows per-request timings staggered into stalls, suspect single-TCP HOL blocking; look for QUIC/HTTP-3 fallback or connection-per-request strategies as mitigations. Diagnostic test: compare response-time distribution with loss present via controlled packet loss (tc netem) between HTTP/1.1 vs HTTP/2 vs HTTP/3 — first is serial-loss-sensitive, second is shared-connection-loss-sensitive, third is per-stream-resilient.


## Q76: How do you design an end-to-end network performance measurement strategy?

**A:** An end-to-end strategy measures all layers consistently, continuously, and with a known baseline. It combines: (1) active probes (ping/mtr/iperf scheduled regularly between representative endpoints) for path health; (2) passive flow telemetry (netflow, sFlow, eBPF/tcp-stack metrics, connection-level stats from every host) for real traffic; (3) application-level timings (TTFB, RTT percentiles, SLO metrics) for user-visible impact. Each layer informs the others, and correlation is the payoff.

The measurement architecture should produce coherent time-series: per-hop latency/loss from mtr, aggregate loss/RTT/throughput from flow sampling, and per-service p50/p95/p99 from app instrumentation — stored with matching timestamps and dimensions (source, dest, region, ASN) to enable correlation during incidents. Alerting should be hierarchically layered: path-health alerts, flow-anomaly alerts, and SLO alerts, each with bounds set from baselines, not guesses.

The discipline matters more than the tools: define the source of truth per metric, automate collection, and standardize on the same measurements across every environment (cloud regions, offices, hybrid) so that "does performance differ regionally?" is answerable in a query, not a week of ad-hoc testing. Finally, an incident runbook should describe each metric's expected value and the first hypothesis to test when it breaches.

## Q77: How do you differentiate application-layer latency from network latency in a slow-response problem?

**A:** Differentiating app vs network latency requires measuring where time goes within the request/response cycle. The clean separation: obtain TTFB and its components; record the time from the client sending the request to the server receiving it (network+server ingress), the server's processing time (app), and the time for the response to return (network egress). Captures at client and server with synchronized clocks (or careful one-sided timestamps) provide the sub-half measurements.

The practical method without perfect sync: measure pure round-trip probes (ping: network) vs. full request round-trip (app+network). If TTFB ≈ ping time + server processing → app dominates; if TTFB ≈ ping time only → the network is the main contributor and the app is fast; if TTFB is much larger than ping + plausible app time → network, server stack (TLS, queue), or app scheduling ate the delta. Increasing confidence requires app-side instrumentation (e.g., request timing logs) to isolate server processing.

Advanced differentiation uses trace spans across the request path (client→LB→service→DB) to see where the big time bucket sits: queue-in-front-of-server, app code, DB, or remote call. Network latency shows as a consistent floor; app latency as server-side time; the sum and the ratio tell you whether to tune the network, the upstream third-party, or the code.

## Q78: What is TCP pacing and when is it necessary for high throughput?

**A:** TCP pacing spreads the bytes of a congestion window evenly over the RTT rather than bursting a window back-to-back. Bursts arrive at the bottleneck buffer in a pile, causing loss and queueing — exactly what pacing prevents. Pacing is especially important at high rates: at 10 Gbps, a large window burst fills a router buffer in microseconds; the buffer drains at line rate, but the arrival pile triggers drops and queueing-driven RTT inflation.

Standard stacks pace automatically using pacing rates from the congestion algorithm; BBR is fundamentally pacing-based. Some scenarios need explicit pacing tuning: multi-gigabit paths with small bottleneck buffers, path bursts from servers in data centers that have large windows, and shared links where bursts harm other flows. On such paths, achieving full throughput while keeping latency low is often only possible with pacing (measured as sustained rate + low p99 without pacing).

Practical signs pacing is needed: iperf single-flow is far below the link capacity; the measured RTT under load is wildly higher than idle; packet captures show clumped transmission bursts followed by silence. Enable pacing (fq/pacing in the scheduler, or `SO_MAX_PACING_RATE`), re-test both throughput and p99 RTT — if both improve into line, bursts were the enemy.

## Q79: How do you configure sysctls to improve TCP throughput for high-BDP paths?

**A:** Key sysctls for high-BDP paths: `net.ipv4.tcp_rmem`/`tcp_wmem` (socket buffers — increase max, e.g., 16-64MB, letting auto-tuning grow); `net.core.rmem_max`/`wmem_max` (global caps that must be ≥ buffer max); `net.ipv4.tcp_window_scaling` (ensure on); `tcp_congestion_control` (choose bbr for BDP paths, cubic as fallback); `tcp_sack` (enable); `tcp_timestamps` (enable for accurate RTT/PAWS); `tcp_slow_start_after_idle`=0 (avoid window collapse after idle); `tcp_notsent_lowat` for low-latency to tune flushing.

The systematic approach: compute the BDP (bandwidth × RTT), then set socket-buffer maximums to 1.5-2× the BDP; enable window scaling/timestamps/SACK (verify options aren't stripped); choose the algorithm tuned to loss/delay of the path. Practical testing loop: change, iperf, `ss -ti` verify cwnd reached the BDP, confirm per-flow throughput nears the ceiling.

Cautions: raised buffers increase memory per connection at scale (multiply by connection count), so size by worst-case connection count; congestion-control choice interacts with fairness on shared bottlenecks; sysctls are per-host, so configure consistently across the fleet (include those path hosts). Always baseline and verify changes against measurement before leaving them set.

## Q80: How do you use `ethtool` and interface statistics to find host-side bottlenecks?

**A:** Host-side networking bottlenecks live below the socket layer: NIC hardware, driver, IRQ/softirq CPU, buffers, offloads. `ethtool` is the primary lens: `ethtool -S dev` shows detailed counters (rx_/tx_ errors, drops, overruns, packets-per-queue); `ethtool -g dev` shows ring buffer sizes; `ethtool -G dev rx N` resizes them; `ethtool -l dev` shows RSS queue counts; `ethtool -L dev combined N` changes queue count; `ethtool -k dev` displays offload feature state.

Bottleneck signatures: RX overruns = hardware receive ring overflow (increase ring); RX-drop growth + softirq CPU saturation = host CPU wall (increase queues, set IRQ affinity, use RSS/RPS); TX drops = transmit ring exhaustion or egress policy; counters that grow only under load with no link-marked error = capacity limitation of that stage. Pair `ethtool -S` deltas with CPU per-core stats.

Classification discipline: hardware errors (CRC, frame, nibble) signal a physical/medium fault; kernel drops (via `ip -s` or `netstat -si`) signal host limits; egress drops in tc/qdisc stats signal queue policy. The golden method: create load (iperf) and read counter deltas while watching CPU — whichever single stage saturates first is the host bottleneck. Fix that stage (ring, affinity, offload, queue count) and rectify the ceiling.

## Q81: What is active queue management (AQM) and how do CoDel and fq_codel relate to bufferbloat?

**A:** Active queue management (AQM) proactively controls queue depth before it grows pathological, rather than accepting deep FIFO queues and only dropping on overflow. CoDel detects when queues are building excessively (tracking the minimum sojourn time of recent packets) and then drops or marks packets in a targeted fashion to signal TCP to slow down — specifically designed to defeat bufferbloat by keeping queues low yet loss-bounded.

fq_codel is the packet-scheduler on top: a fair-queue discipline that interleaves many flows' packets (protecting interactive flows from bulk flows' saturation) and applies CoDel per-flow. This combination gives the good properties: low queueing delay for interactive traffic, fair sharing, and meaningful backlog resolution. It's the default on many modern Linux/router stacks (`tc qdisc`).

Troubleshooting with AQM: if you measure high RTT-under-load with stable loss — classic bufferbloat — deploy fq_codel at the bottleneck (often the WAN/router egress). Then re-measure: latency-under-load should collapse while throughput stays near full. The diagnosis is simple (load vs idle RTT), the fix is standard (AQM), and the verification is the same measurement. Where hardware queue policies block AQM, redesign capacity or use rate-limiting upstream of the affected queue.

## Q82: How does the choice of congestion control algorithm (Cubic vs BBR) affect high-latency paths?

**A:** Cubic (default Linux) is loss-based: it grows the window aggressively and reacts to loss, building up queues before loss triggers its backoff. On BDP-heavy paths with tiny loss, Cubic still oscillates the queue up and down, and its throughput is bounded by the loss-derived ceiling sqrt(1.5/ (loss×RTT)) — meaning real (even sub-1%) loss cuts it far below link capacity. BBR runs on a model of bottleneck rate and minimum RTT, targeting the queue-free saturation point, and is far more tolerant of loss because it doesn't use loss as its primary signal.

For high-latency paths (satellite, international fiber, mobile) the difference is stark: on a 200ms RTT, 1 Gbps link, Cubic's achievable throughput under 0.5% loss can drop to a small fraction of 1 Gbps, while BBR typically sustains near-link rates with far lower queuing delay. BBR also handles RTT variability with less tail latency. But BBR's fairness with Cubic flows on shared paths is weaker: BBR doesn't retreat on loss, so a mixed fleet may see Cubic flows squeezed.

Selection process: on paths where loss > ~0.1% or RTT is high and buffers are large, test Cubic versus BBR with iperf, observing both throughput and RTT-under-load. Choose BBR where throughput collapses under loss-based control, twin it with fq pacing, and monitor fairness on shared bottlenecks. On clean, small-RTT paths the difference is minor — don't over-optimize.

## Q83: How do you pin down the exact location of latency in a multi-hop path?

**A:** Localize which hop adds latency using per-hop RTT via mtr and one-way delay where possible. mtr's per-hop RTT aggregates: total path latency, idx mean, per-hop. The algorithm: compute the expected propagation or the previous hop's RTT and flag hops where the delta jumps abnormally. A hop that adds e.g. 80ms where neighbors add 5ms is your suspect — likely a cross-region/transit crossing or a queued hop.

Cross-checking: correlate with any captive-latency text (transit name codes from mtr resolve), verify direction (run mtr back), and test traffic on that hop with ICMP vs TCP probing (tcptraceroute) since some routers prioritize probe ICMP differently. Captures enable precise localization: time the packet at the first capture point and the second capture point (capturing at both ends across the suspect segment) computes the segment's contribution. With multi-path (ECMP), per-hop RTTs can bounce between routes, adding confusing variance.

When the suspect hop is inside your control (router boundary, cloud NPM/LB, modem), inspect its queue/CPU/config; when it's an ISP/transit, report with the mtr evidence. Practical guidance: compute the floor for each hop's plausible propagation (distance-based) and use "RTT − floor" as the queueing component; the hop with the biggest unexplained queueing delta is where the latency lives.

## Q84: What is the "close" (TIME_WAIT, FIN) behavior and how does it affect servers?

**A:** TCP teardown leaves the side that initiated the close in TIME_WAIT for 2×MSL (typically 60s Linux default) — ensuring the finals and retransmitted segments are dead before ports get reused. On busy servers, short-lived connections create a TIME_WAIT pile-up that consumes the ephemeral port space (16-bit local ports, bounded by `ip_local_port_range`) and memory, and can cause "cannot assign requested address" errors when new connections can't find ports.

Interpretation for performance: TIME_WAIT accumulation is a symptom of connection churn. Lots of short connections (HTTP/1.0-style, or clients not reusing connections) produce TIME_WAIT storms. Mitigations: enable connection reuse/keep-alive at the client/protocol level, tune `tcp_tw_reuse` (client-side only, safe under RFC 6056's port randomization), shorten `tcp_fin_timeout` cautiously, or size ports accordingly. For server-side, TIME_WAIT is more storage than a grave problem — measure whether you're actually exhausting ports.

Diagnosis: `ss -tan state time-wait | wc -l` with growth over time; `net.ipv4.ip_local_port_range`; error logs "Address already in use". The correct fix is almost always better connection reuse (fewer TIME_WAIT) rather than fiddling with reuse/recycle sysctls — that reduces actual load, not just symptom-pressure. Treat TIME_WAIT as a protocol-correctness feature; the design response is connection amortization.

## Q85: How do you use synthetic traffic (load generation) to test network capacity?

**A:** Synthetic load generation (iperf, netperf, hping/trex for packets, tcpreplay for captured flows) measures capacity and policy without relying on real user traffic. Correct method: generate at the rate/pattern of the production profile (packet mix, sizes, concurrency), measure achieved rate/延迟/loss/jitter, and compare against computed ceilings (BDP, NIC limits, per-queue CPU, AQM threshold). Vary variables one at a time: parallel flows, packet size, window, algorithm.

Practical battery: (1) iperf TCP single-flow → per-flow ceiling; (2) iperf UDP at fixed rate → loss jitter; (3) netperf (request/response) → RPS/small-packet latency; (4) trex/pktgen for pps capacity and NIC offload testing; (5) replay at realistic burst pattern → how bursts behave; (6) balanced source/dest across hops to see each segment's ceiling. Record results with the exact config for reproducibility.

Interpretation pitfalls: synthetic traffic at unrealistically high rates can trigger reliability mechanisms (policers, congestion collapse) that real traffic wouldn't; and synthetic small-packet floods test host-packet-path (pps), not link bandwidth (bps). So the test must mirror the production workload (sizes, distribution, flow count). Capacity results without a recorded methodology are noise — standardize the battery and baseline before and after changes.

## Q86: How do you troubleshoot slow performance for a single client but not others?

**A:** A single-slow-client pattern (one user/office slow, everyone else fine) excludes server-side and shared-infrastructure causes and points to the client's unique path or local conditions. Begin with the discriminating tests: compare ping/mtr from the slow client vs a healthy client to the same server; compare iperf to the same server from both; compare DNS resolution. The comparison isolates whether the problem is at the client's link (Wi-Fi, ISP uplink saturation), the client's local path (VPN, proxy, middleware), or the local branch route.

Common single-site culprits: saturated local link (home/office bandwidth exhausted by other workloads), upstream ISP congestion or packet loss on that path, VPN/proxy overhead (tunneled paths increase RTT and MTU issues), local DNS slowness, Wi-Fi medium contention/interference (radio-level loss generating TCP chaos), or middle-boxes (firewall with per-connection limits, transparent proxy of degraded quality).

Method: measure in-branch LAN latency, WAN path from that branch, and VPN/proxy passed latency; capture locally on the client while reproducing. If the local capture shows clean path but app is slow, the app's path (DNS/certs/upstream) is the issue. If local link shows loss/jitter, work radio or ISP. The branch-specific differential test turns a "network is down" report into a precise single-stage diagnosis.

## Q87: How do you measure and interpret packet loss inside a capture (retransmissions, gaps, out-of-order)?

**A:** Packet loss inside a capture appears as sequence gaps plus their repair: certain transmitted sequence ranges never appear, and the sender responds with retransmissions. When drop analysis properly works, you see: (1) missing segment numbers (gap in received data); (2) duplicate ACKs from the receiver; (3) the retransmission arriving (same segment retransmitted); (4) perhaps SACK blocks listing the missing ranges. Rate = retransmitted bytes ÷ total bytes over the flow.

Interpreting out-of-order: if the "gap" later fills with an original (non-retransmitted segment), that's reordering, not loss — distinguish by retaining the sequence and whether it's a retransmission. TCP timestamps help: a retransmission carries a new timestamp; reordering preserves the original timestamp; flowsmith expert-info in Wireshark flags both. If you see many duplicate ACKs but no subsequent retransmission, that's benign reordering.

Capture caveats: capture loss itself (dropped by the capture mechanism) mimics network gaps — validate capture completeness (e.g., capture at multiple points or check the capture-loss counters), and be aware that offloads (TSO/GRO) hide/recombine segments from the view. The accuracy of your loss numbers depends on knowing what the capture really saw.

## Q88: What metrics would you track in a network SLO/SLI framework?

**A:** As service-level indicators (SLIs), network-focused metrics include: availability (link/route reachability — error-free connectivity %, measured via probes), latency (RTT/TTFB percentiles vs target, e.g., p95 < 100ms), loss (drop/retransmission rate below threshold), throughput/goodput (achieved vs expected), jitter (for interactive/real-time), and connection success rate (SYN-in-SYN-ACK within budget). Each must be measured from meaningful vantage points (edge, per-region, per-critical-path) and continuously.

Designing SLOs: define time windows (typically 30-rolling), error budgets (allowed violation fraction), and where to measure (user-visible point — the client-side vantage, or infrastructure-attached probes). Correlate at multiple layers: an SLA statement like "99.9% of requests complete with TTFB < 500ms" maps to client probes, flow data, and app timings simultaneously; each layer's SLO must be internally consistent with the others.

Practical structure: one top-level user-visible SLO (e.g., TTFB/distribution or request-error rate), a set of component SLIs feeding it (path latency, loss, retrieval, connection errors), each with budget. Alert on budget consumption trend, not on single breaches. The framework's value is forcing measurement and correlation — the specific numbers must derive from your actual traffic baseline, not generic targets.

## Q89: How do you do capacity planning for network throughput?

**A:** Network capacity planning forecasts the infrastructure needed to serve expected traffic with acceptable latency and loss. The method: baseline current utilization (bandwidth, pps, connection rate, buffer/queue depths) per path and per device, model growth (users × per-user throughput, or application growth), add headroom (typically 50-80% max utilization band), and size the segments with the binding constraint (the bottleneck link or host stage first). Validate with load tests at projected volumes.

The plumbing details: convert projections into demand per layer (bps at link, pps at routers/firewalls, connections/sec at LBs). Compute the BDP-corrected effective throughput for the path (not nominal bandwidth), and remember that real flows achieve less than line rate due to protocol overhead and congestion control. Redundancy and failover capacity: sizing must account for a segment's neighbors carrying their load when a segment fails (e.g., during a failover, a link may carry 2× normal).

Management practice: continuously monitor the utilization-vs-capacity trend at the bottleneck (alert when crossing 70-80% sustained), re-baseline seasonal peaks, and provision in lead-time to respond. The discipline is review-and-adjust: forecasts, not predictions; every capacity plan needs a documented trigger to re-run and a defined upgrade trigger.

## Q90: How do you build a systematic troubleshooting playbook for "the network is slow"?

**A:** A playbook turns "the network is slow" into a decision tree: define the symptom precisely (which user, which destination, which direction, what time, which app); then run the baseline layer isolation. Step order: (1) verify reachability and sanity (ping, DNS, basic TCP connect); (2) measure the user's path (mtr, ping percentiles); (3) measure transport (iperf, TCP stats: retrans, windows, receiver); (4) capture on both ends and reproduce; (5) check host resources (CPU/IRQ/offload/buffers); (6) correlate with monitoring/flow data for load or incidents.

Each step appends or excludes a hypothesis: if the path is clean and host is healthy but app is slow, the layer has moved to application/upstream — hand off with evidence (timers stacked). The playbook must define for each measurement "expected value" and "what threshold triggers the next stage," or the team re-derives context on every incident. Escalation criteria: when a step's measurement cannot explain the symptom, state the evidence and escalate toward the next layer.

Best-practice principles: reproduce under controlled conditions, change one variable at a time, keep baselines for every environment (so "expected" is a number, not a guess), and document the runbook's measured ranges. A strong playbook ends with a taxonomy of final diagnoses (link congestion, host ceiling, app stall, DNS latency, MTU/IPMTU, mTLS) with the evidence signature for each.

## Q91: How do you distinguish between sender-side and receiver-side TCP problems?

**A:** TCP problems have directional signatures. Sender-side problems show up in outbound behavior: low/oscillating cwnd, high retransmit counts, tiny ssthresh after loss, busy send buffers, or pacing constraints. Receiver-side problems show up in the advertised window and ACK behavior: zero-window or small-window advertisements, delayed ACKs inflating RTT estimates, receive-buffer exhaustion, or CPU-stall on ACK generation.

Measurement discriminates: capture both endpoints (or use `ss` on each). If the receiver advertises a small window while the sender has big buffers and no retransmits → receiver buffer/application consumption is the issue. If the sender's cwnd is collapsed while receiver windows are ample → sender-side congestion control/loss is limiting. Retransmit count and its pattern also split: sender-driven timeouts (RTO without duplicate-ACKs) vs receiver-acknowledged-loss (fast-retransmit storms with window intact on receiver side).

One-way delay per direction (synchronized clocks) and per-client TCP stats (`ss -ti` on both sides) give the definitive breakdown. When a "slow transfer" is reported, check each side's role in the window/cwnd/ack loop — the receiver-for-sending throughput and the sender-for-cwnd dynamics are the two halves that must agree, and whichever constrains it below expectation is the one to fix.

## Q92: What is the effect of ECMP / multi-path routing on TCP performance?

**A:** ECMP spreads flows across parallel paths; on a per-packet basis without flow-affinity it can split packets of a single flow across paths with different delays, causing reordering, reduced throughput, and spurious retransmissions. The near-universal fix is flow-level hashing (5-tuple), which keeps one flow on one path — preventing the worst reordering in steady state — at the cost of coarse per-flow distribution and potential hot spots under hash collisions.

Path asymmetry from ECMP also affects measurement: mtr/traceroute may show different paths on successive runs (or even during one run), making per-hop RTT interpretation ambiguous. ICMP probes and data flow can traverse different paths between the same hosts, explaining probe/data mismatch. RTT variance and reordering in TCP stats (`ooo`, duplicate ACKs without loss) frequently correlate with ECMP path divergence.

Troubleshooting methodology: check for consistent reordering/ooo signatures without matching loss; compare mtr output across runs; use TCP timestamps to verify RTT variance patterns; verify flow affinity at the load-balancer/network by looking at consistent path selection. If reordering is persistent, options: converge on per-flow hashing, enable reordering-tolerant congestion control, or remove the multi-path segment causing divergence — measure which improvement restores throughput.

## Q93: How do you interpret `ip -s` output and what does per-address vs per-link tell you?

**A:** `ip -s link` (per-link) gives aggregate counters: RX/TX bytes, packets, errors, dropped, overruns, mcast, and for some drivers per-queue details. `ip -s address` breaks out per-IP-address receive/transmit, and `ip -s link show dev` with `-s -s` shows extended stats (rx_fifo_overrun, near-miss, name taken). Per-link counters answer "is this interface healthy?"; per-address counters answer "does this specific IP/VM/vlan see the traffic pattern?"

Interpretation anchors: `rx_dropped` growing = kernel dropping (check buffer, filter, or softirq); `rx_overrun` = ring overflow (hardware); `err` counts on RX = medium-level corruption (CRC) or framing; TX errors = cable/negotiation/fault. Rates matter: compute delta-per-second between two reads to see the drop rate under load vs idle. Also `ip -s link` doesn't count hardware-offloaded processing, which offloads like GRO/TSO mask.

Usage for troubleshooting: correlate per-link drop growth with CPU softirq (host ceiling) vs per-link error growth with medium faults; correlate per-address counters with a specific application's traffic to see if it's the source of the interface's load. Combined with `ethtool -S` (driver-level, even finer), you can attribute link behavior to correct stage: the NIC, the kernel stack, or the tier of the app.

## Q94: How do you use networking information from the kernel (eBPF/perf) to profile host-side delay?

**A:** Host-side delay profiling decomposes time spent inside the network stack on the host: NIC to kernel queue, net_rx softirq to socket, socket to app, plus send-side queueing. Tools: `perf`/`perf record --call-graph -g sleep` on softirq and `softirqs`/`irq` events; bcc/bpftrace tools like `tcplife`, `tcpconnect`, `tcpretrans`, `runqlat`, `softirqs`, `cpuunclaimed`; eBPF kprobes on `tcp_sendmsg`/`tcp_recvmsg`/`skb` functions to measure in-stack time; and `netstat`/`ss`-context checks for queue sizes.

Typical findings: high softirq CPU with low app CPU → kernel/NIC-hash bottleneck (fix affinity, offload); high `skb` queueing time → NIC-to-socket throughput ceiling; packet delay inside the VM → hypervisor/virtio overhead; RTT differences between a local client and server on the same host → host stack serialization. `tcpretrans` with eBPF attaches retransmission events to the exact flow and timestamp, making causality direct.

The practical method: while reproducing, capture stack traces on softirq (`perf record -g -e irq:softirq... -c 1 sleep 10`), run metric tools concurrently, and correlate with `ss -ti` and interface counters. When the in-kernel time matches the extra per-hop latency you don't otherwise see in-based probes, you've located the host-stage bottleneck. This is the modern step up from `netstat -i` hand-in-counting, giving exact function-level breakdown.

## Q95: How do you approach performance issues in cloud VMs vs bare metal?

**A:** Cloud VMs share the host's NIC, CPU, and network path with neighbors, so performance variance, capped rates, and host-level noise appear that bare metal doesn't show. Differences that matter: (1) virtual NIC (virtio/ENA/gve) with pps/bps caps set by the cloud provider — verify the instance's advertised network rate limits; (2) shared host CPU for packet processing (softirq can be throttled by building neighbor contention); (3) cloud network paths through VPC/overlays add hops (traceroute into the overlay, not physical hops); (4) bursts are often rate-limited rather than just queued (spike → rebuild to fill window or lose).

Methodology adaptation: cloud testing must include "borrow the instance's advertised rate," wait for spiky neighbor noise by averaging repeated tests, and correlate with the provider's retry/heavy-usage signals (burst re-credit, VCPU steal). Compare latency to a mapping instance or regional baseline; check the provider's metrics (CloudWatch, GCP's network metrics, Azure's Log Analytics counters) for the instance-level tx/rx rates against the caps.

Bare-metal keeps classic LAN behavior: physical NIC performance, driver tuning, and CPU affinity rule. The same measurement battery runs on both, but the thresholds and the "expected value" differ: cloud abides by metered caps and neighbor noise; bare metal by hardware capability. Document the platform ceiling before diagnosing a "throughput" discrepancy — a VM capped at 16 Gbps that "should" hit 32 is working correctly, not broken.

## Q96: How do you integrate network metrics into observability (metrics, logs, traces) for ongoing performance?

**A:** Network observability integration makes network state a first-class signal alongside application metrics: (1) per-flow metrics (RTT, cwnd, retransmits, buffer usage) exported from hosts via Node Exporter/ebpf exporters or cloud agent metrics; (2) flow-level sampling (netflow/sFlow/IPFIX) into pipelines (e.g., Flow collector, kafka→store) for path/volume analysis; (3) active probes (ping/mtr/iperf schedules) as synthetic sources; (4) traces with span-level "network hops" (DB call, HTTP call) that embed network timing; (5) logs of connection events (SYN failures, resets) from stacks and firewalls.

Correlation design: tag metrics with source/dest/region/ASN, so at incident time you can join app SLO breaches to network signals (e.g., p99 TTFB up + path loss spike + cwnd collapse = highly correlated). Define the "already-known" facts: this is a network-journeyman setup where the SLO breach either has a network correlate or cleanly excludes the network (app-only), dramatically shortening incident scope.

Operational aspects: set alert thresholds from baselined percentiles, retain enough history (min 30d) for trend/capacity analysis, and document dashboards mapping the top talkers, the path with the highest loss, and per-region latency distribution. This makes the standard answer "is it the network?" data-backed rather than vibes-based.

## Q97: What is the difference between measuring latency at layer 2/3/4/7?

**A:** Each layer's latency measures different scope: L2 = link-layer (MAC-level frame delivery on one segment, VID/gateway — ~sub-ms to few ms); L3 = IP forwarding path (per-hop router delays, including queueing — this is what ping/ICMP and mtr capture); L4 = transport end-to-end (TCP handshake, RTT measured at the transport — includes processing at hosts); L7 = application/HTTP-level (TTFB, response time — includes server processing and protocol stack on both ends). Each measurement includes all layers below it plus its own overhead.

Interpretation value: layer deltas localize. If TTFB (L7) is 500ms but L4 RTT is 40ms → ~460ms lives in the server/app or protocol stack above transport. If L4 RTT (90ms) exceeds L3 ICMP RTT (40ms) → transport stack processing at endpoints or TCP-specific behavior (queueing in host sockets) is adding time. This stacked measurement — L3 ping → L4 TCP RTT (ss, syncookies handshake) → L7 timing — is the standard "latency locator" technique.

Tooling mapping: L3 = ping/mtr; L4 = TCP handshake (curl -w connect time, tcptraceroute, ss rtt), L7 = curl -w TTFB/AppTotalTime, browser devtools timing breakdown. Each has its own filter-policy caveats (ICMP vs TCP vs HTTP prioritized differently by tools/devices). The layered comparison is the discipline — measuring just one layer can't localize; measuring the stack narrows exactly where the time sits.

## Q98: What are the common causes of throughput lower than link speed and how do you classify them?

**A:** Throughput-below-link-speed has four categories. (1) Per-flow protocol ceilings: cwnd/BDP windows, single-flow burst limits, slow-start ramp, retransmission pauses — visible when multi-flow iperf saturates but single-flow doesn't. (2) Loss-driven congestion: packet loss on the path (beyond tiny fractions) collapses classic congestion control; retransmit rate correlates proportionally. (3) Host-side ceilings: NIC speed (negotiated lower), CPU softirq saturation, buffer exhaustion, offload disabled, NIC queue limits — visible via ethtool/CPU stats. (4) Shaping/policing/quotas: ISP or cloud caps, rate-limit policies, protocol-specific throttles — clean path but hard cap.

The classification battery: iperf single vs parallel; iperf UDP to find raw capacity; ping/mtr loss & latency; ethtool/NIC counters and CPU; provider/ISP caps check; capture of the flow to see the constraint knob (cwnd, window, loss). Match the observed ceiling to the category: single-流-limited = protocol; rate-correlated loss = path; CPU-softirq-saturated = host; hard rate cap = policy.

Then the fix follows the category: algorithm/window/buffer tuning for protocol; path repair or BBR for loss; NIC/CPU/offload for host; contract/plan for policy. Most production "slower than expected" is a combination — the proper diagnosis states which category dominates and validates the fix by re-measurement.

## Q99: How do you use packet capture to verify TCP performance for a database connection?

**A:** Database capture analysis targets the connection's behavior: handshake and TLS setup time, request/response round-trips, window use, retransmits, and bytes-per-request ratio. Filter on the DB port (e.g., 5432 for PostgreSQL, 3306 for MySQL) and host pair. Analyze: RTT of the request→response cycle (capture's two segments' timestamps vs TCP RTT — catching app-hold latency inside the DB or the driver); TTFB per query shape; whether transmissions are strictly serial (N+1 pattern) — visible as alternating single requests; and whether any large-result fetches are throughput-limited.

Whether the capture is on the app or DB side determines the view: app-side capture shows the transmissions the client sees; DB-side capture shows what actually arrived — comparing both distinguishes client→server loss from server→client loss and a slow DB from a slow network. Also verify window scaling/SACK/TLS session reuse (from the option fields) to confirm protocol-level tuning; TLS handshake repeated per connection (session cache evictions) adds RTTs per new connection.

The performance conclusions: query latency pattern (per-query RTT × count) tells if the time is distributed or concentrated; a DB flow that shows the app holding connections idle (long gaps between packets) indicates pool/connection misuse; throughput-bound streams (no large gaps, windows at ceiling, low loss) indicate the transfer is the cost. Convert these to actions: driver polling, N+1 reduction, connection reuse, TLS session resumption, or larger fetch windows.

## Q100: What is the balanced approach to using network tools versus databases/build systems for diagnosis?

**A:** Real-world diagnosis requires knowing when a tool's output is trustworthy and which layer each tool sees. The discipline splits: active tools (ping/traceroute/iperf/mtr) test the path as they see it — possibly different from user flows (ICMP vs TCP, probe size vs real packets, probe rate vs actual load); capture tools (tcpdump/tshark/Wireshark) give ground truth for the traffic they actually saw, but sees its own visibility limits (filtering, offload, capture loss); kernel counters (ss/netstat/ethtool) summarize what the box processed, hiding the deepest details without eBPF/perf.

The authoritative sequence during an incident: (1) define the exact symptom and the expected value from baselines; (2) start with the least intrusive measurement (counters, `ss`, monitors) — most problems are "neutered" by a single counter; (3) escalate to active tests (mtr, iperf) to isolate layer/path; (4) capture both endpoints when precision is required (exact location, exact cause) — the most convincing evidence; (5) kernel profiling (perf/eBPF) for host-side time. Each result is documented with the measurement conditions, so the narrative "network slow → it was the DB" is provable, not asserted.

The final discipline is avoiding dogmatism: verify each conclusion with a second independent method (counters + capture; mtr + iperf; iperf + app timer) and test the fix by re-measuring. The best diagnostician knows both the tools and their measurement blind spots, and communicates the evidence trail, whether the answer lies in the network, the host, the app, or the provider.
