# Kernel vs User Mode and Privilege Levels

> **TL;DR**: CPUs enforce two (or more) execution privilege levels — user mode and kernel mode — so untrusted applications cannot execute privileged instructions, touch kernel memory, or hijack devices; the kernel is the only software allowed in the highest-privilege mode.

## 1. Why Does This Exist?
If every program could execute privileged instructions (writing page tables, disabling interrupts, directly programming DMA), a single bug or malicious app could corrupt memory, crash the OS, or read other users' secrets. Dual (multi-)mode operation exists so that the *only* code that can touch privileged resources is the small, audited kernel. Without it, there is no isolation, no multi-user security, and no trust boundary. It is the hardware foundation for everything else in OS security: syscalls, protection, and virtualization all assume a mode bit exists.

## 2. How Does It Work?
- The CPU tracks the current privilege level (CPL). On x86, modes are called **rings**: Ring 0 = kernel (highest privilege), Ring 3 = user; Rings 1-2 mostly unused. ARM has EL0 (user)…EL3 (secure firmware).
- Certain instructions are **privileged**: they fault if executed below Ring 0 (e.g., `lgdt`, `lidt`, `cli`, `sti`, `hlt`, writing `CR3`, `IN/OUT`).
- User code cannot *directly* switch to kernel mode; it must use a **trap instruction** (`syscall`/`sysenter` on x86-64, `svc` on ARM, `scall` on RISC-V) that atomically raises privilege and jumps to a fixed kernel entry point.
- The kernel sets up **gate structures** (IDT, MSRs) so only sanctioned entry points exist; everything else is a fault.

## 3. When Is It Used?
- **Every syscall**: `read`, `write`, `fork`, `mmap` — each traps to Ring 0.
- **Every hardware interrupt**: timer ticks, network packets, keypresses — CPU enters kernel mode to run the ISR.
- **Every exception/fault**: page faults, divide-by-zero, invalid instructions — kernel mode handles them.
- **Mode switches also happen for**: system control instructions (`HLT`), TLB maintenance, saving/restoring context.
- **Virtualization**: hypervisors (KVM, Hyper-V) run in Ring 0/-1 (VMX root) while guests run in Ring 0 with reduced privileges — the mode machinery is reused for nested isolation.

## 4. Why Wasn't Another Approach Chosen?
- **No mode distinction (single privilege level)**: all code equally privileged — simple, fast, but catastrophic security; used only in ancient OSes and bare-metal MCUs. Rejected for general-purpose computing.
- **Software-enforced protection (no hardware mode bits)**: the OS could *attempt* to check every instruction via interpretation — way too slow; hardware enforcement is a single bit check per instruction.
- **More rings (Intel iAPX 432 had 8+)**: never adopted — the OSes using them didn't ship, and 2-4 levels cover the real needs (kernel/user/firmware/hypervisor).
- **Capability-based security instead of modes (Plessey, KeyKOS)**: elegant fine-grained capabilities, but expensive to implement and no mainstream hardware; mode bits won on pragmatism.
The chosen approach — a small number of hardware privilege levels with trap-gated entry — is the right balance of performance (cheap mode checks) and security (a hard kernel boundary).

## 5. Intuition
Modes are like the **floor levels of a high-security building**. The vault floor (Ring 0) has the master keys (privileged instructions) and the money (kernel memory). Regular employees (user processes) work on the upper floors and can only reach the vault floor by taking a *guarded elevator* (the syscall instruction), which always arrives at a checkpoint where the guard (kernel) inspects your badge and request. You can't just walk down the stairs (no direct mode switch).

## 6. Real-World Analogy
A **hospital restricted area**: patients (user apps) walk around public wards (Ring 3). The operating theater (Ring 0) has restricted access. Staff use keycards (syscalls); a random visitor can't open the pharmacy door (privileged instruction) — if they try, the door beeps (fault). Security guards (interrupts) can also override access when an emergency happens (hardware event forces a mode change).

