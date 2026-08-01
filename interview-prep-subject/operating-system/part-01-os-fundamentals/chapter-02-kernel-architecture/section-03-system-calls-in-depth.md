# System Calls in Depth

> **TL;DR**: A system call is the only sanctioned door from user space into the kernel — user code triggers a trap with a syscall number, the kernel dispatches through `sys_call_table` to a handler that runs privileged logic and returns results across the boundary.

## 1. Why Does This Exist?
User programs need privileged operations (I/O, process creation, memory mapping, signals) but must never execute them directly. A system call is the *controlled interface*: it exists to (1) give applications a stable, portable API to privileged services, (2) funnel every privileged request through kernel validation and security checks, and (3) keep the mode-switch machinery a small, auditable, well-understood surface. Without syscalls, either apps would execute privileged code (no security) or the kernel would expose nothing (no usable OS).

## 2. How Does It Work?
High-level flow:
1. User code (usually via libc) sets the **syscall number** in a register (`%rax` on x86-64) and arguments in defined registers, then executes the trap instruction (`syscall`).
2. The CPU saves minimal user state, raises privilege to Ring 0, and jumps to the kernel's fixed entry point (`entry_SYSCALL_64`).
3. The kernel validates the number (bounds-check against `NR_syscalls`), swaps to the kernel stack, saves the full user register context, looks up the handler in `sys_call_table[number]`, and calls it.
4. The handler runs with kernel privileges, copies/validates any user pointers (`copy_from_user`), performs the work, and returns a result (usually negative `errno` or a positive value).
5. The kernel restores user registers and returns with `sysretq`, dropping back to Ring 3.

## 3. When Is It Used?
- **Every process syscall**: `fork`, `execve`, `exit`, `wait`, `kill`, `getpid`, `setrlimit`.
- **Every file syscall**: `open`, `read`, `write`, `close`, `stat`, `mmap`, `fsync`.
- **Every networking syscall**: `socket`, `bind`, `connect`, `send`, `recv`, `epoll`, `poll`.
- **Every synchronization syscall**: `futex`, `semop`, `flock`, `setitimer`.
- **Memory**: `mmap`, `munmap`, `mprotect`, `brk`, `madvise`.
- **Info/queries**: `gettimeofday` (often vDSO), `sysinfo`, `uname`, `getrandom`.
- **Practical production use**: `strace` shows every syscall; databases tune `io_uring` to batch syscalls; seccomp filters *which* syscalls a sandboxed process may make.

## 4. Why Wasn't Another Approach Chosen?
- **Direct calls into kernel functions** (just `call` the address): impossible/useless — kernel code is not mapped as callable from user, no gate would validate arguments, and a wrong target would corrupt the kernel.
- **`int 0x80` (legacy interrupt-based syscalls)**: works, but slow — the full interrupt path (IDT, exception frame) is heavyweight. Replaced by `syscall`/`sysenter` fast instructions.
- **Making everything a library call (no kernel boundary)**: no security; libraries can't be trusted with hardware.
- **Microkernel-style remote calls (IPC as the only mechanism)**: elegant but slow per-op; modern kernels keep a syscall ABI and use IPC for special paths.
- **vDSO**: not a replacement, an *addition* — safe read-only syscalls (`gettimeofday`) are served from a user-mapped page to skip the mode switch entirely.
The chosen approach — a fixed, numbered syscall ABI with a fast trap instruction — is the fastest secure mechanism.

## 5. Intuition
A system call is like a **bank teller window**. You (user program) can't walk into the vault (kernel). You slide a written request (syscall number + args) through the slot (trap instruction). The teller (kernel entry) checks it against the menu (sys_call_table), does the work, and hands back cash (return value). Every request is logged and validated; the vault doors never open for you directly.

## 6. Real-World Analogy
A **restaurant order**: the waiter (libc wrapper) takes your order (registers: `%rax`=what, `%rdi`/`%rsi`/... = details), calls the kitchen through the pass-through window (syscall instruction). The kitchen (kernel) checks the menu (valid syscall number) and cooks (handler). A wrong order (bad number) gets rejected ("grilled menu item doesn't exist"). You never walk into the kitchen.

