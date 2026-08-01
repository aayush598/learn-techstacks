# Interrupts, Traps, and Exceptions

> **TL;DR**: The CPU interrupts normal flow to handle events — hardware devices raise asynchronous *interrupts*, software deliberately triggers *traps* (syscalls), and faults/errors become *exceptions* — all routed through the Interrupt Descriptor Table (IDT) to kernel handlers, which split work into fast top halves and deferred bottom halves.

## 1. Why Does This Exist?
The CPU can't just poll devices — a network card may deliver a packet at any moment; a timer must fire exactly on schedule; a page fault needs kernel action. Without an event mechanism, the OS could never react to hardware, never preempt, and never protect itself. Interrupts/traps/exceptions exist so the CPU can **asynchronously (interrupt) or synchronously (trap/fault) transfer control to the kernel**, letting devices notify the OS and letting the OS catch errors. They are the "bottom-up" half of the OS's control flow (syscalls are the top-down half).

## 2. How Does It Work?
- The kernel builds an **IDT** (Interrupt Descriptor Table) at boot, mapping each event vector (0-255) to a handler.
- When an event fires: the CPU saves minimal state (SS/RSP/RFLAGS/CS/RIP on stack), checks privilege, and jumps to the handler (raising privilege to Ring 0).
- **Interrupts** (async, from devices/timer): `INTR`/`NMI`; the kernel's `do_IRQ`/`common_interrupt` runs the ISR.
- **Exceptions** (sync, from the executing instruction):
  - **Faults** (recoverable, e.g., page fault #PF, #GP): the instruction *re-runs* after handler fixes it.
  - **Traps** (intentional, e.g., `int3` breakpoint, syscall): execution continues *after* the trapping instruction.
  - **Aborts** (unrecoverable, e.g., machine check #MC): severe; system may panic.
- Hardware uses the **APIC (local/IO APIC)** to route device IRQs to CPUs; the kernel masks/unmasks via `cli`/`sti`.

## 3. When Is It Used?
- **Timer interrupt** (PIT/HPET/TSC-based): drives preemptive scheduling and jiffies.
- **Device IRQs**: NIC packet arrival, disk completion (NVMe MSI-X), keyboard, USB — bottom-halves wake I/O waiters.
- **Page faults**: demand paging, COW (fork), swap-in, `mmap` loading.
- **Divide-by-zero / invalid opcode / alignment**: SIGFPE/SIGILL/SIGBUS delivery.
- **Syscalls** (`int 0x80` legacy, or the fast `syscall` path): traps.
- **Debugging**: `int3` breakpoints, single-step traps.
- **NMI / machine check**: hardware errors, watchdog resets.
- **Virtualization**: VMEXIT on sensitive instructions — the hypervisor's "interrupt".

## 4. Why Wasn't Another Approach Chosen?
- **Polling** instead of interrupts: CPU would spin checking device status — wastes cycles; only used for very low-latency or rare events (some high-speed NIC drivers poll in busy-poll mode; `POLL` still exists). Interrupts win for event-driven efficiency.
- **Software signals for hardware events**: too slow and lossy; interrupts are hardware-vectored with no user-space round-trip.
- **One giant handler**: fast but unfriendly — interrupts would be masked too long, hurting latency. The kernel splits **top half (fast, atomic, masks) vs bottom half (deferred: softirq/tasklet/workqueue)** so latency-sensitive hardware is serviced immediately and heavy work is queued.
- **Handling everything in user space**: impossible — page faults and timer ticks need kernel privileges immediately.

## 5. Intuition
Think of **working in a busy office**: a ringing phone (device interrupt) is asynchronous — you stop typing, note the message, and later finish the report (bottom half). A colleague *interrupting you mid-word* is a synchronous exception — something in your current task is wrong and must be fixed now (fault). A scheduled alarm to take medicine (timer interrupt) forces you to act at a precise moment. Traps are you *deliberately* knocking on your manager's door (syscall) — intentional, not a surprise.

## 6. Real-World Analogy
A **hospital**: the heart monitor beeps (device interrupt) — a nurse (ISR) rushes in, stabilizes (top half), then writes the chart later (bottom half). A patient's allergic reaction during a procedure (exception) halts the procedure to fix it (fault) or ends it (abort). The emergency exit drill bell (NMI) is unscheduled and urgent. The reception desk where patients check in intentionally (syscall) is the trap.

## 7. Formal Definition
- **Interrupt**: an asynchronous hardware-initiated event that suspends the current instruction stream and transfers control to a handler via an IDT vector (maskable `INTR` or non-maskable `NMI`).
- **Exception**: a synchronous event caused by the currently executing instruction — **fault** (precise, re-executable: page fault, #GP), **trap** (precise, continue after: breakpoints, some syscalls), **abort** (imprecise, fatal: machine check).
- **ISR (Interrupt Service Routine)**: the handler run in kernel mode; in Linux the split is **top half** (atomic, quick, disables/masks IRQs) and **bottom half** (deferred `softirq`/`tasklet`/`workqueue`).

## 8. Example
A **network packet arrives** (e1000e NIC, MSI-X to CPU 2):
1. NIC writes packet to DMA ring, raises IRQ vector 47 → LAPIC interrupts CPU 2.
2. CPU saves context (already in kernel or traps in), jumps via IDT to `common_interrupt`.
3. Top half (`irq_handler`): acknowledges the IRQ (`EOI`), adds the driver's NAPI poll to the softirq list, returns.
4. **Softirq** (`NET_RX_SOFTIRQ`) runs shortly after: driver polls the ring, builds `skb`, passes up the network stack (IP/TCP), wakes the socket waiter (sets a task runnable).
5. Scheduler runs the woken task later; the packet reaches `recvfrom()`.
The **split** means the CPU is only in the critical ISR for microseconds, so other IRQs aren't starved.

## 9. Internal Working
1. **Setup**: `trap_init()`/`idt_setup_early_handler` fills `idt_table[256]` with `entry_*.S` stubs; `MSR_IST`/TSS set up stacks (e.g., separate NMI/MCE stacks on x86-64).
2. **Delivery**: CPU pushes frame (SS,RSP,RFLAGS,CS,RIP, error code for some exceptions), checks CPL/DPL, sets Ring 0, jumps.
3. **Common entry** (`.entry_trampoline`/`common_interrupt`): swapgs (if from user), switch to kernel stack if needed, save full pt_regs.
4. **Dispatch**: `do_IRQ` (hardware) → `handle_irq_event` → driver `handle_irq` → top-half routine.
5. **Defer**: mark `softirq` pending → on return, `__do_softirq` runs (or `ksoftirqd` if overrun) → bottom halves (NAPI, tasklets, RCU callbacks).
6. **Exit**: restore regs, `iretq` (or `sysretq` for syscall-trap path).
7. **Exception handling**: `do_page_fault`, `do_general_protection` etc. → kernel oops or signal delivery.

## 10. Time Complexity
- Interrupt dispatch: **O(1)** (IDT index).
- Top-half ISR: O(1) typically (ack + mark pending).
- Softirq processing: O(events) batched; bounded per `max_action` (e.g., 2ms budget before `ksoftirqd`).
- Context switch caused by interrupt → wake: O(1) amortized (EEVDF O(log n) worst-case).
- NMI/machine-check handling: O(1), may be fatal.
- Latency goals: interrupt latency (event → ISR start) ~1-20µs; scheduling latency ~100µs on tuned systems.

## 11. Advantages
- **Asynchronous, event-driven efficiency**: no busy-waiting on devices.
- **Priority & preemption**: timer interrupts enable preemptive scheduling.
- **Fault tolerance**: page faults, COW, and demand paging are impossible without exceptions.
- **Deterministic device response**: IRQ latency is bounded by ISR length + masking rules.
- **Separation of concerns**: top half fast/atomic, bottom half flexible — keeps latency low.

## 12. Disadvantages
- **Latency**: ISRs mask interrupts (esp. with `cli`/legacy) — long top halves delay other IRQs.
- **Interrupt storms**: high-frequency IRQs (e.g., DDoS on a NIC) starve the CPU; mitigated by NAPI polling, IRQ coalescing, throttling.
- **Complexity**: nested/prioritized delivery, deferred handling, per-CPU softirqs, RCU interactions — a rich source of bugs.
- **Non-maskable events**: NMIs/MCE can hit while the kernel holds locks, requiring special no-lock handlers.
- **Preemption/masking correctness**: `cli`-region bugs freeze the whole CPU.

## 13. Interview Questions
1. **Q: What is the difference between an interrupt and an exception?** A: Interrupt = asynchronous, hardware-initiated (device/timer). Exception = synchronous, caused by the executing instruction (page fault, #GP, breakpoint). Syscall traps are the user-initiated exception case.
2. **Q: What is the IDT?** A: The Interrupt Descriptor Table — a 256-entry table mapping vectors (0-255) to handler code/gates; the CPU uses it to find handlers for interrupts, exceptions, and legacy `int` syscalls.
3. **Q (TRICKY): Why does Linux split interrupt handling into top/bottom halves?** A: Top half must be short and atomic (ack the IRQ, mark work) so interrupts aren't masked long and other devices aren't starved; heavy processing (packet parsing, wakeups) is deferred to softirq/tasklet/workqueue.
4. **Q: What is the difference between softirq, tasklet, and workqueue?** A: softirq — statically compiled, per-CPU, runs in softirq context (interrupts on, preemption off); tasklet — dynamic, built on softirq; workqueue — runs in process context, can sleep, scheduled by kernel threads (`kworker`).
5. **Q: How does a page fault work?** A: CPU raises #PF vector 14 → kernel `do_page_fault` → checks the faulting VMA: valid → map/demand-page/COW and re-run the faulting instruction; invalid → SIGSEGV (or kill).
6. **Q: What is NAPI and why do high-speed NICs use it?** A: New API — after the first IRQ, the driver *polls* the receive ring for a budget of packets instead of IRQ per packet, avoiding interrupt storms at high packet rates (used by e1000e, mlx5, etc.).
7. **Q (SCENARIO): Your server's `softirq` CPU usage is 90%. What's happening?** A: Likely a network interrupt storm — per-packet softirq cost dominates. Fixes: NAPI budget tuning, IRQ coalescing, RPS/RSS to spread queues across CPUs, or DPDK-style polling for extreme rates.
8. **Q: What is the timer interrupt for?** A: It drives the scheduler (preemption/ticks), jiffies timekeeping, timers, and process accounting. Modern Linux uses TSC/deadline timers, sometimes tickless (NO_HZ) to reduce overhead.
9. **Q: What happens if an exception occurs in kernel mode?** A: It's handled by the same IDT vector; if it's fatal (kernel oops/panic) or a recoverable case (e.g., fixing up a user pointer fault) the kernel handles it internally; an unhandled fault in kernel → `BUG()`/panic.
10. **Q: What is an NMI?** A: Non-maskable interrupt — cannot be disabled by `cli`; used for watchdog resets, machine checks, hardware errors; handler must be deadlock-free (can't take normal locks).
11. **Q (PRODUCTION): What is IRQ affinity / RPS / RSS?** A: IRQ affinity pins an IRQ to specific CPUs; RPS (Receive Packet Steering) distributes packet processing across CPUs in software; RSS distributes it in hardware (NIC hashing) — all to scale out and avoid a single softirq bottleneck.
12. **Q: What is the difference between a fault and a trap?** A: A fault re-executes the faulting instruction after the handler returns (page fault); a trap continues after the instruction (breakpoint, syscall). Aborts don't return at all.
13. **Q: What is `cli`/`sti` and why do kernel developers avoid them?** A: They mask/unmask interrupts locally. They're avoided because they disable preemption/timing guarantees and hurt latency; Linux prefers `local_irq_disable` scoped regions, spinlocks (`spin_lock_irqsave`), and RCU.
14. **Q: What is the machine check exception (#MC)?** A: A hardware error (ECC memory, bus parity) that the kernel either recovers from or panics on; often logged via `mcelog`/`rasdaemon`.
15. **Q (TRICKY): Can a syscall be made via an interrupt on x86-64?** A: Historically yes — `int 0x80` is a trap through the IDT. Modern kernels route user syscalls through the `syscall`/`sysenter` fast path, but `int 0x80` still works (slower) for compat.
16. **Q: How does the kernel know which device sent an interrupt?** A: Via the IRQ number (vector) routed by the IO-APIC/LAPIC, plus the driver that registered that IRQ (`request_irq`); shared IRQs are disambiguated by each driver checking its status register.

## 14. Follow-Up Questions
1. **Q: What is interrupt coalescing?** A: The NIC delays generating an interrupt until several packets or a timer threshold — reduces IRQs/sec at the cost of latency (tunable via ethtool).
2. **Q: What is a clock event device vs clock source?** A: Clock source (TSC, HPET) provides time; clock event devices (local APIC timer) generate future interrupts — the two halves of the timer framework.
3. **Q: What is the difference between per-CPU interrupt stack and normal kernel stack?** A: Interrupts use separate per-CPU stacks (e.g., `exception_stacks`) to avoid overflowing the task's small kernel stack during nested/prioritized interrupts.
4. **Q: What is RCU and how does it interact with interrupts?** A: Read-Copy-Update defers reclaim of data to a quiescent point; softirq/RCU callback processing must observe the end of interrupt contexts to reclaim safely.
5. **Q: How does KVM deliver virtual interrupts?** A: LAPIC virtualization (posted interrupts) lets a VM's device IRQ be injected directly (posted interrupt descriptor), avoiding a full VMEXIT — the "interrupt within a VM" analog.

## 15. Coding Example
```c
/* Linux kernel: registering an interrupt handler with request_irq */
#include <linux/interrupt.h>
#include <linux/module.h>
#include <linux/delay.h>

static irqreturn_t my_handler(int irq, void *dev_id) {
    /* TOP HALF: quick, atomic, no sleeping */
    /* typically: ack hardware, set a flag / schedule_work */
    return IRQ_WAKE_THREAD;               /* or IRQ_HANDLED */
}

static struct work_struct my_work;
static void my_bottom_half(struct work_struct *w) {
    /* BOTTOM HALF: process context, can sleep */
    printk(KERN_INFO "bottom half ran\n");
}

static int __init mod_init(void) {
    INIT_WORK(&my_work, my_bottom_half);
    /* IRQF_SHARED since IRQ may be shared */
    return request_irq(irq, my_handler, IRQF_SHARED, "my_dev", &my_work);
}
```
```pseudocode
# Exception classification at a glance
Interrupt (async): NIC packet, timer tick -> vector via IDT, ISR + bottom half
Exception (sync):
  Fault:   page fault #PF, #GP -> handler fixes, re-executes instruction
  Trap:    int3 breakpoint, int 0x80 syscall -> continue after instruction
  Abort:   machine check #MC -> fatal/panic, no return
```

## 16. Industry Usage
- **Linux**: `kernel/irq/` (irq subsystem), `arch/x86/kernel/irq.c`, `arch/x86/entry/entry_64.S`, `net/core/dev.c` (NAPI), `kernel/softirq.c`, `kernel/workqueue.c`. Cloud infra depends on tuned IRQ affinity and NAPI.
- **Windows NT**: `KeInsertQueueDpc` (DPC = deferred procedure call, the bottom-half analog), IRQLs (interrupt request levels) — the interrupt model is a core Windows Internals topic.
- **macOS/XNU**: `IOKit` handles device IRQs; `WorkLoop` for deferred work.
- **RTOS (FreeRTOS)**: ISRs only signal; tasks do the work — the same top/bottom split in miniature (critical sections via `portDISABLE_INTERRUPTS`).
- **Networking/cloud**: RDMA, DPDK, AF_XDP move packet handling out of softirq for extreme throughput — the industry's answer to softirq cost.
- **Databases**: fsync-heavy workloads generate many disk IRQs; NVMe uses MSI-X per queue; `io_uring` minimizes completions.
- **Interview angle**: "interrupt storm", "NAPI", "softirq CPU burn", and "top vs bottom half" are classic SRE/backend probing questions.

## 17. References
- Intel SDM Vol. 3A Ch. 6 (Interrupt & Exception Handling), Vol. 3B (NMI, APIC).
- Silberschatz, *OS Concepts*, Ch. 1.2.3 (Interrupts), Ch. 2.6 (OS Operations).
- Tanenbaum, *Modern OS*, Ch. 1.5.3 (Interrupts).
- Linux source: `kernel/irq/handle.c`, `kernel/softirq.c`, `arch/x86/kernel/irq.c`, `net/core/dev.c`, `include/linux/interrupt.h`.
- docs.kernel.org — "Linux Generic IRQ Handling".
- Russinovich, *Windows Internals* (Interrupts & DPCs).

## 18. Cheat Sheet
- Interrupt = async device event; Exception = sync instruction event; Trap = intentional sync.
- Fault re-executes; trap continues after; abort is fatal.
- IDT = 256-entry vector table → handlers.
- Top half: quick/atomic ISR; bottom half: softirq/tasklet/workqueue (deferred).
- Timer interrupt → scheduler preemption + jiffies.
- Page fault = exception-driven demand paging/COW.
- NAPI = poll after first IRQ; kills interrupt storms.
- RPS/RSS/IRQ affinity distribute packet load across CPUs.
- `cli`/`sti` mask interrupts — avoid long critical sections.
- #MC machine check = hardware error, often panic.

## 19. Quiz
1. A device IRQ is: a) synchronous b) asynchronous c) a trap d) an abort → **b**
2. A page fault is a: a) trap b) fault c) interrupt d) NMI → **b**
3. `int3` breakpoint is a: a) fault b) trap c) interrupt d) abort → **b**
4. Linux deferred interrupt work is done by: a) ISR b) softirq/tasklet/workqueue c) systemd d) NMI → **b**
5. NAPI converts: a) IRQ-per-packet to polling b) sync to async c) traps to faults d) IRQ to NMI → **a**
6. Which is NOT a bottom-half mechanism? a) softirq b) workqueue c) tasklet d) ISR → **d**
7. NMI stands for: a) non-maskable interrupt b) net multi-queue irq c) new machine interface d) no-mechanism-irq → **a**
8. `#GP` in user mode usually results in: a) reboot b) SIGSEGV c) SIGUSR1 d) nothing → **b**
9. Which scales packet processing across CPUs in software? a) RSS b) RPS c) IRQ only d) EOI → **b**
10. Faulting instructions re-execute: a) never b) always after handler fixes c) only in RTOS d) only for traps → **b**

