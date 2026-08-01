# Linux Internals: Concepts and Interview Synthesis

> **TL;DR**: Containers = **namespaces** (isolated views: PID, net, mount, UTS, IPC, user, cgroup) + **cgroups** (resource limits: CPU, memory, I/O). `/proc` and `sysfs` expose the kernel as a filesystem. A **context switch** saves/restores registers + switches page tables (with PCID/TLB handling). The capstone answer: **what happens when you type a command** — shell fork/exec → loader → `_start` → `main` → syscalls.

## 1. Why Does This Exist?
Linux internals questions test whether you can connect the abstractions (processes, memory, files, syscalls) to the running system. Three pillars: **namespaces + cgroups** (how containers exist at all — isolation and limits without a hypervisor), **/proc & sysfs** (the kernel's observable, queryable interface — the "everything is a file" philosophy in action), and **the end-to-end traces** (boot → shell → command; fork/exec; context switch) that synthesize every prior part. This section is the interview synthesis: the concepts are the "why", and the trace answers are the "show me you actually understand it".

## 2. How Does It Work?
**Namespaces** (`ns/` subsystem): each namespace gives a process a *different view* of a global resource. Created per-process with `clone(CLONE_NEW*)` or `unshare(2)`; entered with `setns(2)`.
- `PID` — process IDs restart at 1; `ps` inside sees only the namespace's processes.
- `NET` — separate network stack (interfaces, routes, iptables, sockets).
- `MNT` — separate mount table (bind mounts, overlayfs roots).
- `UTS` — own hostname/domainname. `IPC` — own System V IPC / MQ. `USER` — own UID/GID mapping (root in container ≠ root on host). `CGROUP` — own cgroup root view.
- `mnt`/`pid` are hierarchical; all are per-process but shared by a process tree.

**cgroups** (control groups, `cgroupfs`): hierarchical resource controllers.
- **v1**: per-controller hierarchies (cpu, memory, blkio, devices, freezer...).
- **v2**: unified hierarchy (all controllers under one tree), thread-aware, `cgroup.controllers`.
- CPU: `cpu.weight`, `cpu.max` (CFS shares + throttling). Memory: `memory.max`, `memory.high` (limit/soft limit), `memory.current`, OOM killer per-cgroup. I/O: `io.weight`/`io.max`. `cgroup.kill`, `cgroup.freeze`.
- Systemd manages cgroups for services (slice/unit model).

**/proc & sysfs**:
- `/proc`: process info (`/proc/<pid>/status, stat, maps, fd, smaps, wchan`), plus kernel info (`/proc/meminfo`, `/proc/loadavg`, `/proc/interrupts`, `/proc/sys/*` — sysctls, `/proc/kallsyms`). Tied to `task_struct`/`mm`/`fd` via `proc_file_operations`.
- `/sys`: device model, kernel objects (`/sys/class`, `/sys/block`, `/sys/module`, `/sys/devices`), tunables (`/sys/kernel/*`, `/sys/fs/cgroup`). Backed by kobjects/`kobj_attr`.
- Both are **virtual filesystems** implemented through VFS (Part 08 Sec 04) — data generated on read.

**Context switch** (`kernel/sched/core.c`): `__schedule` → `context_switch` → `switch_mm` (CR3/ASID, TLB handling) + `switch_to` (save/restore callee-saved regs, stack, `prev`/`next` via `__switch_to_asm`); per-task `cpu_context`.

**"Type a command" trace**:
1. Shell reads input, parses `ls -l`.
2. `fork()` (COW — Section 01) → child.
3. Child `execve("/bin/ls", ...)` → `load_elf_binary`: `flush_old_exec`, map PT_LOAD, set up stack/argv/envp, `auxv`, entry → dynamic loader `ld-linux.so` → `_start` → `main`.
4. `main` runs, makes syscalls (`openat`, `readdir`, `statx`, `write`) via glibc wrappers (Section 04) → VFS → page cache → block layer.
5. `_exit(status)` → zombie → parent `wait4` → reaped; shell prints prompt again.

## 3. When Is It Used?
- **Containers**: Docker/podman/containerd — runc creates namespaces (`CLONE_NEWPID|NEWNET|NEWMNT|NEWUTS|NEWIPC|NEWUSER`) + cgroups for limits; Kubernetes pod sandboxes; `nsenter` to enter them.
- **Resource governance**: systemd units (CPU/memory limits), `ulimit` vs cgroups, `systemd-run --scope`; OOM protection (`memory.oom.group`).
- **Observability**: `ps`, `top`, `htop`, `lsof`, `strace`, `perf`, `/proc`/`/sys` exploration, `bpftrace`.
- **Troubleshooting**: uninterruptible D-state tasks (`ps aux` D), `wchan` (kernel function a task waits on), `/proc/sys/vm/*` tuning.
- **Security**: seccomp + namespaces + cgroups + capabilities = the container security stack.

## 4. Why Wasn't Another Approach Chosen?
- **Full virtualization for isolation (rejected for containers)**: VMs give strong isolation but heavy (kernel per VM); containers share the host kernel — namespaces+cgroups give isolation+limits at near-native cost, trading isolation strength for efficiency.
- **Only cgroups (rejected)**: limits without isolation = processes can still see each other; namespaces add the *views*.
- **Only namespaces (rejected)**: isolation without limits = a process can consume everything; cgroups enforce budgets.
- **`ulimit`/`nice` alone (rejected)**: per-process soft limits only; cgroups are hierarchical + group-level + controllable by systemd.
- **chroot (historical)**: changed the root path but not the view of PIDs/net/IPC — namespaces supersede for real isolation.
- **Plain monolithic debugging (rejected)**: `/proc`/`sysfs`/tracepoints give structured kernel access instead of raw memory poking.

## 5. Intuition
**Containers = a hotel with separate rooms (namespaces) and a per-room budget (cgroups)**: each guest sees only their room's furniture (own PID 1, own network, own filesystem), but the hotel manager (host kernel) also caps how much electricity (CPU), water (memory), and laundry (I/O) each room can use — and can freeze or kill a room's occupants.

**/proc & /sys = the building's dashboard and control panels**: /proc is the live status board (what's running, memory, open files), /sys is the maintenance panel (change device settings, tweak kernel knobs).