## 7. Formal Definition
A **system call** is the programmatic interface between a process and the OS kernel: a trap-based, hardware-assisted transfer of control from user mode to kernel mode, identified by a system call number, with arguments passed in CPU registers (and optionally memory), that executes a kernel service and returns a status/value to the caller. On Linux x86-64, the ABI is: `%rax` = syscall number, `%rdi/%rsi/%rdx/%r10/%r8/%r9` = args 1-6, return in `%rax` (negative = `-errno`), executed via the `syscall` instruction with entry `MSR_LSTAR`.

## 8. Example
Trace `read(3, buf, 4096)`:
1. libc sets `%rax = 0` (SYS_read), `%rdi = 3`, `%rsi = buf`, `%rdx = 4096`, executes `syscall`.
2. CPU saves user RSP/RFLAGS, sets CPL=0, jumps to `entry_SYSCALL_64`.
3. Kernel switches to kernel stack, uses `swapgs`, saves user regs to pt_regs, checks `nr=0 < NR_syscalls` (yes), calls `sys_call_table[0] = __x64_sys_read`.
4. `__x64_sys_read` calls `ksys_read` → validates fd, gets `struct file`, checks access mode, calls `vfs_read`.
5. VFS reads from page cache; `copy_to_user` copies bytes into `buf` (with `access_ok` check).
6. Returns `n` (bytes read) in `%rax`; kernel restores user regs, `swapgs`, `sysretq` → CPL=3. Total ~100-500ns for a cached read.

## 9. Internal Working
1. **Entry**: `arch/x86/entry/entry_64.S` → `entry_SYSCALL_64`: `swapgs`, push user state, `movq %rsp, %rdi` (pt_regs), `call do_syscall_64`.
2. **Dispatch**: `do_syscall_64` reads `%rax`, bounds-checks, and indexes `sys_call_table[nr]` (array of function pointers generated from `syscall_64.tbl`).
3. **Handlers**: `SYSCALL_DEFINE{n}(...)` macros generate the wrapper + validation. `ksys_read`/`ksys_write` etc. live in `kernel/read_write.c`; argument copying uses `copy_from_user`/`copy_to_user`.
4. **Fast paths**: `gettimeofday`/`clock_gettime` served via vDSO (`arch/x86/entry/vdso/`); `futex` fast path avoids a syscall if the lock isn't contended.
5. **Exit**: `sysretq` restores user context; flags are set to prevent user privilege escalation (on sysret the CPU fixes RFLAGS/CS per SDM constraints).
6. **Security**: `seccomp` filters intercept at dispatch to allow/deny syscalls by number/args for sandboxes (Docker, Chrome).

## 10. Time Complexity
- Dispatch: **O(1)** (array index).
- `read`/`write` from page cache: O(1) + O(copied bytes).
- `open` path resolution: O(path segment count) worst case.
- `fork`: O(page-table size) — slow syscall (why Linux favors `vfork`/`clone`/`posix_spawn`).
- vDSO time reads: O(1), zero syscalls — ~10-20ns vs ~60-100ns via syscall.
- `io_uring`: amortizes N ops into ~O(1) syscalls (submit+wait batches).

## 11. Advantages
- **Stable ABI**: apps compiled against syscall numbers run across kernel versions.
- **Central validation/security**: every privileged action passes a checkable chokepoint.
- **Portable**: identical interface across architectures (via libc and arch tables).
- **Observable/debuggable**: `strace`, `perf trace`, `seccomp` all hook the boundary.
- **Extensible**: new syscalls (`io_uring_setup`, `rseq`) are additive.

## 12. Disadvantages
- **Cost**: mode switch + register save/restore + potential data copies per call.
- **ABI burden**: old syscalls stay forever (compat ABI, 32-bit variants); adding params needs new syscalls.
- **Copy overhead**: large buffers cross the boundary; mitigated by `mmap`/`io_uring` zero-copy paths.
- **Attack surface**: a big syscall table = more kernel code exposed to untrusted callers (mitigated by seccomp/LSM).

