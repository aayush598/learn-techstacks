# IPC Overview and Comparison

> **TL;DR**: Pipes/FIFOs (byte streams, related procs), message queues (structured, prioritized), shared memory (fastest, no sync), IPC semaphores (coordination), sockets (network + full-duplex), signals (async events). Choose by **throughput, structure, scope (local/network), synchronization needs, and portability**. Shared memory wins on bandwidth; sockets win on generality; pipes win on simplicity; signals win on eventing.

## 1. Why Does This Exist?
There are many ways processes can talk, and each fits a different need. This section isn't a new mechanism — it's the **decision framework** that ties Sections 01–05 together: given a problem (stream data, exchange records, share a hot buffer, coordinate access, talk over a network, react to an event), which IPC should you pick, and why? Interviewers love this question precisely because there's no universal answer: the right choice trades throughput, latency, structure, complexity, scope, and synchronization cost. Knowing the comparison table cold (plus the two or three real trade-offs per choice) is the whole section.

## 2. How Does It Work? (The Comparison Model)
The decision is driven by a few axes:

| Axis | Pipe/FIFO | Message Queue | Shared Mem | Semaphore | Socket | Signal |
|---|---|---|---|---|---|---|
| **Data model** | byte stream | message (type+len) | raw bytes | counter/flag | bytes/datagram | tiny event |
| **Direction** | one-way | one-way (per queue) | both | — | full-duplex | one-way (async) |
| **Copy cost** | 2 (user↔kernel×2) | 2 | 0 | 0 | 2 (socket buffers) | ~0 (frame) |
| **Syscalls/data transfer** | 2 per op | 2 per msg | 0 after setup | futex (contended only) | 2 per op + protocol | 1 per signal |
| **Ordering** | FIFO | FIFO/priority | none | none | stream order / dgram none | none (RT: prio) |
| **Blocking/flow control** | yes (kernel) | yes (full/empty) | no (app) | yes (wait) | yes (buffer) | no |
| **Sync provided** | no (inherent) | no (inherent) | **no** | **yes** | no (inherent) | no |
| **Scope** | same host | same host | same host | same host | **any host** | same host |
| **Related/unrelated procs** | pipe: related; FIFO: any | any | any | any | any | any |
| **Setup cost** | 1 syscall | key/name | open+mmap | open | socket+bind+listen | sigaction |

**Rules of thumb**:
- **Streams**: pipe/FIFO. **Structured/typed**: MQ. **Throughput-critical**: shared memory. **Coordination**: semaphores. **Network/dual-host or full-duplex + scale**: sockets. **Events/notifications**: signals.
- **Latency** (typical same-host): shared memory < signals < pipes < sockets(AF_UNIX) < MQ < sockets(AF_INET).
- **Throughput** (typical): shared memory ≫ AF_UNIX sockets > pipes > MQ > AF_INET.

## 3. When Is It Used? (Selection Guide)
- **Producer–consumer streaming** (shell pipes, log pipelines, media): **pipes/FIFO** — blocking, ordered, cheap.
- **Job/task queues with priorities** (workers, event buses): **message queues** — structured, prioritized, decoupled.
- **High-frequency / shared hot state** (in-memory DBs, trading, media frames): **shared memory** + **semaphores** for sync.
- **Client–server over network or local service endpoints**: **sockets** (AF_UNIX local, AF_INET remote).
- **Asynchronous notification** (child exited, Ctrl-C, timeout, config reload): **signals**.
- **Multiple resources, cross-process locks**: **semaphores** (or process-shared pthread mutexes).
- **RPC/framework IPC**: built on sockets (gRPC, Thrift) or shared memory (fast local IPC).

