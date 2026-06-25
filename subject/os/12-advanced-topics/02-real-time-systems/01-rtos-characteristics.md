# RTOS Characteristics & Real-Time Scheduling

## Hard vs Soft Real-Time

| Property | Hard Real-Time | Soft Real-Time |
|----------|---------------|----------------|
| **Deadline miss** | System failure (catastrophic) | Degraded quality (acceptable) |
| **Examples** | Airbag, flight control, pacemaker, anti-lock brakes | Video streaming, audio, gaming, VoIP |
| **Guarantee** | Absolute (must meet every deadline) | Statistical (most deadlines met) |
| **Testing** | Formal verification required | Statistical QoS analysis |
| **Scheduling** | RMS, EDF (guaranteed) | CFS with nice values, adaptive |

## RTOS Scheduling Algorithms

### Rate Monotonic Scheduling (RMS)
- **Fixed priority** — shorter period = higher priority
- **Preemptive** — higher-rate task preempts lower-rate
- **Utilization bound:** `U_max = n × (2^(1/n) - 1)`
  - n=1: 100% | n=2: ~83% | n→∞: ~69%
  - If total utilization < bound → **all deadlines guaranteed**
  - If > bound → may fail (but can still work)
- **Priority assignment:** `priority ∝ 1/period`

### Earliest Deadline First (EDF)
- **Dynamic priority** — task with earliest deadline runs next
- **Optimal:** can schedule any task set with ≤ 100% utilization
- **Runtime cost:** deadline queue maintenance (O(log n))
- **Caveat:** overload behavior unpredictable (domino effect)

## Comparison: RMS vs EDF

| Aspect | RMS | EDF |
|--------|-----|-----|
| **Priority** | Fixed | Dynamic |
| **Utilization bound** | ~69% (many tasks) | 100% |
| **Overload behavior** | Predictable (low-priority misses) | Unpredictable (domino effect) |
| **Implementation** | Simple (OS priorities) | Complex (deadline queue) |
| **Overhead** | O(1) (fixed priorities) | O(n)/O(log n) per scheduling |
| **Preemption** | More (higher rate tasks preempt often) | Less (EDF can batch similar deadlines) |

## RTOS Characteristics
- **Deterministic:** worst-case execution time (WCET) known
- **Interrupt latency:** guaranteed max (µs range)
- **Context switch:** low and bounded (not average, WC matters)
- **Kernel preemption:** fully preemptible kernel
- **Priority inversion:** must solve (priority inheritance)

## Common RTOS Examples
| RTOS | Type | Use Case |
|------|------|----------|
| **FreeRTOS** | Open-source, small | Embedded MCUs, IoT |
| **VxWorks** | Commercial, POSIX | Aerospace, industrial |
| **QNX** | Microkernel RTOS | Automotive (BlackBerry) |
| **RT-Linux** | Preempt-RT patch | Hard RT on Linux |
| **Zephyr** | Open-source, scalable | IoT, wearables |

## Real-Time Linux (PREEMPT_RT)
- Mainline Linux kernel patches for real-time
- **Features:** fully preemptible kernel, priority inheritance, high-res timers
- **Latency target:** ~10–100µs (good for soft RT, some hard RT)
- **Not hard RT** — best-effort guarantees (interrupts may be disabled for short periods)

## WCET (Worst-Case Execution Time) Analysis
- **Static analysis:** examine code path, cache behavior
- **Measurement:** run many times, take maximum
- **Challenges:** cache misses, branch prediction, pipeline stalls
- **Caches complicate WCET** — some RTOS disable caches for deterministic timing

## Interview Tips
- *"Hard RT: missing deadline = disaster. Soft RT: occasional miss OK."*
- *"EDF is optimal (100% utilization) but complex; RMS is simpler but ~69% bound"*
- *"Priority inversion: high-priority task blocked by low-priority lock holder"*
- *"Real-time is about guarantees, not speed — determinism matters"*