## 13. Interview Questions
1. **Q: What is a system call?** A: The kernel's programmatic API — a trap-based request from user mode to kernel mode, identified by a syscall number, executing a privileged service.
2. **Q: What is the difference between a syscall and a library function?** A: A syscall executes in kernel mode (privileged); a library function executes in user mode and may call syscalls internally. E.g., `printf` (libc) → `write` (syscall); `malloc` (libc) → `mmap`/`brk`.
3. **Q (TRICKY): How does the CPU know which kernel code to run for a syscall?** A: The kernel registers a fixed entry point — on x86-64 via `MSR_LSTAR` — and the `syscall` instruction jumps there. Dispatch then uses the number in `%rax` to index `sys_call_table`.
4. **Q: Why is the `syscall` instruction faster than `int 0x80`?** A: `int 0x80` goes through the full IDT exception path (stack switch via TSS, exception frame setup). `syscall`/`sysenter` are optimized for fast transitions — minimal state save, no TSS-based stack switch — cutting several hundred cycles.
5. **Q: How are syscall arguments passed?** A: Registers: `%rdi,%rsi,%rdx,%r10,%r8,%r9` for args 1-6 on x86-64 (note `%r10` replaces `%rcx` which `syscall` clobbers). More than 6 args go via a pointer to a user-space struct.
6. **Q: What does `strace` show you and how is it implemented?** A: Every syscall + args + return. Implemented via `ptrace` (and/or `seccomp` for efficiency) — it observes the syscall boundary without modifying the traced program.
7. **Q (PRODUCTION): Why is a service with 1M tiny syscalls/sec slow, and how do you fix it?** A: Each syscall pays entry+exit+copy overhead (~100ns+), so 1M/s ≈ 100ms of pure overhead. Fix: buffer/batch (`readv`/`writev`), use `mmap` for shared data, use `io_uring` for async/batched I/O, or keep data in the vDSO (time).
8. **Q: What is `copy_from_user` and why do we need it?** A: It safely copies user-space data into kernel memory, validating the pointer with `access_ok()` and handling page faults — user pointers are never dereferenced directly by the kernel.
9. **Q: What is seccomp?** A: A kernel facility (`seccomp(2)`) that allows a process to install filters restricting which syscalls it can make (by number and args) — the basis of container sandboxing (Docker default profile) and Chrome's sandbox.
10. **Q (SCENARIO): You fork 100k processes/sec. What syscalls hurt?** A: `fork` (copy page tables + mm), `execve` (load new image), `wait` (reap). Better: use `vfork`/`clone` with sharing, `posix_spawn` (uses `clone` + internal `exec`), or a thread/worker pool.
11. **Q: What's the vDSO and which syscalls use it?** A: A read-only kernel page mapped into every process exposing user-space implementations of safe, hot syscalls: `gettimeofday`, `clock_gettime`, `getcpu`, `time`. Avoids mode switches.
12. **Q (TRICKY): Can a syscall be interrupted/restarted?** A: Yes — syscalls that block can be interrupted by signals (`EINTR`) and may be auto-restarted if the handler is installed with `SA_RESTART`. Some are restartable (`read`/`write` on slow devices); design of `io_uring` avoids most EINTR.
13. **Q: How does Linux generate the syscall table?** A: From `arch/x86/entry/syscalls/syscall_64.tbl` via a script that emits `sys_call_table` plus prototypes — keeping number↔name↔handler in sync.
14. **Q (PRODUCTION): What is `io_uring` in one paragraph?** A: A Linux async I/O framework using shared ring buffers (SQE/CQE) between user and kernel; you enqueue ops without a syscall per op, and the kernel processes them in batches — near-zero syscall overhead, used by RocksDB/ScyllaDB/QEMU/nginx.
15. **Q: Why do return values use negative numbers for errors?** A: The kernel returns `-errno` (e.g., `-EINVAL = -22`) in `%rax`; libc checks the sign, sets `errno = -retval`, and returns -1. A single register carries both success value and error marker.

## 14. Follow-Up Questions
1. **Q: What is `sysretq`'s security nuance?** A: `sysret` only restores a user-controlled frame if CS/RFLAGS are "safe" (fixed values), preventing a user from returning to Ring 0 — the SDM mandates `swapgs`+`sysret` ordering to avoid a spec-exec gadget.
2. **Q: How does KPTI interact with syscalls?** A: With KPTI enabled, the kernel page table is loaded on entry and user page table on exit — extra CR3 writes that add latency; mitigated by PCID for fast flushes.
3. **Q: What is `clone` vs `fork` vs `vfork`?** A: All create tasks; `clone` takes flags to share address space/fds (threads), `fork` copies, `vfork` shares until exec — Linux implements `fork` via `clone(SIGCHLD)`.
4. **Q: Why are there `*at` syscalls (`openat`, `unlinkat`)?** A: To anchor path resolution to a directory fd — atomic and race-free vs `chdir`+relative, and enables per-fd permission checks.
5. **Q: What is a restart sequence / `rseq`?** A: `rseq(2)` lets user-space code register a restartable critical section — if it's preempted, the kernel restarts it — enabling lock-free user-space algorithms with kernel backup.

