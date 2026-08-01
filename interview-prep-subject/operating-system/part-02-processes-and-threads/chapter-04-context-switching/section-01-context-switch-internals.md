# Context Switch Internals

> **TL;DR**: A context switch saves the running task's registers, program counter, and kernel stack pointer, then loads the next task's — for processes it also switches the address space via `switch_mm` (CR3/page tables) — all orchestrated by `schedule()` in the kernel.

## 1. Why Does This Exist?
Multitasking requires that the CPU *stop* running one task and *start* another — but the CPU has exactly one set of registers, one stack pointer, one PC, and one address space at a time. Context switching exists to preserve the outgoing task's execution state (so it can resume perfectly later) and to install the incoming task's state. Without it, preemption, timeslicing, and I/O-driven rescheduling would be impossible — no multitasking, no responsiveness. It's the mechanism that turns "many tasks" into "many tasks that *appear* to run simultaneously."

## 2. How Does It Work?
When the scheduler picks a new task (`pick_next_task`), it calls the context switch (`context_switch` in `kernel/sched/core.c`):
1. `switch_to()` — saves the outgoing task's callee-saved registers and stack pointer into its PCB (`thread` struct in `task_struct`), then loads the incoming task's and jumps to its saved instruction pointer.
2. `switch_mm()` (only for processes, not for threads in the same process) — reloads CR3 with the new process's page-table base; TLB entries now map the new address space.
3. The kernel stack changes (each task has its own kernel stack); `current` (via per-CPU variable or stack top) now resolves to the incoming task.

## 3. When Is It Used?
- **Every scheduler tick**: a timer interrupt fires → `schedule()` → possibly a switch.
- **When a task blocks**: I/O wait, lock, sleep → `schedule()` → switch to a runnable task.
- **When a task exits**: `do_exit` → schedule the next.
- **Preemption**: a higher-priority task becomes ready → `schedule()`.
- **On wakeup**: an I/O event completes → `try_to_wake_up` → if higher priority, preempt → switch.
- **Voluntary yield**: `sched_yield()`.
- **Migration**: a task moved from one CPU to another (NUMA load balancing) — a switch with extra cache/TLB pain.

## 4. Why Wasn't Another Approach Chosen?
- **Cooperative (no preemptive switch)**: tasks switch only when they voluntarily yield — simpler, but a runaway task freezes the system; rejected for general-purpose OSes (kept in some RTOS/embedded).
- **Hardware context switching (TSS, x86 task gates)**: the CPU switches full task state via the Task State Segment. Rejected — slow (all registers + LDT/CR3), inflexible, and mostly irrelevant to software scheduling; modern kernels use software save/restore with the TSS only for kernel stack/ring transitions.
- **Interpretation/simulation of tasks (no real switch)**: way too slow.
- **Copying whole task memory instead of switching page tables**: no — we switch the *mapping*, memory stays put.
The chosen approach — software register save/restore + page-table pointer reload — is minimal and matches how CPUs actually execute.

## 5. Intuition
Imagine **two professors sharing one whiteboard**. Professor A is mid-proof; to let Professor B teach, A must first photograph the board (save registers) and note exactly where they stopped (PC + stack). Then the board is wiped and B's notes projected onto it (switch_mm). When A returns, their photograph is re-projected and they resume mid-sentence. The "photograph" is the saved context; the "board" is the address space; the "projector" is the page table pointer.

## 6. Real-World Analogy
A **relay race handover**: the baton (CPU) must be passed exactly. The outgoing runner records their position (registers), the incoming runner starts from their own position (restored registers). If it's a *different team* (process switch), the officials also change which lanes/equipment are available (address space). If the next runner is on the *same team* (thread switch), the lane stays the same — much faster handover.

## 7. Formal Definition
A **context switch** is the procedure by which the kernel suspends one task and resumes another: it saves the outgoing task's CPU context (program counter, stack pointer, callee-saved and caller-saved registers) into its PCB, and loads the incoming task's context; for a switch between processes it also switches the address space by reloading the page-table base register (CR3 on x86). It is initiated by the scheduler (`schedule()` → `context_switch()`).

## 8. Example
Process P1 (running) → Process P2 (was ready):
1. Timer interrupt (or blocking syscall) → kernel runs in P1's context on P1's kernel stack.
2. `schedule()` → `pick_next_task()` selects P2.
3. `context_switch(P1→P2)`:
   - `switch_mm(P1's mm, P2's mm)`: CR3 ← P2's page table; TLB entries for P1 flushed (or invalidated via PCID).
   - `switch_to(P1, P2)`: push P1's regs to P1's `thread` struct; SP ← P2's kernel stack; pop P2's regs; return to P2's saved instruction pointer.
4. P2 resumes wherever it was when it was switched out (e.g., inside its own syscall return path).

