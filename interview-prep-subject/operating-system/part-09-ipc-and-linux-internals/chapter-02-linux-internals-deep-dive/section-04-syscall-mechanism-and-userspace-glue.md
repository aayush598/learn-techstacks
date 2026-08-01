# Syscall Mechanism and Userspace Glue

> **TL;DR**: A syscall is the controlled way user code enters the kernel. On x86-64 it's the `syscall` instruction (`sysenter` on i386, `int 0x80` legacy) with the number in `%rax` and up to 6 args in registers; the kernel dispatches via the `sys_call_table`, executes, and returns through `sysret`. glibc wraps this (via `SYSCALL_WRAPPER`/`syscall(2)`), and the **vdso** lets some calls (gettimeofday, clock_gettime) never trap at all.

## 1. Why Does This Exist?
User code must be able to perform privileged operations (I/O, process control, memory mapping) that it can't do directly — but it must do so *safely*: the CPU must switch privilege levels, the kernel must validate arguments, and the process must be prevented from corrupting the kernel. The syscall interface is the hardware-software contract for this: a small set of numbered, well-checked entry points. It exists to provide (a) isolation (user can't just write to hardware), (b) portability (libc hides the ABI), (c) a stable kernel API, and (d) observability (every privileged action is a named, logged operation — that's what `strace` shows).

## 2. How Does It Work?
**The ABI (x86-64, Linux)**:
- `syscall` instruction (fast path): sets `MSR_LSTAR` → kernel entry; loads RIP from the entry trampoline; switches to kernel stack.
- Number in `%rax`; args in `%rdi, %rsi, %rdx, %r10, %r8, %r9` (note `%r10` instead of `%rcx`, which syscall clobbers); return in `%rax`; negative errno encoded.
- `sysret` returns; `swapgs` to swap the GS base (user vs kernel per-cpu area).
- Legacy: `int 0x80` (i386 gate, still supported); i386 fast path `sysenter`/`sysexit`.
- `syscall_table` (`arch/x86/entry/syscall_64.c`, `sys_call_table`): index by `%rax` → function pointer (`__x64_sys_read`, etc.). Calls are wrapped: `SYSCALL_DEFINE3(read, ...)` → `__x64_sys_read` validates args, may call `ksys_read`.
- **Return convention**: positive/zero = success; negative = `-errno`; glibc maps to `errno` and returns −1.
- **vdso** (virtual dynamic shared object): a kernel-created ELF mapped into every process (`[vdso]` in maps) containing fast, lock-free implementations of `gettimeofday`, `clock_gettime`, `getcpu` — reading the clock directly (vsyscall page: `gettimeofday`/`time` at fixed 0xffffffffff600000). No trap for these.
- **glibc glue**: `open()` → `INLINE_SYSCALL`/`syscall(SYS_openat,...)` → `arch_syscall` (the `syscall` instruction). `syscall(2)` in libc is the generic wrapper taking `syscall_number, args...`.

## 3. When Is It Used?
- Every time a process does anything privileged: open/read/write/close, fork/exec/wait, mmap/munmap, brk, socket, kill, getpid...
- `strace` uses `PTRACE_SYSCALL` to intercept and log each syscall; `perf trace` uses tracepoints (`sys_enter`/`sys_exit`).
- seccomp filters syscalls (`SECCOMP_RET_*`): containers/browsers restrict the syscall set (seccomp-bpf).
- syscall numbers are per-arch (x86-64 vs arm64) and stable-ish (Linux's "no new syscalls break userspace" policy; new numbers appended).
- Fast paths: glibc `gettimeofday`/`clock_gettime` (vdso), `getpid` (cached via clone), `read`/`write` hot loops.

## 4. Why Wasn't Another Approach Chosen?
- **`int 0x80` alone (legacy)**: slow (interrupt gate, saves more state); kept for compat; `syscall` is the fast path.
- **`sysenter` on i386**: faster than int 0x80 but awkward (separate exit path); `syscall` on x86-64 supersedes.
- **No syscall at all (rejected)**: user can't safely do privileged ops; hardware needs a gate.
- **Message-passing kernel (microkernel-style, rejected by Linux)**: Linux is monolithic — syscalls are direct function calls into one kernel image, not IPC.
- **vdso for everything (rejected)**: only *stateless* pure functions can run in user space (clock reads); anything touching kernel state must trap.
- **Stable ABI (chosen)**: syscall numbers/ABI frozen so binaries keep working across kernels; new syscalls appended (e.g., `clone3`, `openat2`, `io_uring_*`).

## 5. Intuition
**A secure bank's teller window**: you (user space) hand the teller (kernel) a numbered form (syscall number) with the amount (arguments) through the bulletproof glass. The teller checks your request (validates), does the work, and hands back the result — but you can never reach behind the counter yourself. The vdso is the ATM in the lobby: for a few things (checking the time) you don't need the teller at all.

## 6. Real-World Analogy
**Restaurant ordering**: `syscall` = the bell to summon the waiter (entry). Your order number (in `%rax`) tells the waiter what you want; the details (in `%rdi..%r9`) are the specifics. The kitchen (kernel) prepares it and the waiter returns with the dish (result) or "we don't have that" (negative errno). The vdso is the menu board printed on the table — you can read the price (time) without calling the waiter. `strace` is a food critic at the next table writing down every order the waiter takes.

## 7. Formal Definition
On x86-64: `syscall` transfers control to `entry_SYSCALL_64` (set in `MSR_LSTAR`), saving user regs, switching to the kernel stack (`swapgs`), and dispatching on `%rax` through `sys_call_table` to `__x64_sys_<name>`. Convention: `%rax = number`, `%rdi/%rsi/%rdx/%r10/%r8/%r9 = args`, result `%rax`, error = `-errno`. `SYSCALL_DEFINEn` macro generates the handler (with `__user` annotations and arg checking). Return path: `syscall_return_slowpath` → `sysretq` (with `swapgs` + stack restore). The vdso (`arch/x86/entry/vdso/vclock_gettime.c`) provides user-space `clock_gettime`/`gettimeofday`/`getcpu` reading `struct pvclock_vsyscall_time_info`/TSC — no trap. `syscall(2)` is the libc generic wrapper; glibc uses inline `SYSCALL_WRAPPER` macros for performance.

## 8. Example
`write(1, "hi\n", 3)` disassembled (the essential part):
```asm
    mov     $1, %rax        ; syscall number for write (1 on x86-64)
    mov     $1, %rdi        ; arg0: fd
    lea     msg(%rip), %rsi ; arg1: buffer
    mov     $3, %rdx        ; arg2: count
    syscall                 ; trap into the kernel
    test    %rax, %rax      ; result: bytes written or -errno
    js      error
```
Kernel side: `sys_call_table[1] = __x64_sys_write` → `ksys_write` → `vfs_write` (Section 03).

`strace` output for the same:
```
write(1, "hi\n", 3)                = 3
```

vdso fast path (no trap): `clock_gettime(CLOCK_MONOTONIC, &ts)` on glibc goes through the vdso when `AT_SYSINFO_EHDR` is set — `strace` shows **no** `clock_gettime` syscall for the monotonic case (that's how you can tell).

## 9. Internal Working
1. User: `syscall` → CPU checks CPL → jumps to `MSR_LSTAR` entry (kernel). Kernel: `swapgs` (per-cpu GS), switch to the task's kernel stack (`sp_scratch`), save user registers in `pt_regs` on the stack.
2. Dispatch: `%rax` → `sys_call_table[%rax]` (bounds-checked). Call `__x64_sys_write` etc. (generated by `SYSCALL_DEFINE3`), which does `kys_*` work and returns a long.
3. Return path: if signals pending (`TIF_SIGPENDING`/`TIF_NEED_RESCHED`) → `syscall_return_slowpath` handles; else set return value in `%rax`, `swapgs`, `sysretq` to user.
4. `strace`: `PTRACE_SYSCALL` sets `TIF_SYSCALL_TRACE` → `trace_sys_enter` hook reports (number, args) → after execution `trace_sys_exit` reports result.
5. seccomp: `__secure_computing` in the entry path filters before dispatch (`SECCOMP_RET_KILL/ERRNO/TRACE/ALLOW`).
6. `io_uring` (modern): avoids per-op syscalls — `io_uring_enter` submits many ops from a shared ring in one trap; completions read from a ring with no syscall.

## 10. Time Complexity
- `syscall` instruction + dispatch: ~100 ns–1 µs overhead (vs ~5–20 ns function call) — dominated by privilege switch + reg save/restore + TLB/state checks.
- vdso fast path: ~10–25 ns (no trap) — why `gettimeofday` is ~10× cheaper through the vdso.
- `int 0x80` (legacy): slower than `syscall` (~1.5–2×) — compat only.
- Batching (`io_uring`): amortizes per-op overhead to ~tens of ns with ring submission.

## 11. Advantages
- **Safety**: privilege separation + validation on every entry.
- **Stable ABI**: number-based, frozen — binary compat across kernels.
- **Fast enough**: `syscall` is cheap (~100 ns); vdso removes traps for hot pure functions; `io_uring` batches.
- **Observable**: `strace`/`perf trace`/`ftrace`/seccomp all hook the well-defined entry.
- **Portable interface**: glibc hides the ABI; C programs don't know the mechanism.

## 12. Disadvantages
- **Overhead**: each trap costs a privilege switch + register save/restore (~100 ns+) — hot paths must batch (io_uring) or avoid traps (vdso).
- **Arg passing limits**: 6 register args; larger data passed by pointer (validated with `copy_from_user`).
- **Attack surface**: syscalls are the main entry into the kernel — bugs here (in validation, copy, dispatch) are security-critical (hence seccomp hardening).
- **Arch divergence**: numbers/ABI differ per arch (x86-64 vs arm64) — portability handled by libc.
- **Semantics rigidity**: adding/changing a syscall is heavy (needs a new number + ABI); newer Linux adds syscalls conservatively.

## 13. Interview Questions
1. **Q: What is a syscall and how does it enter the kernel?** A: A numbered, privileged operation invoked from user space. On x86-64: `syscall` instruction with the number in `%rax`, args in `%rdi..%r9`; the kernel dispatches via `sys_call_table`, runs the handler, returns via `sysret`.
2. **Q: `syscall` vs `int 0x80`?** A: `syscall` (x86-64) is the modern fast path (dedicated instruction, lighter save/restore); `int 0x80` is the legacy i386 interrupt gate, kept for compatibility, slower.
3. **Q: How are arguments passed?** A: Registers: `%rdi, %rsi, %rdx, %r10, %r8, %r9` (up to 6); larger data via pointers the kernel validates and copies (`copy_from_user`). Return in `%rax`; errors as `-errno`.
4. **Q: What is `sys_call_table`?** A: The array mapping syscall number → kernel function (`__x64_sys_<name>`); dispatch is an indexed jump. Generated from `syscall_64.tbl`.
5. **Q: What is the vdso?** A: A kernel-mapped ELF page (`[vdso]`) with user-space implementations of `gettimeofday`/`clock_gettime`/`getcpu` that read the clock without trapping — the reason some "syscalls" never appear in `strace`.
6. **Q: How does `strace` work?** A: `ptrace(PTRACE_SYSCALL)` sets `TIF_SYSCALL_TRACE`; the entry path calls `trace_sys_enter` (log number + args) and `trace_sys_exit` (log result) around the handler.
7. **Q: What is seccomp?** A: A syscall filter (seccomp-bpf): the kernel evaluates a BPF program on each syscall number/args before dispatch and can `ALLOW`, `ERRNO`, `KILL`, or `TRACE` — used by containers/browsers to shrink the attack surface.
8. **Q: Why does `clock_gettime` sometimes show no syscall?** A: Because glibc routes it through the vdso (user-space clock read) — the syscall only happens for clocks the vdso can't serve (e.g., `CLOCK_REALTIME` in some configs, or vdso disabled).
9. **Q: How is the syscall ABI kept stable?** A: Numbers and semantics are frozen (POSIX/Linux ABI); new features get *new* syscalls appended (e.g., `clone3`, `openat2`, `io_uring_*`) rather than changing existing ones.
10. **Q: What is `syscall(2)`?** A: The libc generic wrapper: `long syscall(long number, ...)` — call any syscall by number from C; used when no dedicated wrapper exists.
11. **Q: What is `io_uring` and why does it matter?** A: A high-performance async I/O interface: apps submit many operations into a shared ring and get completions in another, with batching (`io_uring_enter`) — minimizing per-op syscall overhead for servers/databases.
12. **Q: What happens on return from a syscall?** A: The handler returns a long; the entry path checks for signals/rescheduling (slow path), sets `%rax`, `swapgs`, `sysretq` — resuming user code after the `syscall`.

## 14. Follow-Up Questions
1. **Q: What is the difference between `clone` and `clone3`?** A: `clone` takes flags/size in registers; `clone3` passes a `struct clone_args` (extensible, more flags) — the modern API.
2. **Q: What is `audit`?** A: A kernel audit subsystem hooking syscall entry to log security-relevant operations (files, execs) — used in compliance.
3. **Q: What is `perf trace` vs `strace`?** A: `perf trace` uses tracepoints (`sys_enter`/`sys_exit`) — lower overhead, less invasive; `strace` uses ptrace — more detailed but slower.
4. **Q: Can user space call syscalls directly?** A: Yes — `syscall`/`int 0x80` inline, or via `syscall(2)`, or through libc wrappers; that's what `libc` and runtimes like Go/rust do.

## 15. Coding Example
```c
#include <stdio.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <string.h>
#include <errno.h>

// Direct syscall via syscall(2) — no libc wrapper for SYS_write, but this
// shows the mechanism: number + args -> kernel -> return in rax.
long my_write(int fd, const void *buf, size_t count) {
    return syscall(SYS_write, fd, buf, count);   // glibc does the same
}

int main(void) {
    const char *msg = "direct syscall write\n";
    long n = my_write(STDOUT_FILENO, msg, strlen(msg));
    if (n < 0) {
        fprintf(stderr, "errno=%d (%s)\n", errno, strerror(errno));
        return 1;
    }
    printf("wrote %ld bytes\n", n);

    // The vdso fast path — clock_gettime may not appear in strace
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    printf("monotonic seconds: %ld\n", ts.tv_sec);
    return 0;
}
```
Try: `strace -f -e trace=write,clock_gettime ./a.out` — the `write` shows, `clock_gettime` may not (vdso).

## 16. Industry Usage
- **Kernel**: `arch/x86/entry/entry_64.S` (`entry_SYSCALL_64`), `arch/x86/entry/syscall_64.c`, `kernel/entry/common.c`, `include/linux/syscalls.h` (`SYSCALL_DEFINEn`), `arch/x86/entry/vdso/`.
- **glibc**: `sysdeps/unix/sysv/linux/x86_64/sysdep.h` (`SYSCALL_WRAPPER`), `syscall(2)`.
- **Security**: seccomp (Docker/K8s default profiles, Chrome), `audit`, `landlock`.
- **Tracing**: `strace`, `ltrace`, `perf trace`, `ftrace`/`tracefs`.
- **High performance**: `io_uring` (rocksdb, liburing), `eventfd`/`epoll`, DPDK (bypasses kernel).
- **Runtimes**: Go/rust use raw syscalls for fast paths; JVM uses libc.

## 17. References
- Love, *Linux Kernel Development*, Ch. 5 "System Calls".
- Silberschatz, *Operating System Concepts*, Ch. 1.5–1.6 (system calls), Linux chapter.
- Tanenbaum, *Modern Operating Systems*, Ch. 1.5.1 (system calls).
- Kernel docs: `Documentation/admin-guide/syscall-user-dispatch.rst`, `Documentation/security/seccomp_filter.rst`.
- `man 2 syscall`, `man 2 seccomp`, `man 2 ptrace`, `man 2 io_uring_setup`; `strace`(1).

## 18. Cheat Sheet
- x86-64: `syscall` (fast), `int 0x80` (legacy), `sysenter` (i386).
- `%rax` = number; args `%rdi,%rsi,%rdx,%r10,%r8,%r9`; return `%rax`; err = −errno.
- Dispatch: `sys_call_table[%rax]` → `__x64_sys_*`.
- Entry: `entry_SYSCALL_64` → swapgs, kernel stack, pt_regs; exit: `sysretq`.
- vdso: user-space `gettimeofday`/`clock_gettime`/`getcpu` — no trap.
- `SYSCALL_DEFINEn` wraps handlers; glibc `SYSCALL_WRAPPER` wraps calls.
- `strace` = ptrace TIF_SYSCALL_TRACE; seccomp = BPF filter; `io_uring` = batched rings.
- ABI frozen; new syscalls appended (clone3, openat2, io_uring_*).

## 19. Quiz
1. Fast x86-64 syscall instruction? a) int 0x80 b) syscall c) sysenter d) call → **b**
2. Syscall number register? a) %rdi b) %rax c) %r8 d) %rcx → **b**
3. Error return is? a) NULL b) −errno c) 0 d) errno → **b**
4. vdso provides? a) all syscalls b) gettimeofday/clock_gettime c) write d) none → **b**
5. strace uses? a) seccomp b) ptrace c) vdso d) audit → **b**
6. Dispatch table? a) IDT b) sys_call_table c) GDT d) TSS → **b**

