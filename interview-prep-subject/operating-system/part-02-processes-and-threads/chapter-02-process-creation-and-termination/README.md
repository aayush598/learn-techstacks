# Chapter: Process Creation and Termination

## What you'll learn
- The exact mechanics of `fork()`, `exec()`, and `clone()` — the syscalls that create every process on Linux — including return values, copy-on-write, and the multi-threaded fork pitfalls.
- What happens at termination: `exit()`, exit status, `wait()`, and why zombies and orphans exist.
- What daemons are and how they detach (setsid, chdir, umask, redirect fds).
- How processes form trees and how to read them (`ps`, `pstree`, `ppid`).

## Prerequisites (linked)
- [Ch-01 Process Concept](../chapter-01-process-concept/README.md) — PCB, states, process vs program.
- [Part 01 Ch-02 System Calls](../../part-01-os-fundamentals/chapter-02-kernel-architecture/section-03-system-calls-in-depth.md) — the syscall path.
- Feeds into [Ch-03 Threads](../chapter-03-threads/README.md) — `clone` is the primitive behind threads.

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Fork and Exec in Depth](section-01-fork-and-exec-in-depth.md) | The creation syscalls: return values, COW, clone flags, fork-in-multithread traps |
| [Section 02 — Zombie, Orphan, and Daemon Processes](section-02-zombie-orphan-and-daemon-processes.md) | Life-after-death: reaping, adoption, and background daemons |
| [Section 03 — Process Hierarchies and ps Tree](section-03-process-hierarchies-and-ps-tree.md) | Process trees, ppid chains, `ps`/`pstree` reading |

## One-paragraph narrative connecting all sections
Processes come into existence only through `fork`/`clone` + `exec`, and leave only through `exit` + `wait` — understanding those syscalls, their return-value contract, and COW is the core of this chapter (Section 01). What happens at the edges — a process that dies before being reaped (zombie), a parent that dies first (orphan), or a process that detaches to live forever (daemon) — defines the process "afterlife" every production system must handle (Section 02). Put many creations and exits together and you get a process tree — the family structure visible in `ps`/`pstree`, which is both a debugging tool and the origin of signal/group semantics (Section 03).

## Common interview trap in this chapter
Believing `fork` copies all memory. It does **not** — it uses copy-on-write (pages shared read-only; first write duplicates). Also, in a *multi-threaded* process, `fork` duplicates only the calling thread — a classic source of hidden deadlocks. And `exec` returns `-1` only on failure; on success the process never "returns" from `exec` — the new image starts running.

## Checklist before moving on
- [ ] I can predict `fork()`'s return values (0 = child, >0 = child PID, -1 = error).
- [ ] I can explain COW and why `fork`+`exec` is the idiomatic pattern.
- [ ] I can write a parent that correctly reaps children (no zombies).
- [ ] I can explain orphan adoption and daemonization steps.
- [ ] I can read `ps`/`pstree` output and identify parent-child relationships.
- [ ] I know the `clone` flags that create threads vs processes.
- [ ] I know the multi-threaded-fork deadlock trap and the `pthread_atfork`/`posix_spawn` fixes.