## 4. Why Wasn't Another Approach Chosen? (Per Mechanism)
- **Pipe vs socket**: pipe = simplest stream for related procs; socket = needed when full-duplex, addressing, or networking appears.
- **MQ vs socket**: MQ = local typed/prioritized exchange with kernel buffering; socket = when you might go remote, or want streaming/connection semantics.
- **Shm vs everything**: shm = only when throughput dominates and you accept sync responsibility; otherwise the copy cost of pipes/MQs/sockets is worth the safety.
- **Signals vs polling**: signals = push; polling = pull. If you need *state* not just "something happened", poll/epoll on sockets or a pipe.
- **SysV vs POSIX**: POSIX is the modern choice (fd-based, futex-backed, cleaner); SysV remains for compatibility (key-based, arrays, SEM_UNDO).

## 5. Intuition
Think of IPC as **transport modes**:
- **Pipe** = a conveyor belt (one-way, ordered, backpressured).
- **Message queue** = a post office with sorting trays (typed, prioritized, buffered).
- **Shared memory** = a shared whiteboard (fastest, but no one manages who writes — you bring the rules).
- **Semaphore** = the traffic light (coordination only, no data).
- **Socket** = a phone system (full-duplex, networked, addressing).
- **Signal** = the tap on the shoulder (async event, no payload to speak of).

Pick the vehicle by the cargo and the trip: bytes → belt; records → post office; hot shared state → whiteboard (+ light); remote → phone; events → shoulder tap.

## 6. Real-World Analogy
**A company campus**: 
- **Pipes** = the internal interoffice mail tubes between adjacent departments (fast, one-way, only for those departments).
- **MQs** = the central mailroom with priority bins (anyone can send; urgent bins cleared first; mail sits until picked up).
- **Shared memory** = the shared planning wall every department reads/writes directly (instant, but everyone must agree who writes first).
- **Semaphores** = the single restroom key (coordination, nothing else).
- **Sockets** = the phone system (any phone to any phone, inside or outside the campus).
- **Signals** = the PA announcement / intercom ping ("meeting at 3", "all clear").

## 7. Formal Definition
IPC = mechanisms enabling processes (separate address spaces) to exchange data or synchronize, provided by the kernel. Mechanisms: **pipes** (`pipe`, `pipe_buffer` ring, unidirectional); **FIFOs** (named pipes, `mkfifo`); **message queues** (SysV `msg_queue`, POSIX `mqueue`, typed/prioritized); **shared memory** (POSIX shm_open+mmap, SysV shmget/shmat — shared physical pages); **semaphores** (SysV `sem_array`, POSIX `sem_t` over futexes); **sockets** (`AF_UNIX`/`AF_INET` + `sk_buff`); **signals** (per-process pending sets + handlers). Selection criteria: data model (stream/message/bytes/event), direction (one-way/full-duplex/async), copy count (0/2), ordering guarantee, flow control (kernel/app), scope (local/network), synchronization included (yes/no), setup cost, and portability.

## 8. Example
Compare sending 100 KB from producer to consumer via:
- **Pipe**: `write(fd, buf, 100000)` — one copy into the ring (in PIPE_BUF-sized chunks), consumer `read`s it back out. Total: 2 kernel copies, 2+ syscalls, ordered, backpressured.
- **MQ**: `mq_send` — message copied into the kernel queue (limited by `mq_msgsize`; a 100 KB message needs a big queue), then `mq_receive` copies it out. 2 copies, no ordering issues, but queue limits + one message.
- **Shared memory**: producer `memcpy`s into the shared region, consumer reads it — **0 copies, 0 syscalls**; both must agree on layout + a semaphore to prevent tearing.
- **Socket**: `send`/`recv` via AF_UNIX — copies into socket buffers (2), plus protocol overhead; stream mode has no message boundary.
- **Signal**: can't carry 100 KB — tiny payload only.

Real decision: for a 100 KB hot buffer → shared memory + semaphore. For 100 KB of streamed logs → pipe. For 100 KB as a typed job → MQ or socket.

