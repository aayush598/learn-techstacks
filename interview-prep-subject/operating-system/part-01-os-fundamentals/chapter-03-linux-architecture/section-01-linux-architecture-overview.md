# Linux Architecture Overview

> **TL;DR**: Linux is a layered monolithic kernel — hardware → kernel subsystems (process, memory, VFS, network, IPC, security) → syscall API → system libraries → utilities/apps — where every kernel service is reachable through syscalls and much kernel state is exposed as virtual files in `/proc` and `/sys`.

## 1. Why Does This Exist?
Linux needed a single coherent architecture that (1) runs on everything from routers to supercomputers, (2) stays fast by keeping the kernel monolithic, (3) stays maintainable by dividing the kernel into clean subsystems, and (4) exposes its internal state to operators so the OS can be observed and tuned. The layered architecture exists to make the monolithic kernel *comprehensible and auditable*: each subsystem has one job, each boundary is a syscall or a virtual file, and user-space tools never bypass these interfaces.

## 2. How Does It Work?
The stack, bottom to top:
1. **Hardware**: CPU, MMU, RAM, disks, NICs — with arch-specific code (`arch/x86/`).
2. **Kernel (Ring 0)**:
   - **Process/scheduler**: `kernel/sched/` — EEVDF scheduler, task management.
   - **Memory manager**: `mm/` — paging, buddy/slab, page cache, swap.
   - **VFS**: `fs/` — filesystem abstraction over ext4/xfs/procfs/sysfs/tmpfs.
   - **Network stack**: `net/` — sockets, TCP/IP, netfilter.
   - **IPC & signals**: `ipc/`, `kernel/signal.c` — pipes, shared memory, futexes.
   - **Security**: LSM, seccomp, capabilities, IMA.
   - **Entry layer**: `arch/x86/entry/` — syscalls, IDT, interrupts.
3. **System libraries**: glibc/musl in Ring 3 — wrap syscalls (`open`, `read`), add buffering and standards (POSIX).
4. **Utility programs / daemons**: bash, `ls`, systemd, sshd — user-space, use libc + syscalls.
5. **Applications**: nginx, Postgres, containers — use everything above.
Everything the kernel does is triggered by (a) syscalls from above or (b) interrupts from below; all kernel state is observable via `/proc`, `/sys`, `dmesg`, `perf`.

