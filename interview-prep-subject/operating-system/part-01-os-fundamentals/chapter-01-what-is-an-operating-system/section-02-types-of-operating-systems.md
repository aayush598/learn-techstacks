# Types of Operating Systems

> **TL;DR**: OSes are classified by how they schedule work and how predictable they must be — batch (throughput), time-sharing (interactivity), real-time (deadlines), distributed (scale), and embedded/mobile — each trading simplicity for responsiveness or determinism.

## 1. Why Does This Exist?
One OS design cannot serve all workloads. A supercomputer wants raw throughput on batch jobs; a desktop wants snappy response to a mouse click; a car airbag controller needs an answer within a hard deadline or lives are at risk; an IoT sensor needs to run for years on a coin battery. The *type* of OS encodes the priority: maximize work done, maximize interactivity, or maximize determinism. Classifying OS types matters because it drives scheduling policy, memory strategy, kernel design (micro vs monolithic), and even whether there is a full memory manager at all.

## 2. How Does It Work?
Each type is defined mostly by its **scheduler** and **I/O model**:
- **Batch**: jobs queued, executed back-to-back; no user interaction during run.
- **Multiprogrammed**: several jobs resident; scheduler switches to keep CPU busy during I/O.
- **Time-sharing**: preemptive round-robin-ish scheduling with short quantum; every user gets interactive response.
- **Real-time**: static priorities / rate-monotonic scheduling; guarantees worst-case latency; often no virtual memory.
- **Distributed**: OS manages a cluster of machines as one (message passing, global file system).
- **Embedded/Mobile**: resource-constrained; power-aware; often RTOS core plus app framework.

## 3. When Is It Used?
- **Batch**: mainframe batch jobs, scientific computing clusters (slurm queues), CI pipelines.
- **Time-sharing**: every desktop/laptop OS (Linux, Windows, macOS), cloud VMs.
- **Soft real-time**: video/audio streaming, web serving (responsiveness matters, missed deadline ≠ disaster).
- **Hard real-time**: aircraft flight controls, automotive airbags/ABS, medical defibrillators, robotics (FreeRTOS, QNX, VxWorks).
- **Distributed**: cloud platforms (Kubernetes over many hosts), Google's Borg, HDFS clusters.
- **Embedded/Mobile**: Android, iOS, smart TVs, routers (OpenWrt), wearables.

## 4. Why Wasn't Another Approach Chosen?
- **Batch → why not interactive?** Early computers were too expensive to let a human idle them; the answer was *time-sharing* only when hardware got cheap enough.
- **Time-sharing → why not for all real-time?** Time-sharing optimizes *average* latency; real-time needs *worst-case* guarantees. A scheduler cannot give both efficiently — hence separate RTOS design.
- **RTOS → why not just Linux with priorities?** Standard Linux (CFS/EEVDF) optimizes fairness/throughput and its worst-case latency is unbounded; `PREEMPT_RT` and `SCHED_FIFO` approximate RT, but hard RT still needs a deterministic OS (or a dedicated core/CPU isolation).
- **Microkernel → why not everywhere?** Microkernels isolate faults (QNX) but IPC cost hurt performance; the industry chose hybrids. Types coexist because the *requirements* differ, not because one is universally better.
- **Distributed OS → why not N copies of a single OS?** Managing machines as one logical computer (like Amoeba, Sprite) failed because network latency/partial failure semantics differ from local calls; industry settled on clusters with message-passing middleware (MPI, gRPC) over ordinary OSes.

## 5. Intuition
Type = what the OS optimizes when resources are scarce. Think of a **hospital emergency room**:
- Batch = "process all paperwork in the queue, nobody interacts until done."
- Time-sharing = "every patient gets a quick check every few minutes so nobody waits forever."
- Hard real-time = "the crash cart must arrive within 90 seconds, always — no exceptions, no 'best effort'."
- Distributed = "several hospitals share one system so a patient can be treated at any site seamlessly."

