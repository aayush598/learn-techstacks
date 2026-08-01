# Chapter: Scheduling Fundamentals

## What you'll learn
- The scheduling criteria that define "good" (CPU utilization, throughput, turnaround, waiting, response) and the conflicts between them.
- The three scheduler levels — long-term (admission), short-term (dispatcher), medium-term (swap) — and which one actually runs per-tick.
- Preemptive vs non-preemptive scheduling, what "preemption" means, and where the timer interrupt fits.

## Prerequisites (linked)
- [Part 02 Process Concept](../../part-02-processes-and-threads/chapter-01-process-concept/README.md) — process states (ready/running), PCB, runqueue.
- [Part 02 Context Switching](../../part-02-processes-and-threads/chapter-04-context-switching/README.md) — what dispatch actually costs.
- Feeds into [Ch-02 Algorithms](../chapter-02-scheduling-algorithms/README.md).

## Sections (linked table)
| Section | Core idea |
|---|---|
| [Section 01 — Scheduling Criteria and Goals](section-01-scheduling-criteria-and-goals.md) | Utilization, throughput, TAT, wait, response — and their trade-offs |
| [Section 02 — Long/Short/Medium-Term Schedulers](section-02-long-term-short-term-and-medium-term-schedulers.md) | Admission, dispatcher, swap — who does what |
| [Section 03 — Preemptive vs Non-Preemptive Scheduling](section-03-preemptive-vs-non-preemptive-scheduling.md) | Who may take the CPU away, and the timer's role |

## One-paragraph narrative connecting all sections
Scheduling exists because the CPU is scarce and tasks compete; we first need agreed *criteria* for what "good" means — and those criteria conflict (Section 01). The actual scheduling work is split across three levels: admission control, the per-tick dispatcher, and memory-pressure swapping (Section 02). The deepest design decision is whether the OS *may take* the CPU away mid-execution — preemptive vs non-preemptive — which is what gives us interactive responsiveness and what the timer interrupt enables (Section 03). With criteria, levels, and preemption understood, every algorithm in Chapter 02 becomes a policy choice over this machinery.

## Common interview trap in this chapter
Conflating **turnaround** with **waiting time** and **response time**. Turnaround = completion − arrival (includes execution). Waiting = time in the ready queue only (excludes execution). Response = time from arrival to *first* CPU allocation. Many algorithm questions fail because candidates compute the wrong one.

## Checklist before moving on
- [ ] I can define all 5-6 scheduling criteria and name a metric for each.
- [ ] I can explain the conflict between utilization/throughput and response/latency.
- [ ] I can classify any scheduling decision as long/short/medium-term.
- [ ] I can explain preemption and the role of the timer interrupt.
- [ ] I know examples of non-preemptive (SJF, FCFS, older) vs preemptive (RR, SRTF, EEVDF) algorithms.
- [ ] I can say what "dispatch latency" is.