## 9. Internal Working
1. **Entry**: interrupt/syscall → `entry_SYSCALL_64`/IDT handler → saves `pt_regs` on the task's kernel stack; `schedule()` called from the scheduler path.
2. **pick_next_task**: runqueue (EEVDF rbtree) → next task, or idle task if empty.
3. **prepare_arch_switch**: arch-specific (e.g., arm64 VMID, x86 spec_ctrl for Spectre mitigations).
4. **switch_mm_irqs_off**: loads the new `mm`'s PGD into CR3; if PCID is enabled, loads the new PCID so the TLB keeps only that context's entries; otherwise the TLB is fully flushed (a big cost driver).
5. **switch_to**: `__switch_to` — saves callee-saved regs (r12-r15, rbx, rbp, rsp) into the old task's `thread` struct, loads the new task's, and `ret` into the new task's `switch_return` point; also switches FPU state (lazily on x86) and kernel stack.
6. **finish**: `finish_task_switch` — cleans up locks, updates `current`, wakes the "saved" task's CPU affinity state; on return the new task continues as if it had been scheduled.
7. **Thread switch shortcut**: if next mm == prev mm (same process), `switch_mm` is skipped entirely.

## 10. Time Complexity
- Software overhead: **O(1)** — fixed number of register loads/stores (tens of instructions).
- Real-world cost: ~1-5µs (thread), ~2-10µs+ (process) including scheduler + TLB/cache effects.
- TLB flush (no PCID): O(number of TLB entries) on some archs; with PCID/ASID: O(1) tag switch.
- The *dominant* cost is not the instructions — it's cache/TLB miss recovery and pipeline refills (microarchitectural, not algorithmic).

## 11. Advantages
- **Enables preemptive multitasking** and responsive scheduling.
- **Cheap enough for thousands of switches/sec** (~1-5µs each; typical systems do 1k-100k switches/sec).
- **Thread switches are nearly free** (no address-space change).
- **Portable**: arch-specific save/restore is isolated in `arch/`.

## 12. Disadvantages
- **Cache/TLB pollution**: the new task's data isn't in the caches — miss rates spike after every process switch.
- **Kernel entry/exit cost**: every switch passes through the kernel (KPTI adds a page-table switch).
- **Scaling penalty**: many tasks + frequent switches = measurable overhead (the "too many threads" problem).
- **FPU/AVX state**: saving large vector state can cost hundreds of cycles (mitigated by lazy save).
- **Determinism loss**: switches perturb real-time/latency-sensitive workloads.

## 13. Interview Questions
1. **Q: What is a context switch?** A: The kernel suspending one task and resuming another: saving the outgoing task's registers/PC/kernel-stack into its PCB and loading the incoming task's, switching address space (CR3) when they're different processes.
2. **Q: What's the difference between a mode switch and a context switch?** A: Mode switch = privilege change within the same task (syscall: user→kernel). Context switch = changing which task runs. A syscall doesn't context-switch; a context switch always passes through kernel mode.
3. **Q: What exactly is saved during a switch?** A: The task's registers (callee-saved + PC + SP), kernel stack pointer, FPU state (lazily), and scheduling state; for processes, the page-table pointer (CR3) is switched via `switch_mm`.
4. **Q (TRICKY): Why is switching between threads cheaper than between processes?** A: Threads share the same `mm_struct`/page tables, so `switch_mm` (CR3 reload + TLB flush) is skipped — only registers + kernel stack change. Process switches reload CR3 and suffer TLB/cache misses.
5. **Q: Who initiates a context switch?** A: `schedule()` — called from: timer interrupt (preemption), blocking syscalls (I/O, sleep, locks), exit, wakeup of a higher-priority task, or explicit `sched_yield`.
6. **Q: What does `switch_mm` do?** A: Loads the new process's page-table base into CR3 (and PCID if enabled), so the CPU's memory translations now map the new address space; it's the point where the TLB's old mappings become invalid for the new context.
7. **Q: Where is a task's saved context stored?** A: In its PCB — on Linux in `task_struct.thread` (the `thread_struct` holding SP/regs) plus the `pt_regs` frame on its kernel stack; the kernel stack pointer is in `task_struct.stack`.
8. **Q (SCENARIO): A system shows 100k context switches/sec with high CPU. What's wrong?** A: Too many runnable tasks churning — likely oversubscribed threads, tight loops yielding, or lock convoying. Fix: reduce threads (pools), batch work, pin tasks (affinity), increase time slices where acceptable.
9. **Q: How does the kernel switch the kernel stack?** A: Each task has its own kernel stack; `switch_to` swaps the SP to the incoming task's kernel stack (found from `task_struct.stack`/`thread.sp`), so kernel-mode execution continues on the right stack. The TSS's RSP0 is updated for the next user→kernel transition.
10. **Q: What is the idle task and does switching to it count?** A: When no task is runnable, `pick_next_task` returns the idle task (per-CPU) — the switch happens, then the CPU halts (`hlt`) until an interrupt. It still costs a switch to go idle and back.
11. **Q (TRICKY): Does a context switch always flush the TLB?** A: No — with PCID (x86) / ASID (ARM), the TLB is tagged per context; only that context's entries are invalidated (or reused). Without it, CR3 reloads flush fully. Also thread switches (same mm) flush nothing.
12. **Q: What is `sched_yield` and when is it harmful?** A: It moves the task to the end of the runqueue (voluntary yield). Harmful when overused — busy-wait loops yielding cause thrashing and can burn CPU; prefer blocking on proper synchronization.
13. **Q: How does a wakeup relate to a context switch?** A: `try_to_wake_up` makes a blocked task runnable (enqueues it); if its priority beats the running task and preemption is enabled, `schedule()` runs → a context switch to the woken task.
14. **Q: What is the cost in cycles?** A: Software path ~1-5µs total including scheduler; the instructions are O(1) but the dominant cost is cache/TLB misses after the switch (new working set), plus kernel entry/exit. Perf can measure with `perf sched`.
15. **Q: What is `finish_task_switch` for?** A: Post-switch bookkeeping: releases runqueue locks, updates `current`, calls arch-specific finalizers, and wakes the CPU's idle/preemption state — it completes the switch safely after the new task has begun.

