# Message Passing IPC

## Overview
- Processes communicate by **exchanging messages** — no shared address space
- OS provides `send(message)` and `receive(message)` system calls
- **Kernel involved** in every message (copies between address spaces)
- Naturally avoids race conditions (no shared state)

## Direct vs Indirect Communication

| | Direct | Indirect |
|---|--------|----------|
| **Naming** | Explicitly name sender/receiver | Use **mailbox** (port) as intermediary |
| **Send** | `send(P, message)` — to process P | `send(A, message)` — to mailbox A |
| **Receive** | `receive(Q, &message)` — from Q | `receive(A, &message)` — from A |
| **Link** | Automatic (pair formed by naming) | Explicit — processes share a mailbox |
| **Property** | Exactly 1 link per pair | N processes can share a mailbox |
| **Example** | MPI point-to-point | POSIX mqueues, System V msg queues |

```
Direct:  P ──────────────► Q   (P names Q, Q names P)

Indirect:   ┌──────────┐
           P┼─► Mailbox ├─►Q
           R┼─►     A   ├─►S  (many-to-many)
            └──────────┘
```

## Synchronous vs Asynchronous (Blocking vs Non-blocking)

| | Blocking (Synchronous) | Non-blocking (Asynchronous) |
|---|------------------------|----------------------------|
| **Send** | Process blocks until message received | Sends and continues immediately |
| **Receive** | Blocks until message available | Returns immediately (with or without msg) |
| **Buffering** | Zero-capacity (rendezvous) — sender must wait for receiver | Bounded/unbounded queues |
| **Pros** | Automatic synchronization, simple | Higher concurrency |
| **Cons** | Less concurrency (must wait) | Must poll or use notification |
| **Also called** | Rendezvous | Mailbox |

### Combinations
- **Blocking send + Blocking receive** = **Rendezvous** (tight synchronization)
- **Non-blocking send + Blocking receive** = Most common (server pattern)
- **Non-blocking send + Non-blocking receive** = Fully async (event-driven)

## Mailbox Concepts

| Property | Description |
|----------|-------------|
| **Capacity** | Zero (rendezvous), bounded (fixed queue), unbounded (infinite) |
| **Ownership** | Process-owned (only owner can receive) or OS-owned (anyone authorized) |
| **Port** | Mailbox identifier (integer) — used in indirect communication |
| **Operations** | Create, send, receive, delete |

```c
// POSIX message queue (indirect, async)
#include <mqueue.h>

mqd_t mq = mq_open("/myqueue", O_CREAT | O_RDWR, 0644, NULL);
mq_send(mq, "hello", 6, 0);                   // non-blocking send
ssize_t n = mq_receive(mq, buf, buflen, NULL); // blocking receive
mq_close(mq);
mq_unlink("/myqueue");
```

## Port Addressing

- **Port**: Kernel-identified endpoint for IPC (used in socket/mailbox IPC)
- Each port has a **unique number** per machine
- Ports can be:
  - **Well-known** (fixed, e.g., port 80 for HTTP)
  - **Dynamic** (assigned at runtime)
- Used in **socket IPC** (TCP/UDP), **Mach ports**, **Windows LPC**

### Key Interview Distinctions
- **Message passing** is preferred for **distributed systems** (across machines via network)
- **Shared memory** is preferred for **local, high-throughput** communication
- **Blocking vs Non-blocking** is about sync mode; **Direct vs Indirect** is about naming scheme
