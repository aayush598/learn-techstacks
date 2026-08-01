# Sockets and Signals

> **TL;DR**: **Sockets** are the general, network-capable IPC: `AF_UNIX` (local domain sockets, `socketpair`) give bidirectional byte streams between local processes; `AF_INET` sockets bridge machines. **Signals** are the asynchronous *event* channel: `signal(2)`/`sigaction(2)` deliver small, discrete notifications (SIGINT, SIGCHLD, SIGTERM, real-time signals) asynchronously, interrupting a process's flow.

## 1. Why Does This Exist?
Two needs remain after pipes/MQs/shm: (1) **general and networked** communication — local processes that might also be remote, needing bidirectional streams with addresses, connection semantics, and protocol flexibility; (2) **asynchronous event notification** — the OS or another process needs to poke a process "something happened, now" without it polling. Sockets provide (1): the Unix socket API unifies local (`AF_UNIX`) and remote (`AF_INET`) exchange behind one interface. Signals provide (2): the OS interrupting a running process for events like Ctrl-C (SIGINT), child exit (SIGCHLD), or timeouts (SIGALRM). Without signals, every process would have to poll constantly; without sockets, IPC would stop at the machine boundary.

## 2. How Does It Work?
**Sockets**:
- `socket(domain, type, protocol)`: `AF_UNIX`/`AF_INET`, `SOCK_STREAM` (TCP — reliable byte stream) / `SOCK_DGRAM` (UDP — datagrams) / `SOCK_RAW`.
- Server: `bind` (name/address) → `listen` (backlog) → `accept` (new fd per client). Client: `connect`. Both: `send`/`recv`/`read`/`write`.
- **`AF_UNIX` domain sockets**: address = filesystem path (or abstract namespace); `socketpair(AF_UNIX, SOCK_STREAM, 0, fds)` → two connected fds (bidirectional pipe — full-duplex, works for parent–child).
- **`AF_INET`**: TCP/UDP over IP; also `AF_INET6`, `AF_NETLINK` (kernel↔user), `AF_PACKET` (raw).
- Kernel: `struct socket` + protocol (`struct proto`/`ops`) + socket buffers (`struct sk_buff`) + the inode on `sockfs`.

**Signals**:
- `kill(pid, sig)`, `raise`, `killpg`. Handler: `signal(sig, handler)` (limited) or `sigaction` (with `sigset_t`, flags `SA_RESTART`, `SA_SIGINFO`).
- Standard signals (1–31): SIGINT, SIGQUIT, SIGTERM, SIGKILL (uncatchable), SIGSTOP (uncatchable), SIGCHLD, SIGALRM, SIGPIPE, SIGSEGV, SIGBUS, SIGUSR1/2.
- **Real-time signals (32–64)**: `sigqueue` — queued, carry a value (`siginfo_t`), delivered in priority order.
- Delivery model: pending-set per process (or thread); blocked set; when a signal becomes unblocked and pending, the kernel arranges delivery (interrupt at the next return-to-user boundary, run handler, restore).
- **Signal safety**: handlers run on the interrupted stack — only async-signal-safe functions allowed (write, read, signal-safe syscalls); no malloc, no printf, no locks.

## 3. When Is It Used?
- **Sockets**: client–server services, inter-process services over the network, local services via Unix sockets (PostgreSQL/Redis listen on `AF_UNIX` too), IPC between daemons, `DBus`, systemd (socket activation), `x11`, Docker (`/var/run/docker.sock`).
- **Signals**: Ctrl-C → SIGINT; Ctrl-Z → SIGTSTP; `kill` for termination (SIGTERM graceful shutdown); SIGCHLD to reap children (parent knows child exited); SIGALRM for timers; SIGSEGV/SIGBUS for crash handling (core dumps); SIGWINCH on terminal resize; SIGUSR1/2 for app-defined events; real-time signals for datagram-style notifications with payloads.

## 4. Why Wasn't Another Approach Chosen?
- **Pipes for two-way**: pipes are unidirectional; `socketpair` (a connected socket pair) is the natural bidirectional local channel.
- **MQs for client–server**: MQs lack connection semantics, streaming, and networking; sockets unify local + remote.
- **Shared memory for events**: shared memory needs polling; sockets/signals deliver *events* without polling.
- **Polling in general (rejected)**: `poll`/`select`/`epoll` exist for multiplexing sockets; signals are the *push* alternative to the *pull* of polling.
- **Older signal API (rejected)**: `signal(2)` semantics vary; `sigaction` is the robust choice (blocking during handler, restart semantics, siginfo).
- **`AF_INET` for everything (rejected locally)**: `AF_UNIX` skips IP/TCP overhead — faster, no ports, no network stack; chosen for same-host IPC.