**Context switch = a DJ changing tracks**: the DJ saves where they are on the current record (registers, stack), flips the deck to the next record (page table/CR3), and resumes — with a note to avoid replaying a track they just skipped (TLB flush/PCID).

## 6. Real-World Analogy
**A co-working space**:
- **Namespaces**: each company gets its own floor — their own office numbers (PID 1..N), their own phone lines (network), their own door locks and office layout (mounts) — even if they share the building (host kernel).
- **cgroups**: the building management sets budgets: max electricity (CPU), max floor space/water (memory), and can evict (OOM) or freeze (cgroup.freeze) a company that exceeds them.
- **/proc**: the lobby's live monitors — who's in which room, what they're doing, how much they're using.
- **/sys**: the utility rooms — dials to change how devices and the building systems behave.

## 7. Formal Definition
**Namespace** = a per-process abstraction of a kernel global (PID, net, mnt, uts, ipc, user, cgroup); created/entered via `clone(CLONE_NEW*)`, `unshare`, `setns`; referenced by `nsfs` files (`/proc/<pid>/ns/*`). **cgroup** = a hierarchical set of processes with attached resource controllers; v2 unified tree: `cpu` (weight/max → CFS), `memory` (max/high/current, swap), `io` (weight/max), `pids`, `cpuset`; interfaces via `cgroupfs` (`/sys/fs/cgroup`). **/proc** = procfs, per-process + system pseudo-files implemented as VFS files whose `f_op` reads kernel state (`proc_pid_status`). **/sys** = sysfs, kobject model exposed as files (`sysfs_read_file`). **Context switch** = `__schedule` picks `next`, `context_switch` calls `switch_mm` (CR3 + TLB handling via PCID/ASID; `mmgrab`/`mmdrop` for lazy TLB) and `switch_to` (register save/restore, thread stack). **Container** ≈ namespaces + cgroups + chroot/overlay root + seccomp/caps.