## 9. Internal Working
The kernel components behind each (per mechanism, all in Section 01–05 detail):
- Pipe: `pipe_inode_info` + ring of `pipe_buffer`s; wait queues for flow control.
- MQ: SysV `msg_queue` list; POSIX `mqueue_inode_info` in mqueuefs with priority-ordered list.
- Shm: tmpfs/shmem page cache, `vm_area_struct` with `VM_SHARED`, PTE sharing; `shm_file` linkage.
- Semaphore: SysV `sem_array`/`struct sem` wait queues; POSIX `sem_t` + futex (word in user space, kernel only on contention).
- Socket: `struct socket`/`sock`, protocol ops, `sk_buff` queues; for AF_UNIX, direct delivery into peer queue.
- Signal: per-thread `pending`/`blocked` sigsets; `do_signal`/`setup_rt_frame` at return-to-user; `rt_sigreturn` restore.
All are subject to the scheduler (blocked processes sleep on wait queues and are woken), and all are isolated per IPC/mount namespace in containers.

## 10. Time Complexity (Comparisons)
- Pipes: O(bytes) copy per transfer; O(1) per op overhead.
- MQ: O(bytes) copy + O(n) priority-list insert (n = queued msgs) worst.
- Shared memory: O(bytes) memcpy **once**, O(1) access — no syscalls after setup.
- Semaphores: O(1) atomic op uncontended (no syscall); O(1) futex on contention.
- Sockets (AF_UNIX): O(bytes) copy + O(1) socket-buffer ops; AF_INET adds O(protocol) + segmentation.
- Signals: O(1) enqueue + O(1) frame setup; delivery at next return-to-user.

Relative latency/throughput (order of magnitude, same host): **shm >> AF_UNIX > pipe ≈ FIFO > MQ > AF_INET**.

## 11. Advantages (Per Mechanism, Quick)
- **Pipe**: simplest; auto flow control; reliable ordered bytes.
- **MQ**: structure + priority + decoupling.
- **Shm**: zero copy, zero syscall — max throughput/latency.
- **Semaphore**: kernel-guaranteed atomicity for cross-process coordination.
- **Socket**: full-duplex, network-capable, standard, multiplexable (epoll).
- **Signal**: async push, no polling, OS-integrated events.

## 12. Disadvantages (Per Mechanism, Quick)
- **Pipe**: one-way; related-procs only (unless FIFO); byte framing.
- **MQ**: 2 copies; size/queue limits; priority starvation; cleanup discipline (SysV).
- **Shm**: no sync/ordering/framing; fixed size; lifetime management; NUMA/cache issues.
- **Semaphore**: no ownership; deadlock-prone if misordered; no data.
- **Socket**: heavier setup + copies; more code; protocol overhead.
- **Signal**: tiny payload; async-signal-safety restrictions; non-queued standard signals; EINTR.