## 7. Formal Definition
**User mode (Ring 3 / EL0)**: the execution mode for all application code; the CPU rejects privileged instructions and restricts I/O and page-table access. **Kernel mode (Ring 0 / EL1)**: the mode for OS code with full instruction and I/O privilege. The **CPL (current privilege level)** is held in the x86 CS register (2 bits); a **privileged instruction** executes only if CPL = 0, otherwise it raises a #GP (general protection) fault. The mode switch is performed only via controlled **gate transitions** (syscall/trap or interrupt).

## 8. Example
A process calls `write(1, "hi", 2)`:
1. User code (Ring 3) executes `syscall` with `%rax = 1` (SYS_write).
2. CPU reads `MSR_LSTAR` (syscall target), sets CPL = 0 (Ring 0), jumps to `entry_SYSCALL_64`.
3. Kernel validates args, copies the string via `copy_from_user`, performs the write, returns.
4. `sysretq` restores user state and CPL = 3.
Meanwhile, a **malicious** program executing `mov cr0, rax` (privileged) at Ring 3 raises #GP immediately — the instruction never runs.

## 9. Internal Working
1. **Kernel image mapped** into every process's address space (upper half on x86-64, e.g., `0xffff888000000000+`), with U/S page-table bits marking kernel pages supervisor-only.
2. **Entry points defined** at boot: IDT for interrupts/exceptions, `MSR_LSTAR`/`MSR_GS_BASE` for syscalls (syscall), `MSR_SYSENTER` (sysenter, legacy).
3. **Switch down (user→kernel)**: `syscall` instruction saves RIP/RFLAGS, sets CPL 0, loads target. A new kernel stack (per-task `thread_info`/`kernel_stack`) is switched to; user `%gs` swapped to kernel `%gs` via `swapgs`.
4. **Switch up (kernel→user)**: `sysretq`/`iretq` restores RIP/RFLAGS/SS/RSP, sets CPL 3, flushes the syscall target (STIBP/MELTDOWN mitigations use `KPTI`/`ptrace`-scoped page tables).
5. **Fault path**: any privileged instruction at CPL≠0 → exception vector → kernel handler → signal (`SIGSEGV`/`SIGILL`) or `kill`.

## 10. Time Complexity
- Syscall entry+exit (mode switch): **O(1)** — ~20-40ns on modern x86-64 (optimized entry), 100-1000ns with mitigations/copying.
- Exception dispatch: O(1) (fixed vector table).
- Memory impact: one extra page table (KPTI) + `swapgs`/`syscall` register moves — negligible per-op.

## 11. Advantages
- **Hardware-enforced isolation**: apps can't touch kernel memory or devices.
- **Controlled entry**: only sanctioned syscall vectors; attack surface reduced.
- **Multi-user/multi-tenant security**: a compromised app is contained (absent a kernel exploit).
- **Foundation for virtualization**: hypervisors reuse privilege machinery.
- **Cheap protection**: mode check costs a bit, not a policy evaluation.