## 8. Example
**Run a container by hand** (runc's essentials, conceptually):
```bash
# create namespaces + run a process with them
unshare --pid --net --uts --mount --fork --mount-proc /bin/bash
#    ^-- new PID namespace (shares --fork, /proc remounted)
# now: PID 1 = bash; `ps` only shows this namespace
```
**cgroup for CPU limit** (v2):
```bash
mkdir /sys/fs/cgroup/demo
echo 50000 > /sys/fs/cgroup/demo/cpu.max     # 50% of one CPU (50ms/100ms)
echo $BASHPID > /sys/fs/cgroup/demo/cgroup.procs
```
**Observe a command**:
```bash
strace -f -e trace=clone,execve,openat ls -l /tmp
# clone()  = fork (Section 01)
# execve() = run /bin/ls (Section 01)
# openat() = read the directory (Section 03)
```

## 9. Internal Working
1. **namespace create**: `unshare(CLONE_NEWPID)` → `copy_namespaces` → `create_new_namespaces` → for PID: new `pid_namespace`, first child becomes PID 1; for NET: new `net` struct with fresh loopback; for MNT: new mount namespace.
2. **cgroup attach**: writing `cgroup.procs` → `cgroup_attach_task` → for `cpu`, `tg_set_cfs_bandwidth`/`tg_set_share` adjust the group's `sched_entity` weight (CFS proportional shares); `memory.max` → `mem_cgroup_try_charge` enforcement; `memory.high` throttles; OOM: per-cgroup OOM killer (`oom_score_adj`).
3. **/proc read**: `read("/proc/self/status")` → procfs `f_op` (`proc_pid_status`) → walks `task_struct`/`mm`/`files` → builds the text. `maps` → `proc_pid_maps` walks `mm->mmap` VMAs.
4. **context switch**: timer tick → `scheduler_tick` → `resched_curr` → next schedule point → `__schedule` → `context_switch` → `switch_mm` writes CR3 (new pgd) + flushes/ASIDs TLB → `switch_to` saves `%rsp`/regs on `prev`'s kernel stack, restores `next`'s → return into `next`.
5. **trace**: `strace` ptrace-intercepts at syscall entry/exit (Section 04); `perf` uses tracepoints (sys_enter/sys_exit, sched_switch).

## 10. Time Complexity
- Namespace create: O(1) struct alloc + per-namespace setup; PID ns adds a pid mapping.
- cgroup attach/weight change: O(1) CFS weight update (rbtree rebalance O(log n)).
- /proc read: O(task fields) or O(VMAs) for maps — proportional to data produced.
- Context switch: O(1) register save/restore + O(1) CR3 write (+ TLB flush cost mitigated by PCID; on mm switch: full flush historically).
- Container start: O(fork) + O(exec) + O(namespace setup) — ms-scale.

## 11. Advantages
- **Containers**: near-native performance, fast start (no guest OS), strong-enough isolation with layered security (namespaces + cgroups + caps + seccomp).
- **cgroups**: hierarchical, kernel-enforced, systemd-managed; group-level CPU/memory/I/O budgets and OOM control.
- **/proc & /sys**: universal, scriptable observability and tuning without reboots.
- **Trace answers**: the "type a command" trace shows a genuine, end-to-end understanding — the interview favorite.

## 12. Disadvantages
- **Shared kernel** (containers): a kernel bug/exploit affects all containers; VMs are safer.
- **Namespace leakage**: bind mounts, device access, and `CAP_SYS_ADMIN` can break out; requires hardening.
- **cgroup complexity**: v1→v2 migration, controller conflicts, debugging limits vs actual usage.
- **/proc & /sys as attack surface**: lots of kernel code reachable by unprivileged reads/writes — needs hardening (hidepid, `kptr_restrict`).
- **Context-switch cost**: on heavily shared machines, TLB/ASID churn and cache misses add overhead (mitigated by PCID, lazy mm switch, vhost).

## 13. Interview Questions
1. **Q: What is the difference between a namespace and a cgroup?** A: Namespaces provide *isolation* (separate views of PID/net/mount/UTS/IPC/user); cgroups provide *resource limits* (CPU/memory/I/O budgets). Containers use both.
2. **Q: Name the Linux namespaces.** A: PID (PIDs restart at 1), NET (own network stack), MNT (own mount table), UTS (hostname), IPC (SysV IPC), USER (UID/GID mapping), CGROUP (cgroup view). Created with `clone(CLONE_NEW*)`/`unshare`/`setns`.
3. **Q: What do cgroups do and how are they used?** A: Hierarchical controllers that limit/account CPU (weight/max), memory (max/high/current, OOM), I/O (weight/max), pids; systemd/Docker/K8s put workloads in cgroups to enforce budgets and fairness.
4. **Q: How do containers work without a hypervisor?** A: They share the host kernel: namespaces isolate views, cgroups limit resources, plus a container rootfs (overlayfs), capabilities, and seccomp filters — near-native but weaker isolation than VMs.
5. **Q: What is `/proc` and how is it implemented?** A: procfs — a virtual filesystem whose files are generated on read from kernel state (`task_struct`, `mm`, fds): `/proc/<pid>/status|maps|fd`, `/proc/meminfo`. It's a VFS filesystem with proc `f_op`s.
6. **Q: What is `/sys` (sysfs)?** A: The kernel object model (kobjects) exposed as files — devices, drivers, classes, module params, tunables (`/sys/block`, `/sys/class`, `/sys/module`) — used for device management (udev) and kernel tweaks.
7. **Q: What happens during a context switch?** A: `__schedule` picks the next task; `context_switch` calls `switch_mm` (switch page tables/CR3, TLB handling via PCID/ASID) and `switch_to` (save/restore registers and kernel stack pointer) — switching CPU state between two tasks.
8. **Q: What is the difference between a context switch and a mode switch?** A: Mode switch = user↔kernel within the same task (syscall/interrupt — no task change); context switch = between two tasks (save/restore full CPU state, possibly new address space). Context switches are far more expensive.
9. **Q: Walk through "what happens when you type `ls`"?** A: Shell parses → `fork` (COW child) → child `execve("/bin/ls")` → ELF loader maps segments, sets stack/argv, jumps to `_start`/dynamic loader → `main` → syscalls (`openat`/`readdir`/`statx`/`write`) through glibc/VFS/page cache → `_exit` → zombie → parent `wait4` reaps → prompt returns.
10. **Q: What is a "D" (uninterruptible sleep) process?** A: A task in `TASK_UNINTERRUPTIBLE` — sleeping on I/O it can't be signaled out of (e.g., waiting on a stuck disk/NFS); it doesn't respond to SIGKILL until the I/O completes — a common ops troubleshooting point.
11. **Q: What is `wchan`?** A: The kernel function a task is currently blocked in (`/proc/<pid>/wchan`) — the answer to "what is this process waiting for".
12. **Q: How does `pid 1` (init/systemd) matter?** A: PID 1 is the first process; it reaps orphaned children (default subreaper), is never killed, and systemd uses it to manage services (cgroups, sockets) — its role in the namespace matters for container entrypoints (the container's PID 1 must handle signals/reaping).

## 14. Follow-Up Questions
1. **Q: What is the "container's PID 1" problem?** A: The container's PID 1 must reap zombies and forward signals — a broken PID 1 (e.g., a plain binary) leaves zombies and drops SIGTERM; `tini`/`--init` fixes it.
2. **Q: v1 vs v2 cgroups?** A: v1 = separate controller hierarchies (complex, inconsistently managed); v2 = unified tree, thread-aware, `cgroup.controllers` — the modern standard (systemd/K8s).
3. **Q: What is `cpuset`?** A: A cgroup controller pinning a group to specific CPUs/NUMA nodes — used for isolation/latency.
4. **Q: What is `hidepid` and `kptr_restrict`?** A: Security hardening of /proc (hide other users' process info) and kernel pointers (hide kallsyms addresses from unprivileged users).

## 15. Coding Example
```c
#include <stdio.h>
#include <unistd.h>
#include <sched.h>
#include <sys/wait.h>
#include <sys/mount.h>
#include <stdlib.h>

// A minimal namespace demo: run a child in new PID + mount namespaces.
int main(void) {
    if (unshare(CLONE_NEWPID | CLONE_NEWNS) == -1) { perror("unshare"); return 1; }
    pid_t pid = fork();
    if (pid == 0) {
        // child: PID 1 inside the new PID namespace
        printf("child sees getpid() = %d (PID 1 inside ns)\n", getpid());
        // remount /proc so `ps` shows the namespace's processes
        mount("proc", "/proc", "proc", 0, NULL);
        execlp("ps", "ps", "aux", NULL);
        _exit(0);
    }
    waitpid(pid, NULL, 0);
    return 0;
}
```
Note: `unshare` requires privileges (or user namespaces). This shows namespaces' essence: the child's PID restarts at 1.

## 16. Industry Usage
- **Kernel**: `kernel/nsproxy.c`, `kernel/pid_namespace.c`, `net/core/net_namespace.c`, `fs/namespace.c`, `kernel/cgroup/cgroup.c`, `mm/memcontrol.c`, `kernel/sched/core.c` (context switch), `fs/proc/`, `drivers/base/` (sysfs).
- **Containers**: runc/containerd/cri-o, Docker, Kubernetes (pod cgroups), systemd (slice model), `nsenter`, `unshare`, `cgroups v2`.
- **Cloud**: ECS/Fargate use container isolation; GKE/EKS cgroups + seccomp defaults.
- **Observability**: `/proc`/`/sys` → Prometheus exporters, `top/htop`, `perf`, `bpftrace`, `ss`, `lsof`.

## 17. References
- Love, *Linux Kernel Development*, Ch. 3 (processes/context switch), Ch. 4 (scheduling), Ch. "Virtual Filesystem".
- Silberschatz, *Operating System Concepts*, Ch. 3 (processes), Ch. 5 (scheduling).
- Tanenbaum, *Modern Operating Systems*, Ch. 2 (processes/threads, syscalls), Ch. 10 (Linux).
- Kernel docs: `Documentation/admin-guide/cgroup-v2.rst`, `Documentation/filesystems/proc.rst`, `Documentation/filesystems/sysfs.rst`.
- `man 7 namespaces`, `man 7 cgroups`, `man 1 unshare`, `man 1 nsenter`, `man 5 proc`.

## 18. Cheat Sheet
- Namespaces: PID, NET, MNT, UTS, IPC, USER, CGROUP — isolation views.
- cgroups: CPU (weight/max), memory (max/high/OOM), IO, pids — limits.
- Container = namespaces + cgroups + rootfs (overlay) + caps + seccomp.
- /proc = process/system pseudo-files (status/maps/fd/meminfo).
- /sys = kobject model (devices/classes/module params).
- Context switch = switch_mm (CR3/TLB) + switch_to (regs/stack).
- Mode switch (syscall) ≠ context switch (task change).
- "Type a command": fork → exec(ELF loader) → _start → main → syscalls → exit → wait.
- D-state = uninterruptible sleep (I/O); wchan = where blocked.

## 19. Quiz
1. Isolation views are provided by? a) cgroups b) namespaces c) sysfs d) seccomp → **b**
2. CPU budget? a) ns b) cgroup cpu.max c) /proc d) pid → **b**
3. Container isolation strength vs VM? a) equal b) weaker (shared kernel) c) stronger d) n/a → **b**
4. /proc shows? a) devices b) process/system info c) namespaces d) cgroups → **b**
5. Context switch switches? a) only regs b) page tables + regs c) only CR3 d) nothing → **b**
6. exec replaces? a) process b) program image c) namespace d) cgroup → **b**