## 14. Follow-Up Questions
1. **Q: What is lazy FPU switching?** A: The kernel doesn't save FPU/AVX state on every switch; it marks the state "dirty" and only saves on a real conflict (another task actually using FPU) — saving ~50-100+ cycles per switch in the common case.
2. **Q: What is `rseq` and how does it avoid context switches in user code?** A: Restartable sequences let user code run a critical section that the kernel *restarts* if a context switch happens inside it — enabling lock-free user-space algorithms with kernel support.
3. **Q: What is KPTI's impact on switches?** A: With KPTI, every kernel entry/exit switches page tables (user ↔ kernel), adding cost to *every* syscall/interrupt — historically ~5-30% on syscall-heavy workloads.
4. **Q: What is CPU migration and why is it costly?** A: Moving a task to another CPU means its cached data/TLB is on the old CPU — the new CPU starts cold (cache miss storm). Load balancing balances usage against this cost; `sched_setaffinity` pins tasks to avoid it.
5. **Q: What is the relationship between context switch and signal delivery?** A: Signals also switch to kernel mode and back (mode switch), and delivery runs the handler in user mode — but that's not a context switch unless the scheduler changes tasks.

## 15. Coding Example
```c
/* userspace-simulated context switch: saving/restoring registers (conceptual) */
#include <stdio.h>
#include <setjmp.h>

/* jmp_buf saves a context: registers + SP + PC — the user-space analog */
static jmp_buf envA, envB;
static int turn = 0;

void taskB(void) {
    for (int i = 0; i < 3; i++) {
        printf("B running\n");
        if (setjmp(envB) == 0) longjmp(envA, 1);   /* yield to A */
    }
}
int main(void) {
    if (setjmp(envA) == 0) {
        for (int i = 0; i < 3; i++) {
            printf("A running\n");
            if (setjmp(envA) == 0) longjmp(envB, 1);/* yield to B */
        }
        taskB(); /* won't be reached directly */
    }
    return 0;
}
```
```pseudocode
# Linux context-switch pseudocode (kernel/sched/core.c)
schedule():
    prev = current
    rq = this_rq()
    next = pick_next_task(rq, prev)      # EEVDF: leftmost of rbtree, or idle
    if next != prev:
        context_switch(rq, prev, next)

context_switch(rq, prev, next):
    prepare_arch_switch(next)
    if prev->mm != next->mm:             # process switch
        switch_mm_irqs_off(prev->mm, next->mm)   # CR3 := next->pgd (+PCID)
    switch_to(prev, next, prev)          # save/restore regs + kernel stacks
    finish_task_switch(prev)
```

## 16. Industry Usage
- **Linux**: `kernel/sched/core.c` (`schedule`, `context_switch`, `finish_task_switch`), `arch/x86/kernel/process_64.c` (`__switch_to`), `arch/x86/mm/tlb.c` (PCID/flush), `include/linux/sched.h` (`thread_struct`). Tuned heavily on cloud hosts.
- **Performance engineering**: SREs use `vmstat`, `sar`, `perf sched`, `pidstat -w` to diagnose switch storms; databases tune thread counts; high-frequency trading uses thread-per-core + busy-poll to *avoid* switches.
- **Networking**: kernel-bypass (DPDK, XDP) exists partly to avoid the mode/context switch cost per packet.
- **Virtualization**: KVM vCPU switches add another layer of context/VMENTER/VMEXIT cost.
- **Real-time**: PREEMPT_RT reduces preemption latency; RTOSes design for O(1) deterministic switches.
- **Interview angle**: "why is context switching expensive" and "how do you reduce it" are core SRE/systems questions.