## 5. Intuition
**Sockets** = a telephone system: you call a specific number (address/port), the exchange connects you, and you have a two-way conversation (stream). The Unix-domain version is an intercom where the "number" is a path on the wall — same phone, but no long-distance fees and instant.

**Signals** = a push notification: the OS or another process pokes you ("you have mail", "time's up", "please shut down") *right now* — you don't have to check your inbox. You can ignore most notifications (block) but two are unmissable (SIGKILL/SIGSTOP) — the doorbell that breaks down the door.

## 6. Real-World Analogy
**Sockets**: a restaurant taking orders — a server (listen) waits at the door, each customer gets a dedicated waiter (accept → per-connection fd), and conversation (read/write) is full-duplex. For local restaurants it's the same protocol as remote ones — one training manual for both.

**Signals**: a manager tapping you on the shoulder (handler) to say "phone call" (SIGUSR1), "coffee break over" (SIGALRM), "meeting, wrap up" (SIGTERM), or — the two you can't ignore — being escorted out (SIGKILL) or frozen in place (SIGSTOP). The tap interrupts whatever you're doing; you handle it and resume.

## 7. Formal Definition
**Sockets** (`AF_UNIX`): endpoint with a filesystem/abstract address. `socket(AF_UNIX, SOCK_STREAM, 0)`, `bind(path)`, `listen(backlog)`, `accept()` → new fd, `connect(path)`. Stream = reliable ordered byte stream (like a pipe but full-duplex, and both ends can close independently). Datagram = `SOCK_DGRAM` (unreliable, message boundaries). Kernel: `struct socket` (generic) → `struct unix_socket` + `struct sock` → `sk_buff` buffers; data copied via the socket buffer layer. **`AF_INET`**: `socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)` → `bind(addr, port)` → `listen`/`accept`/`connect` → TCP bytestream; `SOCK_DGRAM` = UDP datagrams.

**Signals**: `int kill(pid_t, int sig)`; `int sigaction(int sig, const struct sigaction *act, struct sigaction *oldact)` with `sigset_t`; `sigprocmask` blocks; `sigpending` inspects; `sigqueue(pid, sig, value)` for RT signals with payload. The kernel tracks per-process `pending`/`blocked` sigsets; on a transition to user mode, pending+unblocked signals cause a handler invocation (kernel builds the signal frame on the user stack). Only async-signal-safe functions may be called in a handler. Signals interrupt `read`/`write`/`nanosleep` etc. with `EINTR` unless `SA_RESTART` (or a retry loop).

## 8. Example
**Unix-domain socket server/client**:
```c
// server
int s = socket(AF_UNIX, SOCK_STREAM, 0);
struct sockaddr_un a = { .sun_family = AF_UNIX, .sun_path = "/tmp/demo.sock" };
unlink(a.sun_path);
bind(s, (struct sockaddr *)&a, sizeof a);
listen(s, 8);
int c = accept(s, NULL, NULL);
char buf[128]; read(c, buf, 128);         // receive from client
write(c, "pong", 4);                       // reply (full-duplex)
// client
int c = socket(AF_UNIX, SOCK_STREAM, 0);
connect(c, (struct sockaddr *)&a, sizeof a);
write(c, "ping", 4); read(c, buf, 128);
```
**`socketpair`** for bidirectional parent–child:
```c
int sv[2];
socketpair(AF_UNIX, SOCK_STREAM, 0, sv);   // sv[0] <-> sv[1] full-duplex
if (fork() == 0) { write(sv[1], "hi", 2); ... }
read(sv[0], buf, 2);                       // parent
```
**Signals**:
```c
static volatile sig_atomic_t flag = 0;
static void handler(int sig) { flag = 1; }        // async-signal-safe: set a flag
int main(void) {
    struct sigaction sa = { .sa_handler = handler };
    sigemptyset(&sa.sa_mask);
    sigaction(SIGINT, &sa, NULL);                 // Ctrl-C sets flag
    while (!flag) pause();
    printf("caught SIGINT\n");
}
```