## 20. Flashcards
- **Q: Namespace vs cgroup?** → **A:** Isolation (views) vs limits (resources).
- **Q: List namespaces?** → **A:** PID, NET, MNT, UTS, IPC, USER, CGROUP.
- **Q: What is a container?** → **A:** Namespaces + cgroups + rootfs + caps + seccomp.
- **Q: /proc?** → **A:** Pseudo-FS over kernel state (task/mm/fd).
- **Q: Context switch?** → **A:** switch_mm (CR3/TLB) + switch_to (regs/stack).
- **Q: Type a command?** → **A:** fork → exec(loader) → _start → main → syscalls → exit.

## 21. Revision
Linux internals coalesce around three pillars. **Namespaces** give containers their isolation (separate PID/net/mount/UTS/IPC/user views via `clone(CLONE_NEW*)`); **cgroups** give them budgets (v2 unified tree: `cpu.max`, `memory.max`, `io` limits enforced by the kernel, managed by systemd/K8s). **/proc and /sys** expose the kernel as files — process state, device model, tunables — for observability and control. A **context switch** is the expensive save/restore of registers + page tables (with PCID/TLB mitigation); a **mode switch** (syscall) stays within the task. The capstone "what happens when you type a command" answer chains every concept: fork → COW, exec → ELF loader → `_start` → `main`, syscalls through glibc/VFS/page cache, exit → zombie → `wait`. Master this trace and you've synthesized Parts 02–09.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Namespace vs cgroup?" | 13 Q1 / 2 How |
| "Name the namespaces." | 13 Q2 / 2 How |
| "What do cgroups do?" | 13 Q3 / 8 Example |
| "How do containers work?" | 13 Q4 / 5 Intuition |
| "What is /proc?" | 13 Q5 / 2 How |
| "What happens in a context switch?" | 13 Q7 / 9 Internal |
| "Walk through typing a command." | 13 Q9 / 8 Example |
| "What is a D-state process?" | 13 Q10 / 3 When |