## 20. Flashcards
- **Q: Interrupt vs exception?** → **A:** Async hardware event vs sync instruction event.
- **Q: Fault vs trap vs abort?** → **A:** Re-execute / continue-after / fatal.
- **Q: What is the IDT?** → **A:** 256-entry table mapping vectors to handlers.
- **Q: Top vs bottom half?** → **A:** Atomic quick ISR vs deferred softirq/workqueue.
- **Q: Why NAPI?** → **A:** Poll after first IRQ to avoid interrupt storms.
- **Q: Page fault?** → **A:** Exception → demand paging/COW, re-execute.
- **Q: Timer interrupt?** → **A:** Drives preemptive scheduling and jiffies.
- **Q: RPS/RSS/IRQ affinity?** → **A:** Spread packet processing across CPUs (SW/HW).
- **Q: What is NMI?** → **A:** Non-maskable interrupt for watchdogs/MCE.

## 21. Revision
The CPU routes events through the IDT: interrupts (async, hardware), traps (intentional, e.g., syscalls), faults (recoverable, re-execute — page faults), and aborts (fatal). Handlers split into fast atomic top halves and deferred bottom halves (softirq/tasklet/workqueue) to keep IRQ latency low. NAPI polling prevents interrupt storms; RPS/RSS/IRQ affinity scale packet handling across cores. Timer interrupts drive preemption. Every device I/O and every protection violation you'll ever discuss resolves to this model.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Interrupt vs exception?" | 2 How It Works / 7 Formal Definition |
| "What is the IDT?" | 13 Q2 / 9 Internal Working |
| "Top half vs bottom half?" | 13 Q3 / 9 Internal Working |
| "What is NAPI / interrupt storm?" | 13 Q6-7 / 16 Industry Usage |
| "What is a page fault?" | 13 Q5 / 7 Formal Definition |
| "Why is softirq CPU 90%?" | 13 Q7 / 16 Industry Usage |
| "Fault vs trap?" | 13 Q12 / 7 Formal Definition |
| "What is NMI / machine check?" | 13 Q10, Q14 |
| "How are IRQs distributed across CPUs?" | 13 Q11 / 16 Industry Usage |
| "cli/sti and critical sections?" | 13 Q13 / 12 Disadvantages |