## 3. When Is It Used?
- **Every Linux boot and every container**: container runtimes (runc) create processes via `clone`, isolate via namespaces + cgroups (kernel features), and filesystems via mount namespaces.
- **Observation/tuning in production**: `/proc/meminfo`, `/proc/slabinfo`, `/proc/net/*`, `/sys/kernel/mm/*`; `sysctl` knobs; `perf`, `bpftrace`, `eBPF` (which compiles programs into the kernel's tracing/verifier path).
- **Driver and FS development**: kernel modules, VFS backends.
- **Embedded**: Linux as RTOS-ish (PREEMPT_RT) or as tiny kernels for routers/NAS.
- **Cloud**: every cloud VM/container host runs this exact stack; hypervisor KVM is a Linux module.

## 4. Why Wasn't Another Approach Chosen?
- **Microkernel design for Linux**: rejected — Linux chose monolithic for performance and momentum; microkernel-style isolation exists at the *module* level and via KVM, but the core is shared-address-space.
- **Everything as a separate process (BSD-style "everything is a file" service processes)**: Linux keeps the file abstraction but implements filesystems *in kernel* (VFS) — user-space FUSE exists for safe third-party filesystems, proving both directions coexist.
- **No /proc, real files only**: rejected — a virtual filesystem is the cleanest way to expose arbitrary kernel state to standard tools (`cat /proc/loadavg`), and it made debugging infinitely easier.
- **POSIX-only interface**: Linux's syscall ABI is *de facto* POSIX-ish but Linux-specific; glibc provides the portable POSIX layer above it. This layering lets Linux evolve its ABI while apps stay portable.
- **One big blob (no modules)**: rejected — modules enable drivers/FS without recompiling the kernel; they are dynamic, not isolated.

## 5. Intuition
Think of Linux as a **city government** with departments: the kernel is city hall (privileged, holds the master keys). `kernel/sched` is the traffic department, `mm/` the public-works department, `fs/` the records office, `net/` the ports authority. Citizens (apps) never enter city hall — they file forms at the window (syscalls). The city posts its decisions on public boards (`/proc`, `/sys`) so anyone can read them with normal tools (`cat`).

## 6. Real-World Analogy
A **library with restricted stacks**: the kernel is the archival stacks (only librarians enter). The catalog (VFS) lets patrons find items via standard cards (`/proc`, `/sys` are like the "current holdings" bulletin). Librarians (syscalls) fetch books; the front desk (glibc) translates your request into librarian-speak. Patrons (apps) never physically enter the stacks, but they can always check the bulletin board for what's in.

## 7. Formal Definition
The **Linux architecture** is a layered, modular **monolithic kernel** plus user space: the kernel implements processes, scheduling, memory management, the virtual filesystem, networking, IPC, and security in a single privileged address space (with arch-specific code in `arch/<cpu>/`), exposing services through a syscall ABI (`sys_call_table`) and kernel state through virtual filesystems (`procfs`, `sysfs`, `debugfs`, `devtmpfs`). Above the kernel, a user-space toolchain (libc, GNU utilities, daemons, package systems) composes the full operating system ("GNU/Linux").

## 8. Example
Trace `$ ls /proc` end-to-end through the architecture:
1. `ls` (utility, Ring 3) calls `opendir("/proc")` in glibc → `getdents64` syscall.
2. Kernel VFS (`fs/proc/`) recognizes `/proc` as procfs and calls `proc_root_lookup` → `proc_readdir`.
3. procfs enumerates PIDs by walking the kernel's PID namespace → each entry's `filldir` populates `3, 1, 1234, ...`.
4. glibc packs dirents; `ls` formats them.
So "listing `/proc`" is really "querying kernel process state through the syscall + procfs interfaces" — zero disk I/O.

## 9. Internal Working
1. **Entry**: syscalls (`arch/x86/entry/entry_64.S`), IDT for interrupts/exceptions, `vDSO` for hot time reads.
2. **Process/scheduler**: `task_struct` in `include/linux/sched.h`; EEVDF runqueue in `kernel/sched/fair.c`; `kernel/fork.c` for create; `kernel/exit.c` for termination.
3. **Memory**: `mm/memory.c` (page tables, faults), `mm/slab_common.c` + SLUB (small allocs), `mm/page_alloc.c` (buddy), `mm/vmscan.c` (reclaim).
4. **VFS**: `fs/` — superblock/inode/dentry/file abstractions; per-FS implementations; the page cache in `mm/filemap.c`.
5. **Network**: `net/` — socket layer, TCP/IP (`net/ipv4/`), `sk_buff` allocation, `netfilter`.
6. **IPC**: `ipc/` (SysV msg/sem/shm), futexes in `kernel/futex.c`, signals in `kernel/signal.c`.
7. **Security**: `security/` (LSM hooks, SELinux/AppArmor), `kernel/seccomp.c`, `kernel/capability.c`.
8. **Virtual FS**: `fs/proc/`, `fs/sysfs/`; `dmesg` reads the kernel ring buffer (`kernel/printk/printk.c`).
Each layer communicates via well-defined in-kernel interfaces, so a filesystem change doesn't require touching the scheduler.

## 10. Time Complexity
- Syscall dispatch: **O(1)**; hot paths via vDSO.
- Scheduler pick-next: O(log n) worst case (rbtree), O(1) amortized (EEVDF with cached leftmost).
- Page fault / `mmap`: O(1) amortized (VMA rbtree O(log n) lookup).
- Path resolution: O(path components).
- `/proc` readdir: O(number of entries) — cheap, no disk.
- `dmesg` read: O(ring buffer size).

## 11. Advantages
- **Performance**: monolithic function-call paths, shared address space, per-subsystem caching.
- **Portability**: one kernel, 30+ architectures via `arch/`; hardware abstracted behind subsystems.
- **Observability**: `/proc`, `/sys`, `perf`, `eBPF`, `ftrace` make the whole OS introspectable — a huge production advantage.
- **Extensibility**: modules, FUSE, eBPF programs, io_uring — features added without kernel rewrites.
- **Ubiquity & ecosystem**: the same architecture powers cloud, mobile (Android), embedded, and HPC — one skill set everywhere.

## 12. Disadvantages
- **Monolithic risk**: a driver or FS bug can corrupt the kernel (mitigated by KASAN, modules, testing).
- **Single-image complexity**: enormous codebase, complex interactions; hard to verify (mitigated by coccinelle, KCSAN, syzkaller).
- **Module security**: loading unsigned modules bypasses lockdown; signed-module enforcement is optional.
- **ABI churn**: syscall additions are permanent; internal interfaces change constantly (a feature for contributors, a hazard for out-of-tree drivers).
- **Not fully preemptible by default**: latency-sensitive apps need PREEMPT_RT/CPU isolation for hard deadlines.

## 13. Interview Questions
1. **Q: Draw the Linux architecture.** A: Hardware → kernel (syscall entry, scheduler/process, memory, VFS, network, IPC, security; `arch/` glue) → glibc → utilities/daemons → apps. Name each layer's job.
2. **Q: Is Linux a microkernel or monolithic?** A: Monolithic with loadable modules; drivers and FS run in Ring 0, share address space; modules are dynamic, not isolated.
3. **Q: What is the VFS?** A: The Virtual Filesystem — an in-kernel abstraction (superblock/inode/dentry/file) letting ext4/xfs/procfs/sysfs/tmpfs coexist behind one API (`open`/`read`/...). This is how `/proc` looks like a directory tree.
4. **Q (PRODUCTION): How do you check memory pressure on a Linux box?** A: `free -m`, `/proc/meminfo`, `/proc/slabinfo`; watch `vmstat`, `sar`, `perf mem`; `/sys/fs/cgroup/memory.usage_in_bytes` for cgroup accounting; oom-killer log in `dmesg`.
5. **Q: What's the difference between procfs and sysfs?** A: procfs (`/proc`) exposes process/task and runtime kernel info (historically "process filesystem"); sysfs (`/sys`) exposes device/driver/object topology and tunables — both are virtual, kernel-generated, no disk.
6. **Q (TRICKY): When you `cat /proc/meminfo`, is that a disk read?** A: No — it's a syscall (`open`/`read`) handled by procfs, which formats kernel counters into the buffer you requested. No disk device is touched.
7. **Q: What does glibc do above the syscall layer?** A: It provides the portable POSIX API: wrappers (arg marshaling), buffering (stdio), string/format (`printf`), dynamic loading (`dlopen`), thread/process helpers (`pthread_create` → `clone`), and math/locale.
8. **Q: What is a kernel module and how do you manage it?** A: Loadable code inserted into kernel space at runtime (`insmod`/`modprobe`, removed with `rmmod`; inspect with `lsmod`). Drivers and filesystems ship as modules. They share kernel memory — a bug crashes the kernel.
9. **Q: What is eBPF and where does it sit architecturally?** A: A kernel bytecode VM + verifier in `kernel/bpf/` — safe user-supplied programs run in kernel context (tracing, networking, observability). It's "programmable kernel observability."
10. **Q (SCENARIO): Your container can't see other processes but `ps` works inside it. Why?** A: PID namespace — the kernel gives the container its own PID numbering; `/proc` (procfs) is mounted per-namespace, so the virtual FS view is namespace-scoped. That's kernel virtualization of the "list processes" operation.
11. **Q: How does KVM fit the architecture?** A: KVM is a kernel module (`arch/x86/kvm/`) that turns the kernel into a hypervisor: guests run on the CPU in VMX non-root mode; KVM handles VMEXITs. The OS doubles as a hypervisor host.
12. **Q: What's the relationship between systemd and the kernel?** A: systemd is PID 1, a user-space service manager. It talks to the kernel through syscalls (`clone`, `mount`, `cgroup` via files in `/sys/fs/cgroup`), not by kernel code.
13. **Q (TRICKY): Where does Android sit in this architecture?** A: Android uses the Linux kernel (with Google's patches: Binder, wakelocks, low-memory killer) plus a userspace of Zygote/ART, not the GNU userland. Same kernel, different userspace — proof the architecture separates them.
14. **Q: How does Linux expose kernel state besides `/proc`?** A: `/sys` (devices), `debugfs` (debug), `tracefs` (ftrace), the `dmesg` ring buffer, netlink sockets (`ss`/`ip` use them), and eBPF maps.
15. **Q: What does `dmesg` read, and why is it useful in production?** A: The kernel's printk ring buffer — boot messages, driver errors, oopses, OOM kills, NIC link state. It's often the first evidence when debugging hardware/kernel issues.

## 14. Follow-Up Questions
1. **Q: What is the difference between a system call and a kernel API (e.g., `file_operations`)?** A: Syscalls are the user↔kernel boundary; in-kernel APIs (like VFS `file_operations`) are internal interfaces between subsystems — not callable from userspace.
2. **Q: What is a "character device" vs "block device"?** A: Char devices (`/dev/tty`, `/dev/null`) transfer byte streams; block devices (`/dev/sda`) transfer blocks with buffering/caching — the device filesystem (`devtmpfs`) exposes them to userspace.
3. **Q: What is copy-on-write and where is it implemented?** A: COW in `mm/` — `fork` shares pages read-only; the first write faults and duplicates. It's why `fork` is cheap and why `fork`+`exec` is efficient.
4. **Q: What is the page cache?** A: Kernel's buffer for file pages in `mm/filemap.c` — reads/writes hit RAM before disk; `fsync`/`O_DIRECT` bypass or flush it. Critical for DB/perf reasoning.
5. **Q: How does the kernel isolate containers?** A: Namespaces (mount, pid, net, ipc, uts, user, cgroup) + cgroups (resource limits) + seccomp/LSM — all kernel mechanisms implemented in `kernel/nsproxy.c`, `kernel/cgroup/`, `kernel/seccomp.c`.

## 15. Coding Example
```bash
#!/bin/bash
# Exploring the Linux architecture from user space
echo "== kernel subsystem locations (source tree on dev box) =="
ls -d /usr/src/linux-headers-$(uname -r)/kernel/sched \
      /usr/src/linux-headers-$(uname -r)/mm \
      /usr/src/linux-headers-$(uname -r)/fs \
      /usr/src/linux-headers-$(uname -r)/net 2>/dev/null

echo "== /proc: kernel state as files =="
head -5 /proc/meminfo /proc/loadavg /proc/slabinfo 2>/dev/null
echo "loadavg: $(cat /proc/loadavg)"

echo "== /sys: device/driver topology =="
ls /sys/block /sys/class/net | head
cat /sys/class/net/$(ip route show default | awk '{print $5}' | head -1)/speed 2>/dev/null

echo "== who is what (kernel vs userspace) =="
ps -eo pid,comm | grep -E "ksoftirqd|kworker|systemd|sshd|kthreadd"
```
```c
/* Observing the kernel via /proc from a program */
#include <stdio.h>
#include <stdlib.h>
int main(void) {
    FILE *f = fopen("/proc/meminfo", "r");
    char line[128];
    while (fgets(line, sizeof line, f) && line[0] != '\n') printf("%s", line);
    fclose(f);
    return 0;
}
```

## 16. Industry Usage
- **Cloud (AWS/GCP/Azure)**: Linux host kernels; container hosts tuned with cgroups, io_uring, tuned networking (RPS/XPS); observability via `perf`/eBPF (used heavily by Netflix, Meta, Google).
- **Android**: Linux kernel on ~3B devices — Binder IPC, LMK, wakelocks are kernel features.
- **Databases**: Postgres (page cache, fsync), RocksDB/ScyllaDB (`io_uring`), Redis (kernel event loop via epoll).
- **Networking**: nginx, Cilium (eBPF dataplane in the kernel), DPDK/XDP for extreme rates.
- **HPC**: Linux on top-500 supercomputers; tuned with cpu affinity, huge pages, NUMA.
- **Embedded/Edge**: Yocto/Buildroot Linux on routers, NAS, IoT gateways; PREEMPT_RT for real-time-ish workloads.
- **Interview angle**: "architecture + observability" is a Meta/Netflix/Amazon specialty — knowing `/proc`, eBPF, cgroups, and VFS separates senior candidates.

## 17. References
- Linux source: `kernel/sched/core.c`, `mm/memory.c`, `fs/read_write.c`, `net/ipv4/tcp.c`, `kernel/fork.c`, `arch/x86/entry/entry_64.S`.
- docs.kernel.org — "Linux Kernel Documentation" (admin, mm, filesystems, tracing).
- LWN.net articles on scheduler/EEVDF, io_uring, eBPF.
- Silberschatz, *OS Concepts*, Ch. 21 (The Linux System).
- Tanenbaum, *Modern OS*, Ch. 10 (Linux case study).
- Love, *Linux Kernel Development*.
- `proc(5)`, `sysfs(5)`, `cgroup(7)`, `namespaces(7)` man pages.

## 18. Cheat Sheet
- Layers: HW → kernel (sched/mm/VFS/net/IPC/security) → syscalls → glibc → utils → apps.
- Linux = monolithic + modules; modules are dynamic, not isolated.
- VFS: superblock/inode/dentry/file abstraction; procfs/sysfs are virtual FS.
- `/proc` = process + runtime state; `/sys` = device/driver topology.
- `cat /proc/meminfo` = kernel counters via syscalls, no disk.
- glibc wraps syscalls with POSIX API + buffering.
- systemd is userspace PID 1, talks to kernel via syscalls/cgroups.
- eBPF = verified user programs in kernel for observability.
- Android = Linux kernel + non-GNU userspace.
- `dmesg`/`perf`/`ss`/`sysctl` = core observation tools.

## 19. Quiz
1. Linux's kernel type: a) micro b) monolithic+modules c) hybrid d) exokernel → **b**
2. `/proc` is backed by: a) disk partition b) kernel virtual FS (procfs) c) tmpfs d) sysfs only → **b**
3. Which is NOT a kernel subsystem? a) VFS b) scheduler c) glibc d) page cache → **c**
4. Reading `/proc/meminfo` involves: a) disk I/O b) syscalls + procfs formatting c) DMA d) no CPU → **b**
5. glibc's role: a) kernel driver b) POSIX API + syscall wrappers c) bootloader d) scheduler → **b**
6. KVM is: a) a userspace daemon b) a Linux kernel module c) firmware d) a container runtime → **b**
7. `/sys` exposes: a) processes b) device/driver topology c) logs d) cron jobs → **b**
8. Android's kernel is: a) XNU b) Linux c) QNX d) FreeRTOS → **b**
9. systemd is: a) kernel code b) user-space PID 1 c) a driver d) a filesystem → **b**
10. eBPF programs run: a) in user space b) in kernel context after verification c) in firmware d) on GPU → **b**