## 6. Real-World Analogy
An **airport baggage conveyor**:
- Batch: fill one plane fully, then the next — great throughput, a passenger can't interrupt.
- Time-sharing: round-robin — every flight's bags get a few seconds on the belt, so no plane waits long (interactive feel).
- Hard real-time: the emergency brake system — it must respond within 5 ms, guaranteed.
The *same conveyor* runs all three strategies at different times of day; the OS just commits to one policy based on workload.

## 7. Formal Definition
- **Batch OS**: an OS that executes jobs in groups (batches) with no user interaction, maximizing throughput.
- **Multiprogrammed OS**: an OS that keeps multiple jobs in memory, switching the CPU among them to overlap computation with I/O.
- **Time-sharing (multitasking) OS**: a multiprogrammed OS that preemptively time-slices the CPU so users get interactive response.
- **Real-time OS (RTOS)**: an OS that guarantees bounded (worst-case) response times, classified as *hard* (missed deadline = system failure) or *soft* (degradation only).
- **Distributed OS**: an OS that presents a cluster of independent machines as a single coherent system.
- **Embedded/mobile OS**: a compact OS designed for resource-constrained, often real-time, single-purpose devices.

## 8. Example
A **time-sharing OS with three jobs** (quantum = 4 time units):
- Job A needs 8 units, Job B needs 4, Job C needs 12.
- Schedule: A(4) → B(4 done) → C(4) → A(4 done) → C(4) → C(4 done). Completion: A=12, B=8, C=16; average turnaround = (12+8+16)/3 = 12.
- Same jobs on **batch** (A,B,C order): completion A=8, B=12, C=24; average turnaround = 14.67 — batch wins throughput per job but a new interactive user starves. That trade-off is the whole story of OS types.

## 9. Internal Working
How a **hard RTOS (FreeRTOS)** internally differs from a desktop OS:
1. **Scheduler**: FreeRTOS uses fixed-priority preemptive scheduling; the highest-priority *ready* task always runs; no aging, no fairness.
2. **Memory**: often static allocation — no heap fragmentation; some run everything from one address space (no MMU on Cortex-M0).
3. **Interrupts**: minimal interrupt latency; ISRs only set flags / send semaphores; deferred handling in tasks.
4. **Timing**: tick-driven (`SysTick`), with configurable tick rate; worst-case latency can be analytically computed from priorities.
5. **No virtual memory**: avoids page-fault latency (a page fault is an unbounded stall — unacceptable for hard RT).
6. By contrast, a **time-sharing Linux** kernel has a run queue with EEVDF, dynamic priorities, virtual memory, and I/O scheduling — optimized for fairness and throughput, not determinism.

## 10. Time Complexity
- Time-sharing scheduling decision: O(1) amortized pick-next (Linux EEVDF/rbtree O(log n) worst case insert).
- FreeRTOS scheduler: **O(1)** pick-next (bitmap of ready queues, one per priority).
- Batch job scheduling (FCFS): O(n) average wait computation; SJF: O(n log n) to sort.
- Distributed messaging: O(latency) network-bound, not CPU-bound.
- RTOS worst-case response: O(max ISR latency + context switch) — analytically bounded, typically microseconds on MCUs.

## 11. Advantages
- **Batch**: maximal throughput for long compute jobs; simple to reason about.
- **Multiprogramming**: hides I/O latency; raises CPU utilization.
- **Time-sharing**: interactive; fair-ish; supports many users cheaply.
- **RTOS**: deterministic deadlines; small footprint; low power; reliable safety cases.
- **Distributed**: scale-out capacity and fault tolerance.
- **Embedded/mobile**: long battery life, small memory, cheap hardware.

## 12. Disadvantages
- **Batch**: no interactivity; a hung job stalls the queue.
- **Time-sharing**: scheduling overhead; worst-case latency unbounded (bad for hard deadlines).
- **RTOS**: complex app logic (no rich filesystem/VM); harder debugging; expensive certification.
- **Distributed**: partial failures, consistency complexity, network latency.
- **Mobile**: constrained resources force aggressive memory killing (Android LMK) — apps get killed, which users see as loss of state.

