# Microsoft — OS Topics Interview Guide

## Windows NT Kernel Architecture

```
Application (User Mode)
    ↓ Win32 API / .NET / COM
Win32 Subsystem (csrss.exe)    Environment Subsystems
    ↓
    NT Kernel Executive
    ├── I/O Manager (file systems, drivers)
    ├── Memory Manager
    ├── Process Manager
    ├── Object Manager
    ├── Security Reference Monitor
    ├── Cache Manager
    └── Configuration Manager (registry)
    ↓
    NT Kernel (scheduler, trap handling, synchronization)
    ↓
    HAL (Hardware Abstraction Layer)
```

## Key Concepts
- **Hybrid kernel:** monolithic executive + microkernel-inspired modularity
- **HAL:** abstracts hardware differences (x86, ARM, etc.)
- **NT Executive:** kernel-mode services (I/O, VM, security, object management)

## Processes & Threads
| Property | Windows | Linux |
|----------|---------|-------|
| **Process object** | Section object (memory) + process block | `task_struct` |
| **Thread** | ETHREAD + KTHREAD (executive + kernel) | `task_struct` with `CLONE_THREAD` |
| **Fiber** | User-mode scheduled (like green threads) | N/A |
| **Job** | Group processes for mgmt | cgroups |
| **Minimal thread** | `CreateThread` → ~2000ns | `pthread_create` → ~10–50μs |

## Windows Scheduling
- **32 priority levels:** 0 (idle) → 15 (variable) → 31 (real-time)
- **Dynamic boosting:** foreground process gets priority boost (reduces after use)
- **Quantum:** default ~30ms (client) | ~180ms (server) — configurable
- **Context switching:** lazy FPU state save (MXCSR + x87 unless needed)

## Memory Management
- **VAD (Virtual Address Descriptor):** tree of mapped regions (efficient page fault handling)
- **Working set:** physical pages currently in memory per process
- **Page file:** `pagefile.sys` — backing store for modified pages
- **AWE (Address Windowing Extensions):** 32-bit apps access >4GB physical
- **Section object:** shared memory (backed by page file or mapped file)

## I/O System
- **IRP (I/O Request Packet):** kernel structure for I/O operations
- **IOCP (I/O Completion Ports):** scalable async I/O (like epoll)
  - Thread pool + completion queue: threads wait on completion port
  - **Proactor pattern** — kernel notifies when I/O **completes**
- **Driver stack:** layered (file system → volume → disk → port → miniport)
- **PnP manager:** automatic driver loading, power management

## File System: NTFS
- **MFT (Master File Table):** $MFT — all files and directories in B-tree
- **Journaling:** $LogFile — metadata journal (recoverable after crash)
- **Features:** compression, encryption (EFS), quotas, reparse points
- **Alternate data streams (ADS):** multiple data streams per file

## Hyper-V (Type 1 Hypervisor)
- **Root partition** hosts management OS
- **Child partitions** run guest OS (enlightened or emulated)
- **Enlightened I/O:** synthetic devices for better performance (VMBus)
- **Nested virtualization:** Hyper-V can run inside Hyper-V

## Interview Tips
- *"Windows NT is a hybrid kernel — monolithic executive with HAL abstraction"*
- *"IOCP is Windows' answer to epoll — proactor pattern (completion-based)"*
- *"Windows scheduling: 32 levels, dynamic boosting for foreground processes"*
- *"Know IRP, VAD, and MFT — they define Windows' I/O, memory, and file systems"*