## 15. Coding Example
```c
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

int main(void) {
    /* High-level: libc calls the syscall for you */
    int fd = open("/etc/hostname", O_RDONLY);
    if (fd < 0) {
        printf("open failed: %s (errno %d)\n", strerror(errno), errno);
        return 1;
    }
    char buf[64];
    ssize_t n = read(fd, buf, sizeof(buf) - 1);
    close(fd);
    if (n < 0) return 1;
    buf[n] = 0;
    printf("raw read via syscall returned %zd bytes: %s", n, buf);
    return 0;
}
```
```c
/* Direct raw syscall (bypassing libc), Linux x86-64 */
#include <unistd.h>
#include <sys/syscall.h>

long raw_write(int fd, const void *buf, size_t count) {
    long ret;
    __asm__ volatile(
        "syscall"
        : "=a"(ret)
        : "a"(SYS_write), "D"(fd), "S"(buf), "d"(count)
        : "rcx", "r11", "memory");
    return ret;
}

int main(void) {
    const char *msg = "hello from a raw syscall\n";
    raw_write(1, msg, 25);
    return 0;
}
```
```pseudocode
# The syscall path, step by step
USER:  rax=0(read) rdi=fd rsi=buf rdx=n; syscall
CPU:   CPL 3->0; RIP <- MSR_LSTAR; RSP <- kernel stack (from TSS/per-task)
KERNEL entry_SYSCALL_64:
  swapgs                      # kernel per-CPU data now reachable
  push pt_regs (saved regs)
  nr = rax; if nr >= NR_syscalls: return -ENOSYS
  handler = sys_call_table[nr]            # e.g., __x64_sys_read
  ret = handler(pt_regs)                  # validates, does work
  restore regs; swapgs; sysretq           # CPL -> 3
```

## 16. Industry Usage
- **Linux**: `arch/x86/entry/entry_64.S`, `kernel/sys.c`, `fs/read_write.c`, `include/linux/syscalls.h`, `kernel/io_uring/`. Used by every cloud workload; tuned via `strace`/`perf`.
- **Windows NT**: `KiSystemCall64`, `NtXxx` native API vs Win32 API — syscalls are the "native API."
- **macOS/XNU**: `syscall`/`svc` gate; BSD syscalls + Mach traps.
- **Databases**: Postgres uses `read`/`write`+`fsync`; RocksDB/ScyllaDB use `io_uring`; MySQL uses `pread`.
- **Web/edge**: nginx uses `epoll` (communication syscalls); Cloudflare Workers/Wasm often run under seccomp-restricted syscalls.
- **Runtimes**: Go's goroutines block via `futex`; Java NIO uses `epoll`/`kqueue`; Node.js libuv wraps the same syscalls.
- **Interview gold**: being able to say "that's a syscall — here's the cost and here's how I'd batch it" is a strong signal for FAANG SRE/backend roles.

## 17. References
- Linux man: `syscalls(2)`, `syscall(2)`, `seccomp(2)`, `vDSO(7)`, `io_uring(7)`, `clone(2)`, `signal(7)`.
- Linux source: `arch/x86/entry/entry_64.S`, `arch/x86/entry/syscalls/syscall_64.tbl`, `include/linux/syscalls.h`, `kernel/sys.c`, `fs/read_write.c`, `kernel/fork.c`.
- Intel SDM Vol. 3B: SYSCALL/SYSENTER semantics.
- Silberschatz, *OS Concepts*, Ch. 1.11-1.12 (System Calls).
- Tanenbaum, *Modern OS*, Ch. 1.6.5 (POSIX API).
- Kerrisk, *The Linux Programming Interface* (syscall chapters).