## 13. Interview Questions
1. **Q: Difference between batch and time-sharing OS?** A: Batch runs jobs to completion without user interaction (throughput-oriented); time-sharing preemptively time-slices so users get interactive response (latency-oriented).
2. **Q: What is multiprogramming?** A: Keeping multiple jobs in memory and switching the CPU to another job when one does I/O, so the CPU never idles during I/O.
3. **Q: What is the difference between multitasking and multiprogramming?** A: Multiprogramming overlaps CPU with I/O (no preemption guarantee); multitasking preemptively switches the CPU among jobs on a timer — it's what gives interactivity.
4. **Q (TRICKY): Is "multiprocessing" a type of OS?** A: No — multiprocessing means multiple CPUs/cores; it's a hardware characteristic any OS type can use. Multiprogramming (memory-resident jobs) and multitasking (preemptive sharing) are the OS concepts; people conflate them often.
5. **Q: What is a hard real-time system? Give an example.** A: A system where missing a deadline is catastrophic: an airbag controller must inflate within ~15 ms of a crash signal; a page fault or scheduling delay is unacceptable.
6. **Q: Soft real-time vs hard real-time?** A: Soft — missed deadline degrades quality but not safety (video call frame drop); hard — missed deadline = failure (flight control).
7. **Q (SCENARIO): Can Linux run a real-time task?** A: Yes, approximately: `SCHED_FIFO`/`SCHED_RR` give static priorities, `PREEMPT_RT` patch makes the kernel fully preemptible, and CPU isolation + `NO_HZ_FULL` reduce jitter — but worst-case latency isn't *mathematically* guaranteed like FreeRTOS/QNX.
8. **Q: Why does an RTOS avoid virtual memory?** A: A page fault is an unbounded latency event (disk I/O); hard RT can't tolerate unbounded stalls, so RTOSes run in physical memory with predictable allocation.
9. **Q: What is a distributed OS? Why did it fail commercially?** A: An OS presenting multiple machines as one computer. It lost because network calls are slow and partially fail — semantics differ from local syscalls; clusters (Kubernetes/MPI) won instead.
10. **Q (PRODUCTION): What kind of OS is Android?** A: Android is a Linux-based OS (monolithic Linux kernel) with a mobile framework (Zygote, ART) — it's *Linux*, not a microkernel; Google modified it heavily (Binder IPC, wakelocks, LMK).
11. **Q: Why is mobile OS power-aware?** A: Battery is the scarcest resource; schedulers favor energy (DVFS/Idle states), apps get frozen (app standby), and background work is batched — a desktop OS optimizes speed instead.
12. **Q: What does "time-sharing" mean literally?** A: The CPU is shared in time slices among processes — each user gets a small quantum of CPU periodically — so N users feel they each have a machine.
13. **Q (TRICKY): What's the difference between a server OS and a desktop OS?** A: Server: throughput/safety first, headless, high thread counts, network-optimized schedulers, aggressive caching; desktop: interactive latency first, GUI, audio/video scheduling. Both are time-sharing at heart.
14. **Q: Why was time-sharing invented?** A: Batch machines idled while humans waited; with cheaper terminals and CPUs, it became affordable to let each user interact — massively improving programmer productivity.
15. **Q: Can a batch system be preemptive?** A: Batch *classically* is not (jobs run to completion), but modern batch schedulers (slurm, LSF) can preempt low-priority jobs for higher ones — the term drifted to "workload management."