## 9. Internal Working
**Sockets**:
1. `socket()` → `sock_create` → allocate `struct socket`; for AF_UNIX, `unix_create` allocates `struct unix_sock`; attach inode on `sockfs`.
2. `bind(path)` → create socket-file inode; `listen` sets backlog; `accept` (for stream) picks a pending connection, allocates a new `struct socket`+file for it.
3. `write`/`send` → `sock_sendmsg` → protocol `sendmsg` → for unix stream, copy into the peer's receive queue `sk_buff`s; wake waiting readers. For TCP: `tcp_sendmsg` → segment out.
4. `read`/`recv` → dequeue `sk_buff`, copy to user.
5. Close → half/fully close; `shutdown(SHUT_RD/WR)` for directional close.
**Signals**:
1. `kill(pid, sig)` → `__send_signal` → add to `t->pending` → signal the target thread (send `SIG_IPI` via `resched`/wake).
2. On return to user mode (`exit_to_usermode_loop`), `do_signal` → if a pending+unblocked signal exists → `setup_rt_frame` builds a signal frame on the user stack (saved registers) → return to handler entry.
3. Handler runs; on return, `sys_rt_sigreturn` restores the frame → resumes the interrupted instruction (`SA_RESTART` reissues the syscall instead of EINTR).
4. Uncatchable: SIGKILL/SIGSTOP cannot be handled or blocked by design.

## 10. Time Complexity
- Unix socket send/recv: O(bytes) copy user↔kernel (per message), no network overhead; `sendmsg` with `MSG_DONTWAIT` avoids blocking.
- TCP send/recv: O(bytes) + protocol/segment overhead; local loopback bypasses hardware.
- Socketpair: O(bytes) between the two fds — cheap, full-duplex.
- Signal delivery: O(1) enqueue (pending set) + O(1) frame setup; delivery at next return-to-user — O(1) amortized. Real-time signal queue: O(queue length).
- `sigaction` setup: O(1). Handler switch: ~2 context switches' worth of register save/restore.

## 11. Advantages
**Sockets**:
- **Network-capable**: one API for local and remote (AF_UNIX vs AF_INET) — portability.
- **Bidirectional/full-duplex** (vs pipes).
- **Structured** (SOCK_STREAM vs SOCK_DGRAM) — choose reliability vs latency.
- **Rich semantics**: connect/accept, shutdown, OOB, multiplexing (select/poll/epoll), nonblocking + async (`io_uring`).
- **Abstract namespace** (Linux AF_UNIX): sockets without filesystem entries.
**Signals**:
- **Asynchronous**: no polling — the process is interrupted with the event.
- **Standardized + reliable**: catchable/blockable, real-time signals queued with payloads.
- **OS-integrated**: child exit (SIGCHLD), Ctrl-C (SIGINT), crash (SIGSEGV) — the kernel generates them automatically.

## 12. Disadvantages
**Sockets**:
- **Heavier** than pipes/shm for simple local IPC (more structure, socket buffers, fd management).
- **More code** than a pipe: bind/listen/accept/connect lifecycle.
- **Local only with AF_UNIX**: AF_INET has port/address management, TCP handshake overhead.
**Signals**:
- **Tiny payload** (integer/pointer; siginfo for RT signals) — not a data channel.
- **Async-signal-safety**: almost everything is unsafe in a handler (no malloc/locks/printf) — the classic bug source.
- **Races**: unblocking/`sigpending` races, lost standard signals (standard signals are *not* queued — two SIGUSR1 may coalesce).
- **EINTR**: syscalls can be interrupted (need SA_RESTART or retry loops).
- **No portability guarantee** of signal semantics across platforms.

