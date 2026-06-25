# Google — OS Topics Interview Guide

## Google's OS Stack
- **ChromeOS:** Linux-based, focused on web apps, verified boot
- **Fuchsia:** microkernel (Zircon), Flutter UI, designed for all form factors
- **Android:** Linux kernel + ART runtime, app sandbox, Binder IPC

## Container & Virtualization Strategy
| Technology | Description |
|------------|-------------|
| **gVisor** | User-space kernel intercepting syscalls — sandboxes containers |
| **Borg** | Google's internal cluster manager (predecessor to Kubernetes) |
| **Kubernetes** | Open-source container orchestration (derived from Borg) |
| **cgroups v2** | Resource limits (CPU, memory, I/O) |

### gVisor Deep Dive
- **Sentry:** user-space kernel implementing Linux syscall interface
- **Gofer:** file proxy for 9P protocol (isolates I/O)
- No VM needed (lighter than Kata Containers)
- Intercepts ~250 syscalls with application-level gate

## Key Topics Google Asks
- **Memory Management:** page tables, TLB, huge pages, NUMA
- **Scheduling:** CFS, EDF, real-time scheduling, priority
- **Concurrency:** mutexes, lock-free structures, Go scheduler (GMP model)
- **Distributed Systems:** consensus, replication, consistency models
- **Performance:** profiling, perf, flame graphs, cache misses

## Android-Specific OS Topics
- **Binder IPC:** Android's inter-process communication (shared memory + ioctl)
- **ART (Android Runtime):** AOT + JIT compilation, generational GC
- **ashmem:** anonymous shared memory (Android-specific)
- **LMK (Low Memory Killer):** memory pressure → kill least important process
- **Wakelocks:** power management (holds device awake)

## Go Scheduler (GMP Model)
- **G** = goroutine, **M** = machine (OS thread), **P** = processor (context)
- Max P = GOMAXPROCS (default = #CPU cores)
- Work-stealing: idle P steals goroutines from other P's runqueue
- Network poller: goroutines blocked on I/O parked separately

## Interview Tips
- *"Google focuses on scale — how does your system behave with millions of goroutines/VMs?"*
- *"Know gVisor architecture: Sentry intercepts syscalls, Gofer handles files"*
- *"Fuchsia Zircon: capability-based, microkernel, targeting embedded to desktop"*
- *"Borg → K8s evolution: cluster management, declarative state, self-healing"*