## 17. References
- Silberschatz, *OS Concepts*, Ch. 3.2 (Context Switch).
- Tanenbaum, *Modern OS*, Ch. 2.1.3.
- Linux source: `kernel/sched/core.c`, `arch/x86/kernel/process_64.c`, `arch/x86/include/asm/switch_to.h`, `arch/x86/mm/tlb.c`.
- Intel SDM (PCID, TSS).
- Love, *Linux Kernel Development*, Ch. 4 (Scheduling, context switch).
- Kernel docs: "Context Switch" in kernel/sched/.

## 18. Cheat Sheet
- Context switch = save one task's regs/PC/stack, load another's; process switch also changes CR3.
- `switch_to` = registers + kernel stacks; `switch_mm` = CR3/page tables.
- Thread switch skips switch_mm → cheaper.
- Mode switch ≠ context switch (syscall = mode switch).
- Cost: ~1-5µs thread, ~2-10µs+ process; TLB/cache misses dominate.
- PCID/ASID tag TLB per context → avoids full flushes.
- Triggered by: timer, block, exit, wakeup-preempt, yield.
- Saved in task_struct.thread + kernel stack pt_regs.
- Idle task runs when runqueue empty (hlt).
- Too many switches = CPU burn; fix with pools, affinity, batching.

## 19. Quiz
1. A context switch between processes changes: a) only regs b) regs + CR3 c) nothing d) the kernel image → **b**
2. Thread switch skips: a) switch_to b) switch_mm c) schedule d) nothing → **b**
3. Mode switch is: a) a context switch b) a privilege change in the same task c) a reboot d) an ISR → **b**
4. The saved registers live in: a) user stack b) task_struct.thread / kernel stack c) disk d) heap → **b**
5. PCID helps by: a) speeding disk b) tagging TLB entries per context c) larger cache d) compressing regs → **b**
6. Which does NOT trigger a context switch? a) timer tick b) blocking read c) a simple function call d) wakeup of higher priority → **c**
7. Switch cost is dominated by: a) register count b) TLB/cache misses c) RAM speed d) disk I/O → **b**
8. `pick_next_task` returning idle means: a) empty runqueue b) deadlock c) panic d) reboot → **a**
9. sched_yield moves a task to: a) the front b) the end of the runqueue c) a wait queue d) another CPU → **b**
10. The idle task does: a) busy loop b) hlt until interrupt c) reboot d) spin forever → **b**

## 20. Flashcards
- **Q: What is a context switch?** → **A:** Save one task's context, load another's; processes also switch CR3.
- **Q: Mode vs context switch?** → **A:** Privilege change (same task) vs task change.
- **Q: Why are thread switches cheaper?** → **A:** Same mm → no switch_mm/CR3/TLB work.
- **Q: What's saved?** → **A:** Registers, PC, kernel stack; in task_struct.thread.
- **Q: What does switch_mm do?** → **A:** Load new process's page tables into CR3.
- **Q: Dominant cost?** → **A:** TLB/cache misses, not instructions.
- **Q: PCID?** → **A:** Tag TLB entries per context; avoid full flushes.
- **Q: Triggers?** → **A:** Timer, block, exit, preempt-on-wake, yield.
- **Q: Idle task?** → **A:** Runs when runqueue empty; hlt until interrupt.

## 21. Revision
A context switch saves the outgoing task's registers/PC/kernel-stack and loads the incoming task's; between processes it also reloads CR3 (`switch_mm`), which is why thread switches (shared mm) skip it and cost less (~1-5µs vs 2-10µs+). It's triggered by timers, blocking, exit, and preemptive wakeups. The instruction cost is O(1); the real cost is TLB/cache misses, mitigated by PCID/ASID, CPU affinity, and reducing switch frequency (thread pools, batching). Mode switch (syscall) ≠ context switch. Too many switches = CPU burn.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "What is a context switch?" | 7 Formal Definition / 2 How It Works |
| "Mode switch vs context switch?" | 13 Q2 / 8 Example |
| "What is saved during a switch?" | 13 Q3 / 9 Internal Working |
| "Why are thread switches cheaper?" | 13 Q4 / 10 Time Complexity |
| "Who triggers a switch?" | 13 Q5 / 9 Internal Working |
| "Does a switch always flush TLB?" | 13 Q11 / 14 Follow-Up Q3 |
| "100k switches/sec — problem?" | 13 Q8 / 16 Industry Usage |
| "What is the idle task?" | 13 Q10 / 9 Internal Working |
| "What is lazy FPU switching?" | 14 Follow-Up Q1 |
| "How do you reduce switching cost?" | 16 Industry Usage / 14 Q4 |