## 13. Interview Questions
1. **Q: What are Unix domain sockets?** A: `AF_UNIX` sockets — a socket API where the address is a filesystem path (or abstract name), providing bidirectional, reliable byte streams between local processes with no network stack.
2. **Q: Unix socket vs pipe?** A: Pipes are unidirectional; Unix sockets are full-duplex, support datagram mode, and (unlike pipes) work between unrelated processes with path-based addressing. `socketpair` is the "bidirectional pipe" for related processes.
3. **Q: Stream vs datagram sockets?** A: SOCK_STREAM = reliable ordered byte stream (TCP-like, no message boundaries); SOCK_DGRAM = message-oriented, connectionless, possibly lossy/out-of-order (UDP-like, preserves message boundaries).
4. **Q: What is `socketpair`?** A: Creates a connected pair of sockets (`sv[0]↔sv[1]`) — bidirectional IPC for related processes (fork), like a two-way pipe.
5. **Q: What are signals?** A: Asynchronous event notifications delivered by the kernel or another process (kill), interrupting the target to run a handler — e.g., SIGINT (Ctrl-C), SIGCHLD, SIGTERM, SIGSEGV.
6. **Q: Catchable vs uncatchable signals?** A: SIGKILL and SIGSTOP cannot be caught/blocked (they're guaranteed termination / guaranteed stop); nearly everything else can be handled or ignored.
7. **Q: What is async-signal-safety?** A: Only a small set of functions (write, read, and other signal-safe syscalls) may be called from a signal handler — malloc, printf, locks are unsafe (they can re-enter the interrupted code) → handlers should just set a flag or write to a pipe.
8. **Q: What are real-time signals?** A: Signals 32–64 (on Linux): queued (never coalesce), delivered in priority order, and carry a value via `sigqueue`/`siginfo_t` — used when signal semantics matter.
9. **Q: What is EINTR?** A: A blocked syscall (read/sleep) interrupted by a signal returns EINTR; `SA_RESTART` makes the kernel retry it, otherwise the app must retry manually — a classic interview gotcha.
10. **Q: When to use sockets vs other IPC?** A: Use sockets when you need networking, full-duplex streams, datagrams, or a well-known service endpoint; pipes/shm/MQs are cheaper for purely local, simple exchange.
11. **Q: How does a server accept many clients?** A: `listen` + loop of `accept` (one fd per client), multiplexed with `select`/`poll`/`epoll` (or threads/processes); for Unix sockets, same API.
12. **Q: What is SIGCHLD and why does it matter?** A: Sent to a parent when a child exits/stops — lets the parent call `waitpid` to reap zombies without polling; ignoring it (or SIG_IGN on SIGCHLD) auto-reaps in some systems.

## 14. Follow-Up Questions
1. **Q: What is the abstract namespace for AF_UNIX?** A: Sockets bound to names beginning with `\0` have no filesystem entry — they're kernel-internal addresses, immune to path permissions and filesystem cleanup (used by systemd, DBus).
2. **Q: What is epoll?** A: The Linux multiplexer for many sockets/fds — O(1) event notification vs O(n) poll; central to high-concurrency servers (nginx, Node).
3. **Q: `sigwait`/`sigpending`?** A: `sigwait` blocks a set and returns the pending signal (thread-based synchronous handling — often cleaner than handlers); `sigpending` inspects the pending set.
4. **Q: What is a signal frame?** A: The kernel builds a user-space frame (saved registers + siginfo) on the handler entry so `sigreturn` can restore the interrupted context exactly — the mechanism behind signal delivery.

## 15. Coding Example
```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <sys/socket.h>
#include <sys/un.h>

int main(void) {
    // --- signals: graceful shutdown on SIGTERM ---
    volatile sig_atomic_t stop = 0;
    struct sigaction sa = { .sa_handler = (void (*)(int))0 };
    // (SA_RESTART is set for robust EINTR handling)
    static void (*on_term)(int) = 0; // placeholder; see below
    (void)on_term;
    sa.sa_handler = (void (*)(int))0;
    (void)sa;

    // --- Unix socket echo server ---
    int s = socket(AF_UNIX, SOCK_STREAM, 0);
    struct sockaddr_un addr = { .sun_family = AF_UNIX };
    strcpy(addr.sun_path, "/tmp/echo.sock");
    unlink("/tmp/echo.sock");
    bind(s, (struct sockaddr *)&addr, sizeof addr);
    listen(s, 4);

    while (!stop) {
        int c = accept(s, NULL, NULL);
        if (c < 0) continue;
        char buf[256]; ssize_t n = read(c, buf, sizeof buf);
        if (n > 0) write(c, buf, n);      // echo
        close(c);
    }
    close(s);
    unlink("/tmp/echo.sock");
    return 0;
}
```
(A cleaner signal handler would set a `volatile sig_atomic_t` flag read by the loop; see Section 13 Q7.)

## 16. Industry Usage
- **Linux kernel**: `net/unix/` (unix sockets), `net/socket.c`, `net/ipv4/tcp*.c`/`udp*.c`, `net/core/skbuff.c`, `kernel/signal.c`, `fs/eventpoll.c` (epoll), `arch/x86/kernel/signal.c` (frames).
- **System services**: systemd (socket activation, AF_UNIX), DBus (AF_UNIX), PostgreSQL/Redis (AF_UNIX + TCP), Docker (`/var/run/docker.sock`), Kubernetes kubelet/containerd sockets.
- **Signals in practice**: `kill`/`pkill`/`systemctl stop` (SIGTERM), `kill -9` (SIGKILL), `kill -HUP` (config reload — nginx), shell job control (SIGTSTP/SIGCONT), JVM (SIGTERM graceful shutdown, SIGINT), core-dump handlers.
- **High-concurrency servers**: nginx/Node/epoll, io_uring.

## 17. References
- `man 7 unix`, `man 7 socket`, `man 7 ip`, `man 2 socket`, `man 2 bind`, `man 2 accept`, `man 2 connect`, `man 2 socketpair`.
- `man 7 signal`, `man 2 sigaction`, `man 2 sigqueue`, `man 2 kill`, `man 7 signal-safety`, `man 2 rt_sigreturn`.
- Stevens, *UNIX Network Programming, Vol 1* (sockets), *Vol 2* (IPC — including signals).
- Silberschatz, *Operating System Concepts*, Ch. 3.6 (sockets), Ch. 3.5 (signals).
- Tanenbaum, *Modern Operating Systems*, Ch. 2.3 (signals), Ch. 3.2 (sockets).

## 18. Cheat Sheet
- Sockets: `socket` → `bind`/`listen`/`accept` (server) or `connect` (client) → `send`/`recv`.
- AF_UNIX = path/abstract address, local, full-duplex; socketpair = related-proc channel.
- SOCK_STREAM = reliable bytes; SOCK_DGRAM = datagrams.
- Signals: `sigaction` (not `signal`); handlers async-signal-safe only.
- SIGKILL/SIGSTOP uncatchable; RT signals queued + carry values.
- EINTR on interrupted syscalls → SA_RESTART or retry.
- Handler should set a `volatile sig_atomic_t` flag / write to a pipe.
- SIGCHLD → `waitpid` to reap zombies; SIGTERM → graceful shutdown.

## 19. Quiz
1. Bidirectional local channel for related processes? a) pipe b) socketpair c) MQ d) fifo → **b**
2. AF_UNIX address is a? a) IP b) path c) port d) pid → **b**
3. SIGKILL is? a) catchable b) blockable c) uncatchable d) queued → **c**
4. A handler should? a) printf b) malloc c) set a flag d) sleep → **c**
5. EINTR means? a) error b) interrupted syscall c) timeout d) kill → **b**
6. RT signals are? a) coalesced b) queued c) dropped d) uncatchable → **b**