## 14. Follow-Up Questions
1. **Q: Which scheduling algorithm does a hard RTOS use?** A: Fixed-priority preemptive scheduling; rate-monotonic scheduling (RMS) is optimal for static priorities with periodic tasks.
2. **Q: What is the critical instant in RMS analysis?** A: The moment all tasks are released simultaneously; worst-case response is bounded by analyzing that release pattern — provable schedulability.
3. **Q: Why does a time-sharing scheduler need a timer interrupt?** A: Preemption requires the kernel to regain control periodically; without a tick, a runaway process could monopolize the CPU forever.
4. **Q: What's the difference between a single-tasking embedded OS and an RTOS?** A: Single-task (super-loop) has no scheduler at all; an RTOS preemptively schedules tasks with priorities — better response and modularity, more memory.
5. **Q: Why do mobile OSes kill background apps?** A: Memory is capped (no swap on some), and battery matters; the low-memory killer reclaims frames under pressure, trading app state for system responsiveness.

## 15. Coding Example
```c
/* FreeRTOS: two tasks at different priorities — demonstrates RTOS tasking model */
#include "FreeRTOS.h"
#include "task.h"

void vSensorTask(void *pv) {          /* priority 3 */
    for (;;) {
        vSemaphoreTake(&xSensorSem, portMAX_DELAY);  /* wait for ISR signal */
        /* read sensor, guaranteed prompt handling due to high priority */
        vTaskDelay(pdMS_TO_TICKS(5));
    }
}

void vDisplayTask(void *pv) {         /* priority 1 */
    for (;;) {
        vTaskDelay(pdMS_TO_TICKS(50));   /* low priority, only runs when idle */
    }
}

int main(void) {
    xTaskCreate(vSensorTask, "sensor", 128, NULL, 3, NULL);
    xTaskCreate(vDisplayTask, "display", 128, NULL, 1, NULL);
    vTaskStartScheduler();            /* fixed-priority preemptive scheduling begins */
    return 0;
}
```
```pseudocode
# Conceptual: time-sharing vs real-time priority decision
TimeSharing:  pick = process with most "due" runtime (fairness)
RTOS:         pick = highest priority READY task (determinism)
if no RT task ready:  run background idle
```

## 16. Industry Usage
- **Cloud**: Linux time-sharing on every VM/container; schedulers tuned for latency (BQL, EEVDF, cgroup throttling).
- **Bare-metal HPC**: batch schedulers — Slurm, PBS/Torque, LSF — queue science/ML jobs on cluster nodes.
- **Automotive**: QNX and AUTOSAR-class RTOS in ECUs (QNX runs in 235M+ vehicles, incl. many ADAS); Tesla and most OEMs use Linux for infotainment.
- **Aerospace/defense**: VxWorks (Mars rovers), Integrity-178B (DO-178C certifiable).
- **IoT**: FreeRTOS (AWS IoT core, ~billions of devices), Zephyr, RIOT.
- **Mobile**: Android (Linux) + iOS (XNU). Both are time-sharing with power-focused policies.
- **Every FAANG interviewer** expects you to classify OS types and know that Kubernetes is *not* an OS but a cluster *orchestrator* on top of Linux.

## 17. References
- Silberschatz, *Operating System Concepts*, Ch. 1 (Types of OS) and Ch. 6 (Real-Time Scheduling).
- Tanenbaum, *Modern Operating Systems*, Ch. 1.3–1.7, Ch. 10 (case studies).
- FreeRTOS docs: freertos.org ("Scheduler" and "Tasks" pages).
- Linux `sched(7)` man page (`SCHED_FIFO`, `SCHED_RR`, `SCHED_DEADLINE`).
- QNX: qnx.com — "QNX Neutrino RTOS" overview.
- Liu & Layland, 1973, *Scheduling Algorithms for Multiprogramming in a Hard-Real-Time Environment* (RMS).

