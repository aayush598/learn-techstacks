# Linux Kernel Architecture

## Monolithic Kernel + Modules
- **Monolithic**: entire OS runs in kernel space (no microkernel IPC overhead)
- **Loadable Kernel Modules** (LKM): `.ko` files loaded/unloaded dynamically
  - `insmod`, `rmmod`, `modprobe`, `lsmod`
- Kernel modules can be device drivers, filesystems, system calls

## User Space vs Kernel Space
| Aspect | User Space | Kernel Space |
|--------|-----------|--------------|
| **Ring** | Ring 3 | Ring 0 |
| **Memory** | Virtual address space per process | Shared kernel memory |
| **Access** | Restricted (cannot touch hardware) | Full hardware access |
| **Crash** | Process dies (segfault) | Kernel panic (entire system) |
| **Transition** | System calls, interrupts | — |

## System Call Interface
- User → kernel transition via `syscall` instruction (x86_64)
- glibc wrapper functions for most syscalls
- `sys_call_table`: array of function pointers indexed by syscall number

## Kernel Subsystems
```
┌────────── System Call Interface ──────────┐
│  VFS   │ Process Mgmt │ Memory Mgr │ Net │ Drv │
│  (ext4,│ (scheduler,  │ (page alloc│ (TCP/│ (PCI,│
│   NFS)  │  fork/exec,  │  slab, OOM │  IP) │  USB)│
│         │  signals)    │  vmalloc)  │      │      │
└──────────────────────────────────────────┘
```

## Key Kernel Components
- **VFS** (Virtual File System): abstract FS layer
- **Process Management**: scheduling, IPC, signals
- **Memory Manager**: virtual memory, page cache, swap
- **Network Stack**: TCP/IP, sockets, netfilter
- **Device Drivers**: char, block, network devices
- **Interrupt Handling**: IRQs, softirqs, tasklets, workqueues

## Virtual Filesystems
- **/proc**: process and kernel info (`/proc/cpuinfo`, `/proc/meminfo`)
- **/sys**: device and driver info (sysfs, hierarchical)
- **/dev**: device files (`/dev/sda`, `/dev/null`)
- **/sys/class/net**: network interfaces