## 12. Disadvantages
- **Mode-switch cost**: every syscall pays entry/exit (cache/TLB pollution, KPTI makes it worse).
- **Kernel bugs escape the model**: a Ring-0 bug has no safety net — one bad pointer in a driver crashes everything (mitigation: modules, Windows driver signing, `io_uring`'s ring memory).
- **Coarse boundary**: capability-style fine-grained per-object permission isn't possible with just a mode bit.
- **Speculative-execution leaks**: Meltdown/Spectre showed mode-based isolation can be side-channeled across the boundary.

## 13. Interview Questions
1. **Q: Why does the CPU need user and kernel modes?** A: To prevent untrusted applications from executing privileged instructions (I/O, page-table writes, interrupt control) that would corrupt or compromise the OS — mode bits give hardware-enforced isolation.
2. **Q: What is the ring model?** A: x86 has 4 rings: Ring 0 (kernel), 1-2 (usually unused, drivers in some systems), Ring 3 (user). CPL is the current ring in CS. ARM uses EL0-EL3; RISC-V uses U/S/M modes.
3. **Q (TRICKY): Can a user process become a kernel process?** A: No — there's no "set mode" instruction for user code. The only transitions are via syscall/trap instructions (user-initiated, gated) or interrupts/exceptions (hardware-initiated). A kernel exploit isn't a "mode change," it's a bug that breaks the gate.
4. **Q: What instructions are privileged?** A: Those that could bypass protection: `lgdt`/`lidt`/`ltr` (descriptor tables), `cli`/`sti` (interrupt masking), `hlt`, `in`/`out` (I/O ports), writes to control registers `CR0/CR3/CR4` (page tables), and MSR writes.
5. **Q: How does a process make a syscall at the hardware level?** A: It executes a trap instruction — `syscall` (x86-64) or `sysenter` (legacy 32-bit) or `svc` (ARM64) — the CPU sets CPL=0 and jumps to the kernel's registered entry point (MSR_LSTAR on x86-64).
6. **Q: What happens if user code executes `cli` (disable interrupts)?** A: #GP general-protection fault → kernel exception handler → usually the process gets `SIGSEGV`; the kernel's interrupt state is never touched. (This is a classic "tricky" answer.)
7. **Q: What is the cost of a mode switch?** A: ~20-40ns for entry on modern x86-64 (entry+exit), plus indirect costs: kernel stack switch, TLB/cache pollution, KPTI page-table switch (which added ~5-30% syscall-heavy overhead historically), and `swapgs`.
8. **Q (PRODUCTION): What was KPTI (Meltdown mitigation) and why did it cost performance?** A: Kernel Page Table Isolation unmapped most kernel memory from user page tables, so speculative reads couldn't leak kernel data — but every syscall/interrupt now switches page tables, adding TLB flushes and cost.
9. **Q: How do hypervisors fit the mode model?** A: With VT-x/AMD-V, the hypervisor runs in VMX root (Ring -1 concept); guests run in VMX non-root. Even guest Ring 0 code (guest kernel) traps (VMEXIT) on privileged operations — so the hypervisor is more privileged than any guest.
10. **Q (SCENARIO): Your app does millions of tiny syscalls and is slow. Kernel-mode argument?** A: This is expected mode-switch overhead — batch I/O (`readv`/`io_uring`), use the vDSO where possible, or move work to a daemon. The mode split is the price of isolation.
11. **Q: What is `swapgs` for?** A: x86-64 syscall entry/exit — it swaps the user `%gs` (used for TLS, e.g., thread-local storage) with the kernel's `%gs` (per-CPU data). Ensures kernel per-CPU structures are reachable without user control.
12. **Q: Does every syscall enter the kernel through the same door?** A: Mostly yes (one entry point per arch + a few special gates), and that uniformity is a security win — it's audited, validated (`access_ok`), and mitigates kernel-address leaks.
13. **Q (TRICKY): Is a driver in Ring 3 safe from kernel bugs?** A: Safe *from* the kernel, but it can't do privileged work directly and must IPC to the kernel for everything — that's the microkernel trade (isolation for IPC overhead). In monolithic Linux, drivers run in Ring 0 and share the kernel's fate.
14. **Q: What's the difference between mode switch and context switch?** A: Mode switch: privilege level change within the same process (syscall). Context switch: the kernel switches between processes (changes PCBs, page tables). A syscall need not context-switch; a context switch always involves kernel mode.

## 14. Follow-Up Questions
1. **Q: Why rings 1 and 2 are unused on x86?** A: OSes that used them (OS/2 drivers in Ring 2) proved too fragile; modern OSes just need kernel (0) and user (3); virtualization added "below zero" via VMX root.
2. **Q: What is a #GP fault?** A: General protection fault — raised for privileged instructions at wrong CPL, bad segment references, etc.; the kernel turns most into SIGSEGV.
3. **Q: What is DPL/RPL vs CPL?** A: Descriptor privilege level (in gate descriptors) and requested privilege level (segment selector) — gates check CPL vs DPL/RPL to decide access.
4. **Q: What happens on a page fault in user mode?** A: The CPU traps to the kernel's page-fault handler; if the faulting address maps to a valid VMA (demand paging), the kernel maps the page and resumes; otherwise it sends SIGSEGV.
5. **Q: How does ARM64 differ?** A: EL0 (user), EL1 (kernel), EL2 (hypervisor), EL3 (secure firmware/TrustZone); syscalls via `svc` with `SVC#` immediate; similar gate model.

## 15. Coding Example
```c
#include <stdio.h>
#include <stdint.h>

/* A privileged instruction attempt — will fault at user level */
int main(void) {
    /* Write to control register CR3 (page table pointer). At Ring 3
       this raises #GP; the kernel kills us with SIGSEGV. */
    __asm__ volatile("mov %0, %%cr3" :: "r"((uint64_t)0) : "memory");
    printf("unreachable\n");
    return 0;
}
```
```pseudocode
# Gate model (x86-64 syscall path)
USER ring3:
  mov rax, SYS_read
  mov rdi, fd
  mov rsi, buf
  mov rdx, len
  syscall                      # CPU: CPL=0, jump MSR_LSTAR, switch kernel stack
KERNEL ring0:
  entry_SYSCALL_64:            # swapgs; switch to kernel stack; save user regs
  validate nr < NR_syscalls
  call sys_call_table[nr]      # e.g., ksys_read()
  restore user regs; swapgs; sysretq    # CPL=3
```

## 16. Industry Usage
- **Linux**: x86-64 `arch/x86/entry/entry_64.S` (syscall entry), `arch/x86/kernel/cpu/common.c` (mode setup); KPTI switch in `arch/x86/mm/pti.c`. Used on all cloud providers.
- **Windows NT**: `KiSystemCall64` entry; kernel uses Ring 0, apps Ring 3; KVA shadow (KPTI equivalent) in `ntoskrnl.exe`.
- **macOS/iOS XNU**: Ring 0 kernel (Mach+BSD), `svc`/`syscall` gates; AMFI/SIP enforced in kernel mode.
- **ARM TrustZone (EL3)** on phones: secure world (fingerprint, DRM, payments) above the kernel — mode hierarchy used for mobile security.
- **Hypervisors**: KVM (Linux kernel module) uses VMX root vs non-root; AWS Nitro uses a microhypervisor as its trust root.
- **RTOS on MCUs** (FreeRTOS): often runs everything in privileged mode or uses the MPU for a crude user/kernel split — the mode model scales down when security requirements allow.

## 17. References
- Intel SDM Vol. 3A — "Protected Mode", "Privilege Levels", "System-Call instructions" (SYSCALL/SYSENTER).
- Silberschatz, *OS Concepts*, Ch. 1.5 (Dual-Mode Operation).
- Tanenbaum, *Modern OS*, Ch. 1.6.1.
- Linux: `arch/x86/entry/entry_64.S`, `arch/x86/mm/pti.c`, Documentation/x86 (PTI).
- ARM: ARMv8-A *Architecture Reference Manual* (Exception levels EL0-EL3).
- Gruss et al., *KASLR is Dead: Long Live KASLR* (Meltdown/KPTI context).

## 18. Cheat Sheet
- Ring 0 = kernel, Ring 3 = user; CPL in CS register.
- Privileged ops fault at wrong CPL: #GP → SIGSEGV.
- Mode up: `syscall`/`sysenter`/`svc`; mode down: `sysretq`/`iretq`.
- Kernel maps its image in upper half of every process address space.
- `swapgs` swaps user/kernel %gs at entry/exit.
- KPTI = separate page tables, Meltdown mitigation, syscall cost.
- Hypervisor = VMX root; guests trap on privileged ops (VMEXIT).
- Mode switch ≠ context switch.
- ARM: EL0/EL1/EL2/EL3; RISC-V: U/S/M.

## 19. Quiz
1. User processes run at: a) Ring 0 b) Ring 3 c) EL3 d) any ring → **b**
2. Executing `cli` at Ring 3 causes: a) interrupts disabled b) #GP fault c) hang d) nothing → **b**
3. The x86-64 syscall instruction is: a) int 80 b) syscall c) sysret d) sysenter → **b**
4. Which is NOT privileged? a) mov cr3 b) in/out c) lgdt d) mov rax, rbx → **d**
5. KPTI was a mitigation for: a) Spectre b) Meltdown c) Rowhammer d) Heartbleed → **b**
6. Hypervisors run in: a) Ring 0 only b) VMX root c) Ring 3 d) EL0 → **b**
7. `swapgs` is used for: a) memory copy b) user/kernel %gs swap c) stack growth d) TLB flush → **b**
8. ARM64 kernel mode is: a) EL0 b) EL1 c) EL2 d) EL3 → **b**
9. A syscall mode switch costs roughly: a) 1ns b) 20-40ns c) 1ms d) 1s → **b**
10. A mode switch is the same as a context switch: a) always b) never c) only in RTOS d) only with threads → **b**

