# Chapter: IPC Mechanisms

## What you'll learn
- **Pipes and FIFOs**: the classic unidirectional byte streams — `pipe(2)` for parent–child, `mkfifo` for unrelated processes, with kernel buffering and blocking semantics.
- **Message queues**: structured, priority-aware exchange — POSIX `mq_*` vs System V `msgget/msgsnd/msgrcv`, kernel `struct msg_queue`.
- **Shared memory**: the fastest IPC — POSIX `shm_open`/`mmap` and System V `shmget`/`shmat`, with the synchronization requirement.
- **IPC semaphores**: kernel semaphore arrays for coordinating shared-memory access — POSIX named/unnamed vs System V `semget`/`semop`.
- **Sockets and signals**: the network-grade channel (unix domain sockets, `socketpair`) and the asynchronous event channel (`signal`, `sigaction`, real-time signals).
- **An overview/comparison**: bandwidth, latency, scope, and "which to choose" for interviews.

## Prerequisites (linked)
- [Part 04 Process Synchronization](part-04-process-synchronization/README.md) — mutex/semaphore primitives (IPC semaphores build directly on these).
- [Part 02 Processes and Threads](part-02-processes-and-threads/README.md) — what a process is, fork, context.
- [Part 07 Virtual Memory](part-07-virtual-memory/README.md) — mmap, page tables (shared memory needs both).

## Sections (linked table)
| # | Section | Core question it answers |
|---|---|---|
| 01 | [Pipes and FIFOs](section-01-pipes-and-fifos.md) | How do two processes stream bytes to each other? |
| 02 | [Message Queues: POSIX vs System V](section-02-message-queues.md) | How do you pass structured, prioritized messages? |
| 03 | [Shared Memory and mmap](section-03-shared-memory-and-mmap.md) | What's the fastest way for processes to share data? |
| 04 | [IPC Semaphores and Synchronization](section-04-ipc-semaphores.md) | How do processes coordinate access to shared state? |
| 05 | [Sockets and Signals](section-05-sockets-and-signals.md) | Network-grade IPC and asynchronous event delivery |
| 06 | [IPC Overview and Comparison](section-06-ipc-overview-and-comparison.md) | Which IPC for which job, and why |

## One-paragraph narrative connecting all sections
IPC answers "how do processes share data and coordinate?" Section 01 starts simple: **pipes** are the kernel-buffered unidirectional byte stream (a pipe inode + ring buffer) that shells use to connect `cmd | cmd` — cheap, reliable, but one-directional and byte-oriented. Section 02 adds structure: **message queues** pass typed, sized messages with priorities (POSIX `mq_*` and System V `msgget`), at the cost of copy overhead and edge-triggering complexity. Section 03 removes the copies: **shared memory** maps the same physical pages into both address spaces (`mmap`/`shmget`) — the fastest channel, but it gives no synchronization, which is exactly Section 04's **IPC semaphores** (named/unamed, System V arrays) for. Section 05 covers the other two channels: **sockets** (including `AF_UNIX` domain sockets — the most general, network-compatible IPC) and **signals** (asynchronous, tiny payloads). Section 06 ties it together: bandwidth, latency, portability, and the interview decision table.

## Common interview trap in this chapter
**Trap:** Forgetting that shared memory provides *no* synchronization (it's the app's job — this is the classic follow-up question). Also: assuming a pipe is bidirectional (it's not — that's `socketpair`), confusing System V and POSIX APIs (`msgget` vs `mq_open`), and thinking signals are a data channel (they're an *event* channel with a tiny payload). And: "IPC vs threads" — the shared-address-space question (threads share memory by definition; IPC is for processes).

## Checklist before moving on
- [ ] I can `pipe(2)` two processes and explain buffer + blocking semantics.
- [ ] I can state the difference between POSIX and System V message-queue APIs.
- [ ] I can explain why shared memory is fastest and what it's missing.
- [ ] I can write a producer–consumer with `shm_open` + `mmap` + a POSIX named semaphore.
- [ ] I can explain `AF_UNIX` domain sockets and `socketpair`.
- [ ] I can compare all mechanisms in bandwidth/latency/scope terms (Section 06).