## 20. Flashcards
- **Q: Unix sockets?** → **A:** AF_UNIX, path-addressed, full-duplex local.
- **Q: socketpair?** → **A:** Connected fd pair — bidirectional pipe for related procs.
- **Q: Stream vs datagram?** → **A:** Reliable bytes vs message-oriented (maybe lossy).
- **Q: What are signals?** → **A:** Async event notifications that interrupt the process.
- **Q: Async-signal-safe?** → **A:** Only write/read etc.; no malloc/locks/printf.
- **Q: SIGKILL/SIGSTOP?** → **A:** Uncatchable/unblockable by design.

## 21. Revision
Sockets and signals cover the two remaining IPC axes. Sockets are the general, network-capable channel: `AF_UNIX` domain sockets provide path-addressed, full-duplex, reliable local streams (and `socketpair` is the bidirectional cousin of a pipe), while `AF_INET` extends the same API across machines — with `SOCK_STREAM`/`SOCK_DGRAM` choosing reliability vs datagrams. Signals are the asynchronous event channel: the kernel (or `kill`) interrupts a process to run a handler for events like SIGINT, SIGCHLD, SIGTERM, SIGSEGV, with SIGKILL/SIGSTOP uncatchable, real-time signals queued with payloads, and a strict async-signal-safety rule for handlers. Together they give the interview toolkit its "general IPC" and "eventing" answers — and they connect to `epoll`/`io_uring` for the high-concurrency server story.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What are Unix domain sockets?" | 13 Q1 / 2 How |
| "Unix socket vs pipe?" | 13 Q2 / 4 Why not |
| "Stream vs datagram?" | 13 Q3 / 2 How |
| "What is socketpair?" | 13 Q4 / 8 Example |
| "What are signals?" | 13 Q5 / 2 How |
| "Catchable vs uncatchable?" | 13 Q6 / 7 Formal |
| "What is async-signal-safety?" | 13 Q7 / 12 Disadvantages |
| "What is EINTR?" | 13 Q9 / 12 Disadvantages |