## 20. Flashcards
- **Q: Ring model levels?** → **A:** x86: Ring0 kernel, Ring3 user; ARM: EL0-EL3.
- **Q: What happens on a privileged instruction at user level?** → **A:** #GP fault → SIGSEGV.
- **Q: How to enter kernel mode?** → **A:** Only via syscall/trap instruction or interrupt/exception.
- **Q: KPTI?** → **A:** Separate user/kernel page tables, Meltdown mitigation, adds syscall cost.
- **Q: Mode switch vs context switch?** → **A:** Privilege change vs switching between processes.
- **Q: swapgs purpose?** → **A:** Swap user TLS %gs with kernel per-CPU %gs.
- **Q: Hypervisor privilege?** → **A:** VMX root; guests trap via VMEXIT.
- **Q: ARM exception levels?** → **A:** EL0 user, EL1 kernel, EL2 hypervisor, EL3 secure.

## 21. Revision
CPU privilege levels are the hardware foundation of OS security: Ring 0 (kernel) vs Ring 3 (user), with privileged instructions (I/O, CR3, IDT) faulting at user level. Entry to kernel mode is gated — via `syscall`/`sysenter` (x86-64), `svc` (ARM), with the target defined at boot (MSR_LSTAR/IDT). `swapgs` handles per-CPU state, `sysretq` returns to user. KPTI unmaps kernel memory from user page tables to defeat Meltdown. Hypervisors sit "below" Ring 0 in VMX root. Mode switch (privilege change) differs from context switch (process change). Any system-call, interrupt, or exception question decomposes into this model.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Why do we need user/kernel mode?" | 1 Why Does This Exist |
| "What is the ring model?" | 2 How It Works / 7 Formal Definition |
| "What happens if user code disables interrupts?" | 13 Q6 / 8 Example |
| "Cost of a syscall / mode switch?" | 13 Q7 / 10 Time Complexity |
| "What is KPTI / Meltdown?" | 13 Q8 / 16 Industry Usage |
| "Privileged instructions examples" | 13 Q4 / 7 Formal Definition |
| "Can a process become kernel mode?" | 13 Q3 / 4 Why Not |
| "How does a hypervisor fit in?" | 13 Q9 / 16 Industry Usage |
| "swapgs / sysretq details" | 13 Q11 / 9 Internal Working |
| "Mode vs context switch" | 13 Q14 / 14 Follow-Up |
