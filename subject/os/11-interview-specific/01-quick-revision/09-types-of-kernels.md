# Types of Kernels

## Comparison Table

| Property | Monolithic | Microkernel | Hybrid | Exokernel |
|----------|------------|-------------|--------|-----------|
| **Architecture** | All services in kernel space | Minimal kernel (IPC, scheduling) | Monolithic-like with modularity | App manages hardware directly |
| **Performance** | Fast (direct function calls) | Slower (IPC between services) | Good | High (app-level control) |
| **Modularity** | Low | High | Medium | Very high |
| **Stability** | Lower (bug in driver crashes kernel) | High (services crash independently) | Medium | High |
| **Size** | Large (millions of LOC) | Tiny (<10k LOC) | Medium | Minimal |
| **Examples** | Linux, FreeBSD, Windows 9x | Minix, QNX, L4, seL4 | Windows NT, macOS XNU | MIT ExOS, Nemesis |

## Monolithic Kernel
- All OS services **in kernel space**: scheduler, file system, networking, drivers, VM
- **Pros:** fast IPC (function calls), tight integration
- **Cons:** huge codebase, any driver bug crashes system
- **Linux:** technically monolithic but with **loadable kernel modules** (LKM) for drivers

## Microkernel
- **Minimal kernel:** only IPC, scheduler, basic VM
- Everything else: file system, drivers, network stack run as **user-space processes**
- **Pros:** modular, fault-isolated, secure (small TCB)
- **Cons:** IPC overhead (message passing between services)
- **seL4:** mathematically verified microkernel (no bugs!)
- **QNX:** hard RTOS used in cars (BlackBerry QNX)

## Hybrid Kernel (NT kernel)
- **Monolithic-like (services in kernel)** + **microkernel-like (modular)**  
- Windows NT: kernel (scheduler, VM) + executive (I/O manager, security, cache) + HAL
- macOS XNU: **Mach microkernel** + **BSD** (single address space — hybrid)
- Practically monolithic with better modularity

## Exokernel
- **Minimal abstraction** — kernel only multiplexes hardware
- **Library OS** (libOS) in user space manages resources
- **App-level decisions** on scheduling, memory management
- **Unikernels:** app compiled with libOS → single address space, no context switches
- Research project; influenced **container** and **unikernel** design

## Kernel Space vs User Space
| | Kernel Space | User Space |
|---|-------------|------------|
| **Privilege** | Ring 0 (full access) | Ring 3 (limited) |
| **Access** | All hardware, all memory | Restricted (syscall to enter kernel) |
| **Crash impact** | System crash | Only that process dies |
| **Examples** | Kernel, drivers, VM | Applications, services |

## Interview Tip
- *"Linux is monolithic but modular — modules can be loaded/unloaded at runtime"*
- *"Microkernels are more secure due to smaller TCB — but IPC cost is the trade-off"*
- *"Windows NT and macOS XNU are hybrids — combine monolithic performance with modularity"*