## 20. Flashcards
- **Q: syscall entry?** → **A:** `syscall` instr; %rax number; sys_call_table dispatch.
- **Q: arg regs?** → **A:** %rdi,%rsi,%rdx,%r10,%r8,%r9.
- **Q: error return?** → **A:** −errno in %rax.
- **Q: vdso?** → **A:** User-space clock reads, no trap.
- **Q: strace?** → **A:** ptrace TIF_SYSCALL_TRACE hooks.
- **Q: io_uring?** → **A:** Batched async I/O via rings, fewer syscalls.

## 21. Revision
The syscall is the hardware-gated interface between user and kernel: `syscall` (x86-64 fast path; `int 0x80` legacy) with the number in `%rax`, args in registers, dispatch through `sys_call_table` to `SYSCALL_DEFINEn` handlers, and `sysret` return with −errno semantics. glibc wraps it (inline `SYSCALL_WRAPPER`/`syscall(2)`), so C code rarely sees the ABI. The vdso eliminates traps entirely for clock reads; `strace`/`seccomp`/`audit` hook the well-defined entry; and `io_uring` batches many ops into a few traps for performance. Stable numbering keeps binaries running forever, with new syscalls appended. This is the front door to everything Sections 01–03 described — process creation, memory layout, and file I/O all entered through this mechanism.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a syscall / how is it invoked?" | 13 Q1 / 2 How |
| "syscall vs int 0x80?" | 13 Q2 / 4 Why not |
| "How are arguments passed?" | 13 Q3 / 7 Formal |
| "What is sys_call_table?" | 13 Q4 / 9 Internal |
| "What is the vdso?" | 13 Q5 / 2 How |
| "How does strace work?" | 13 Q6 / 9 Internal |
| "What is seccomp?" | 13 Q7 / 9 Internal |
| "What is io_uring?" | 13 Q11 / 10 Complexity |
