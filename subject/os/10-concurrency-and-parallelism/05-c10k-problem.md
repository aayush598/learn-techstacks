# C10K Problem & Modern I/O Models

## C10K: Handling 10,000 Concurrent Connections

### The Problem
- Thread-per-connection: 10,000 threads → 8+ GB stack space, context-switch thrash
- Process-per-connection: even worse (higher overhead)
- Need: handle many connections with **fewer threads**

## I/O Multiplexing Models

| Model | Call | Complexity | Max FDs | Platform |
|-------|------|------------|---------|----------|
| **select()** | Linear scan all FDs | O(n) | 1024 | POSIX |
| **poll()** | Linear scan, no 1024 limit | O(n) | unlimited | POSIX |
| **epoll** | Event-driven, callback | O(1) | unlimited | Linux |
| **kqueue** | Event-driven, filter | O(1) | unlimited | BSD/macOS |
| **io_uring** | Completion queue (async) | O(1) | unlimited | Linux 5.1+ |

### How They Work
- **select/poll:** kernel checks each FD on every call — O(n) scan
- **epoll:** `epoll_create()` → `epoll_ctl()` (add FD) → `epoll_wait()` (get ready FDs only)
  - Red-black tree + ready list; O(1) for returned events
  - Edge-triggered (ET) vs Level-triggered (LT)
- **io_uring:** shared ring buffer kernel↔userspace, zero-copy I/O
  - `io_uring_setup` → `io_uring_enter` → reap completions
  - Supports: read, write, open, accept, stat, **all** via async

## Reactor Pattern
- Single event loop demultiplexes I/O events
- Dispatches to handler callbacks
- **Used by:** Node.js, Nginx, Redis, HAProxy
- **Pros:** simple, predictable, no threading overhead
- **Cons:** CPU-bound ops block the loop → need worker threads

## Proactor Pattern
- Async I/O: kernel notifies on **completion** (not readiness)
- **Used by:** Windows IOCP, Boost.Asio, io_uring
- **Differences from reactor:** reactor = "can read" → you read; proactor = "data read" → use it

## Real-World Usage

| System | Model | Connections per Node |
|--------|-------|---------------------|
| **Nginx** | epoll + async workers | 10k–500k |
| **Node.js** | libuv (epoll/kqueue/IOCP) | 10k–100k |
| **Redis** | Single-threaded epoll | 10k–100k |
| **HAProxy** | epoll + multi-process | 100k–1M |

## C10M Problem (10 Million Connections)
- Kernel overhead becomes bottleneck (packet processing, interrupts)
- **Solutions:**
  - **DPDK** (Data Plane Dev Kit): bypass kernel, user-space NIC drivers
  - **XDP** (eXpress Data Path): BPF program runs at driver level
  - **AF_XDP:** socket family for zero-copy from NIC to userspace
  - **Kernel bypass:** Solarflare OpenOnload, Mellanox VMA

## Interview Tips
- *"Nginx uses epoll with non-blocking I/O in a reactor pattern"*
- Know **edge-triggered** vs **level-triggered** epoll
- io_uring is the modern answer (Linux 5.1+) — less syscall overhead
- C10M: *"Kernel can't keep up — need DPDK/XDP for userspace networking"*