## 18. Cheat Sheet
- Syscall = user→kernel trap, numbered, via `sys_call_table`.
- x86-64 ABI: `%rax`=number, `%rdi..%r10` args, return in `%rax`, `-errno` on error.
- `syscall` fast instruction (vs `int 0x80` slow path).
- libc wraps syscalls; vDSO serves hot reads (`gettimeofday`).
- `copy_from_user` + `access_ok` = safe pointer crossing.
- `strace`/`ptrace`/`seccomp` observe or filter the boundary.
- EINTR = interrupted syscall; SA_RESTART re-runs it.
- Batch with `readv`/`writev`/`io_uring` to cut mode switches.
- seccomp = syscall allow-list for sandboxes.
- fork is expensive (page tables); prefer clone/posix_spawn.

## 19. Quiz
1. On x86-64 the syscall number goes in: a) `%rdi` b) `%rax` c) `%rcx` d) stack → **b**
2. `int 0x80` is slower because it uses: a) sysret b) the full IDT exception path c) vDSO d) seccomp → **b**
3. A negative return from a syscall means: a) success b) `-errno` c) overflow d) syscall not found → **b**
4. Which is served from the vDSO? a) `open` b) `gettimeofday` c) `fork` d) `execve` → **b**
5. `strace` uses which mechanism? a) seccomp only b) ptrace c) io_uring d) KVM → **b**
6. Which pair is libc-call → syscall? a) printf→write b) write→open c) malloc→free d) fork→exit → **a**
7. `io_uring` reduces: a) memory b) syscall per-op overhead c) CPU cores d) disk size → **b**
8. Kernel reads user pointers safely via: a) memcpy b) copy_from_user c) strcpy d) direct deref → **b**
9. `fork` is slow because it: a) allocates a thread b) copies page tables/mm c) does I/O d) calls seccomp → **b**
10. EINTR means: a) fatal error b) syscall interrupted by a signal c) bad fd d) timeout → **b**

## 20. Flashcards
- **Q: Syscall definition?** → **A:** Trap-based user→kernel service request, numbered, dispatched via sys_call_table.
- **Q: x86-64 syscall ABI?** → **A:** `%rax`=nr, `%rdi,%rsi,%rdx,%r10,%r8,%r9`=args, ret in `%rax`, `-errno` on error.
- **Q: Why `syscall` over `int 0x80`?** → **A:** Minimal state save, no TSS/IDT overhead.
- **Q: vDSO?** → **A:** User-space copy of hot syscalls like gettimeofday.
- **Q: Safe user-pointer copy?** → **A:** access_ok + copy_from_user/copy_to_user.
- **Q: EINTR + SA_RESTART?** → **A:** Signal interruption; auto-restart of syscall.
- **Q: seccomp?** → **A:** Filter restricting allowed syscalls (sandboxing).
- **Q: How to cut syscall overhead?** → **A:** readv/writev, mmap, io_uring, vDSO.

## 21. Revision
A system call is the gated door between user and kernel: a trap instruction (`syscall` on x86-64) with the number in `%rax`, dispatched through `sys_call_table`, handlers validated with `copy_from_user`, results returned via `sysretq`. It's slower than a function call (mode switch, stack swap, copies) so production systems batch (`readv`/`io_uring`) and use the vDSO for time reads. `strace`/`ptrace`/`seccomp` operate on this boundary. Errors come back as `-errno`. Understand the path, the ABI, the cost, and the batching techniques — that's the whole syscall story.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a system call?" | 7 Formal Definition / 2 How It Works |
| "Syscall vs library function" | 13 Q2 / 14 Follow-Up Q1 |
| "How is a syscall dispatched?" | 9 Internal Working / 13 Q3 |
| "Why syscall > int 0x80?" | 13 Q4 / 4 Why Not |
| "How are args passed?" | 13 Q5 / 7 Formal Definition |
| "Why is my app slow (syscall overhead)?" | 13 Q7 / 16 Industry Usage |
| "What is seccomp / io_uring / vDSO?" | 13 Q9, Q14, Q11 |
| "How does strace work?" | 13 Q6 / 16 Industry Usage |
| "Why is fork slow?" | 13 Q10 / 10 Time Complexity |
| "What is EINTR?" | 13 Q12 / 14 Follow-Up |