## 18. Cheat Sheet
- Types: batch, multiprogrammed, time-sharing, real-time (hard/soft), distributed, embedded/mobile.
- Time-sharing = preemptive time-slicing; multiprogramming = overlap I/O; multitasking = preemption; multiprocessing = multiple CPUs (hardware).
- RTOS = static priorities + no VM + bounded ISR latency + tick-driven.
- Hard RT: missed deadline = failure; Soft RT: degraded quality.
- RMS is optimal for static-priority periodic hard-RT scheduling.
- Linux ≈ time-sharing; FreeRTOS/QNX/VxWorks ≈ real-time; Android = Linux-based.
- Kubernetes is an orchestrator, not an OS.
- Batch = throughput; time-sharing = latency; RT = determinism.

## 19. Quiz
1. Which optimizes *determinism*? a) batch b) time-sharing c) RTOS d) distributed → **c**
2. Multiprogramming's key benefit is: a) faster compute b) overlap CPU with I/O c) less memory d) no scheduler → **b**
3. An airbag controller is: a) soft RT b) hard RT c) batch d) time-sharing → **b**
4. Video streaming is best classified as: a) hard RT b) soft RT c) batch d) distributed only → **b**
5. Which is a hardware concept? a) multitasking b) multiprogramming c) multiprocessing d) time-sharing → **c**
6. Android's kernel is: a) microkernel b) Linux c) Mach only d) VxWorks → **b**
7. FreeRTOS scheduling is: a) fair CFS b) fixed-priority preemptive c) round-robin only d) lottery → **b**
8. A page fault is unacceptable in: a) desktop Linux b) hard RTOS c) Android d) web servers → **b**
9. Distributed OSes lost to: a) faster CPUs b) clusters + message passing c) microkernels d) batch → **b**
10. Which is NOT a real OS? a) QNX b) VxWorks c) Kubernetes d) Zephyr → **c**

## 20. Flashcards
- **Q: OS types by optimization goal?** → **A:** Batch=throughput, time-sharing=latency, RT=determinism, distributed=scale.
- **Q: Multiprogramming vs multitasking?** → **A:** Overlap CPU/I/O vs preemptive sharing.
- **Q: Hard vs soft real-time?** → **A:** Deadline miss=failure vs quality degradation.
- **Q: RTOS kernel features?** → **A:** Static priorities, no VM, minimal ISR latency, tick-driven.
- **Q: Optimal static-priority RT scheduler?** → **A:** Rate-monotonic (RMS).
- **Q: Android's kernel?** → **A:** Linux (monolithic, heavily modified).
- **Q: Why no virtual memory in RTOS?** → **A:** Page faults are unbounded stalls.
- **Q: Slurm is a?** → **A:** Batch/job scheduler for HPC clusters.

## 21. Revision
OS types exist because workloads optimize different things. Batch systems maximize throughput (mainframes, Slurm). Multiprogramming keeps the CPU busy by overlapping I/O. Time-sharing adds preemptive time-slicing for interactivity (all desktops/cloud). Real-time systems guarantee deadlines — hard (airbag, QNX/FreeRTOS) or soft (streaming); RTOSes use fixed-priority scheduling, no virtual memory, and analytically bounded latency. Distributed OSes failed as OSes but won as clusters (Kubernetes). Android is Linux-based. Multiprocessing is hardware; multiprogramming/multitasking are software.

## 22. What Interview Questions Come From This Section?
| Interview question | Source section |
|---|---|
| "Batch vs time-sharing" | 2 How It Works / 8 Example |
| "What is multiprogramming?" | 3 When Is It Used / 13 Q2 |
| "Multitasking vs multiprogramming vs multiprocessing" | 13 Q4 |
| "Hard vs soft real-time + examples" | 3 When Is It Used / 13 Q5-6 |
| "Can Linux be real-time?" | 13 Q7 / 16 Industry Usage |
| "Why no VM in RTOS?" | 13 Q8 / 9 Internal Working |
| "What OS does Android run?" | 13 Q10 |
| "Why was time-sharing invented?" | 13 Q14 / 4 Why Not |
| "Is Kubernetes an OS?" | 16 Industry Usage |
| "Fixed-priority scheduling / RMS" | 14 Follow-Up |