## 20. Flashcards
- **Q: Linux kernel type?** → **A:** Monolithic with loadable modules.
- **Q: VFS purpose?** → **A:** Common FS abstraction (ext4/xfs/procfs/sysfs) behind one API.
- **Q: procfs vs sysfs?** → **A:** Process/runtime state vs device/driver topology.
- **Q: What is `/proc/meminfo` reading?** → **A:** Kernel counters formatted via procfs, no disk.
- **Q: glibc?** → **A:** Userspace POSIX API wrapping syscalls.
- **Q: systemd?** → **A:** User-space PID 1 (service manager), not kernel.
- **Q: KVM?** → **A:** Kernel module making Linux a hypervisor.
- **Q: eBPF?** → **A:** Verified bytecode programs running in kernel for observability/networking.
- **Q: Android kernel?** → **A:** Linux (heavily patched) with non-GNU userspace.
- **Q: Core observability tools?** → **A:** dmesg, /proc, /sys, perf, ss, sysctl.

## 21. Revision
Linux is a modular monolithic kernel: one privileged address space with subsystems for scheduling, memory, VFS, networking, IPC, and security, reached through the syscall ABI and observable through virtual filesystems (`/proc`, `/sys`). Above it, glibc provides the POSIX API and utilities/daemons form user space. Modules are dynamic, not isolated; eBPF adds safe in-kernel programs for observability; KVM makes the kernel a hypervisor. The boundary question — kernel vs userspace — is the quickest way to demonstrate depth: systemd, bash, and Android's non-GNU userspace are all user space on Linux.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Draw/diagram Linux architecture" | 2 How It Works / 8 Example |
| "Monolithic or microkernel?" | 13 Q2 / 4 Why Not |
| "What is the VFS?" | 13 Q3 / 9 Internal Working |
| "Check memory pressure" | 13 Q4 / 16 Industry Usage |
| "procfs vs sysfs / is /proc disk I/O?" | 13 Q5-6 / 7 Formal Definition |
| "What is glibc's role?" | 13 Q7 / 2 How It Works |
| "Kernel modules management" | 13 Q8 / 12 Disadvantages |
| "What is eBPF?" | 13 Q9 / 16 Industry Usage |
| "Why can't a container see other PIDs?" | 13 Q10 / 14 Follow-Up Q5 |
| "How does KVM work?" | 13 Q11 / 16 Industry Usage |
