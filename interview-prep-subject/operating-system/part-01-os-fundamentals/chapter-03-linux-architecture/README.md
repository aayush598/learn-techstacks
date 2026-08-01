# Chapter: Linux Architecture

## What you'll learn
- The layered Linux block diagram: hardware → kernel (system call interface, process/memory/VFS/network/IPC/security subsystems) → system libraries (glibc/musl) → utility programs → applications.
- How the user/kernel boundary is drawn in Linux: syscall API, virtual filesystems (`/proc`, `/sys`), and the tools that read kernel state.
- The precise difference between **utility programs** (bash, `ls`, `systemd`, `gcc`, daemons) and the **kernel** — and why that distinction is a favorite interview probe.
- Real kernel source paths to cite (`kernel/sched/`, `mm/`, `fs/`, `net/`, `ipc/`, `arch/x86/`).

## Prerequisites (linked)
- [Ch-01 (What is an OS)](../chapter-01-what-is-an-operating-system/README.md) and [Ch-02 (Kernel Architecture)](../chapter-02-kernel-architecture/README.md) — the mode model and syscall machinery are assumed here.
- Feeds forward to [Part 02 (Processes & Threads)](../../part-02-processes-and-threads/README.md) — Linux processes are the concrete example used throughout.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Linux Architecture Overview](section-01-linux-architecture-overview.md) | The full stack: kernel core, subsystems, and the syscall/vFS interface |
| [Section 02 — Utility Programs vs Kernel](section-02-utility-programs-vs-kernel.md) | Who is kernel, who is userspace utility — and why the boundary matters |

## One-paragraph narrative connecting all sections
Linux's architecture is a layered monolith: hardware at the bottom; the kernel in the middle, split into coherent subsystems (process/scheduler, memory, VFS, network, IPC, security) that all communicate through the syscall interface (Section 01). Above the kernel live libraries and utilities — glibc, shells, daemons, compilers — which are *user-space programs*, not the OS, and this boundary is where interviews check your precision (Section 02). Understanding exactly what runs in Ring 0 versus Ring 3, and how each layer uses the others (a shell calling `fork`/`exec`, `/proc` exposing kernel state as files), is the practical skill this chapter builds.

## Common interview trap in this chapter
Saying "systemd is part of the kernel" or "the shell is the OS." Both are user-space. Also: `/proc` and `/sys` are *virtual filesystems implemented by the kernel* — reading them is a syscall (`open`/`read`) on kernel state, not a real disk read. Be able to state the ring and subsystem for any named Linux component.

## Checklist before moving on
- [ ] I can draw the Linux layered diagram from hardware to app with every layer named.
- [ ] I can name the major kernel subsystems and one source path each (`kernel/sched/core.c`, `mm/memory.c`, `fs/`, `net/`, `ipc/`).
- [ ] I can list the kernel's *virtual filesystems* (`/proc`, `/sys`, `/dev`, `debugfs`) and say what each exposes.
- [ ] I can classify 10 Linux programs (bash, ls, systemd, nginx, glibc, modprobe, kthreadd, ksoftirqd, sshd, gcc) as kernel/utility/library.
- [ ] I can explain what `modprobe`, `dmesg`, `lsmod`, and `insmod` do in relation to the kernel.
- [ ] I know that `/proc/<pid>/` exposes each process's PCB-ish state and can name 3 files under it.