## 13. Interview Questions
1. **Q: How do you choose an IPC mechanism?** A: By data model (stream/message/bytes/event), direction, throughput/latency, scope (local vs network), whether you want kernel-managed ordering/flow-control, and portability. There's no universal best — it's a trade-off.
2. **Q: Which is fastest and why?** A: Shared memory — zero copies and zero syscalls after setup; both processes' PTEs map the same physical pages, so access is a plain load/store.
3. **Q: Which is most general?** A: Sockets — full-duplex, connection-oriented or datagram, and identical API for local (AF_UNIX) and remote (AF_INET) communication; the only IPC that spans machines.
4. **Q: When would you use a pipe over shared memory?** A: When you want kernel-managed flow control/ordering and simplicity, and the data rate is modest — pipes are far simpler to get right; shm's speed only matters when throughput is the bottleneck and you can handle sync.
5. **Q: Signals vs pipes for notification?** A: Signals are push (async interrupt) but limited (tiny payload, async-signal-safety); a pipe is the "self-pipe" trick — write a byte into a pipe in the handler (signal-safe) and `epoll` it — robust async notification.
6. **Q: When to use sockets vs message queues?** A: MQ = local typed/prioritized exchange, decoupled, kernel-buffered; sockets = when you need networking, full-duplex, connection semantics, or scale/multiplexing (epoll). For local client–server, AF_UNIX sockets are often the modern choice.
7. **Q: What's the cost of shared memory (the hidden tax)?** A: Synchronization — you must add semaphores/mutexes/futexes, design the layout, handle lifetime (unlink/REM), and be careful about ordering and false sharing; that's the "free lunch" that isn't free.
8. **Q: Compare SysV vs POSIX IPC overall.** A: POSIX (named, fd-based, futex-backed, cleaner, per-object unlink) is preferred today; System V (key-based, persistent until explicit remove, arrays/SEM_UNDO) remains for legacy compat — glibc/kernel support both.
9. **Q: Which IPC supports flow control?** A: Pipes/FIFOs and sockets (kernel buffers fill → sender blocks); MQs block when full; shared memory does NOT (you'd overflow or need your own signaling); signals have none.
10. **Q: What's the difference between "data" and "synchronization" IPC?** A: Data IPC (pipes, MQ, shm, sockets, signals) carries information; synchronization IPC (semaphores, and mutexes/condition variables) coordinates *access/order* and carries no data — though semaphores also appear as the lock for data IPC.
11. **Q: What is the self-pipe trick?** A: Signal handler writes one byte to a pipe; a main loop `select`/`epoll`s the pipe read end — turning an async signal into a pollable fd event (the safe way to bridge signals and event loops).
12. **Q: If you needed 10 GB/s between two local processes, what would you use?** A: Shared memory (plus sync + careful layout + hugepages/NUMA pinning); nothing else approaches it — this is why trading/media/microservice "fastpath" IPC uses shm or AF_UNIX with zero-copy.

## 14. Follow-Up Questions
1. **Q: What is `io_uring`'s role in IPC?** A: High-throughput async I/O with shared ring buffers — reduces syscall overhead for sockets/files; pairs with shm/socket APIs for high-performance servers.
2. **Q: IPC vs threads for concurrency?** A: Threads share an address space (memory, fds) — cheaper context switch, direct sharing, but a crash kills all and sync is mandatory; processes (IPC) isolate failure, need explicit channels, costlier switching. Choose by isolation vs sharing needs.
3. **Q: What's the "fastpath" in modern microservices?** A: AF_UNIX sockets or shared-memory RPC (e.g., Cap'n Proto RPC, gRPC over UDS) — shm for the hottest path, UDS for general RPC.
4. **Q: How does D-Bus work?** A: An AF_UNIX (and now socketpair-based peer-to-peer in newer versions) message bus for desktop/system services — message-oriented IPC with a broker.

## 15. Coding Example
```c
// Choosing IPC by workload — a tiny benchmark of "send N bytes" round trips
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/wait.h>

int main(void) {
    // 1. Shared memory: 0 syscalls after setup
    int fd = shm_open("/bench", O_CREAT | O_RDWR, 0666);
    ftruncate(fd, 4096);
    char *buf = mmap(NULL, 4096, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);

    pid_t pid = fork();
    if (pid == 0) {
        // 2. AF_UNIX socketpair (child writes, parent reads)
        int sv[2]; socketpair(AF_UNIX, SOCK_STREAM, 0, sv);
        write(sv[1], "ping", 4);      // through the socket
        // 3. shared memory write (no syscall)
        strcpy(buf, "data via shm");
        _exit(0);
    }
    int sv[2]; socketpair(AF_UNIX, SOCK_STREAM, 0, sv);
    char r[8]; read(sv[0], r, 4);  printf("socket got: %s\n", r);
    wait(NULL);
    printf("shm  got: %s\n", buf); // visible instantly (no syscall)

    munmap(buf, 4096); shm_unlink("/bench");
    return 0;
}
```
The lesson: `socketpair` required a read syscall; the shared-memory read was just `buf` — that's the fundamental trade-off.

## 16. Industry Usage
- **Pipes**: shell pipelines, systemd journal streaming, build tools.
- **MQs**: embedded/RTOS, legacy enterprise middleware.
- **Shm**: trading/Media (DPDK), in-memory stores, Varnish, PostgreSQL shared buffers, boost.interprocess.
- **Semaphores**: databases (PostgreSQL PGSemaphore), cross-process singleton locks.
- **Sockets**: the dominant IPC — systemd, DBus, Docker/containerd, gRPC, Redis/PostgreSQL clients, web servers, databases, Kubernetes.
- **Signals**: process supervision (systemd, supervisord), shell job control, daemon reload (SIGHUP), crash handling.

## 17. References
- Stevens, *UNIX Network Programming Vol 2* (IPC — the classic comparison).
- Silberschatz, *Operating System Concepts*, Ch. 3.5–3.6 (IPC mechanisms).
- Tanenbaum, *Modern Operating Systems*, Ch. 3.2 (IPC), Ch. 2 (threads/processes).
- Linux `man 7 sysvipc`, `man 7 sem_overview`, `man 7 shm_overview`, `man 7 mq_overview`, `man 7 unix`, `man 7 signal`.
- Love, *Linux Kernel Development* (fs/pipe.c, ipc/, net/, kernel/signal.c).

## 18. Cheat Sheet
- **Stream** → pipe/FIFO; **message** → MQ; **hot bytes** → shm; **sync** → semaphores; **network/full-duplex** → sockets; **events** → signals.
- Speed: shm >> AF_UNIX > pipe > FIFO > MQ > AF_INET.
- Copies: shm 0; others 2; signals ~0.
- Flow control: pipes/MQ/sockets kernel-side; shm none.
- POSIX over SysV: cleaner/fd-based/futex-backed.
- shm's tax = synchronization (semaphores).
- Sockets are the only network-capable IPC.
- Signals: tiny payload, async-signal-safe handlers only.

## 19. Quiz
1. Fastest IPC? a) pipe b) shm c) socket d) MQ → **b**
2. Which spans machines? a) pipe b) MQ c) socket d) semaphore → **c**
3. Full-duplex local channel? a) pipe b) socketpair c) FIFO d) signal → **b**
4. shm's missing feature? a) speed b) synchronization c) size d) naming → **b**
5. Structured/prioritized exchange? a) pipe b) shm c) MQ d) signal → **c**
6. Best for async events? a) shm b) socket c) signal d) pipe → **c**

## 20. Flashcards
- **Q: Choose by?** → **A:** Data model, direction, speed, scope, sync, portability.
- **Q: Fastest?** → **A:** Shared memory (0 copies, 0 syscalls).
- **Q: Most general?** → **A:** Sockets (full-duplex, networked).
- **Q: shm's tax?** → **A:** Synchronization is your problem.
- **Q: For events?** → **A:** Signals (async push) or self-pipe + epoll.
- **Q: SysV vs POSIX?** → **A:** POSIX preferred; SysV legacy compat.

## 21. Revision
The six IPC mechanisms form a decision space. **Pipes/FIFOs** are the simplest ordered streams for related/any local processes. **Message queues** add structure, type, and priority for decoupled job/event exchange. **Shared memory** is the zero-copy, zero-syscall winner for hot shared state — but hands synchronization to you (semaphores). **IPC semaphores** are the coordination primitive (SysV arrays with SEM_UNDO, POSIX futex-backed named/unnamed). **Sockets** are the general, full-duplex, network-capable channel (AF_UNIX for local, AF_INET for remote). **Signals** are the async event push (with strict handler safety). Choosing IPC is a trade-off — shm for bandwidth, sockets for scope/generality, pipes for simplicity, MQ for structure, semaphores for coordination, signals for events — and the interview answer is always "it depends, here's the trade-off."

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "How do you choose IPC?" | 13 Q1 / 2 How |
| "Which is fastest?" | 13 Q2 / 8 Example |
| "Which is most general?" | 13 Q3 / 2 How |
| "Pipe vs shm?" | 13 Q4 / 4 Why not |
| "Sockets vs MQs?" | 13 Q6 / 3 When |
| "Cost of shared memory?" | 13 Q7 / 12 Disadvantages |
| "Flow control provided by?" | 13 Q9 / 2 How |
| "10 GB/s between processes?" | 13 Q12 / 16 Industry |
